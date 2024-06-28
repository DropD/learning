import pytest
import torch
import gym

from .extract import GymExtractor


@pytest.fixture
def gym_extractor():
    device = torch.device('cpu')
    env = gym.make('CartPole-v0').unwrapped
    env.reset()
    yield GymExtractor(env, device)


def test_get_cart_location(gym_extractor):
    gym_extractor.get_cart_location()


def test_get_screen(gym_extractor):
    screen = gym_extractor.get_screen()
    assert bool((torch.tensor(screen.shape) == torch.tensor([1, 3, 40, 80])).all())
