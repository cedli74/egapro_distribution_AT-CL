# EgaPro Distribution

Ce projet propose deux services complémentaires pour interroger les données d’égalité professionnelle entre les femmes et les hommes :

- Une **API REST** avec documentation interactive via **Swagger**
- Un service **gRPC** permettant de requêter les données depuis un client Python

L’ensemble est orchestré via **Docker** et **Docker Compose**, ce qui permet une mise en route simple et rapide.

---

## Fonctionnalités

- Recherche d’une entreprise par numéro SIREN via REST ou gRPC
- Affichage des informations détaillées depuis un fichier CSV
- Interface Swagger pour explorer les endpoints REST
- Reverse proxy via Nginx pour un accès unifié

---

## Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Lancer le projet

### 1. Cloner le dépôt

```bash
https://github.com/cedli74/egapro_distribution_AT-CL.git
cd egapro_distribution 
```

Ajouter le fichier CSV
Le projet utilise un fichier de données CSV nommé index-egalite-fh-utf8.csv. Pour que le projet fonctionne :

Créez un dossier data/ à la racine du projet s'il n'existe pas déjà

Ajoutez le fichier CSV téléchargé depuis le site data.gouv.fr dans ce dossier

Structure attendue :

```bash
Copier
Modifier
egapro_distribution/
├── data/
│   └── index-egalite-fh-utf8.csv
```
⚠️ Assurez-vous que le fichier s'appelle exactement index-egalite-fh-utf8.csv.

3. Lancer Docker
Lancez tous les services d'un coup avec Docker Compose :
```bash
docker-compose up --build
```
Cette commande :

- Construit les images si nécessaire
- Lance les 4 services :
    - rest_api (port 5000)
    - grpc_service (port 50051)
    - swagger (port 5001)
    - nginx (port 80)

Vous pouvez maintenant accéder à l’API REST, à Swagger et utiliser gRPC.

Accès aux services
1. API REST
Pour récupérer les informations d'une entreprise via son SIREN :

```bash
[docker-compose up --build]
(http://localhost:5000/api/v1/entreprises/{SIREN})
```
Exemple :
```bash
http://localhost:5000/api/v1/entreprises/352383715
```

2. Interface Swagger
Swagger est accessible à deux adresses :

Directement via : http://localhost:5001/apidocs/

Via Nginx (reverse proxy partiellement configuré) : http://localhost/swagger/

La redirection via Nginx est en place, mais l'affichage complet de Swagger ne fonctionne pas encore (les ressources et sous-pages ne sont pas encore correctement servies).

Service gRPC
Un client Python est disponible pour tester le service gRPC.

Exécution dans le conteneur :

```bash
docker-compose exec grpc_service python client.py
```

Ce client :

Demande un numéro de SIREN

Affiche les informations de l’entreprise correspondante

À savoir sur le reverse proxy Nginx
Un début de configuration est en place pour un reverse proxy unique (tout via http://localhost), mais seul Swagger est partiellement redirigé. Actuellement :

/swagger/ est redirigé vers /apidocs/

Mais les ressources (CSS, JS, JSON) ne sont pas encore toutes servies correctement

Le reverse proxy pour REST et gRPC n'est pas encore intégré



![image](https://github.com/user-attachments/assets/0ad930eb-f88e-40b3-a98d-ee0e2e771b28)

![image](https://github.com/user-attachments/assets/603dbc09-6b7b-4c97-b51e-6780d5ebabb7)

![image](https://github.com/user-attachments/assets/5c73a670-8146-4903-8935-df60da4d4643)

![image](https://github.com/user-attachments/assets/22afb652-2e46-41ba-94d0-876583e94ea1)


![image](https://github.com/user-attachments/assets/7a53501f-0e81-4d0f-ba88-aaf9e7435eb1)

![image](https://github.com/user-attachments/assets/eb70d90e-fafa-4e54-bc75-3800d5e71ac2)

