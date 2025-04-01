FROM nginx:alpine

# Supprimer la config par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copier votre configuration dans le dossier de configuration d'Nginx
COPY default.conf /etc/nginx/conf.d/default.conf
