from xgboost import XGBRegressor, DMatrix, XGBClassifier
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import score_model as score
from collections import defaultdict


def predict_game(model, game_features):
    """Predict a single game score"""
    pred = model.predict(game_features)
    return pred[0, 0], pred[0, 1]  # away_score, home_score

def simulate_series(model, game_features, series, n_simulations=10000, home_advantage=False):
    sim = 0
    """
    Simulate a best-of-7 NBA playoff series using Monte Carlo.
    
    game_features: DataFrame row with features for this matchup
    n_simulations: number of times to simulate the full series
    """
    away_wins_total = 0
    home_wins_total = 0
    series_lengths = []
    series_results = defaultdict(int)  # e.g. '4-2': 1500

    for _ in range(n_simulations):
        away_wins = 0
        home_wins = 0
        game_num = 0

        while away_wins < series and home_wins < series:
            game_num += 1

            # Predict base scores
            away_score, home_score = predict_game(model, game_features)

            # Add noise to simulate game-to-game variance
            # Goal is to change scale to be based upon some sort of team stat instead of flat rate
            away_score += np.random.normal(0, scale=7.5) 
            home_score += np.random.normal(0, scale=7.5)

            # Optional: small home court advantage
            if home_advantage:
                home_score += 2.5

            if away_score > home_score:
                away_wins += 1
            else:
                home_wins += 1
        if(sim % 100 == 0):
            print(sim)
        sim += 1

        # Record results
        series_lengths.append(game_num)
        series_results[f"{max(away_wins, home_wins)}-{min(away_wins, home_wins)}"] += 1

        if away_wins > home_wins:
            away_wins_total += 1
        else:
            home_wins_total += 1

    return {
        'away_win_pct':   away_wins_total / n_simulations,
        'home_win_pct':   home_wins_total / n_simulations,
        'avg_series_length': np.mean(series_lengths),
        'series_length_dist': {
            length: count / n_simulations
            for length, count in sorted(
                pd.Series(series_lengths).value_counts().items()
            )
        },
        'series_result_dist': {
            result: count / n_simulations
            for result, count in sorted(
                series_results.items(),
                key=lambda x: x[1],
                reverse=True
            )
        }
    }

def run_series_prediction(model, game_features, away_team, home_team, series, n_simulations=10000):
    results = simulate_series(model, game_features, series, n_simulations)

    print(f"\n{'='*45}")
    print(f"  {away_team} (Away) vs {home_team} (Home)")
    print(f"  Simulations: {n_simulations:,}")
    print(f"{'='*45}")

    print(f"\nWin Probability:")
    print(f"  {away_team}: {results['away_win_pct']:.1%}")
    print(f"  {home_team}: {results['home_win_pct']:.1%}")

    print(f"\nSeries Length:")
    print(f"  Average: {results['avg_series_length']:.2f} games")
    for length, pct in results['series_length_dist'].items():
        bar = '█' * int(pct * 40)
        print(f"  {length} games: {pct:.1%}  {bar}")

    print(f"\nMost Likely Series Outcomes:")
    for result, pct in results['series_result_dist'].items():
        print(f"  {result}: {pct:.1%}")

    return results

"""
#run_series_prediction(model, game_features, 'Celtics', 'Lakers', n_simulations=10000)
#TESTING!!

df = pd.read_csv('training_data.csv')
dropping = ['Away Score', 'Home Score']
X = df.drop(columns=dropping)
y = df[['Away Score', 'Home Score']].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
model, results, actual = score.train(X_train, X_test, y_train, y_test)
model.predict()
#run_series_prediction(model, [[0.3297046238159187,0.8906160622814961,1.5760285762933934,3.3555054165696125,1.1595963846656439,1.5152319190418255,0.7773003602966615,1.8910250492732938,0.9681853540649887,0.40428701563846464,0.35423409271160533,0.7179929883269698,1.482103816725652,5.253199329446106,2.0138080359241823,0.4444826315976365,519.0350046238108,1531.8878160622662,3024.0271285762637,6628.226105416505,2022.5102963846457,2536.1827319190165,1038.4780503602863,2831.7239750492454,2525.5218853540396,854.89603701563,401.0099340927076,1387.883692988313,2222.165853816704,9608.181949329351,1872.2378080359056,314.63548263159447]], 'Indiana Pacers','Los Angeles', n_simulations=10000)


for idx, scores in results.items():
    print(f"Row {idx}: Away {scores['Away Score']} — Home {scores['Home Score']}")

tests = len(results)
print(tests)
correct = 0

for (k1, v1), (k2, v2) in zip(results.items(), actual.items()):
    if v1['Away Score'] > v1['Home Score'] and v2['Away Score'] > v2['Home Score']:
        correct += 1
    elif v1['Home Score'] > v1['Away Score'] and v2['Home Score'] > v2['Away Score']:
        correct += 1
    
print(correct)
print((correct / tests) * 100)
        
dict1 = testing[0]
dict2 = testing[1]

home_scores = predictions[:,1]
away_scores = predictions[:,0]
tests = len(home_scores)
correct = 0
i = 0

for (k1, v1), (k2, v2) in zip(dict1.items(), dict2.items()):
    if (v1 > v2):
        if(home_scores[i] > away_scores[i]):
            correct += 1
    else:
        if(home_scores[i] < away_scores[i]):
            correct += 1
    i+=1
print(correct)
print((float(correct) / tests) * 100.0)
"""
