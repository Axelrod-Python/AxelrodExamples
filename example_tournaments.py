
"""
Runs example tournaments using the Axelrod library available at
https://github.com/marcharper/Axelrod
"""

import multiprocessing
import os
import sys

import axelrod


def ensure_directory(directory):
    """Makes sure that a directory exists and creates it if it does not."""

    head, tail = os.path.split(directory)
    if head:
        ensure_directory(head)

    if not os.path.isdir(directory):
        os.mkdir(directory)

def axelrod_strategies(cheaters=False):
    """Obtains the list of strategies from Axelrod."""

    s = []
    s.extend(axelrod.basic_strategies)
    s.extend(axelrod.ordinary_strategies)
    if cheaters:
        s.extend(axelrod.cheating_strategies)
    #return s
    return [t() for t in s]

def finite_memory_strategies(lower=0, upper=float('inf')):
    """Filter strategies down to those that have finite memory_depth."""

    strategies = []
    for s in axelrod_strategies():
        if s.memory_depth >= lower and s.memory_depth < upper:
            strategies.append(s)
    return strategies

def memoryone_strategies():
    """Filter strategies down to those that are memoryone, that is having
    memory_depth 0 or 1."""

    return finite_memory_strategies(lower=0, upper=2)

def tscizzle_strategies():
    """The list of strategies used in @tscizzle's Morality Metrics paper."""

    strategies = [
        axelrod.Cooperator(),
        axelrod.Defector(),
        axelrod.Eatherley(),
        axelrod.Champion(),
        axelrod.GTFT(p=0.1),
        axelrod.GTFT(p=0.3),
        axelrod.GoByMajority(soft=True),
        axelrod.GoByMajority(soft=False),
        axelrod.TitFor2Tats(),
        axelrod.Random(0.8),
        axelrod.Random(0.2),
        axelrod.WinStayLoseShift(), # Pavlov
        axelrod.TitForTat(),
        axelrod.TwoTitsForTat(),
        axelrod.Grudger(), # Friedman
        axelrod.Tester(),
        axelrod.SuspiciousTitForTat(),
        axelrod.Joss(0.1),
        axelrod.Joss(0.3),
    ]
    return strategies

def sp_strategies():
    """The list of strategies used in Stewart and Plotkin's 2012 tournament."""

    strategies = [
        axelrod.Cooperator(), # ALLC
        axelrod.Defector(), # ALLD
        axelrod.GTFT(),
        axelrod.GoByMajority(soft=False), # HARD_MAJO
        #axelrod.GoByMajority(soft=True), # SOFT_MAJO
        axelrod.TitFor2Tats(), # TFT2
        axelrod.HardTitFor2Tats(), # HARD_TFT2
        axelrod.Random(), # RANDOM
        axelrod.WinStayLoseShift(), # WSLS
        axelrod.TitForTat(),
        axelrod.HardTitForTat(), # HARD_TFT
        axelrod.Grudger(), # GRIM
        axelrod.Joss(), # HARD_JOSS
        axelrod.ZDGTFT2(),
        axelrod.ZDExtort2(),
        axelrod.Prober(),
        axelrod.Prober2(),
        axelrod.Prober3(),
        axelrod.HardProber(),
        axelrod.Calculator(),
    ]
    return strategies

def run_tournament(name, strategies, repetitions=1000, with_ecological=False,
               processes=None, rebuild_cache=True, noise=0):
    if not processes:
        # Use them all!
        processes = multiprocessing.cpu_count()
    # Make sure the output directories exist
    output_directory = os.path.join("assets", name)
    ensure_directory(output_directory)

    # Set up a tournament manager
    tm = axelrod.TournamentManager(output_directory=output_directory,
                                   with_ecological=with_ecological,
                                   save_cache=rebuild_cache)
    tm.add_tournament(name, strategies, repetitions=repetitions,
                      processes=processes, noise=noise)
    # Run the tournaments
    tm.run_tournaments()

if __name__ == "__main__":
    try:
        repetitions = int(sys.argv[1])
    except:
        repetitions = 20
    noise = 0.05

    for strategies, name in [
        (memoryone_strategies(), "Memoryone"),
        (finite_memory_strategies(), "FiniteMemory"),
        (tscizzle_strategies(), "tscizzle"),
        (sp_strategies(), "StewartPlotkin2012"),
        (axelrod_strategies(cheaters=False), "AllFairStrategies")]:
        print "Running tournament: %s with %s strategies, repeated %s times" % (name, len(strategies), repetitions)
        run_tournament(name, strategies, repetitions=repetitions)

        print "Running tournament: %s with %s strategies, repeated %s times, with noise" % (name, len(strategies), repetitions)
        run_tournament(name + "-5", strategies, repetitions=repetitions, noise=noise)



