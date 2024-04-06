# Utiliser une image de base officielle Python 3.12.2
FROM python:3.12.2

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances dans le répertoire de travail courant
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application dans le conteneur
COPY . .

# Ajouter le répertoire de travail courant (/app) à PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Définir la variable d'environnement FLASK_APP pour indiquer le fichier d'entrée de l'application Flask
ENV FLASK_APP app.py

# Exposer le port sur lequel l'application Flask écoute
EXPOSE 5000

# Définir la commande pour exécuter l'application Flask
CMD ["flask", "run", "--host=0.0.0.0"]