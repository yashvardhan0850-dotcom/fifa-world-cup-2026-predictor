
# ============================================================
# src/match_prediction.py
# ============================================================

# PURPOSE:
# Simplified & Realistic FIFA WC 2026 Match Engine
#
# PHILOSOPHY:
# ✅ Simpler > Overengineered
# ✅ Elo handles team strength
# ✅ xG handles scoring realism
# ✅ ML handles match probabilities
#
# FIXES:
# ✅ removed recursive inflation
# ✅ removed elite multipliers
# ✅ removed chaos factor
# ✅ removed adjusted_strength stacking
# ✅ fixed Switzerland domination
# ✅ cleaner calibration
# ✅ faster execution
#
# ============================================================



# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import os
import sys
import joblib

from scipy.stats import poisson



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

    build_team_profiles,

    load_data,

    create_elo_dict
)



# ============================================================
# LOAD TEAM PROFILES
# ============================================================

print("Loading team profiles...")

team_profiles_df = build_team_profiles()



# ============================================================
# TEAM STATS DICTIONARY
# ============================================================

team_stats_dict = (

    team_profiles_df

    .set_index('team')

    .to_dict(orient='index')
)



# ============================================================
# LOAD DATA
# ============================================================

results, elo = load_data()



# ============================================================
# ELO DICTIONARY
# ============================================================

elo_dict = create_elo_dict(
    elo
)



# ============================================================
# LOAD MODEL
# ============================================================

print("Loading trained model...")

model = joblib.load(

    os.path.join(

        BASE_DIR,

        'models',

        'xgb_wc_predictor.pkl'
    )
)



# ============================================================
# CREATE MATCH FEATURES
# ============================================================

def create_match_features(
    home_team,
    away_team
):

    # --------------------------------------------------------
    # ELO
    # --------------------------------------------------------

    home_elo = elo_dict.get(
        home_team,
        1500
    )



    away_elo = elo_dict.get(
        away_team,
        1500
    )



    # --------------------------------------------------------
    # TEAM STATS
    # --------------------------------------------------------

    home_stats = team_stats_dict.get(
        home_team,
        {}
    )



    away_stats = team_stats_dict.get(
        away_team,
        {}
    )



    # --------------------------------------------------------
    # ATTACK
    # --------------------------------------------------------

    home_attack = home_stats.get(
        'avg_goals_scored',
        1.5
    )



    away_attack = away_stats.get(
        'avg_goals_scored',
        1.5
    )



    # --------------------------------------------------------
    # DEFENSE
    # --------------------------------------------------------

    home_defense = home_stats.get(
        'avg_goals_conceded',
        1.0
    )



    away_defense = away_stats.get(
        'avg_goals_conceded',
        1.0
    )



    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    home_form = home_stats.get(
        'win_pct',
        0.5
    )



    away_form = away_stats.get(
        'win_pct',
        0.5
    )



    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    features = pd.DataFrame({

        'home_elo': [home_elo],

        'away_elo': [away_elo],

        'elo_diff': [
            home_elo - away_elo
        ],



        'home_rank': [50],

        'away_rank': [50],

        'rank_diff': [0],



        'neutral': [1],

        'is_competitive': [1],



        'home_form': [
            home_form * 3
        ],

        'away_form': [
            away_form * 3
        ],



        'form_diff': [
            home_form - away_form
        ],



        'home_attack_strength': [
            home_attack
        ],

        'away_attack_strength': [
            away_attack
        ],



        'home_defense_strength': [
            home_defense
        ],

        'away_defense_strength': [
            away_defense
        ],



        # ----------------------------------------------------
        # KEEP MODEL COMPATIBILITY
        # ----------------------------------------------------

        'elite_score_diff': [0],

        'adjusted_strength_diff': [0]
    })



    return features



# ============================================================
# MATCH PREDICTION
# ============================================================

# ============================================================
# MATCH PREDICTION USING xG + POISSON
# ============================================================

def predict_match(
    home_team,
    away_team
):

    # --------------------------------------------------------
    # EXPECTED GOALS
    # --------------------------------------------------------

    home_xg, away_xg = expected_goals(

        home_team,

        away_team
    )



    # --------------------------------------------------------
    # SCORE PROBABILITIES
    # --------------------------------------------------------

    max_goals = 6



    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0



    for home_goals in range(max_goals + 1):

        for away_goals in range(max_goals + 1):

            prob = (

                poisson.pmf(

                    home_goals,

                    home_xg
                )

                *

                poisson.pmf(

                    away_goals,

                    away_xg
                )
            )



            # ------------------------------------------------
            # RESULT TYPE
            # ------------------------------------------------

            if home_goals > away_goals:

                home_win_prob += prob



            elif home_goals < away_goals:

                away_win_prob += prob



            else:

                draw_prob += prob



    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    total = (

        home_win_prob

        +

        draw_prob

        +

        away_win_prob
    )



    home_win_prob /= total

    draw_prob /= total

    away_win_prob /= total



    return {

        'home_win_prob':
            round(home_win_prob, 3),

        'draw_prob':
            round(draw_prob, 3),

        'away_win_prob':
            round(away_win_prob, 3)
    }




# ============================================================
# EXPECTED GOALS
# ============================================================

def expected_goals(
    home_team,
    away_team
):

    # --------------------------------------------------------
    # TEAM STATS
    # --------------------------------------------------------

    home_stats = team_stats_dict.get(
        home_team,
        {}
    )



    away_stats = team_stats_dict.get(
        away_team,
        {}
    )



    # --------------------------------------------------------
    # ATTACK
    # --------------------------------------------------------

    home_attack = home_stats.get(
        'avg_goals_scored',
        1.5
    )



    away_attack = away_stats.get(
        'avg_goals_scored',
        1.5
    )



    # --------------------------------------------------------
    # DEFENSE
    # --------------------------------------------------------

    home_defense = home_stats.get(
        'avg_goals_conceded',
        1.0
    )



    away_defense = away_stats.get(
        'avg_goals_conceded',
        1.0
    )



    # --------------------------------------------------------
    # ELO
    # --------------------------------------------------------

    home_elo = elo_dict.get(
        home_team,
        1500
    )



    away_elo = elo_dict.get(
        away_team,
        1500
    )



    elo_diff = (

        home_elo

        -

        away_elo
    )



    # --------------------------------------------------------
    # BASE xG
    # --------------------------------------------------------

    home_xg = (

        home_attack

        *

        (1.4 / away_defense)
    )



    away_xg = (

        away_attack

        *

        (1.4 / home_defense)
    )



    # --------------------------------------------------------
    # ELO IMPACT
    # --------------------------------------------------------

    home_xg += elo_diff / 1000

    away_xg -= elo_diff / 1000



    # --------------------------------------------------------
    # SMALL HOME ADVANTAGE
    # --------------------------------------------------------

    home_xg += 0.15



    # --------------------------------------------------------
    # LIMITS
    # --------------------------------------------------------

    home_xg = max(
        0.2,
        min(home_xg, 3.2)
    )



    away_xg = max(
        0.2,
        min(away_xg, 3.2)
    )



    return home_xg, away_xg



# ============================================================
# SIMULATE SCORE
# ============================================================

def simulate_score(
    home_team,
    away_team
):

    home_xg, away_xg = expected_goals(

        home_team,

        away_team
    )



    home_goals = poisson.rvs(
        home_xg
    )



    away_goals = poisson.rvs(
        away_xg
    )



    return home_goals, away_goals



# ============================================================
# SIMULATE KNOCKOUT MATCH
# ============================================================

def simulate_knockout_match(
    home_team,
    away_team
):

    home_goals, away_goals = simulate_score(

        home_team,

        away_team
    )



    # --------------------------------------------------------
    # PENALTIES
    # --------------------------------------------------------

    if home_goals == away_goals:

        if np.random.rand() < 0.5:

            winner = home_team

        else:

            winner = away_team



    elif home_goals > away_goals:

        winner = home_team

    else:

        winner = away_team



    return winner



# ============================================================
# MATCH SUMMARY
# ============================================================

def match_summary(
    home_team,
    away_team
):

    probs = predict_match(

        home_team,

        away_team
    )

# --------------------------------------------------------
# EXPECTED GOALS
# --------------------------------------------------------

    home_xg, away_xg = expected_goals(

        home_team,

        away_team
    )



# --------------------------------------------------------
# MOST LIKELY SCORE
# --------------------------------------------------------

    home_goals = round(home_xg)

    away_goals = round(away_xg)




    summary = {

        'home_team':
            home_team,

        'away_team':
            away_team,

        'predicted_score':
            f'{home_goals}-{away_goals}',

        'home_win_probability':
            probs['home_win_prob'],

        'draw_probability':
            probs['draw_prob'],

        'away_win_probability':
            probs['away_win_prob']
    }



    return summary



# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("==============================================")
    print(" FIFA WC 2026 MATCH PREDICTION ENGINE ")
    print("==============================================")



    summary = match_summary(

        'France',

        'Argentina'
    )



    print("\nMatch Summary:\n")



    for key, value in summary.items():

        print(f"{key}: {value}")
