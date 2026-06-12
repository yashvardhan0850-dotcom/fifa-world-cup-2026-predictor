
# ============================================================
# src/team_strength.py
# ============================================================

# PURPOSE:
# Build advanced FIFA World Cup team strength profiles
#
# FEATURES:
# ✅ opponent-adjusted strength
# ✅ elite wins
# ✅ World Cup upset tracking
# ✅ confederation difficulty coefficients
# ✅ realistic international balancing
# ✅ small-team inflation reduction
# ✅ modular architecture
# ✅ Windows-safe paths
#
# ============================================================



# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import os



# ============================================================
# PROJECT ROOT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



# ============================================================
# ELITE TEAMS
# ============================================================

elite_teams = [

    'Argentina',
    'France',
    'Brazil',
    'Spain',
    'England',
    'Germany',
    'Portugal',
    'Netherlands',
    'Italy',
    'Croatia'
]



# ============================================================
# CONFEDERATION STRENGTH COEFFICIENTS
# ============================================================

confederation_strength = {

    # --------------------------------------------------------
    # UEFA
    # --------------------------------------------------------

    'France': 1.00,
    'England': 1.00,
    'Spain': 1.00,
    'Germany': 1.00,
    'Portugal': 1.00,
    'Netherlands': 1.00,
    'Switzerland': 1.00,
    'Belgium': 1.00,
    'Croatia': 1.00,
    'Italy': 1.00,
    'Denmark': 1.00,
    'Serbia': 1.00,
    'Poland': 1.00,



    # --------------------------------------------------------
    # CONMEBOL
    # --------------------------------------------------------

    'Argentina': 0.98,
    'Brazil': 0.98,
    'Uruguay': 0.98,
    'Colombia': 0.98,
    'Chile': 0.98,
    'Ecuador': 0.98,



    # --------------------------------------------------------
    # CAF
    # --------------------------------------------------------

    'Morocco': 0.90,
    'Senegal': 0.90,
    'Nigeria': 0.90,
    'Ghana': 0.90,
    'Egypt': 0.90,
    'Cameroon': 0.90,
    'Algeria': 0.90,



    # --------------------------------------------------------
    # AFC
    # --------------------------------------------------------

    'Japan': 0.85,
    'South Korea': 0.85,
    'Iran': 0.85,
    'Saudi Arabia': 0.85,
    'Australia': 0.85,
    'Qatar': 0.85,



    # --------------------------------------------------------
    # CONCACAF
    # --------------------------------------------------------

    'USA': 0.83,
    'Mexico': 0.83,
    'Canada': 0.83,
    'Costa Rica': 0.83,
    'Panama': 0.83
}



# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    # --------------------------------------------------------
    # FILE PATHS
    # --------------------------------------------------------

    results_path = os.path.join(

        BASE_DIR,

        'data',

        'cleaned',

        'wc_2026_filtered_results.csv'
    )



    elo_path = os.path.join(

        BASE_DIR,

        'data',

        'raw',

        'elo_ratings.csv'
    )



    # --------------------------------------------------------
    # LOAD CSV FILES
    # --------------------------------------------------------

    results = pd.read_csv(
        results_path
    )



    elo = pd.read_csv(
        elo_path
    )



    # --------------------------------------------------------
    # DATE CONVERSION
    # --------------------------------------------------------

    results['date'] = pd.to_datetime(
        results['date']
    )



    if 'snapshot_date' in elo.columns:

        elo['snapshot_date'] = pd.to_datetime(
            elo['snapshot_date']
        )



    return results, elo



# ============================================================
# CREATE ELO DICTIONARY
# ============================================================

def create_elo_dict(elo):

    # --------------------------------------------------------
    # DETECT TEAM COLUMN
    # --------------------------------------------------------

    if 'country' in elo.columns:

        team_col = 'country'

    elif 'team' in elo.columns:

        team_col = 'team'

    else:

        raise ValueError(
            "No valid team column found in elo dataset"
        )



    # --------------------------------------------------------
    # DETECT RATING COLUMN
    # --------------------------------------------------------

    if 'elo_rating' in elo.columns:

        rating_col = 'elo_rating'

    elif 'rating' in elo.columns:

        rating_col = 'rating'

    elif 'elo' in elo.columns:

        rating_col = 'elo'

    else:

        raise ValueError(
            "No valid elo rating column found"
        )



    # --------------------------------------------------------
    # CREATE DICTIONARY
    # --------------------------------------------------------

    elo_dict = dict(

        zip(

            elo[team_col],

            elo[rating_col]
        )
    )



    return elo_dict



# ============================================================
# CALCULATE TEAM STATS
# ============================================================

def calculate_team_stats(

    team,

    results
):

    # --------------------------------------------------------
    # HOME MATCHES
    # --------------------------------------------------------

    home_matches = results[

        results['home_team'] == team
    ]



    # --------------------------------------------------------
    # AWAY MATCHES
    # --------------------------------------------------------

    away_matches = results[

        results['away_team'] == team
    ]



    # --------------------------------------------------------
    # TOTAL MATCHES
    # --------------------------------------------------------

    total_matches = (

        len(home_matches)

        +

        len(away_matches)
    )



    if total_matches == 0:

        return None



    # --------------------------------------------------------
    # GOALS SCORED
    # --------------------------------------------------------

    home_goals_scored = (

        home_matches['home_score']
        .sum()
    )



    away_goals_scored = (

        away_matches['away_score']
        .sum()
    )



    goals_scored = (

        home_goals_scored

        +

        away_goals_scored
    )



    # --------------------------------------------------------
    # GOALS CONCEDED
    # --------------------------------------------------------

    home_goals_conceded = (

        home_matches['away_score']
        .sum()
    )



    away_goals_conceded = (

        away_matches['home_score']
        .sum()
    )



    goals_conceded = (

        home_goals_conceded

        +

        away_goals_conceded
    )



    # --------------------------------------------------------
    # WINS
    # --------------------------------------------------------

    home_wins = len(

        home_matches[

            home_matches['home_score']

            >

            home_matches['away_score']
        ]
    )



    away_wins = len(

        away_matches[

            away_matches['away_score']

            >

            away_matches['home_score']
        ]
    )



    wins = home_wins + away_wins



    # --------------------------------------------------------
    # WIN %
    # --------------------------------------------------------

    win_pct = wins / total_matches



    # --------------------------------------------------------
    # AVERAGES
    # --------------------------------------------------------

    avg_goals_scored = (

        goals_scored

        /

        total_matches
    )



    avg_goals_conceded = (

        goals_conceded

        /

        total_matches
    )



    # --------------------------------------------------------
    # ELITE WINS
    # --------------------------------------------------------

    elite_wins = 0



    for elite_team in elite_teams:

        # Home wins
        elite_home_wins = len(

            home_matches[

                (home_matches['away_team'] == elite_team)

                &

                (
                    home_matches['home_score']

                    >

                    home_matches['away_score']
                )
            ]
        )



        # Away wins
        elite_away_wins = len(

            away_matches[

                (away_matches['home_team'] == elite_team)

                &

                (
                    away_matches['away_score']

                    >

                    away_matches['home_score']
                )
            ]
        )



        elite_wins += (

            elite_home_wins

            +

            elite_away_wins
        )



    # --------------------------------------------------------
    # WORLD CUP UPSETS
    # --------------------------------------------------------

    world_cup_upsets = 0



    world_cup_matches = results[

        results['tournament']

        .str.contains(
            'World Cup',
            case=False,
            na=False
        )
    ]



    upset_home = len(

        world_cup_matches[

            (world_cup_matches['home_team'] == team)

            &

            (
                world_cup_matches['away_team']

                .isin(elite_teams)
            )

            &

            (
                world_cup_matches['home_score']

                >

                world_cup_matches['away_score']
            )
        ]
    )



    upset_away = len(

        world_cup_matches[

            (world_cup_matches['away_team'] == team)

            &

            (
                world_cup_matches['home_team']

                .isin(elite_teams)
            )

            &

            (
                world_cup_matches['away_score']

                >

                world_cup_matches['home_score']
            )
        ]
    )



    world_cup_upsets = (

        upset_home

        +

        upset_away
    )



    # --------------------------------------------------------
    # BASE ADJUSTED STRENGTH
    # --------------------------------------------------------

    adjusted_strength = (

        (win_pct * 40)

        +

        (avg_goals_scored * 25)

        -

        (avg_goals_conceded * 15)

        +

        (elite_wins * 6)

        +

        (world_cup_upsets * 8)
    )



    # --------------------------------------------------------
    # SMALL SAMPLE PENALTY
    # --------------------------------------------------------

    if total_matches < 20:

        adjusted_strength *= 0.70

    elif total_matches < 50:

        adjusted_strength *= 0.85



    # --------------------------------------------------------
    # CONFEDERATION ADJUSTMENT
    # --------------------------------------------------------

    regional_factor = confederation_strength.get(

        team,

        0.80
    )



    adjusted_strength *= regional_factor



    # --------------------------------------------------------
    # SAFETY FLOOR
    # --------------------------------------------------------

    adjusted_strength = max(
        adjusted_strength,
        1
    )



    return {

        'team': team,

        'matches_played': total_matches,

        'wins': wins,

        'win_pct': round(
            win_pct,
            3
        ),

        'avg_goals_scored': round(
            avg_goals_scored,
            3
        ),

        'avg_goals_conceded': round(
            avg_goals_conceded,
            3
        ),

        'elite_wins': elite_wins,

        'world_cup_upsets': world_cup_upsets,

        'adjusted_strength': round(
            adjusted_strength,
            2
        )
    }



# ============================================================
# BUILD TEAM PROFILES
# ============================================================

def build_team_profiles():

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    results, elo = load_data()



    # --------------------------------------------------------
    # UNIQUE TEAMS
    # --------------------------------------------------------

    teams = sorted(

        set(results['home_team'])

        |

        set(results['away_team'])
    )



    # --------------------------------------------------------
    # TEAM PROFILES
    # --------------------------------------------------------

    profiles = []



    for team in teams:

        profile = calculate_team_stats(

            team,

            results
        )



        if profile is not None:

            profiles.append(profile)



    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    team_profiles_df = pd.DataFrame(
        profiles
    )



    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    team_profiles_df = (

        team_profiles_df

        .sort_values(

            by='adjusted_strength',

            ascending=False
        )

        .reset_index(drop=True)
    )



    # --------------------------------------------------------
    # SAVE OUTPUT
    # --------------------------------------------------------

    output_dir = os.path.join(

        BASE_DIR,

        'data',

        'cleaned'
    )



    os.makedirs(

        output_dir,

        exist_ok=True
    )



    output_path = os.path.join(

        output_dir,

        'team_strength_profiles.csv'
    )



    team_profiles_df.to_csv(

        output_path,

        index=False
    )



    print("\n")

    print("✅ Team strength profiles created successfully!")



    return team_profiles_df



# ============================================================
# TESTING SECTION
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("================================================")
    print(" FIFA WC 2026 TEAM STRENGTH ENGINE ")
    print("================================================")



    team_profiles = build_team_profiles()



    print("\nTOP 20 TEAMS:\n")



    print(

        team_profiles.head(20)
    )
