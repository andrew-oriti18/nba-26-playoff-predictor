from xgboost import XGBRegressor, DMatrix
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.multioutput import MultiOutputRegressor

def train(X_train, X_test, y_train, y_test):

    model = xgb.XGBRegressor(
            n_estimators=1000,
            learning_rate=0.02,
            max_depth=5,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            early_stopping_rounds=75,
            objective='reg:squarederror',
            multi_strategy='multi_output_tree'
        )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test,y_test)],
        verbose=50)

    preds = model.predict(X_test)

    target_names = ['Away Score', 'Home Score']
    for i, name in enumerate(target_names):
        rmse = root_mean_squared_error(y_test[:, i], preds[:, i])
        mae  = mean_absolute_error(y_test[:, i], preds[:, i])
        #r2   = r2_score(y_test[:, i], preds[:, i])
        print(f"{name} — RMSE: {rmse:.4f} | MAE: {mae:.4f}")

    results = {
        idx: {
            'Away Score': round(preds[i, 0], 2),
            'Home Score': round(preds[i, 1], 2)
        }
        for i, idx in enumerate(X_test.index)
    }

    actual = {
        idx: {
            'Away Score': round(y_test[i, 0], 2),
            'Home Score': round(y_test[i, 1], 2)
        }
        for i, idx in enumerate(X_test.index)
    }

    return model, results, actual