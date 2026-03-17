# Dockerfile pour EasyConnect FastAPI
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers requirements.txt si tu en as
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code de ton projet
COPY . .

# Expose le port FastAPI
EXPOSE 8000

# Commande pour lancer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]