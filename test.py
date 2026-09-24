import score_model
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import predict_winner
import xgboost as xgb
from xgboost import XGBRegressor, DMatrix, XGBClassifier

"""
df = pd.read_csv('training_data.csv')
dropping = ['Away Score', 'Home Score']
df.columns = df.columns.str.strip().str.strip("'")
#print(df.columns.tolist())  # add this
X = df.drop(columns=dropping)
y = df[['Away Score', 'Home Score']].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
model, results, actual = score_model.train(X_train, X_test, y_train, y_test)
model.save_model('basketball_predictor.json')
"""
model = XGBRegressor()
model.load_model('basketball_predictor.json')


df1 = pd.read_html('https://www.basketball-reference.com/teams/SAS/2026.html')
df2 = pd.read_html('https://www.basketball-reference.com/teams/NYK/2026.html')
dframe = pd.read_csv('team_stats.csv')

table1 = df1[1]
table2 = df2[1]
data1 = np.zeros(16)
data2 = np.zeros(16)

for idx, row in table1.iterrows():
    if idx != 0 and row.Player != 'Team Totals':
        stats_dat = [row['3P'], row['3PA'], row['2P'], row['2PA'], row['FT'], row['FTA'],
         row['ORB'], row['DRB'], row['AST'], row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS']]
                            
        oE = ((3 * row['3P'] - row['3PA'] + 2 * row['2P'] - row['2PA'] + row['FT'] - 0.5 * row['FTA']
        + 0.5 * row['ORB'] + 1.5 * row['AST'] - 1.5 * row['TOV'] + row['PTS']) * 4) / row['MP']
        stats_dat.append(oE)

        dE = ((row['DRB'] + 2 * row['BLK'] + 1.5  * row['STL'] - 1.25 * row['PF']) * 4) / row['MP']
        stats_dat.append(dE)

        stats = np.array(stats_dat)
        stats = stats * float(row['MP'])

        data1 += stats

team_stats = [102.3,0.574,0.704,0.468,0.422,0.467,0.359]
#data1 *= 2.135

for idx, row in table2.iterrows():
    if idx != 0 and row.Player != 'Team Totals':
        stats_dat = [row['3P'], row['3PA'], row['2P'], row['2PA'], row['FT'], row['FTA'],
         row['ORB'], row['DRB'], row['AST'], row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS']]
                            
        oE = ((3 * row['3P'] - row['3PA'] + 2 * row['2P'] - row['2PA'] + row['FT'] - 0.5 * row['FTA']
        + 0.5 * row['ORB'] + 1.5 * row['AST'] - 1.5 * row['TOV'] + row['PTS']) * 4) / row['MP']
        stats_dat.append(oE)

        dE = ((row['DRB'] + 2 * row['BLK'] + 1.5  * row['STL'] - 1.25 * row['PF']) * 4) / row['MP']
        stats_dat.append(dE)

        stats = np.array(stats_dat)
        stats = stats * float(row['MP'])

        data2 += stats

team_stats_2 = [99.0,0.556,0.689,0.464,0.449,0.439,0.373]
#data2 *= 2.135

print(table1)
training = np.concatenate([data1, team_stats, data2, team_stats_2])
predict_winner.run_series_prediction(model, [training], 'Away', 'Home',4, 5000)
#print(predict_winner.predict_game(model, [training]))