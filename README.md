# ⚽ FIFA World Cup 2026 Analytics Platform

An end-to-end football analytics and prediction platform built using Machine Learning, Elo Ratings, Poisson Goal Modeling, Monte Carlo Simulation, and Streamlit.

This project forecasts FIFA World Cup 2026 matches, tournament probabilities, team strengths, dark horses, and upset potential through a fully interactive web application.

---

# 🚀 Features

## ⚽ Match Prediction Engine

* Predicts match outcomes
* Calculates:

  * Win probability
  * Draw probability
  * Expected scoreline
* Uses:

  * Elo Ratings
  * Poisson Goal Modeling
  * Team attack/defense metrics

---

## 🏆 Tournament Simulation

* Monte Carlo World Cup forecasting
* Champion probability estimation
* Weighted tournament simulations
* Competitive probability calibration

---

## 📊 Analytics Dashboard

Provides:

* Power Rankings
* Most Dangerous Attacks
* Best Defenses
* Dark Horse Teams
* Upset Potential Rankings

---

## 🌍 FIFA World Cup 2026 Groups

* Complete 48-team World Cup structure
* Group A → Group L
* Realistic tournament presentation

---

## 📈 Visualizations

* Champion probability charts
* Team strength charts
* Attack/Defense comparison graphs
* Analytics visualizations

---

# 🧠 Technologies Used

| Technology             | Purpose                     |
| ---------------------- | --------------------------- |
| Python                 | Core development            |
| Pandas                 | Data processing             |
| NumPy                  | Numerical computations      |
| Scikit-learn           | ML utilities                |
| XGBoost                | Match prediction model      |
| Matplotlib             | Data visualization          |
| Streamlit              | Interactive web application |
| Elo Ratings            | Team strength modeling      |
| Poisson Distribution   | Goal simulation             |
| Monte Carlo Simulation | Tournament forecasting      |

---

# 🏗️ Project Architecture

```bash
fifa-wc-2026-predictor/

│
├── app/
│   └── streamlit_app.py
│
├── src/
│   ├── analytics_engine.py
│   ├── data_filter.py
│   ├── match_prediction.py
│   ├── qualified_teams.py
│   ├── simulation_engine.py
│   ├── team_strength.py
│   ├── visualization.py
│   └── world_cup_groups.py
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── outputs/
│   └── visualizations/
│
├── models/
│   └── xgb_wc_predictor.pkl
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
https://github.com/yashvardhan0850-dotcom/fifa-world-cup-2026-predictor
```

---

## 2️⃣ Navigate to Project

```bash
cd fifa-wc-2026-predictor
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Start Streamlit App

```bash
streamlit run app/streamlit_app.py
```

---

# 📸 Application Modules

## ⚽ Match Simulator

Predict:

* Match winner
* Draw probability
* Expected score

---

## 🏆 Tournament Simulator

Run:

* Monte Carlo simulations
* World Cup winner forecasting

---

## 🌍 World Cup Groups

View:

* Full FIFA World Cup 2026 groups

---

## 📊 Analytics Dashboard

Analyze:

* Team strengths
* Dark horses
* Upset potential
* Attack & defense rankings

---

# 📊 Modeling Approach

## Elo Ratings

Used to estimate long-term team strength.

---

## Poisson Goal Modeling

Used to simulate realistic football scores based on expected goals (xG).

---

## Monte Carlo Simulation

Used to forecast tournament outcomes over hundreds of simulations.

---

## Machine Learning

XGBoost model trained on historical international football matches.

---

# 🎯 Key Challenges Solved

* Removed non-World Cup teams from analysis
* Fixed draw probability inflation
* Reduced unrealistic tournament randomness
* Cleaned historical football data
* Calibrated elite vs dark-horse balance
* Optimized Streamlit performance

---

# 📌 Future Improvements

* Real Round-of-32 simulation engine
* Live FIFA ranking integration
* API-based match updates
* Advanced xG models
* Player-level analytics
* Cloud deployment

---

# 👨‍💻 Author

Developed by Yashvardhan Vase

Passionate about:

* Data Science
* Sports Analytics
* Machine Learning
* Football Intelligence Systems

---

# ⭐ If You Like This Project

Consider starring the repository and sharing feedback!
