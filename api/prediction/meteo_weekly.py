import requests

def fetch_and_filter_meteo_data():
    # URL de l'API
    url = "https://api.meteo-concept.com/api/forecast/daily?token=ab1fbb7d149618b5fd349b55f364b7047281678cf2cf2ac759ff2d8d9921f21a&insee=35238"

    # Envoyer une requête HTTP pour récupérer les données
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Imprimer le type de contenu et le contenu lui-même
        print("Content-Type:", response.headers['Content-Type'])
        print("Response [200]")
    else:
        print(f"Failed to retrieve data: {response.status_code}")


    # Adapter le traitement des données
    import pandas as pd

    df = None
    if 'application/json' in response.headers['Content-Type']:
        # Parser les données JSON
        data = response.json()

        # Extraire les informations pertinentes et les mettre dans un DataFrame
        forecasts = data.get('forecast', [])
        df = pd.DataFrame(forecasts)
    else:
        print("Unexpected content type:", response.headers['Content-Type'])


    # Filtrage
    # Convertir la colonne 'datetime' en datetime si elle n'est pas déjà convertie
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        df['datetime'] = pd.to_datetime(df['datetime'])

    # Convertir aujourd'hui en un objet "tz-aware"
    today = pd.Timestamp.today().tz_localize('UTC')  # Définir le fuseau horaire à UTC

    # Calculer la date de la semaine prochaine
    next_week = today + pd.Timedelta(days=7)

    # Filtrer les prévisions pour les prochains 7 jours
    filtered_df = df[(df['datetime'] >= today) & (df['datetime'] <= next_week)]

    # Suppression des colonnes inutiles
    # Liste des colonnes à supprimer
    colonnes_inutiles = ['insee', 'cp', 'latitude', 'longitude', 'probafrost', 'probafog', 'probawind70', 'probawind100', 'gustx']

    # Supprimer les colonnes inutiles
    filtered_df.drop(colonnes_inutiles, axis=1, inplace=True)

    filtered_df.to_csv('api/prediction/output/test.csv', index=False)

