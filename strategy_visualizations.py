
"""
Runs example tournaments using the Axelrod library available at
https://github.com/Axelrod-Python/Axelrod
"""

import argparse
import copy
import os
from operator import itemgetter, attrgetter

import numpy
import matplotlib
from matplotlib import pyplot, gridspec

import axelrod

from example_tournaments import axelrod_strategies, ensure_directory


def parse_args():

    parser = argparse.ArgumentParser(description="Run Sample Axelrod tournaments")

    parser.add_argument(
        '-f',
        '--function',
        type=str,
        default='c',
        help="Must be c, oc, s, or sd")

    parser.add_argument(
        '-t',
        '--turns',
        type=int,
        default=200,
        help='turns per pair')

    parser.add_argument(
        '-r', '--repetitions',
        type=int,
        default=200,
        help='round-robin repetitions')

    parser.add_argument(
        '-n', '--noise',
        type=float,
        default=0,
        help='Noise level')

    args = parser.parse_args()

    return (args.turns, args.repetitions, args.noise,
            args.function)

def game_extremes():
    """
    Returns the max and min game matrix values to set the colorbar endpoints.
    """
    game = axelrod.Game()
    scores = game.RPST()
    return min(scores), max(scores)


class CooperationAggregator(object):
    def __init__(self):
        self.mapping = {'C': 1, 'D': 0}
        self.counts = []
        self.rows = 0

    def add_data(self, row1, row2):
        if not self.counts:
            self.counts = [0] * len(row1)
        for i, play in enumerate(row1):
            self.counts[i] += self.mapping[play]
        self.rows += 1

    def normalize(self):
        return numpy.array(self.counts) / float(self.rows)


class OpponentCooperationAggregator(object):
    def __init__(self):
        self.mapping = {'C': 1, 'D': 0}
        self.counts = []
        self.rows = 0

    def add_data(self, row1, row2):
        if not self.counts:
            self.counts = [0] * len(row2)
        for i, play in enumerate(row2):
            self.counts[i] += self.mapping[play]
        self.rows += 1

    def normalize(self):
        return numpy.array(self.counts) / float(self.rows)


class ScoreAggregator(object):
    def __init__(self):
        game = axelrod.Game()
        self.mapping = game.scores
        self.counts = []
        self.rows = 0

    def add_data(self, row1, row2):
        if not self.counts:
            self.counts = [0] * len(row1)
        for i, (play1, play2) in enumerate(zip(row1, row2)):
            play = (play1, play2)
            self.counts[i] += self.mapping[play][0]
        self.rows += 1

    def normalize(self):
        return numpy.array(self.counts) / float(self.rows)


class ScoreDiffAggregator(object):
    def __init__(self):
        game = axelrod.Game()
        self.mapping = game.scores
        self.counts = []
        self.rows = 0

    def add_data(self, row1, row2):
        if not self.counts:
            self.counts = [0] * len(row1)
        for i, (play1, play2) in enumerate(zip(row1, row2)):
            play = (play1, play2)
            self.counts[i] += self.mapping[play][0] - self.mapping[play][1]
        self.rows += 1

    def normalize(self):
        return numpy.array(self.counts) / float(self.rows)


def iterate_plays(player, opponents, turns=200, repetitions=50, noise=0, aggClass=None):
    """Runs many sequences of play to generate play data for computing the
    average score per turn for each opponent."""
    data = []
    for i, opponent in enumerate(opponents):
        aggregator = aggClass()
        if player.stochastic or opponent.stochastic or noise:
            repetitions_ = repetitions
        else:
            repetitions_ = 1
        for _ in range(repetitions_):
            player.reset()
            opponent.reset()
            player.tournament_length = turns
            opponent.tournament_length = turns
            for _ in range(turns):
                player.play(opponent, noise=noise)
            aggregator.add_data(player.history, opponent.history)
            player.reset()
            opponent.reset()
        averages = aggregator.normalize()
        data.append((i, averages))
    return data

def visualize_strategy(data, player, opponents, directory, turns=200,
                       repetitions=200, noise=0, cmap=None, sort=False,
                       vmin=0, vmax=1,):
    """Plots the average cooperate rate or score per turn for `player` versus
    every opponent in `opponents`."""
    if not cmap:
        cmap = pyplot.get_cmap("RdBu")
    if sort:
        data.sort(key=itemgetter(1))
        sort_order = [x[0] for x in data]
    else:
        sort_order = range(len(opponents))

    data = [x[-1] for x in data]
    data = numpy.array(data)

    player_name = str(player)
    player_name = player_name.replace('/', '-')

    # Plot the data in a pcolor colormap
    pyplot.clf()
    fig, ax = pyplot.subplots(figsize=(30, 15))
    sm = ax.pcolor(data, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_ylim(0, len(opponents))
    yticks = [str(opponents[sort_order[i]]) for i in range(len(opponents))]
    ax.set_title(player_name)
    pyplot.yticks([y + 0.5 for y in range(len(yticks))], yticks)
    cbar = pyplot.colorbar(sm, ax=ax)
    pyplot.xlabel("Rounds")

    output_directory = os.path.join("assets", directory)
    ensure_directory(output_directory)

    filename = os.path.join(output_directory, "%s.png" % (player_name,))
    pyplot.savefig(filename)
    pyplot.close(fig)


def make_figures(strategies, opponents, turns=200, repetitions=50,
                 noise=0, function="c"):
    # Score heatmaps
    if function == 's':
        cmap = pyplot.get_cmap("autumn")
        directory = "score_heatmaps"
        #func = compute_score_data
        vmin, vmax = game_extremes()
        aggClass = ScoreAggregator
    # Score Diff heatmaps
    elif function == 'sd':
        cmap = pyplot.get_cmap("autumn")
        directory = "score_diff_heatmaps"
        #func = compute_score_data
        vmin, vmax = game_extremes()
        aggClass = ScoreDiffAggregator
    # Cooperation heatmaps
    elif function == 'c':
        cmap = pyplot.get_cmap("RdBu")
        directory = "cooperation_heatmaps"
        #func = compute_cooperation_data
        vmin, vmax = None, None
        aggClass = CooperationAggregator
    # Opponent_cooperation_heatmaps
    elif function == 'oc':
        cmap = pyplot.get_cmap("RdBu")
        directory = "opponent_cooperation_heatmaps"
        #func = compute_cooperation_data
        vmin, vmax = None, None
        aggClass = OpponentCooperationAggregator
    else:
        raise ValueError("Invalid function option")
    if noise:
        directory += "_noise"

    for index, strategy in enumerate(strategies):
        print(index, function, strategy)
        data = iterate_plays(strategy, opponents, turns=turns, aggClass=aggClass,
                             repetitions=repetitions, noise=noise)
        visualize_strategy(data, strategy, opponents, directory, noise=noise,
                           cmap=cmap, vmin=vmin, vmax=vmax)
        matplotlib.pyplot.close("all")

if __name__ == "__main__":
    strategies = list(reversed(axelrod_strategies()))
    opponents = list(reversed(axelrod_strategies()))

    turns, repetitions, noise, function = parse_args()

    make_figures(strategies, opponents, turns=turns, repetitions=repetitions,
                 noise=noise, function=function)
