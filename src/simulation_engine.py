
# ============================================================
# src/simulation_engine.py
# ============================================================

from world_cup_groups import groups
import pandas as pd
import numpy as np
import os
import sys



# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



# ============================================================
# ALLOW IMPORTS
# ============================================================

sys.path.append(
    os.path.join(BASE_DIR, 'src')
)



# ============================================================
# IMPORT MODULES
# ============================================================

from team_strength import (
    build_team_profiles,
    load_data,
    create_elo_dict
)



from qualified_teams import (
    qualified_teams
)



# ============================================================
# LOAD DATA
# ============================================================

team_profiles_df = build_team_profiles()



results, elo = load_data()



elo_dict = create_elo_dict(
    elo
)



# ============================================================
# FILTER ONLY WC TEAMS
# ============================================================

team_profiles_df = team_profiles_df[

    team_profiles_df['team'].isin(
        qualified_teams
    )
]



# ============================================================
# CALCULATE TEAM POWER
# ============================================================

def calculate_team_power(team):

    # --------------------------------------------------------
    # TEAM PROFILE
    # --------------------------------------------------------

    row = team_profiles_df[

        team_profiles_df['team'] == team
    ]



    if len(row) == 0:

        return 50



    row = row.iloc[0]



    # --------------------------------------------------------
    # COMPONENTS
    # --------------------------------------------------------

    elo = elo_dict.get(
        team,
        1500
    )



    attack = row['avg_goals_scored']

    defense = row['avg_goals_conceded']

    win_pct = row['win_pct']



    # --------------------------------------------------------
    # POWER FORMULA
    # --------------------------------------------------------

    power = (

        (elo / 35)

        +

        (attack * 12)

        -

        (defense * 8)

        +

        (win_pct * 25)
    )



    return max(power, 1)



# ============================================================
# BUILD POWER TABLE
# ============================================================

power_data = []



for team in qualified_teams:

    power_data.append({

        'team': team,

        'power': calculate_team_power(team)
    })



power_df = pd.DataFrame(
    power_data
)

# ============================================================
# SOFTMAX POWER CALIBRATION
# ============================================================

temperature = 20

# ============================================================
# ELITE BIAS CALIBRATION
# ============================================================

elite_multiplier = 1.35



# ------------------------------------------------------------
# BOOST STRONG TEAMS
# ------------------------------------------------------------

mean_power = power_df['power'].mean()



power_df['adjusted_power'] = np.where(

    power_df['power'] > mean_power,

    power_df['power'] * elite_multiplier,

    power_df['power']
)



# ------------------------------------------------------------
# SOFTMAX
# ------------------------------------------------------------

exp_power = np.exp(

    power_df['adjusted_power'] / temperature
)



power_df['power'] = (

    exp_power

    /

    exp_power.sum()
)




power_df['power'] = (

    exp_power

    /

    exp_power.sum()
)




# ============================================================
# RUN SINGLE WORLD CUP
# ============================================================

def run_world_cup():

    # --------------------------------------------------------
    # RANDOM CHAMPION USING WEIGHTED POWERS
    # --------------------------------------------------------

    champion = np.random.choice(

        power_df['team'],

        p=power_df['power']
    )



    return champion



# ============================================================
# MONTE CARLO SIMULATION
# ============================================================

def monte_carlo_simulation(
    n_simulations=1000
):

    champions = []



    for _ in range(n_simulations):

        champion = run_world_cup()

        champions.append(champion)



    # --------------------------------------------------------
    # COUNT TITLES
    # --------------------------------------------------------

    results_df = pd.Series(
        champions
    ).value_counts().reset_index()



    results_df.columns = [

        'team',

        'titles'
    ]



    # --------------------------------------------------------
    # PROBABILITY
    # --------------------------------------------------------

    results_df['probability'] = (

        results_df['titles']

        /

        n_simulations

        *

        100
    )



    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    results_df = results_df.sort_values(

        by='probability',

        ascending=False
    )



    # --------------------------------------------------------
    # CLEAN INDEX
    # --------------------------------------------------------

    results_df = results_df.reset_index(
        drop=True
    )



    results_df.index += 1



    return results_df[

        [

            'team',

            'probability'
        ]
    ]



# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("==============================================")
    print(" FIFA WC 2026 TOURNAMENT SIMULATOR ")
    print("==============================================")



    probs = monte_carlo_simulation(
        1000
    )



    print("\nChampion Probabilities:\n")



    print(probs.head(15))
