import math
from collections import defaultdict

import random
# FIXME: Still not deterministic even after setting random seed, perhaps something
# with the hashmap and pointers? I really hope not
random.seed(42)

class MCTSNode:
    """
    A wrapper around a board position, with metadata and helpers
    """

    def __init__(self, pos):
        self.visits = 0
        self.reward = 0
        self.pos = pos

    def __hash__(self):
        return hash(self.pos)

    def avg_reward(self):
        return self.reward / (self.visits or 1)

    def __repr__(self):
        return f'MCTSNode(visits={self.visits}, reward={self.reward})'


class MCTS:
    def __init__(self, pos, sims=1):
        self.root = MCTSNode(pos)
        self.children = defaultdict(set)
        self.sims = 1

    def step(self):
        """
        A single step of mcts, expand one node with 'self.sims' simulations.
        """
        path = self.selection(self.root)
        self.expand(path[-1])
        reward = self.simulate(path[-1])
        self.backprop(path, reward)

    def selection(self, root):
        """
        Select a node to expand from
        """

        path = [root]
        while children := self.children.get(path[-1]):
            parent = path[-1]

            def _value(child):
                # must explore unexplored nodes
                if child.visits == 0:
                    return float('inf')

                # remember to rectify min/max relative to our turn!
                exploit = child.avg_reward() * parent.pos.turn
                explore = math.sqrt(math.log(parent.visits) / child.visits )

                # ucb1, with exploration constant 1
                return exploit + (1 * explore)

            child = max(children, key=_value)
            path.append(child)

        return path


    def expand(self, node):
        """
        Expand the tree from a given node, adding empty nodes for all legal moves
        """
        for mv in node.pos.legal():
            child_pos = node.pos.copy()
            child_pos.make_move(mv)
            child = MCTSNode(child_pos)
            self.children[node].add(child)

    def simulate(self, node):
        def single_sim():
            pos = node.pos.copy()
            while True:
                res = pos.result()
                if res is not None:
                    # print(res)
                    return res

                mv = random.choice(list(pos.legal()))
                pos.make_move(mv)

        return sum(single_sim() for i in range(self.sims)) / self.sims


    def backprop(self, path, reward):
        # reversed/not reversed doesn't really matter
        for node in path:
            node.visits += 1
            node.reward += reward


def test_mcts():
    import games

    margin = 0.5
    tests = [
        ([
            0,-1, 0,
            0, 1, 0,
            0, 0, 0, 1
        ], 1),
        ([
            0, 1, 0,
            0,-1, 0,
            0, 0, 0, -1
        ], -1),

        ([
            0, 0, 0,
            0, 0, 0,
            0, 0, 0, 1
        ], 0)
    ]

    for test in tests:
        state, score = test
        # TODO: Move this decoding state logic in games.py
        t = games.TicTacToe(board=state[:9], turn=state[-1])

        mcts = MCTS(t)

        for _ in range(1000):
            mcts.step()

        # forced white win
        mcts_score = mcts.root.avg_reward()
        assert abs(mcts_score - score) < margin, f'got {mcts_score} want {score} pos: {t}'



if __name__ == '__main__':
    test_mcts()
