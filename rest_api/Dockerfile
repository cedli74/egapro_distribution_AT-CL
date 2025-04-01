# Utilisation d'une image Python 3.9
FROM python:3.9

# Définition du dossier de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY app.py requirements.txt /app/

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposition du port 5000 (API Flask)
EXPOSE 5000

# Lancement de l'application avec gunicorn pour un meilleur support de production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
