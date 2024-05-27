import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import time


src_train = "api/prediction/output/train.csv"
src_test = "api/prediction/output/test.csv"

def ML_modeling():
    df_train = pd.read_csv(src_train)
    X_train = df_train.drop(columns=['energie', 'datetime'])
    y_train = df_train['energie']

    df_test = pd.read_csv(src_test)
    colonnes_utiles = X_train.columns
    df_test = df_test[colonnes_utiles]

    # MODELISATION

    # Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100)
    rf_model.fit(X_train, y_train)

    y_pred_rf_for_week = rf_model.predict(df_test)
    df_score = pd.DataFrame({'Predicted': y_pred_rf_for_week})

    # Données de l'exemple
    data = {
        "Predicted": df_score['Predicted'],
        "Day": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    }

    data_to_app = "{" + ", ".join(f"'{day}': {value}" for day, value in zip(data['Day'], data['Predicted'])) + "}"

    return data_to_app


