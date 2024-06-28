"""DQN training."""
import pathlib
import random
import math
from collections import namedtuple
from itertools import count
import pickle

import click
import yaml
import gym
import torch
from torch import optim
from torch.nn import functional as F
from attrdict import AttrDict

from .deepq import DQN
from .replay import ReplayMemory, Transition
from .extract import GymExtractor


Hyperparams = namedtuple('Hyperparams', (
    'batch_size', 'gamma', 'p_rand_start', 'p_rand_end', 'p_rand_decay', 'target_update'))


def decide_random_action(start, end, decay, steps_done):
    sample = random.random()
    threshold = end + (start - end) * math.exp(-1 * steps_done / decay)
    return bool(not sample > threshold)


class DQoach:
    """Training algo for DQN network to learn gym.CartPole-v0."""
    DEFAULT_HY_PARAMS = Hyperparams(
        batch_size=128,
        gamma=0.999,
        p_rand_start=0.9,
        p_rand_end=0.05,
        p_rand_decay=200,
        target_update=10
    )

    def __init__(self, device=torch.device('cpu'), **kwargs):
        """Initialize the hyper parameters, networks and training state."""
        self.device = device
        self._hyper_params = Hyperparams(
            batch_size=kwargs.get('batch_size', self.DEFAULT_HY_PARAMS.batch_size),
            gamma=kwargs.get('gamma', self.DEFAULT_HY_PARAMS.gamma),
            p_rand_start=kwargs.get('p_rand_start', self.DEFAULT_HY_PARAMS.p_rand_start),
            p_rand_end=kwargs.get('p_rand_end', self.DEFAULT_HY_PARAMS.p_rand_end),
            p_rand_decay=kwargs.get('p_rand_decay', self.DEFAULT_HY_PARAMS.p_rand_decay),
            target_update=kwargs.get('target_update', self.DEFAULT_HY_PARAMS.target_update),
        )
        self.nets = AttrDict({
            'policy': DQN().to(self.device),
            'target': DQN().to(self.device)
        })
        self.nets.target.load_state_dict(self.nets.policy.state_dict())
        self.nets.target.eval()
        self.optimizer = optim.RMSprop(self.nets.policy.parameters())
        self.memory = ReplayMemory(10000)
        self.steps_done = 0
        self.cache_file = pathlib.Path(kwargs.get('cache_file', './pytorch-gym-cache.yaml'), mode='rw')
        self.episode_durations = []
        if self.cache_file.exists():
            self._load_state()

    def select_action(self, state):
        sample = random.random
        take_random_action = decide_random_action(
            start=self.hyper_params.p_rand_start,
            end=self.hyper_params.p_rand_end,
            decay=self.hyper_params.p_rand_decay,
            steps_done=self.steps_done
        )
        self.steps_done += 1
        if not take_random_action:
            with torch.no_grad():
                return self.nets.policy(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(2)]], device=self.device, dtype=torch.long)

    def train_step(self):
        if len(self.memory) < self.hyper_params.batch_size:
            return

        transitions = self.memory.sample(self.hyper_params.batch_size)
        batch = Transition(*zip(*transitions))

        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=self.device, dtype=torch.uint8)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        state_action_values = self.nets.policy(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(self.hyper_params.batch_size, device=self.device)
        next_state_values[non_final_mask] = self.nets.target(non_final_next_states).max(1)[0].detach()
        expected_state_action_values = (next_state_values * self.hyper_params.gamma) + reward_batch

        ## Huber loss
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.nets.policy.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        self._save_state()

    def train(self, num_episodes=50, env=gym.make('CartPole-v0').unwrapped):
        extractor = GymExtractor(env, self.device)
        with click.progressbar(range(num_episodes), label='Training Episode') as pbar:
            for i_episode in pbar:
                env.reset()
                last_screen = extractor.get_screen()
                current_screen = extractor.get_screen()
                state = current_screen - last_screen
                for t_count in count():
                    action = self.select_action(state)
                    _, reward, done, _ = env.step(action.item())
                    reward = torch.tensor([reward], device=self.device)

                    last_screen = current_screen
                    current_screen = extractor.get_screen()
                    if not done:
                        next_state = current_screen - last_screen
                    else:
                        next_state = None

                    self.memory.push(state, action, next_state, reward)
                    state = next_state

                    self.train_step()
                    if done:
                        self.episode_durations.append(t_count + 1)
                        break
                if len(self.episode_durations) % self.hyper_params.target_update == 0:
                    self.nets.target.load_state_dict(self.nets.policy.state_dict())
                    self._save_state()
                    self.plot_durations()
        click.echo('Complete')

    def plot_durations(self):
        from matplotlib import pyplot as plt
        import gc
        plt.figure()
        plt.clf()
        durations_t = torch.tensor(self.episode_durations, dtype=torch.float)
        plt.title('Training...')
        plt.xlabel('Episode')
        plt.ylabel('Duration')
        plt.plot(durations_t.numpy())
        if len(durations_t) >= 100:
            means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
            means = torch.cat((torch.zeros(99), means))
            plt.plot(means.numpy())
        plt.savefig('training.pdf')
        plt.clf()
        plt.close()
        gc.collect()

    @property
    def hyper_params(self):
        return self._hyper_params

    def _save_state(self):
        """Serialize the training state to yaml."""
        doc = {
            'hyper_params': self.hyper_params,
            'steps_done': self.steps_done,
            'policy_params': self.nets.policy.state_dict(),
            'target_params': self.nets.target.state_dict(),
            'optimizer_params': self.optimizer.state_dict(),
            'episode_durations': self.episode_durations,
        }
        self.cache_file.write_text(yaml.dump(doc))
        with open('memory', mode='bw') as memfile:
            pickle.dump(self.memory, memfile)

    def _load_state(self):
        """Load the training state from yaml."""
        doc = AttrDict(yaml.load(self.cache_file.read_text()))

        if not doc:
            return None

        self._hyper_params = Hyperparams(*doc.hyper_params)
        self.steps_done = doc.steps_done
        self.nets.policy.load_state_dict(doc.policy_params)
        self.nets.target.load_state_dict(doc.target_params)
        self.episode_durations = list(doc.episode_durations)
        self.optimizer.load_state_dict(doc.optimizer_params)
        with open('memory', mode='br') as memfile:
            self.memory = pickle.load(memfile)

        return None
