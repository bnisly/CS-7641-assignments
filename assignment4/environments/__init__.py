import gym
from gym.envs.registration import register

from .cliff_walking import *
from .frozen_lake import *

__all__ = ['RewardingFrozenLakeEnv', 'WindyCliffWalkingEnv']

register(
    id='RewardingFrozenLake-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '4x4'},
)

register(
    id='RewardingFrozenLake8x8-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '8x8'}
)

register(
    id='RewardingFrozenLakeNoRewards15x15-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '15x15', 'rewarding': False}
)

register(
    id='RewardingFrozenLakeNoRewards8x8-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '8x8', 'rewarding': False}
)

register(
    id='RewardingFrozenLakeWithRewards15x15-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '15x15', 'rewarding': True}
)

register(
    id='RewardingFrozenLakeWithRewards8x8-v0',
    entry_point='environments:RewardingFrozenLakeEnv',
    kwargs={'map_name': '8x8', 'rewarding': True}
)

register(
    id='WindyCliffWalking-v0',
    entry_point='environments:WindyCliffWalkingEnv',
)


def get_rewarding_frozen_lake_environment():
    return gym.make('RewardingFrozenLake8x8-v0')


def get_frozen_lake_environment():
    return gym.make('RewardingFrozenLake-v0')


def get_rewarding_no_reward_frozen_lake_environment():
    return gym.make('RewardingFrozenLakeNoRewards8x8-v0')


def get_large_rewarding_no_reward_frozen_lake_environment():
    return gym.make('RewardingFrozenLakeNoRewards15x15-v0')


def get_rewarding_with_reward_frozen_lake_environment():
    return gym.make('RewardingFrozenLakeWithRewards8x8-v0')


def get_large_rewarding_with_reward_frozen_lake_environment():
    return gym.make('RewardingFrozenLakeWithRewards15x15-v0')


def get_cliff_walking_environment():
    return gym.make('CliffWalking-v0')


def get_windy_cliff_walking_environment():
    return gym.make('WindyCliffWalking-v0')
