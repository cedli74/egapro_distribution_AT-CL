import grpc
from concurrent import futures
import os, csv
import proto.egapro_pb2 as egapro_pb2
import proto.egapro_pb2_grpc as egapro_pb2_grpc

# Mapping entre les noms de colonnes du CSV et les noms des champs dans le message Entreprise
CSV_TO_PROTO = {
    'Année': 'annee',
    'Structure': 'structure',
    "Tranche d'effectifs": 'tranche_effectifs',
    'SIREN': 'siren',
    'Raison Sociale': 'raison_sociale',
    'Nom UES': 'nom_ues',
    'Entreprises UES (SIREN)': 'entreprises_ues',
    'Région': 'region',
    'Département': 'departement',
    'Pays': 'pays',
    'Code NAF': 'code_naf',
    'Note Ecart rémunération': 'note_ecart_remuneration',
    "Note Ecart taux d'augmentation (hors promotion)": 'note_ecart_taux_augmentation_hors_promotion',
    'Note Ecart taux de promotion': 'note_ecart_taux_promotion',
    "Note Ecart taux d'augmentation": 'note_ecart_taux_augmentation',
    'Note Retour congé maternité': 'note_retour_conge_maternite',
    'Note Hautes rémunérations': 'note_hautes_remunerations',
    'Note Index': 'note_index'
}

def load_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "data/index-egalite-fh-utf8.csv")
    data = []
    try:
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                # Appliquer le mapping pour transformer les clés du CSV en clés conformes à notre proto
                transformed = {}
                for key, value in row.items():
                    mapped_key = CSV_TO_PROTO.get(key)
                    if mapped_key:
                        transformed[mapped_key] = value.strip()
                data.append(transformed)
        if data:
            print(f"✅ {len(data)} entreprises chargées depuis le CSV.")
            print("📄 Extrait des 3 premières lignes du CSV transformé :")
            for i, row in enumerate(data[:3]):
                print(f"  Ligne {i+1} : {row}")
        else:
            print("❌ Aucun enregistrement chargé depuis le CSV.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du CSV : {e}")
    return data

class EgaproService(egapro_pb2_grpc.EgaproServiceServicer):
    def __init__(self):
        self.data = load_csv()

    def GetEntreprises(self, request, context):
        entreprises = []
        for row in self.data:
            try:
                entreprises.append(egapro_pb2.Entreprise(**row))
            except Exception as ex:
                print(f"Erreur lors de la création d'une entreprise: {ex}")
        return egapro_pb2.EntreprisesResponse(entreprises=entreprises)

    def GetEntrepriseBySiren(self, request, context):
        siren_input = request.siren.strip()
        entreprise = next((row for row in self.data if row.get("siren", "") == siren_input), None)
        if entreprise:
            try:
                return egapro_pb2.EntrepriseResponse(entreprise=egapro_pb2.Entreprise(**entreprise))
            except Exception as ex:
                context.set_details(f"Erreur lors de la création de l'entreprise: {ex}")
                context.set_code(grpc.StatusCode.INTERNAL)
                return egapro_pb2.EntrepriseResponse()
        else:
            context.set_details("Entreprise non trouvée")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return egapro_pb2.EntrepriseResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    egapro_pb2_grpc.add_EgaproServiceServicer_to_server(EgaproService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("✅ Serveur gRPC en cours d'exécution sur le port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
