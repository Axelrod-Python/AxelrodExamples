
"""
Morality metrics using the Axelrod library available at
https://github.com/marcharper/Axelrod
"""

import itertools

import numpy

import axelrod

from example_tournaments import axelrod_strategies, tscizzle_strategies, random_strategies, memoryone_strategies, run_tournament


def compute_metrics(strategies, noise=0):
    results = run_tournament("tournament", strategies, noise=noise)
    rows = []
    for i in range(len(results.players)):
        row = [str(results.players[i]), numpy.mean(results.normalised_scores[i]), numpy.mean(results.normalised_cooperation[i]), results.good_partner_rating[i], results.eigenjesus_rating[i], results.eigenmoses_rating[i]]
        rows.append(row)
    return rows

def print_rows(rows):
    for row in rows:
        print ",".join(map(str, row))

def wrap_html_tag(tag, data, attr=None):
    attr_str = ""
    if attr: # it's a dict
        for k, v in attr.items():
            attr_str += ' %s="%s"' % (k, v)
    return '<%s%s>%s</%s>' % (tag, attr_str, data, tag)

def row_to_html(row, attr=None, header=False):
    tag = "td"
    if header:
        tag = "th"
    html = ""
    for x in row:
        if not isinstance(x, str):
            x = round(x, 3)
        html += wrap_html_tag(tag, x)
    html = wrap_html_tag("tr", html, attr=attr) + "\n"
    return html

def rows_to_html_table(rows, headers):
    # Headers
    header_html = row_to_html(headers, header=True)
    html = wrap_html_tag("thead", header_html)

    # Body
    body_html = ""
    for row, class_ in itertools.izip(rows, itertools.cycle(["", "alt"])):
        body_html += row_to_html(row, {"class": class_})
    body_html = wrap_html_tag("tbody", body_html)
    html += body_html

    # Wrap in a table tag
    html = wrap_html_tag("table", html, {"class": "tablesorter"})
    return html


def tft_strats():
    strategies = [
        axelrod.TitForTat(),
        axelrod.Alternator(),
        axelrod.CyclerCCD(),
        axelrod.CyclerCCCD(),
        axelrod.CyclerCCCCCD(),
        axelrod.AntiCycler(),
        axelrod.WinStayLoseShift(),
        axelrod.FoolMeOnce()
    ]
    return strategies

if __name__ == "__main__":
    headers = ["Player Name", "Mean Score", "Cooperation Rate",
               "Good Partner Rating", "EigenJesus", "EigenMoses"]

    #strategies = tscizzle_strategies()
    #strategies = axelrod_strategies(cheaters=False, meta=False)
    #strategies = random_strategies()
    strategies = tft_strats()
    rows = compute_metrics(strategies)
    print(rows_to_html_table(rows, headers))
