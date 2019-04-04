import sys

import numpy as np
from gym import utils
from gym.envs.toy_text import discrete
from six import StringIO

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

MAPS = {
    "4x4": [
        "SFFF",
        "FHFH",
        "FFFH",
        "HFFG"
    ],
    "8x8": [
        "SFFFFFFF",
        "FFFFFFFF",
        "FFFHFFFF",
        "FFFFFHFF",
        "FFFHFFFF",
        "FHHFFFHF",
        "FHFFHFHF",
        "FFFHFFFG"
    ],
    "15x15": [
        "SFFFFFHFFFFFFFF",
        "FFFFFFFFFFFFHFF",
        "FFHFFFFFHFFFFFF",
        "FFFFHFFFFFFFHFF",
        "FFFFFFFFFFFFHFF",
        "FFFFHFFHFFFFHFF",
        "FFFFHFFFFFFFHFF",
        "FFFFFFFFHHHHHFF",
        "HHHFHFFFFFFFHFF",
        "FFFFHFFHHFFFHFF",
        "FFFFFFFFFFFFHFF",
        "FFFFHFFFHFFFHFF",
        "FFFFFFFFFFFFFFF",
        "FHFHFHFFFFFFFFF",
        "FFHFFFFFFFHHHFG"
    ],
    "20x20": [
        "SFFFFFFHHHFFFFFFFFFF",
        "FFFFFFFFFFFFFFFFHHFF",
        "FFFHFFFFFFFHHFFFFFFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFFFFHFFFFFFFHHFF",
        "FFFFFHFFFFHHFFFFHHFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFFFFFFFHHHHHHHFF",
        "HHHHFHFFFFFFFFFFHHFF",
        "FFFFFHFFFFHHHFFFHHFF",
        "FFFFFFFFFFFFFFFFHHFF",
        "FFFFFHFFFFFFHFFFHHFF",
        "FFFFFHFFFFFFFFFFHHFF",
        "FFFFFFFFFFFHFFFFFFFF",
        "FHHFFFHFFFFHFFFFFHFF",
        "FHHFHFHFFFFFFFFFFFFF",
        "FFFHFFFFFHFFFFHHFHFG"
    ]
}


# Adapted from https://github.com/openai/gym/blob/master/gym/envs/toy_text/frozen_lake.py
# This is a modified environment where rewards are given for every step in addition to on finding a goal.
# This reward shaping makes the problem easier for the learner to solve.
class RewardingFrozenLakeEnv(discrete.DiscreteEnv):
    """
    Winter is here. You and your friends were tossing around a frisbee at the park
    when you made a wild throw that left the frisbee out in the middle of the lake.
    The water is mostly frozen, but there are a few holes where the ice has melted.
    If you step into one of those holes, you'll fall into the freezing water.
    At this time, there's an international frisbee shortage, so it's absolutely imperative that
    you navigate across the lake and retrieve the disc.
    However, the ice is slippery, so you won't always move in the direction you intend.
    The surface is described using a grid like the following

        SFFF
        FHFH
        FFFH
        HFFG

    S : starting point, safe
    F : frozen surface, safe
    H : hole, fall to your doom
    G : goal, where the frisbee is located

    The episode ends when you reach the goal or fall in a hole.
    You receive a reward of 1 if you reach the goal, -1 for falling in a hole, and a small negative reward otherwise.
    The hole and step rewards are configurable when creating an instance of the problem.

    """

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, desc=None, map_name="4x4", rewarding=True, step_reward=-1, hole_reward=-100, is_slippery=False):
        if desc is None and map_name is None:
            raise ValueError('Must provide either desc or map_name')
        elif desc is None:
            desc = MAPS[map_name]
        self.desc = desc = np.asarray(desc, dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.reward_range = (0, 1)
        self.step_reward = step_reward
        self.hole_reward = hole_reward
        self.rewarding = rewarding
        self.is_slippery = is_slippery

        nA = 4
        nS = nrow * ncol

        isd = np.array(desc == b'S').astype('float64').ravel()
        isd /= isd.sum()

        P = {s: {a: [] for a in range(nA)} for s in range(nS)}

        def to_s(row, col):
            return row * ncol + col

        def inc(row, col, a):
            if a == 0:  # left
                col = max(col - 1, 0)
            elif a == 1:  # down
                row = min(row + 1, nrow - 1)
            elif a == 2:  # right
                col = min(col + 1, ncol - 1)
            elif a == 3:  # up
                row = max(row - 1, 0)
            return (row, col)

        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(4):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter in b'GH':
                        rew = float(100 if letter == b'G' else -100)
                        li.append((1.0, s, rew, True))
                    else:
                        if is_slippery:
                            for b in [(a - 1) % 4, a, (a + 1) % 4]:
                                newrow, newcol = inc(row, col, b)
                                newstate = to_s(newrow, newcol)
                                newletter = desc[newrow, newcol]
                                done = bytes(newletter) in b'GH'
                                rew = float(100 if newletter == b'G' else 0)
                                if self.rewarding:
                                    if newletter == b'F':
                                        rew = self.step_reward
                                    elif newletter == b'H':
                                        rew = self.hole_reward
                                li.append((0.8 if b == a else 0.1, newstate, rew, done))
                        else:
                            newrow, newcol = inc(row, col, a)
                            newstate = to_s(newrow, newcol)
                            newletter = desc[newrow, newcol]
                            done = bytes(newletter) in b'GH'
                            rew = float(100 if newletter == b'G' else 0)
                            if self.rewarding:
                                if newletter == b'F':
                                    rew = self.step_reward
                                elif newletter == b'H':
                                    rew = self.hole_reward
                            li.append((1.0, newstate, rew, done))

        super(RewardingFrozenLakeEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left", "Down", "Right", "Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc) + "\n")

        if mode != 'human':
            return outfile

    def colors(self):
        return {
            b'S': 'green',
            b'F': 'skyblue',
            b'H': 'black',
            b'G': 'gold',
        }

    def directions(self):
        return {
            3: '⬆',
            2: '➡',
            1: '⬇',
            0: '⬅'
        }

    def new_instance(self):
        return RewardingFrozenLakeEnv(desc=self.desc, rewarding=self.rewarding, step_reward=self.step_reward,
                                      hole_reward=self.hole_reward, is_slippery=self.is_slippery)
