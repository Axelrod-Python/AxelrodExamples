
"""
Inferring memory depth of Iterated Prisoner's Dilemma strategies
using scipy and the Axelrod library.
"""

from itertools import islice

import numpy
from scipy import stats

import axelrod

C, D = axelrod.Actions.C, axelrod.Actions.D # The plays


def fet_tests(data_dict):
    """Performs four Fisher exact tests on each possible context."""
    # What has the opponent been doing?
    C_count = sum(v[0] for (k, v) in data_dict.items())
    D_count = sum(v[1] for (k, v) in data_dict.items())

    test_results = dict()
    # Pull out the C and D counts for each context
    for context in data_dict.keys():
        C_count_context = data_dict[context][0]
        D_count_context = data_dict[context][1]

        # Build the conditional table
        table = numpy.array([[C_count, D_count], [C_count_context, D_count_context]])

        # Run the Fisher test
        test_stat, pvalue = stats.fisher_exact(table)
        test_results[context] = (test_stat, pvalue)

    return test_results

def memory_one_estimate(data_dict):
    """Estimates the memory one strategy probabilities from the observed
    data."""
    estimates = dict()
    for context in data_dict.keys():
        C_count = data_dict[context][0]
        D_count = data_dict[context][1]
        try:
            estimates[context] = float(C_count) / (C_count + D_count)
        except ZeroDivisionError:
            estimates[context] = None
    return estimates

def print_dict(d):
    for key, value in sorted(d.items()):
        print key, value

def collect_data(opponent):
    """Generator to collect data from opponent."""
    player = axelrod.Random(0.5)  # The probe strategy
    while True:
        player.play(opponent)
        yield (player.history[-1], opponent.history[-1])

def infer_depth(opponent, test_rounds=200):
    """Collect data and report statistical tests."""
    data_dict = {(C, C): [0, 0],
                 (C, D): [0, 0],
                 (D, C): [0, 0],
                 (D, D): [0, 0]}
    # Save the history locally as we go
    history = []
    for turn in islice(collect_data(opponent), test_rounds + 1):
        history.append(turn)
        if len(history) < 2:
            continue
        # Record opponents play and context
        context = history[-2]
        # Context is reversed for opponent
        context = (context[1], context[0])
        # Count the opponent's Cs and Ds
        if turn[1] == C:
            data_dict[context][0] += 1
        else:
            data_dict[context][1] += 1
    # Perform the Fisher tests
    test_results = fet_tests(data_dict)
    # Estimate the four conditional probabilities
    estimate = memory_one_estimate(data_dict)
    
    return data_dict, test_results, estimate

def main():
    strategies = [axelrod.Cooperator(), axelrod.Defector(),
                  axelrod.Random(0.4), axelrod.Random(0.5), axelrod.Random(0.9),
                  axelrod.Alternator(),
                  axelrod.TitForTat(), axelrod.GTFT(),
                  axelrod.WinStayLoseShift(), axelrod.ZDGTFT2(),
                  axelrod.ZDExtort2(),
                  axelrod.TitFor2Tats(), axelrod.TwoTitsForTat(),
                  axelrod.CyclerCCD(), axelrod.CyclerCCCD(),
                  axelrod.CyclerCCCCCD(), axelrod.HardTitForTat(),
                  axelrod.AntiCycler(),
                  axelrod.Grudger()]

    for opponent in strategies:
        data_dict, test_results, estimate = infer_depth(opponent)

        print opponent
        print "-"*len(str(opponent))
        print "Collected Data"
        print_dict(data_dict)
        C_count = sum(v[0] for (k, v) in data_dict.items())
        D_count = sum(v[1] for (k, v) in data_dict.items())
        print "C count, D count: %s, %s" % (C_count, D_count)
        print "\nFisher Exact Tests"
        print_dict(test_results)
        print "\nEstimated Memory One Probabilities"
        print_dict(estimate)
        print


if __name__ == "__main__":
    main()

