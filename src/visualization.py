
# ============================================================
# src/visualization.py
# ============================================================

# PURPOSE:
# FIFA World Cup 2026 Visualization Engine
#
# FEATURES:
# ✅ Champion probability charts
# ✅ Power ranking charts
# ✅ Attack ranking charts
# ✅ Defense ranking charts
# ✅ Dark horse visualizations
# ✅ Upset potential charts
#
# FIXED VERSION:
# ✅ Windows-safe paths
# ✅ VS Code-safe imports
# ✅ auto-output folders
# ✅ publication-ready charts
#
# ============================================================



# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys



# ============================================================
# PROJECT ROOT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



# ============================================================
# ALLOW IMPORTS FROM src/
# ============================================================

sys.path.append(
    os.path.join(BASE_DIR, 'src')
)



# ============================================================
# IMPORT ANALYTICS ENGINE
# ============================================================

from analytics_engine import (

    get_power_rankings,

    get_attack_rankings,

    get_defense_rankings,

    get_dark_horses,

    get_upset_potential,

    get_champion_probabilities
)



# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

VISUALS_DIR = os.path.join(

    BASE_DIR,

    'outputs',

    'visualizations'
)



os.makedirs(

    VISUALS_DIR,

    exist_ok=True
)



# ============================================================
# CHAMPION PROBABILITY CHART
# ============================================================

def plot_champion_probabilities():

    probs = get_champion_probabilities(

        n_simulations=1000
    )



    top_probs = probs.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_probs['team'],

        top_probs['probability']
    )



    plt.xlabel(
        'Winning Probability (%)'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'FIFA World Cup 2026 Champion Probabilities'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'champion_probabilities.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Champion probability chart saved"
    )



# ============================================================
# POWER RANKINGS CHART
# ============================================================

def plot_power_rankings():

    power = get_power_rankings()



    top_power = power.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_power['team'],

        top_power['adjusted_strength']
    )



    plt.xlabel(
        'Adjusted Strength'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'Top FIFA World Cup Power Rankings'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'power_rankings.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Power rankings chart saved"
    )



# ============================================================
# ATTACK RANKINGS CHART
# ============================================================

def plot_attack_rankings():

    attacks = get_attack_rankings()



    top_attacks = attacks.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_attacks['team'],

        top_attacks['avg_goals_scored']
    )



    plt.xlabel(
        'Average Goals Scored'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'Most Dangerous Attacks'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'attack_rankings.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Attack rankings chart saved"
    )



# ============================================================
# DEFENSE RANKINGS CHART
# ============================================================

def plot_defense_rankings():

    defenses = get_defense_rankings()



    top_defenses = defenses.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_defenses['team'],

        top_defenses['avg_goals_conceded']
    )



    plt.xlabel(
        'Average Goals Conceded'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'Best Defensive Teams'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'defense_rankings.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Defense rankings chart saved"
    )



# ============================================================
# DARK HORSE CHART
# ============================================================

def plot_dark_horses():

    dark_horses = get_dark_horses()



    top_dark_horses = dark_horses.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_dark_horses['team'],

        top_dark_horses['dark_horse_score']
    )



    plt.xlabel(
        'Dark Horse Score'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'Top Dark Horse Teams'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'dark_horses.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Dark horse chart saved"
    )



# ============================================================
# UPSET POTENTIAL CHART
# ============================================================

def plot_upset_potential():

    upsets = get_upset_potential()



    top_upsets = upsets.head(10)



    plt.figure(figsize=(12, 7))



    plt.barh(

        top_upsets['team'],

        top_upsets['upset_score']
    )



    plt.xlabel(
        'Upset Potential Score'
    )



    plt.ylabel(
        'Teams'
    )



    plt.title(
        'Highest Upset Potential Teams'
    )



    plt.gca().invert_yaxis()



    output_path = os.path.join(

        VISUALS_DIR,

        'upset_potential.png'
    )



    plt.savefig(

        output_path,

        bbox_inches='tight'
    )



    plt.close()



    print(
        "✅ Upset potential chart saved"
    )



# ============================================================
# GENERATE ALL VISUALIZATIONS
# ============================================================

def generate_all_visualizations():

    print("\n")

    print("================================================")
    print(" GENERATING FIFA WC 2026 VISUALIZATIONS ")
    print("================================================")



    plot_champion_probabilities()

    plot_power_rankings()

    plot_attack_rankings()

    plot_defense_rankings()

    plot_dark_horses()

    plot_upset_potential()



    print("\n")

    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")



# ============================================================
# TESTING SECTION
# ============================================================

if __name__ == "__main__":

    generate_all_visualizations()
