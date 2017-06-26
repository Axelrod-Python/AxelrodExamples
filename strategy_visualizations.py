
"""
Runs example tournaments using the Axelrod library available at
https://github.com/Axelrod-Python/Axelrod

Requires python 3.4+
"""

import argparse
from collections import Counter, defaultdict
import csv
import itertools
from operator import itemgetter
import os
from pathlib import Path
import sys

import numpy
import matplotlib
from matplotlib import pyplot as plt

import axelrod

from example_tournaments import axelrod_strategies, ensure_directory, run_tournament

C, D = "C", "D"

# Commandline arguments


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
        default=False,
        action="store_true",
        help='Generate Data')

    args = parser.parse_args()

    return (args.turns, args.repetitions, args.noise,
            args.function, args.data)

# Various helpers


def counter_mean(counter):
    """Takes the mean of a collections.Counter object (or dictionary)."""
    mean = 0.
    total = 0.
    for k, v in counter.items():
        if k <= 0:
            k = 200
        mean += k * v
        total += v
    return mean / total


def normalized_name(player):
    """Normalizes the player name."""
    player_name = str(player)
    # for char1, char2 in [('/', '-'), ('\\', ''), ('$', '')]:
    #     player_name = player_name.replace(char1, char2)
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


def csv_filename(player, opponent, noise=None):
    """Provides a standardized filename for storing and loading match data."""
    filename = "{}--{}.csv".format(normalized_name(player),
                                   normalized_name(opponent))
    if noise:
        path = Path("assets") / "csv" / "matches-noisy" / filename
    else:
        path = Path("assets") / "csv" / "matches" / filename
    return path


def load_match_csv(player, opponent, noise=None):
    """Loads a cached CSV file. Returns a list of lists of match plays:
        [
            [('C', 'D'), ('C', 'C'), ... ],
            ...
        ]
    This function will also attempt to change the order if the data is not found,
    since swapping player and opponent will only change the order of plays.
    """
    reverse = False
    filename = csv_filename(player, opponent, noise=noise)
    path = Path(filename)
    # Check to see if data exists for the other permutation
    if not path.exists():
        filename = csv_filename(opponent, player, noise=noise)
        path = Path(filename)
        # No match data exists for these two players
        if not path.exists():
            raise FileNotFoundError("No match data found")
        reverse = True
    with path.open('r') as csvfile:
        reader = csv.reader(csvfile)
        # Separate the plays in each round, handle reversing
        index0, index1 = 0, 1
        if reverse:
            index0, index1 = 1, 0
        for row in reader:
            yield [(elem[index0], elem[index1]) for elem in row]


def write_match_to_csv(data, filename):
    """Takes match data (or a generator) and writes the data to a csv file."""
    path = Path(filename)
    with path.open('w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            csv_row = ["".join(element) for element in row]
            writer.writerow(csv_row)


def generate_match_results(player, opponent, turns=200, repetitions=100,
                           noise=None):
    """Generates match date between two players. Yields rows of the form
    [(C, D), (C, C), ...]."""
    # Make sure we have two distinct player objects
    if not noise:
        noise = 0
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


def is_deterministic(p1, p2, noise=0):
    return not (p1.classifier['stochastic'] or p2.classifier['stochastic'] or noise)


def save_all_match_results(players, turns=200, repetitions=100, noise=0):
    """Caches match results for all pairs of players"""
    for p1, p2 in itertools.combinations_with_replacement(players, 2):
        print(p1, p2)
        # Check if the outcome will be deterministic. If so, only run one
        # repetition.
        if is_deterministic(p1, p2, noise):
            repetitions_ = 1
        else:
            repetitions_ = repetitions
        data = generate_match_results(p1, p2, turns=turns,
                                      repetitions=repetitions_, noise=noise)
        filename = csv_filename(p1, p2, noise=noise)
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
    """Aggregates the cooperation probability of the opponent per round over
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


def aggregated_data(player, opponents, aggClass=None, noise=None):
    """Aggregates cached data for player versus every opponent for plotting."""
    data = []
    for i, opponent in enumerate(opponents):
        aggregator = aggClass()
        match_data = load_match_csv(player, opponent, noise=noise)
        for row in match_data:
            # Produce two history lists
            history1, history2 = unzip(row)
            aggregator.add_data(history1, history2)
        averages = aggregator.normalize()
        data.append((i, averages))
    return data


def aggregated_data_to_csv(players, opponents, noise=None):
    """Aggregates cached data for player versus every opponent for plotting."""
    for name, aggClass in [("score", ScoreAggregator),
                           ("score_diff", ScoreDiffAggregator),
                           ("cooperation", CooperationAggregator),
                           ("opponent_cooperation", OpponentCooperationAggregator)
                           ]:
        for player in players:
            data = aggregated_data(player, opponents, aggClass=aggClass,
                                   noise=noise)
            filename = normalized_name(player)
            if noise:
                filename += "_noisy"
            filename += ".csv"
            path = Path("assets") / "csv" / name / filename
            with path.open('w') as csvfile:
                writer = csv.writer(csvfile)
                for i, row in enumerate(data):
                    csv_row = [normalized_name(opponents[i])]
                    csv_row.extend(row[-1])
                    writer.writerow(csv_row)

# Make Figures


def visualize_strategy(data, player, opponents, directory, turns=200,
                       repetitions=200, noise=0, cmap=None, sort=False,
                       vmin=0, vmax=1,):
    """Plots the average (e.g.) cooperate rate or score per turn for `player` versus
    every opponent in `opponents`."""
    if not cmap:
        cmap = plt.get_cmap("RdBu")
    if sort:
        data.sort(key=itemgetter(1))
        sort_order = [x[0] for x in data]
    else:
        sort_order = range(len(opponents))
    # Toss the sorting index and just graph the value
    data = [x[-1] for x in data]
    data = numpy.array(data)

    player_name = normalized_name(player)

    # Plot the data in a pcolor colormap
    plt.clf()
    fig, ax = plt.subplots()
    figure = ax.get_figure()
    height = 16
    width = 24
    figure.set_size_inches(width, height)

    try:
        sm = ax.pcolor(data, cmap=cmap, vmin=vmin, vmax=vmax)
        # sm = ax.matshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
    except:
        plt.close(fig)
        return
    ax.set_ylim(0, len(opponents))
    yticks = [str(opponents[sort_order[i]]) for i in range(len(opponents))]
    ax.set_title(player_name)
    plt.yticks([y + 0.5 for y in range(len(yticks))], yticks)
    cbar = plt.colorbar(sm, ax=ax)
    plt.xlabel("Rounds")

    filename = os.path.join(directory, "%s.png" % (player_name,))
    ax.tick_params(axis='both', which='both', labelsize=8)
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close(fig)


def make_figures(strategies, opponents, turns=200, repetitions=50,
                 noise=0, function="c"):
    # Score heatmaps
    if function == 's':
        cmap = plt.get_cmap("autumn")
        directory = "score"
        vmin, vmax = game_extremes()
        aggClass = ScoreAggregator
    # Score Diff heatmaps
    elif function == 'sd':
        cmap = plt.get_cmap("autumn")
        directory = "score_diff"
        vmin, vmax = game_extremes()
        aggClass = ScoreDiffAggregator
    # Cooperation heatmaps
    elif function == 'c':
        cmap = plt.get_cmap("RdBu")
        directory = "cooperation"
        vmin, vmax = None, None
        aggClass = CooperationAggregator
    # Opponent_cooperation_heatmaps
    elif function == 'oc':
        cmap = plt.get_cmap("RdBu")
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
        data = aggregated_data(player, opponents, aggClass=aggClass, noise=noise)

        visualize_strategy(data, player, opponents, directory=str(path), noise=noise,
                           cmap=cmap, vmin=vmin, vmax=vmax)
        plt.close("all")


def summarize_matchup(player, opponent, initial=10):
    """Compute various quantities of interest for the given matchup."""
    game = axelrod.Game()
    scores = []
    score_diffs = []
    match_data = load_match_csv(player, opponent)
    context_dict = defaultdict(float)
    context_counts = defaultdict(float)
    initial_plays = [0] * initial
    total_plays = 0
    total_matches = 0
    match_length = 0
    first_defection = defaultdict(int)

    for row in match_data:
        match_length = len(row)  # assumes all are equal
        total_matches += 1
        total_plays += len(row)
        score = 0
        score_diff = 0
        for play1, play2 in row:
            s = game.scores[(play1, play2)]
            score += s[0]
            score_diff += s[0] - s[1]
            if play1 == "C":
                context_dict["C_prob"] += 1
        scores.append(score)
        score_diffs.append(score_diff)

        # The rest of the contexts
        for i in range(1, len(row)):
            plays = row[i]
            key = row[i - 1]
            context_counts[key] += 1
            if plays[0] == "C":
                context_dict[key] += 1

        for i in range(2, len(row)):
            plays = row[i]
            key = (row[i - 2], row[i - 1])
            context_counts[key] += 1
            if play1 == "C":
                context_dict[key] += 1

        # initial_plays
        for i in range(len(initial_plays)):
            play = row[i][0]
            if play == "C":
                initial_plays[i] += 1

        # First defection
        my_history = "".join([x[0] for x in row])
        first_occurrence = my_history.find('D')
        first_defection[first_occurrence + 1] += 1

    # normalize and take means
    initial_plays = numpy.array(initial_plays) / float(total_matches)
    context_dict["C_prob"] /= float(total_plays)
    contexts = [(C, C), (C, D), (D, C), (D, D)]

    for context in contexts:
        try:
            context_dict[context] /= context_counts[context]
        except ZeroDivisionError:
            context_dict[context] = "NA"
    for context in itertools.product(contexts, repeat=2):
        try:
            context_dict[context] /= context_counts[context]
        except ZeroDivisionError:
            context_dict[context] = "NA"

    for key in context_counts.keys():
        if key == "C_prob":
            continue
        total = sum([float(v) for (k, v) in context_counts.items() if len(k[0]) == len(key[0])])
        context_counts[key] /= total

    scores = numpy.array(scores) / float(match_length)
    mean_score = numpy.mean(scores)
    std_score = numpy.std(scores)
    score_diffs = numpy.array(score_diffs) / float(match_length)
    mean_score_diff = numpy.mean(score_diffs)
    std_score_diff = numpy.std(score_diffs)

    mean_first_defection = counter_mean(first_defection)

    return (initial_plays, context_dict, context_counts, mean_score,
            std_score, mean_score_diff, std_score_diff, mean_first_defection)


def table_1(players, initial=10):
    """Table 1:
    For each strategy pair, compute the probability of cooperation on the
    first 10 rounds, the mean, median, and deviation for scores, and
    score diffs, probabilities for each context C, D, CC, CD, DC, DD, ...,
    overall C and D."""
    path = Path("assets") / "csv" / "table_1.csv"
    writer = csv.writer(path.open('w'))

    contexts = [(C, C), (C, D), (D, C), (D, D)]
    context_keys = ["C_prob"]
    context_keys.extend(contexts)
    context_keys.extend(itertools.product(contexts, repeat=2))

    header = ["player_name", "opponent_name",  "stochastic", "memory_depth",
              "mean_score", "std_score", "mean_score_diff", "std_score_diff",
              "mean_first_defection"]
    header.extend(["round_" + str(i+1) for i in range(initial)])
    header.append("C_prob")
    header.extend(["".join(x) for x in contexts])
    header.extend(["".join(x) + "".join(y) for (x, y) in
                   itertools.product(contexts, repeat=2)])
    header.extend(["".join(x) + "_pct" for x in contexts])
    header.extend(["".join(x) + "".join(y) + "_pct"  for (x, y) in
                   itertools.product(contexts, repeat=2)])
    writer.writerow(header)

    for p1 in players:
        for p2 in players:
            (initial_plays, context_dict, context_counts, mean_score, std_score, mean_score_diff, std_score_diff, mean_first_defection) = summarize_matchup(p1, p2, initial=initial)
            row = [normalized_name(p1), normalized_name(p2),
                   p1.classifier["stochastic"], p1.classifier["memory_depth"],
                   mean_score, std_score, mean_score_diff, std_score_diff,
                   mean_first_defection]
            row.extend(initial_plays)
            for key in context_keys:
                row.append(context_dict[key])
            for key in context_keys:
                if key == "C_prob":
                    continue
                row.append(context_counts[key])
            writer.writerow(row)


def summarize_player(player, opponents, initial=10, matches=1000):
    game = axelrod.Game()
    scores = []
    score_diffs = []
    context_dict = defaultdict(float)
    context_counts = defaultdict(float)
    initial_plays = [0] * initial
    total_plays = 0
    total_matches = 0
    match_length = 0
    first_defection = Counter()

    for opponent in opponents:
        # For deterministic matches, we only run one round
        # However we want each matchup to contribute equally
        if is_deterministic(player, opponent):
            multiplier = matches
        else:
            multiplier = 1
        match_data = list(load_match_csv(player, opponent))

        for row in match_data:
            match_length = len(row) # assumes all are equal
            total_matches += multiplier
            total_plays += len(row) * multiplier
            score = 0
            score_diff = 0
            for play1, play2 in row:
                s = game.scores[(play1, play2)]
                score += s[0]
                score_diff += s[0] - s[1]
                if play1 == "C":
                    context_dict["C_prob"] += multiplier
            scores.append(score)
            score_diffs.append(score_diff)

            # The rest of the contexts: CC, CD, DC, DD
            for i in range(1, len(row)):
                plays = row[i]
                key = row[i - 1]
                context_counts[key] += multiplier
                if plays[0] == "C":
                    context_dict[key] += multiplier

            # Two-round Contexts
            for i in range(2, len(row)):
                plays = row[i]
                key = (row[i - 2], row[i - 1])
                context_counts[key] += multiplier
                if plays[0] == "C":
                    context_dict[key] += multiplier

            # initial_plays
            for i in range(len(initial_plays)):
                play = row[i][0]
                if play == "C":
                    initial_plays[i] += multiplier

            # First defection
            my_history = "".join([x[0] for x in row])
            first_occurrence = my_history.find('D')
            first_defection[first_occurrence] += multiplier

    # normalize and take means
    initial_plays = numpy.array(initial_plays) / float(total_matches)
    context_dict["C_prob"] /= float(match_length * total_matches)
    contexts = [(C, C), (C, D), (D, C), (D, D)]
    for context in contexts:
        try:
            context_dict[context] /= context_counts[context]
        except ZeroDivisionError:
            context_dict[context] = "NA"
    for context in itertools.product(contexts, repeat=2):
        try:
            context_dict[context] /= context_counts[context]
        except ZeroDivisionError:
            context_dict[context] = "NA"

    for key in context_counts.keys():
        if key == "C_prob":
            continue
        total = sum([float(v) for (k, v) in context_counts.items() if len(k[0]) == len(key[0])])
        context_counts[key] /= total

    scores = numpy.array(scores) / (float(match_length))
    mean_score = numpy.mean(scores)
    std_score = numpy.std(scores)
    score_diffs = numpy.array(score_diffs) / (float(match_length))
    mean_score_diff = numpy.mean(score_diffs)
    std_score_diff = numpy.std(score_diffs)

    mean_first_defection = counter_mean(first_defection)

    return (initial_plays, context_dict, context_counts, mean_score, std_score,
            mean_score_diff, std_score_diff, mean_first_defection)


def table_2(players, initial=10):
    """
    Table 2: for each strategy:
        name
        memory depth
        is_stochastic
        average over all strategies:
            prob cooperation on first 5 moves
            prob cooperation on last 5 moves
            prob cooperation for each context C, D
            prob cooperation for each context CC, CD, DC, DD
            prob cooperation for each context [C, D]**3
    """

    tournament_data = list(load_tournament_data())

    path = Path("assets") / "csv" / "table_2.csv"
    writer = csv.writer(path.open('w'))

    contexts = [(C, C), (C, D), (D, C), (D, D)]
    context_keys = ["C_prob"]
    context_keys.extend(contexts)
    context_keys.extend(itertools.product(contexts, repeat=2))

    header = ["player_name", "stochastic", "memory_depth",
              "mean_score", "std_score", "mean_score_diff", "std_score_diff",
              "mean_first_defection"]
    header.extend(["round_" + str(i+1) for i in range(initial)])
    header.append("C_prob")
    header.extend(["".join(x) for x in contexts])
    header.extend(["".join(x) + "".join(y) for (x, y) in
                   itertools.product(contexts, repeat=2)])
    header.extend(["".join(x) + "_pct" for x in contexts])
    header.extend(["".join(x) + "".join(y) + "_pct"  for (x, y) in
                   itertools.product(contexts, repeat=2)])

    header.extend(["tournament_score_mean", "tournament_score_std",
                   "tournament_win_mean", "tournament_win_std"])

    writer.writerow(header)

    for i, p1 in enumerate(players):
        print(i, "of", len(players))
        (initial_plays, context_dict, context_counts, mean_score,
         std_score, mean_score_diff, std_score_diff, mean_first_defection) = summarize_player(p1, players, initial=initial)
        row = [normalized_name(p1),
                p1.classifier["stochastic"], p1.classifier["memory_depth"],
                mean_score, std_score, mean_score_diff, std_score_diff, mean_first_defection]
        row.extend(initial_plays)
        for key in context_keys:
            row.append(context_dict[key])
        for key in context_keys:
            if key == "C_prob":
                continue
            row.append(context_counts[key])
        row.extend(tournament_data[i][1:]) # ignore name (first element)
        writer.writerow(row)


def tournament_data(players, turns=200, repetitions=100):
    """
    Run tournaments with repetition and record the following:
        mean score
        mean wins
        wins deviation
        score deviation
    """
    results = run_tournament("--", players, turns=turns, repetitions=repetitions)
    score_data = results.normalised_scores
    win_data = results.wins
    mean_scores = [numpy.mean(s) for s in score_data]
    std_scores = [numpy.std(s) for s in score_data]
    mean_wins = [numpy.mean(w) for w in win_data]
    std_wins = [numpy.std(w) for w in win_data]
    return (mean_scores, std_scores, mean_wins, std_wins)


def save_tournament_data(players, turns=200, repetitions=100):
    (mean_scores, std_scores, mean_wins, std_wins) = tournament_data(
        players, turns=200, repetitions=100)
    path = Path("assets") / "csv" / "tournament.csv"
    with path.open('w') as csvfile:
        writer = csv.writer(csvfile)
        for i, player in enumerate(players):
            row = [normalized_name(player), mean_scores[i], std_scores[i],
                   mean_wins[i], std_wins[i]]
            writer.writerow(row)


def load_tournament_data():
    path = Path("assets") / "csv" / "tournament.csv"
    with path.open('r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row


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
    path = Path("assets") / "csv" / "matches-noisy"
    ensure_directory(str(path))

    path = Path("assets")
    ensure_directory(str(path))
    path = path / "heatmaps"
    ensure_directory(str(path))
    for sub in ["score", "score_diff", "cooperation", "opponent_cooperation"]:
        path = Path("assets") / "csv" / sub
        ensure_directory(str(path))
        path = Path("assets") / "heatmaps" / sub
        ensure_directory(str(path))
        path = Path("assets") / "heatmaps" / (sub + "-noisy")
        ensure_directory(str(path))

if __name__ == "__main__":
    init()
    turns, repetitions, noise, function, gen_data = parse_args()

    players = list(reversed(axelrod_strategies(meta=False)))
    opponents = list(reversed(axelrod_strategies(meta=False)))

    # Generate the data?
    if gen_data:
        save_all_match_results(players, turns=200, repetitions=1000,
                               noise=noise)
        aggregated_data_to_csv(players, opponents, noise=noise)
        save_tournament_data(players)
        table_1(players)
        table_2(players)
        exit()

    # We're assuming that the data has been generated going forward
    # Visualizations
    make_figures(players, opponents, turns=turns, repetitions=repetitions,
                 noise=noise, function=function)
