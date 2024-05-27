import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from concurrent.futures import ThreadPoolExecutor
import time

src_train = "output/train.csv"
src_test = "output/test.csv"

def predict_rf_model(X_train, y_train, df_test):
    rf_model = RandomForestRegressor(n_estimators=100)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(df_test)
    return y_pred_rf

def ML_modeling_thread():
    df_train = pd.read_csv(src_train)
    X_train = df_train.drop(columns=['energie', 'datetime'])
    y_train = df_train['energie']

    df_test = pd.read_csv(src_test)
    colonnes_utiles = X_train.columns
    df_test = df_test[colonnes_utiles]

    # Utiliser ThreadPoolExecutor pour exécuter plusieurs prédictions en parallèle
    with ThreadPoolExecutor() as executor:
        y_pred_rf_for_week = executor.submit(predict_rf_model, X_train, y_train, df_test).result()

    df_score = pd.DataFrame({'Predicted': y_pred_rf_for_week})

    # Données de l'exemple
    data = {
        "Predicted": df_score['Predicted'].values,
        "Day": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    }

    return data


# Avec thread
start_time = time.time()
ML_modeling_thread()
end_time = time.time()
execution_time_with_thread = end_time - start_time
print("Temps d'exécution avec thread:", execution_time_with_thread)

my_data = ML_modeling_thread()

data_to_app = "{" + ", ".join(f"'{day}': {value}" for day, value in zip(my_data['Day'], my_data['Predicted'])) + "}"
print(data_to_app)
