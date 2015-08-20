
"""
Runs example tournaments using the Axelrod library available at
https://github.com/marcharper/Axelrod
"""

import argparse
import multiprocessing
import os
import sys

import numpy

import axelrod

from example_tournaments import tscizzle_strategies, run_tournament


def tscizzle_metrics():
    strategies = tscizzle_strategies()
    results = run_tournament("Tscizzle", strategies)
    for i in range(len(results.players)):
        row = [str(results.players[i]), numpy.mean(results.normalised_scores[i]), results.cooperation_rates[i], results.good_partner_rating[i], results.eigenjesus_rating[i], results.eigenmoses_rating[i]]
        print ",".join(map(str, row))


if __name__ == "__main__":
    tscizzle_metrics()