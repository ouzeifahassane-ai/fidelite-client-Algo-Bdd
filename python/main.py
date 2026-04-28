import mysql.connector
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# ============================================
# CONNEXION À LA BASE DE DONNÉES
# ============================================
def get_connection():
    """Connexion à MySQL via les variables .env"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
def charger_donnees():
    """Charge la vue scoring depuis MySQL dans un DataFrame Pandas"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM vue_scoring", conn)
    conn.close()
    print("✅ Données chargées :")
    print(df.head())
    return df

# ============================================
# ALGORITHME DE SCORING FIDÉLITÉ
# ============================================
def calculer_scoring(df):
    """Calcule le score de fidélité et le segment client"""
    df['score_fidelite'] = (
        df['total_points'] * 0.5 +
        df['nb_achats'] * 10 +
        df['total_depense'] * 0.1
    ).round(2)

    def segmenter(score):
        if score >= 300:
            return 'Gold'
        elif score >= 150:
            return 'Silver'
        else:
            return 'Bronze'

    df['segment'] = df['score_fidelite'].apply(segmenter)
    print("\n✅ Scoring calculé :")
    print(df[['nom', 'total_points', 'score_fidelite', 'segment']])
    return df

# ============================================
# APPEL API EXTERNE
# ============================================
def enrichir_avec_api(df):
    """Enrichit les données avec des infos météo par ville via API"""
    def get_meteo(ville):
        try:
            url = f"https://wttr.in/{ville}?format=j1"
            response = requests.get(url, timeout=5)
            data = response.json()
            temp = data['current_condition'][0]['temp_C']
            return int(temp)
        except:
            return None

    df['temperature_ville'] = df['ville'].apply(get_meteo)
    print("\n✅ Enrichissement API météo :")
    print(df[['nom', 'ville', 'temperature_ville']])
    return df

# ============================================
# SAUVEGARDE DANS MYSQL
# ============================================
def sauvegarder_resultats(df):
    """Sauvegarde les résultats enrichis dans une nouvelle table MySQL"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scoring_clients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            email VARCHAR(100),
            ville VARCHAR(100),
            total_points INT,
            nb_achats INT,
            total_depense DECIMAL(10,2),
            score_fidelite DECIMAL(10,2),
            segment VARCHAR(20),
            temperature_ville INT
        )
    """)

    cursor.execute("DELETE FROM scoring_clients")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO scoring_clients 
            (nom, email, ville, total_points, nb_achats, total_depense, score_fidelite, segment, temperature_ville)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['nom'], row['email'], row['ville'],
            row['total_points'], row['nb_achats'], row['total_depense'],
            row['score_fidelite'], row['segment'], row['temperature_ville']
        ))

    conn.commit()
    conn.close()
    print("\n✅ Résultats sauvegardés dans scoring_clients !")

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    df = charger_donnees()
    df = calculer_scoring(df)
    df = enrichir_avec_api(df)
    sauvegarder_resultats(df)