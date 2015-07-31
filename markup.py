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
<div style="text-align:center">
<img src ="/assets/{0}/{0}_{1}.png" width="45%" alt="{0} {1} without noise"/>
<img src ="/assets/{0}-noise/{0}-noise_{1}.png" width="45%" alt="{0} {1} with 
5% noise"/>
</div>
"""

    for type_, header in [("boxplot", "Score Distributions"),
                         ("payoff", "Pairwise Payoffs")]:
        output = s.format(name, type_)
        print header
        print "*"*len(header)
        print output


if __name__ == "__main__":
    names = os.listdir("assets")
    for name in sorted(names):
        if "-noise" in name:
            continue
        generate_readme_markup(name)