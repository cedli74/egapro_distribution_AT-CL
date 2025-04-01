import grpc
import proto.egapro_pb2 as egapro_pb2
import proto.egapro_pb2_grpc as egapro_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = egapro_pb2_grpc.EgaproServiceStub(channel)
        siren_input = input("Entrez le SIREN de l'entreprise recherchée : ").strip()
        print(f"\n🔍 Recherche de l'entreprise avec SIREN {siren_input}...")
        try:
            response = stub.GetEntrepriseBySiren(egapro_pb2.EntrepriseRequest(siren=siren_input))
            entreprise = response.entreprise
            if entreprise and entreprise.siren:
                print("✅ Entreprise trouvée:")
                for field in entreprise.DESCRIPTOR.fields:
                    value = getattr(entreprise, field.name)
                    print(f"  {field.name}: {value}")
            else:
                print("❌ Entreprise non trouvée")
        except grpc.RpcError as e:
            print(f"❌ Erreur: {e.details()}")

if __name__ == "__main__":
    run()
