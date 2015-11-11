
"""
Runs example tournaments using the Axelrod library available at
https://github.com/Axelrod-Python/Axelrod

Requires python 3.4+
"""

import argparse
import csv # python 3+ usage
import itertools
from operator import itemgetter, attrgetter
import os
from pathlib import Path # python 3.4+
import sys

import numpy
import matplotlib
from matplotlib import pyplot, gridspec

import axelrod

from example_tournaments import axelrod_strategies, ensure_directory

## Python 3.5
#def ensure_directory(path):
    #path.mkdir(parents=True, exist_ok=True)

## Commandline arguments

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

    parser.add_argument(
        '-d', '--data',
        action="store_true",
        help='Generate Data')


    args = parser.parse_args()

    return (args.turns, args.repetitions, args.noise,
            args.function, args.data)

# Various helpers

def normalized_name(player):
    """Normalizes the player name."""
    player_name = str(player)
    for char1, char2 in [('/', '-'), ('\\', ''), ('$', '')]:
        player_name = player_name.replace(char1, char2)
    return player_name

def game_extremes():
    """Returns the max and min game matrix values to set the colorbar
    endpoints."""
    game = axelrod.Game()
    scores = game.RPST()
    return min(scores), max(scores)

def unzip(l):
    """Unpacks a list of tuples pairwise to a lists of lists:
    [('a', 1), ('b', 2)] becomes [['a', 'b'], [1, 2]]"""
    return zip(*l)

## Generate match results and cache to CSV

def csv_filename(player, opponent):
    """Provides a standardized filename for storing and loading match data."""
    filename = "{}--{}.csv".format(normalized_name(player), normalized_name(opponent))
    return filename

def load_match_csv(player, opponent):
    """Loads a cached CSV file. Returns a list of lists of match plays:
        [
            [('C', 'D'), ('C', 'C'), ... ],
            ...
        ]
    This function will also attempt to change the order if the data is not found,
    since swapping player and opponent will only change the order of plays.
    """
    reverse = False
    filename = csv_filename(player, opponent)
    path = Path("csv") / "matches" / filename
    # Check to see if data exists for the other permutation
    if not path.exists():
        reverse = True
        filename = csv_filename(opponent, player)
        path = Path("csv") / "matches" / filename
        # No match data exists for these two players
        if not path.exists:
            raise FileNotFoundError("No match data found")
    with path.open('r') as csvfile:
        reader = csv.reader(csvfile)
        # Separate the plays in each round, handle reversing
        index0, index1 = 0, 1
        if reverse:
            index0, index1 = 1, 0
        for row in reader:
            yield [(elem[index0], elem[index1]) for elem in row]

def write_match_to_csv(data, filename, data_directory="csv"):
    """Takes match data (or a generator) and writes the data to a csv file."""
    #ensure_directory("csv")
    path = Path("csv") / "matches" / filename
    with path.open('w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            csv_row = ["".join(element) for element in row]
            writer.writerow(csv_row)

def generate_match_results(player, opponent, turns=200, repetitions=100,
                           noise=0):
    """Generates match date between two players. Yields rows of the form
    [(C, D), (C, C), ...]."""
    # Make sure we have two distinct player objects
    if player == opponent:
        opponent = opponent.clone()
    # Set tournament_attributes
    tournament_attributes = {'length': turns, 'game': axelrod.Game()}
    player.tournament_attributes = tournament_attributes
    opponent.tournament_attributes = tournament_attributes

    # Run matches
    row = []
    for _ in range(repetitions):
        # Compute a new match
        row = []
        # Reset any accumulated history
        player.reset()
        opponent.reset()
        # Compute rounds and write to CSV
        for _ in range(turns):
            player.play(opponent, noise=noise)
        yield zip(player.history, opponent.history)

def save_all_match_results(players, turns=200, repetitions=100, noise=0):
    """Caches match results for all pairs of players"""
    for p1, p2 in itertools.combinations_with_replacement(players, 2):
        print(p1, p2)
        # Check if the outcome will be deterministic. If so, only run one repetition
        if p1.classifier['stochastic'] or p2.classifier['stochastic'] or noise:
            repetitions_ = repetitions
        else:
            repetitions_ = 1
        data = generate_match_results(p1, p2, turns=turns,
                                        repetitions=repetitions_, noise=noise)
        filename = csv_filename(p1, p2)
        write_match_to_csv(data, filename)

## Classes to reduce the data sets in various ways

class CooperationAggregator(object):
    """Aggregates the cooperation probability per round over many histories."""
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
    """Aggregates the cooperation probability of the opponentper round over
    many histories."""
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
    """Aggregates the mean score per round over many histories."""
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
    """Aggregates the mean score difference per round over many histories."""
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



#def iterate_plays(player, opponents, turns=200, repetitions=50, noise=0, aggClass=None):
    #"""Runs many sequences of play to generate play data for computing the
    #average score per turn for each opponent.

    #For the given player and list of opponents, `repetitions` matches are played
    #for each opponent and the results aggregated.

    #"""
    #tournament_attributes = {
        #'length': turns,
        #'game': axelrod.Game()}
    #data = []
    #for i, opponent in enumerate(opponents):
        #aggregator = aggClass()
        ## Check if the outcome will be deterministic. If so, only run one repetition
        #if player.classifier['stochastic'] or opponent.classifier['stochastic'] or noise:
            #repetitions_ = repetitions
        #else:
            #repetitions_ = 1
        #for _ in range(repetitions_):
            #player_ = player.clone()
            #opponent_ = opponent.clone()
            #player_.tournament_attributes = tournament_attributes
            #opponent_.tournament_attributes = tournament_attributes

            #for _ in range(turns):
                #player_.play(opponent_, noise=noise)
            #aggregator.add_data(player_.history, opponent_.history)

            #player_.reset()
            #opponent_.reset()
        #averages = aggregator.normalize()
        #data.append((i, averages))
    #return data

#def apply_aggregator(data, aggregator):
    #for row in data:
        #history1, history2 = unzip(row)
        #aggregator.add_data(history1, history2)
    #return aggregator.normalize()

def aggregated_data(player, opponents, aggClass=None):
    """Aggregates cached data for player versus every opponent for plotting."""
    data = []
    for i, opponent in enumerate(opponents):
        aggregator = aggClass()
        match_data = load_match_csv(player, opponent)
        for row in match_data:
            # Produce two history lists
            history1, history2 = unzip(row)
            aggregator.add_data(history1, history2)
        averages = aggregator.normalize()
        data.append((i, averages))
    return data

def aggregated_data_to_csv(player, opponents, aggClass=None):
    """Aggregates cached data for player versus every opponent for plotting."""
    data = []
    for i, opponent in enumerate(opponents):
        aggregator = aggClass()
        match_data = load_match_csv(player, opponent)
        for row in match_data:
            # Produce two history lists
            history1, history2 = unzip(row)
            aggregator.add_data(history1, history2)
        averages = aggregator.normalize()
        data.append((i, averages))
    return data

    path = Path("csv") / "matches" / filename
    with path.open('w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            csv_row = ["".join(element) for element in row]
            writer.writerow(csv_row)



def visualize_strategy(data, player, opponents, directory, turns=200,
                       repetitions=200, noise=0, cmap=None, sort=False,
                       vmin=0, vmax=1,):
    """Plots the average (e.g.) cooperate rate or score per turn for `player` versus
    every opponent in `opponents`."""
    if not cmap:
        cmap = pyplot.get_cmap("RdBu")
    if sort:
        data.sort(key=itemgetter(1))
        sort_order = [x[0] for x in data]
    else:
        sort_order = range(len(opponents))

    data = [x[-1] for x in data] # Toss the sorting index and just graph the value
    data = numpy.array(data)

    player_name = normalized_name(player)

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

    filename = os.path.join(directory, "%s.png" % (player_name,))
    pyplot.savefig(filename)
    pyplot.close(fig)


def make_figures(strategies, opponents, turns=200, repetitions=50,
                 noise=0, function="c"):
    # Score heatmaps
    if function == 's':
        cmap = pyplot.get_cmap("autumn")
        directory = "score"
        vmin, vmax = game_extremes()
        aggClass = ScoreAggregator
    # Score Diff heatmaps
    elif function == 'sd':
        cmap = pyplot.get_cmap("autumn")
        directory = "score_diff"
        vmin, vmax = game_extremes()
        aggClass = ScoreDiffAggregator
    # Cooperation heatmaps
    elif function == 'c':
        cmap = pyplot.get_cmap("RdBu")
        directory = "cooperation"
        vmin, vmax = None, None
        aggClass = CooperationAggregator
    # Opponent_cooperation_heatmaps
    elif function == 'oc':
        cmap = pyplot.get_cmap("RdBu")
        directory = "opponent_cooperation"
        vmin, vmax = None, None
        aggClass = OpponentCooperationAggregator
    else:
        raise ValueError("Invalid function option")
    if noise:
        directory += "-noisy"
    path = Path("assets") / "heatmaps" / directory

    for index, player in enumerate(strategies):
        print(index, function, player)
        data = aggregated_data(player, opponents, aggClass=aggClass)
        #data = iterate_plays(strategy, opponents, turns=turns, aggClass=aggClass,
                             #repetitions=repetitions, noise=noise)

        visualize_strategy(data, player, opponents, directory=str(path), noise=noise,
                           cmap=cmap, vmin=vmin, vmax=vmax)
        matplotlib.pyplot.close("all")

def init():
    # Check python version
    version = sys.version.split('.')
    if (int(version[0]) == 2) or (int(version[0] == 3) and int(version[1]) < 4):
        print("Python 3.4+ is required")
        sys.exit()
    # Make sure all the necessary paths exist
    path = Path("assets")
    ensure_directory(str(path))
    path = path / "csv"
    ensure_directory(str(path))
    path = path / "matches"
    ensure_directory(str(path))

    path = Path("assets")
    ensure_directory(str(path))
    path = path / "heatmaps"
    ensure_directory(str(path))
    for sub in ["score", "score_diff", "cooperation", "opponent_cooperation"]:
        path = Path("assets") / "heatmaps" / sub
        ensure_directory(str(path))
        path = Path("assets") / "heatmaps" / (sub + "-noisy")
        ensure_directory(str(path))

def generate_data(players):
    save_all_match_results(players, turns=200, repetitions=1000)

"""Todo:
save aggregrated data to csv
"""

if __name__ == "__main__":
    init()
    turns, repetitions, noise, function, gen_data = parse_args()

    # Grab the strategy lists from axelrod
    players = list(reversed(axelrod_strategies()))
    opponents = list(players)

    # Generate the data?
    if gen_data:
        save_all_match_results(players, turns=200, repetitions=1000)
        exit()

    # Visualizations
    make_figures(players, opponents, turns=turns, repetitions=repetitions,
                 noise=noise, function=function)
