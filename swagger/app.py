from flask import Flask, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app, template_file='swagger.yml')  # Utilisez le fichier de modèle

@app.route("/api/v1/entreprises/<siren>", methods=["GET"])
@swag_from({
    "tags": ["Entreprises"],
    "parameters": [
        {
            "name": "siren",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Numéro SIREN de l'entreprise"
        }
    ],
    "responses": {
        "200": {
            "description": "Données de l'entreprise",
            "examples": {
                "application/json": {
                    "siren": "123456789",
                    "nom": "Entreprise Exemple",
                    "score_egalite": 95,
                    "adresse": "123 Rue Exemple, 75000 Paris",
                    "autres_infos": "..."
                }
            }
        },
        "404": {
            "description": "Entreprise non trouvée"
        }
    }
})
def get_entreprise_by_siren(siren):
    # Logique pour récupérer les données de l'entreprise
    entreprise = {
        "siren": siren,
        "nom": "Entreprise Exemple",
        "score_egalite": 95,
        "adresse": "123 Rue Exemple, 75000 Paris",
        "autres_infos": "..."
    }
    return jsonify(entreprise)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # L'application et Swagger s'exécutent sur le port 5000
