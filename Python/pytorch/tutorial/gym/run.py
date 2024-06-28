import click

import gymlearn.train


@click.command('gymlearn')
@click.argument('num_episodes', type=int)
def main(num_episodes):
    coach = gymlearn.train.DQoach()
    coach.train(num_episodes)


if __name__ == '__main__':
    main()
