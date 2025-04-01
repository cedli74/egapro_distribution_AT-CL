
from flask import Flask, jsonify
from flask_cors import CORS  # 📌 Ajout de Flask-CORS
import csv
import os

app = Flask(__name__)

# 🔥 Activation de CORS pour autoriser Swagger (localhost:5001)
CORS(app, resources={r"/*": {"origins": "http://localhost:5001"}})

# Données chargées au démarrage
DATA = []

def load_data():
    global DATA
    csv_path = os.path.join(os.path.dirname(__file__), "data/index-egalite-fh-utf8.csv")

    try:
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # Spécifiez le séparateur
            DATA = [row for row in reader]

        if DATA:
            print(f"✅ {len(DATA)} entreprises chargées depuis le fichier CSV.")
            print(f"🔍 Colonnes disponibles : {list(DATA[0].keys())}")  # Vérifier les colonnes

            # Afficher les trois premières lignes du fichier CSV
            print("📄 Extrait des premières lignes du CSV :")
            for i, example in enumerate(DATA[:3]):
                print(f"  Ligne {i+1} : {example}")

    except Exception as e:
        print(f"❌ Erreur lors du chargement des données : {e}")

# Charger les données une seule fois
load_data()

def clean_string(value):
    """ Nettoie une chaîne : supprime les espaces et normalise l'encodage. """
    return str(value).strip() if value else ""

@app.route("/", methods=["GET"])
def home():
    """ Test rapide pour voir si l'API fonctionne """
    return jsonify({"message": "API EgaPro fonctionne !"}), 200

@app.route("/api/v1/entreprises/<siren>", methods=["GET"])
def get_entreprise_by_siren(siren):
    siren = clean_string(siren)  # Nettoyer le SIREN en entrée

    # Vérifier si le SIREN est bien chargé dans les données
    all_sirens = [clean_string(e.get('SIREN', '')) for e in DATA]

    if siren not in all_sirens:
        print(f"❌ SIREN {siren} non trouvé dans la base !")
        return jsonify({"message": "Entreprise non trouvée"}), 404

    # Recherche de l'entreprise
    entreprise = next((e for e in DATA if clean_string(e.get('SIREN', '')) == siren), None)

    if entreprise:
        print(f"✅ Entreprise trouvée pour SIREN {siren} : {entreprise['Raison Sociale']}")
        return jsonify(entreprise)
    else:
        print(f"❌ Aucune entreprise trouvée pour le SIREN : {siren}")
        return jsonify({"message": "Entreprise non trouvée"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # 🔥 Ajout de debug=True pour voir les erreurs
