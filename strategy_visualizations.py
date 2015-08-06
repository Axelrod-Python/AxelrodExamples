
"""
Runs example tournaments using the Axelrod library available at
https://github.com/marcharper/Axelrod
"""

import copy
import multiprocessing
import os
import random
import sys

from operator import itemgetter, attrgetter

import numpy
import matplotlib
#matplotlib.use('AGG')
from matplotlib import pyplot, gridspec

import axelrod
from axelrod import Game


def ensure_directory(directory):
    """Makes sure that a directory exists and creates it if it does not."""

    head, tail = os.path.split(directory)
    if head:
        ensure_directory(head)

    if not os.path.isdir(directory):
        os.mkdir(directory)

def axelrod_strategies(cheaters=False, remove_meta=True):
    """Obtains the list of strategies from Axelrod library."""

    s = []
    s.extend(axelrod.basic_strategies)
    s.extend(axelrod.ordinary_strategies)
    if cheaters:
        s.extend(axelrod.cheating_strategies)
    if remove_meta:
        s = [t for t in s if not t.__name__.startswith("Meta")]
    # Instantiate
    s = [t() for t in s]
    # Sort by name
    s.sort(key=str)
    return s

def average_plays(plays):
    """Computes how often a strategy cooperates per turn versus each opponent."""
    averages = []
    mapping = {'C': 1, 'D': 0}
    num_cols = len(plays[0])
    num_rows = len(plays)
    for col in range(num_cols):
        s = 0.
        for row in range(num_rows):
            s += mapping[plays[row][col]]
        averages.append(s / num_rows)
    return averages

def compute_cooperation_data(player, opponents, directory, turns=200,
                             repetitions=50, noise=0,):
    """Runs many sequences of play to generate play data for computing the
    cooperation average per turn for each opponent."""
    data = []
    for i, opponent in enumerate(opponents):
        plays = []
        for _ in range(repetitions):
            player_ = copy.deepcopy(player)
            player_.reset()
            opponent_ = copy.deepcopy(opponent)
            opponent_.reset()
            for _ in range(turns):
                player_.play(opponent_, noise=noise)
            plays.append(player_.history)
        averages = average_plays(plays)
        data.append((i, averages))
    return data

def average_scores(plays):
    """Computes the average score per turn versus each opponent."""
    averages = []
    game = Game()
    mapping = game.scores
    num_cols = len(plays[0][0])
    num_rows = len(plays)
    for col in range(num_cols):
        s = 0.
        for row in range(num_rows):
            s += mapping[ (plays[row][0][col], plays[row][1][col]) ][0]
        averages.append(s / num_rows)
    return averages

def compute_score_data(player, opponents, directory, turns=200, repetitions=50,
                       noise=0,):
    """Runs many sequences of play to generate play data for computing the
    average score per turn for each opponent."""
    data = []
    for i, opponent in enumerate(opponents):
        plays = []
        for _ in range(repetitions):
            player_ = copy.deepcopy(player)
            player_.reset()
            opponent_ = copy.deepcopy(opponent)
            opponent_.reset()
            for _ in range(turns):
                player_.play(opponent_, noise=noise)
            plays.append((player_.history, opponent_.history))
        averages = average_scores(plays)
        data.append((i, averages))
    return data

def visualize_strategy(player, opponents, directory, turns=200, repetitions=200,
                       noise=0, cmap=None, sort=False, vmin=0, vmax=1,
                       func=compute_cooperation_data):
    """Plots the average cooperate rate or score per turn for `player` versus
    every opponent in `opponents`."""
    if not cmap:
        cmap = pyplot.get_cmap("RdBu")
    # Compute many rounds of play and average
    data = func(player, opponents, directory, turns=turns, repetitions=repetitions, noise=noise)

    if sort:
        data.sort(key=itemgetter(1))
        sort_order = [x[0] for x in data]
    else:
        sort_order = range(len(opponents))
    data = [x[1] for x in data]
    data = numpy.array(data)

    player_name = str(player)
    player_name = player_name.replace('/', '-')
    print player_name

    # Plot the data in a pcolor colormap
    pyplot.clf()
    #figure = pyplot.figure()
    fig, ax = pyplot.subplots(figsize=(30, 15))
    sm = ax.pcolor(data, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_ylim(0, len(strategies))
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

def game_extremes():
    """
    Returns the max and min game matrix values to set the colorbar endpoints.
    """
    game = axelrod.Game()
    scores = game.RPST()
    return min(scores), max(scores)

if __name__ == "__main__":
    strategies = list(reversed(axelrod_strategies()))

    matplotlib.pyplot.close("all")
    vmin, vmax = game_extremes()

    # Score heatmaps
    cmap = pyplot.get_cmap("autumn")
    for directory, noise in [("score_heatmaps", 0),
                             ("score_heatmaps_noise", 0.05)]:
        for strategy in strategies:
            visualize_strategy(strategy, strategies, directory, noise=noise,
                               func=compute_score_data, cmap=cmap, vmin=vmin,
                               vmax=vmax)

    # Cooperation heatmaps
    for directory, noise in [("cooperation_heatmaps", 0), 
                             ("cooperation_heatmaps_noise", 0.05)]:
        for strategy in strategies:
            visualize_strategy(strategy, strategies, directory, noise=noise,
                               func=compute_cooperation_data)
