
# ============================================================
# src/data_filter.py
# ============================================================

import pandas as pd
import os

from qualified_teams import qualified_teams



# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



# ============================================================
# LOAD RAW RESULTS
# ============================================================

results_path = os.path.join(

    BASE_DIR,

    'data',

    'raw',

    'results.csv'
)



results = pd.read_csv(
    results_path
)



# ============================================================
# KEEP ONLY WC TEAMS
# ============================================================

results = results[

    results['home_team'].isin(
        qualified_teams
    )

    &

    results['away_team'].isin(
        qualified_teams
    )
]



# ============================================================
# REMOVE OLD FOOTBALL ERAS
# ============================================================

results['date'] = pd.to_datetime(
    results['date']
)



results = results[

    results['date'].dt.year >= 2018
]



# ============================================================
# REMOVE FRIENDLIES
# ============================================================

results = results[

    results['tournament'] != 'Friendly'
]



# ============================================================
# SAVE CLEAN DATASET
# ============================================================

output_path = os.path.join(

    BASE_DIR,

    'data',

    'cleaned',

    'wc_2026_filtered_results.csv'
)



os.makedirs(

    os.path.dirname(output_path),

    exist_ok=True
)



results.to_csv(

    output_path,

    index=False
)



print("\n✅ CLEAN WC DATASET CREATED")
print(f"Matches Remaining: {len(results)}")
