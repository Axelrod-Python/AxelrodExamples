"""
Generate RST figure markup for README.
"""

import os

def ensure_length(s, length):
    """Append spaces until len(s) is at least length."""
    if len(s) < length:
        s += " "*(length - len(s))
    return s

def generate_readme_markup(name):

    s = """
    .. |{0}_{1}| image:: ../assets/{0}/{0}_{1}.png
    :width: 75%
    :align: middle
    :alt: {0} {1} without noise

    .. |{0}_{1}_noise| image:: ../assets/{0}-noise/{0}_{1}.png
    :width: 75%
    :align: middle
    :alt: {0} {1} with 5% noise

    +------------------------------------+------------------------------------+
    | {2} | {3} |
    +------------------------------------+------------------------------------+

    """

    for type_, header in [("boxplot", "Score Distributions"),
                         ("payoff", "Pairwise Payoffs")]:
        s21 = "|{0}_{1}|".format(name, type_)
        s21 = ensure_length(s21, 34)
        s22 = "|{0}_{1}_noise|".format(name, type_)
        s22 = ensure_length(s22, 34)
        output = s.format(name, type_, s21, s22)
        print header
        print "*"*len(header)
        print output



if __name__ == "__main__":
    names = os.listdir("assets")
    for name in sorted(names):
        if "-noise" in name:
            continue
        print name
        generate_readme_markup(name)