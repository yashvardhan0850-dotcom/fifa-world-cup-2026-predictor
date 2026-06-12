
# ============================================================
# app/streamlit_app.py
# ============================================================

# FIFA WORLD CUP 2026 ANALYTICS PLATFORM
#
# FEATURES:
# ✅ Match Simulator
# ✅ Tournament Simulator
# ✅ World Cup Groups
# ✅ Analytics Dashboard
# ✅ Faster Streamlit
# ✅ Fixed dataframe indexes
# ✅ Fixed imports
# ✅ Clean UI
#
# ============================================================



# ============================================================
# PROJECT ROOT FIX
# ============================================================

import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)



# ============================================================
# IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



# ============================================================
# IMPORT MODULES
# ============================================================

from src.match_prediction import (
    match_summary
)

from src.simulation_engine import (
    monte_carlo_simulation,
    run_world_cup
)

from src.analytics_engine import (

    get_power_rankings,

    get_dark_horses,

    get_attack_rankings,

    get_defense_rankings,

    get_upset_potential
)

from src.team_strength import (
    build_team_profiles
)

from src.world_cup_groups import (
    groups
)



# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(

    page_title="FIFA WC 2026 Analytics",

    page_icon="⚽",

    layout="wide"
)



# ============================================================
# CACHE LOADERS
# ============================================================

@st.cache_data
def load_team_profiles():
    return build_team_profiles()



@st.cache_data
def load_power_rankings_cached():
    return get_power_rankings()



@st.cache_data
def load_attack_rankings_cached():
    return get_attack_rankings()



@st.cache_data
def load_defense_rankings_cached():
    return get_defense_rankings()



@st.cache_data
def load_dark_horses_cached():
    return get_dark_horses()



@st.cache_data
def load_upset_potential_cached():
    return get_upset_potential()



# ============================================================
# LOAD TEAMS
# ============================================================

team_profiles = load_team_profiles()

teams = sorted(
    team_profiles['team'].unique()
)



# ============================================================
# TITLE
# ============================================================

st.title(
    "⚽ FIFA World Cup 2026 Analytics Platform"
)



st.markdown(
    """
Advanced football prediction system using:

- Elo Ratings
- Poisson Goal Modeling
- Monte Carlo Simulation
- Machine Learning
- xG-based Match Forecasting
"""
)



# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ Navigation"
)



page = st.sidebar.radio(

    "Select Module",

    [

        "⚽ Match Simulator",

        "🏆 Tournament Simulator",

        "🌍 World Cup Groups",

        "📊 Analytics Dashboard"
    ]
)



# ============================================================
# MATCH SIMULATOR
# ============================================================

if page == "⚽ Match Simulator":



    st.header(
        "⚽ Match Prediction Simulator"
    )



    # --------------------------------------------------------
    # TEAM SELECTORS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)



    with col1:

        home_team = st.selectbox(

            "Home Team",

            teams,

            index=teams.index('France')

            if 'France' in teams else 0
        )



    with col2:

        away_team = st.selectbox(

            "Away Team",

            teams,

            index=teams.index('Argentina')

            if 'Argentina' in teams else 1
        )



    # --------------------------------------------------------
    # PREDICT BUTTON
    # --------------------------------------------------------

    if st.button(
        "🚀 Predict Match"
    ):



        summary = match_summary(

            home_team,

            away_team
        )



        st.subheader(
            "📊 Match Summary"
        )



        st.write(

            f"### {summary['home_team']} vs {summary['away_team']}"
        )



        st.write(

            f"### Predicted Score: {summary['predicted_score']}"
        )



        # ----------------------------------------------------
        # PROBABILITY TABLE
        # ----------------------------------------------------

        probs_df = pd.DataFrame({

            'Outcome': [

                f"{home_team} Win",

                'Draw',

                f"{away_team} Win"
            ],

            'Probability (%)': [

                round(summary['home_win_probability'] * 100, 1),

                round(summary['draw_probability'] * 100, 1),

                round(summary['away_win_probability'] * 100, 1)
            ]
        })



        probs_df = probs_df.reset_index(
            drop=True
        )



        probs_df.index += 1



        st.dataframe(
            probs_df
        )



        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )



        ax.bar(

            probs_df['Outcome'],

            probs_df['Probability (%)']
        )



        ax.set_ylabel(
            'Probability (%)'
        )



        ax.set_title(
            'Match Outcome Probabilities'
        )



        st.pyplot(fig)



# ============================================================
# TOURNAMENT SIMULATOR
# ============================================================

elif page == "🏆 Tournament Simulator":



    st.header(
        "🏆 FIFA World Cup Tournament Simulator"
    )



    n_simulations = st.slider(

        "Number of Simulations",

        min_value=100,

        max_value=1000,

        value=300,

        step=100
    )



    if st.button(
        "🚀 Run Tournament Simulation"
    ):



        st.info(
            "Running simulations..."
        )



        champion_probs = monte_carlo_simulation(

            n_simulations=n_simulations
        )



        champion_probs = champion_probs.reset_index(
            drop=True
        )



        champion_probs.index += 1



        st.subheader(
            "🏆 Champion Probabilities"
        )



        st.dataframe(
            champion_probs
        )



        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        top_probs = champion_probs.head(10)



        fig, ax = plt.subplots(
            figsize=(10, 6)
        )



        ax.barh(

            top_probs['team'],

            top_probs['probability']
        )



        ax.set_xlabel(
            'Winning Probability (%)'
        )



        ax.set_title(
            'World Cup Champion Probabilities'
        )



        ax.invert_yaxis()



        st.pyplot(fig)



        # ----------------------------------------------------
        # RANDOM CHAMPION
        # ----------------------------------------------------

        champion = run_world_cup()



        st.success(
            f"🏆 Simulated Champion: {champion}"
        )



# ============================================================
# WORLD CUP GROUPS
# ============================================================

elif page == "🌍 World Cup Groups":



    st.header(
        "🌍 FIFA World Cup 2026 Groups"
    )



    for group_name, teams_in_group in groups.items():



        st.subheader(group_name)



        group_df = pd.DataFrame({

            'Teams': teams_in_group
        })



        group_df = group_df.reset_index(
            drop=True
        )



        group_df.index += 1



        st.dataframe(
            group_df
        )



# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

elif page == "📊 Analytics Dashboard":



    st.header(
        "📊 Football Analytics Dashboard"
    )



    # --------------------------------------------------------
    # POWER RANKINGS
    # --------------------------------------------------------

    st.subheader(
        "🔥 Power Rankings"
    )



    power = load_power_rankings_cached()



    power = power.reset_index(
        drop=True
    )



    power.index += 1



    st.dataframe(
        power.head(15)
    )



    # --------------------------------------------------------
    # ATTACK RANKINGS
    # --------------------------------------------------------

    st.subheader(
        "⚔️ Most Dangerous Attacks"
    )



    attacks = load_attack_rankings_cached()



    attacks = attacks.reset_index(
        drop=True
    )



    attacks.index += 1



    st.dataframe(
        attacks.head(10)
    )



    # --------------------------------------------------------
    # DEFENSE RANKINGS
    # --------------------------------------------------------

    st.subheader(
        "🛡️ Best Defenses"
    )



    defenses = load_defense_rankings_cached()



    defenses = defenses.reset_index(
        drop=True
    )



    defenses.index += 1



    st.dataframe(
        defenses.head(10)
    )



    # --------------------------------------------------------
    # DARK HORSES
    # --------------------------------------------------------

    st.subheader(
        "🐎 Dark Horse Teams"
    )



    dark_horses = load_dark_horses_cached()



    dark_horses = dark_horses.reset_index(
        drop=True
    )



    dark_horses.index += 1



    st.dataframe(
        dark_horses.head(10)
    )



    # --------------------------------------------------------
    # UPSET POTENTIAL
    # --------------------------------------------------------

    st.subheader(
        "💥 Upset Potential"
    )



    upsets = load_upset_potential_cached()



    upsets = upsets.reset_index(
        drop=True
    )



    upsets.index += 1



    st.dataframe(
        upsets.head(10)
    )



    # --------------------------------------------------------
    # POWER CHART
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )



    top_power = power.head(10)



    ax.barh(

        top_power['team'],

        top_power['adjusted_strength']
    )



    ax.set_xlabel(
        'Adjusted Strength'
    )



    ax.set_title(
        'Top Power Rankings'
    )



    ax.invert_yaxis()



    st.pyplot(fig)



# ============================================================
# FOOTER
# ============================================================

st.markdown("---")



st.markdown(
    """
### ⚽ FIFA WC 2026 Analytics Platform

Built with:
- Python
- Streamlit
- Pandas
- Poisson Modeling
- Elo Ratings
- Monte Carlo Simulation
- Machine Learning
"""
)
