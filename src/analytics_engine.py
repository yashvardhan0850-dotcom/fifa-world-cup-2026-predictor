
# ============================================================
# src/analytics_engine.py
# ============================================================

# PURPOSE:
# FIFA World Cup Analytics & Intelligence Engine
#
# FEATURES:
# - Champion probabilities
# - Dark horse analysis
# - Attack rankings
# - Defense rankings
# - Upset potential
# - Tournament intelligence
#
# SAFE VERSION:
# ✅ modular imports
# ✅ Windows-safe paths
# ✅ VS Code-safe execution
# ✅ reusable architecture
#
# ============================================================



# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
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
# IMPORT MODULES
# ============================================================

from team_strength import (
    build_team_profiles
)



from simulation_engine import (
    monte_carlo_simulation
)



# ============================================================
# LOAD TEAM PROFILES
# ============================================================

print("Loading team profiles...")

team_profiles_df = build_team_profiles()



# ============================================================
# ELITE TEAMS
# ============================================================

elite_teams = [

    'Argentina',
    'France',
    'Brazil',
    'England',
    'Spain',
    'Germany',
    'Portugal',
    'Netherlands'
]



# ============================================================
# ATTACK RANKINGS
# ============================================================

def get_attack_rankings():

    attack_rankings = (

        team_profiles_df

        [

            [

                'team',

                'avg_goals_scored',

                'adjusted_strength'
            ]
        ]

        .sort_values(

            by='avg_goals_scored',

            ascending=False
        )

        .reset_index(drop=True)
    )



    return attack_rankings



# ============================================================
# DEFENSE RANKINGS
# ============================================================

def get_defense_rankings():

    defense_rankings = (

        team_profiles_df

        [

            [

                'team',

                'avg_goals_conceded',

                'adjusted_strength'
            ]
        ]

        .sort_values(

            by='avg_goals_conceded',

            ascending=True
        )

        .reset_index(drop=True)
    )



    return defense_rankings



# ============================================================
# OVERALL POWER RANKINGS
# ============================================================

def get_power_rankings():

    power_rankings = (

        team_profiles_df

        [

            [

                'team',

                'adjusted_strength',

                'win_pct',

                'elite_wins'
            ]
        ]

        .sort_values(

            by='adjusted_strength',

            ascending=False
        )

        .reset_index(drop=True)
    )



    return power_rankings



# ============================================================
# DARK HORSE ANALYSIS
# ============================================================

def get_dark_horses():

    dark_horses = team_profiles_df.copy()



    # --------------------------------------------------------
    # DARK HORSE SCORE
    # --------------------------------------------------------

    dark_horses['dark_horse_score'] = (

        dark_horses['elite_wins'] * 3

        +

        dark_horses['world_cup_upsets'] * 5

        +

        dark_horses['adjusted_strength'] * 0.2

        +

        dark_horses['win_pct'] * 25
    )



    # --------------------------------------------------------
    # REMOVE ELITE TEAMS
    # --------------------------------------------------------

    dark_horses = dark_horses[

        ~dark_horses['team'].isin(
            elite_teams
        )
    ]



    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    dark_horses = (

        dark_horses

        .sort_values(

            by='dark_horse_score',

            ascending=False
        )
    )



    return dark_horses[

        [

            'team',

            'dark_horse_score',

            'elite_wins',

            'world_cup_upsets',

            'adjusted_strength'
        ]
    ]



# ============================================================
# UPSET POTENTIAL
# ============================================================

def get_upset_potential():

    upset_df = team_profiles_df.copy()



    # --------------------------------------------------------
    # UPSET SCORE
    # --------------------------------------------------------

    upset_df['upset_score'] = (

        upset_df['elite_wins'] * 4

        +

        upset_df['world_cup_upsets'] * 6

        +

        upset_df['avg_goals_scored'] * 5

        -

        upset_df['avg_goals_conceded'] * 2
    )



    upset_df = (

        upset_df

        .sort_values(

            by='upset_score',

            ascending=False
        )
    )



    return upset_df[

        [

            'team',

            'upset_score',

            'elite_wins',

            'world_cup_upsets'
        ]
    ]



# ============================================================
# CHAMPION PROBABILITIES
# ============================================================

def get_champion_probabilities(

    n_simulations=1000
):

    champion_probs = monte_carlo_simulation(

        n_simulations=n_simulations
    )



    champion_probs = (

        champion_probs

        .sort_values(

            by='probability',

            ascending=False
        )

        .reset_index(drop=True)
    )



    return champion_probs



# ============================================================
# COMPLETE ANALYTICS REPORT
# ============================================================

def generate_analytics_report():

    print("\n")

    print("================================================")
    print(" FIFA WORLD CUP ANALYTICS REPORT ")
    print("================================================")



    # --------------------------------------------------------
    # POWER RANKINGS
    # --------------------------------------------------------

    print("\n")

    print("TOP POWER RANKINGS:\n")



    power = get_power_rankings()



    print(

        power.head(10)
    )



    # --------------------------------------------------------
    # ATTACKS
    # --------------------------------------------------------

    print("\n")

    print("MOST DANGEROUS ATTACKS:\n")



    attacks = get_attack_rankings()



    print(

        attacks.head(10)
    )



    # --------------------------------------------------------
    # DEFENSES
    # --------------------------------------------------------

    print("\n")

    print("BEST DEFENSES:\n")



    defenses = get_defense_rankings()



    print(

        defenses.head(10)
    )



    # --------------------------------------------------------
    # DARK HORSES
    # --------------------------------------------------------

    print("\n")

    print("DARK HORSE TEAMS:\n")



    dark_horses = get_dark_horses()



    print(

        dark_horses.head(10)
    )



    # --------------------------------------------------------
    # UPSET POTENTIAL
    # --------------------------------------------------------

    print("\n")

    print("UPSET POTENTIAL:\n")



    upsets = get_upset_potential()



    print(

        upsets.head(10)
    )



    # --------------------------------------------------------
    # CHAMPION PROBABILITIES
    # --------------------------------------------------------

    print("\n")

    print("WORLD CUP WIN PROBABILITIES:\n")



    champion_probs = get_champion_probabilities(

        n_simulations=1000
    )



    print(

        champion_probs.head(10)
    )



    return {

        'power_rankings': power,

        'attack_rankings': attacks,

        'defense_rankings': defenses,

        'dark_horses': dark_horses,

        'upset_potential': upsets,

        'champion_probabilities': champion_probs
    }



# ============================================================
# SAVE ANALYTICS
# ============================================================

def save_analytics_outputs():

    outputs = generate_analytics_report()



    output_dir = os.path.join(

        BASE_DIR,

        'outputs'
    )



    os.makedirs(

        output_dir,

        exist_ok=True
    )



    # --------------------------------------------------------
    # SAVE CSV FILES
    # --------------------------------------------------------

    for name, df in outputs.items():

        file_path = os.path.join(

            output_dir,

            f'{name}.csv'
        )



        df.to_csv(

            file_path,

            index=False
        )



    print("\n")

    print("✅ Analytics outputs saved successfully!")



# ============================================================
# TESTING SECTION
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("================================================")
    print(" FIFA WORLD CUP ANALYTICS ENGINE ")
    print("================================================")



    generate_analytics_report()



    save_analytics_outputs()