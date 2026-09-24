import score_model
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import predict_winner

df = pd.read_csv('team_stats.csv')
print(list(df.iloc[0][2:]))