# 🏆 Fidélité Client — Algo & BDD

## 📌 Problématique métier
Comment identifier les clients les plus fidèles, segmenter leur engagement 
et anticiper le désengagement dans un programme de fidélité ?

## 🎯 Objectif
Construire un pipeline complet de data marketing :
- Base de données MySQL modélisée
- Pipeline Python avec scoring et enrichissement API
- Dashboard interactif Plotly

---

## 🗄️ Structure de la base de données

5 tables reliées :
- `clients` — informations des clients
- `programmes` — niveaux de fidélité (Bronze, Silver, Gold)
- `client_programme` — relation many-to-many entre clients et programmes
- `transactions` — achats et points gagnés
- `recompenses` — récompenses échangées

## 🔗 Schéma de la base
> Schéma disponible sur dbdiagram.io

---

## 📦 Structure du projet
---

## 🚀 Lancer le projet

### 1. Prérequis
- Python 3.12+
- MySQL 9.7+
- pip

### 2. Installation des dépendances
```bash
pip3 install mysql-connector-python pandas requests python-dotenv dash
```

### 3. Configuration
Créer un fichier `.env` à la racine :

### 4. Initialiser la base de données
```bash
mysql -u root -p < sql/setup.sql
```

### 5. Lancer le pipeline Python
```bash
python3 python/main.py
```

### 6. Lancer le dashboard
```bash
python3 dashboard/dashboard.py
```
Ouvrir : http://127.0.0.1:8050

---

## 🧮 Algorithme de scoring fidélité

```python
score = total_points * 0.5 + nb_achats * 10 + total_depense * 0.1
```

| Segment | Score |
|---------|-------|
| 🥇 Gold | ≥ 300 |
| 🥈 Silver | ≥ 150 |
| 🥉 Bronze | < 150 |

---

## 🌐 API externe
Enrichissement des données avec l'API météo **wttr.in** — 
température actuelle par ville du client.

---

## 📊 Dashboard
- 3 KPIs : Total clients, Score moyen, Clients Gold
- Graphique camembert : répartition par segment
- Graphique barres : score de fidélité par client
- Filtre dropdown par segment

---

## 🛠️ Technologies utilisées
- **MySQL 9.7** — Base de données
- **Python 3.12** — Pipeline de données
- **Pandas** — Manipulation des données
- **Plotly Dash** — Dashboard interactif
- **mysql-connector-python** — Connexion MySQL
- **python-dotenv** — Gestion des variables d'environnement