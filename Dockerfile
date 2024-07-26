# Basisimage
FROM python:3.12-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Installation von Git und anderen notwendigen Paketen
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Klonen des Git-Repositories in ein spezifisches Verzeichnis
RUN git clone https://github.com/K4esus/LSManagement.git /app/LSManagement

# Wechsel zum geklonten Repository-Verzeichnis
WORKDIR /app/LSManagement/

# Kopieren und Installieren von Python-Abh  ngigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setzen der Umgebungsvariable FLASK_APP
ENV FLASK_APP=app.py

# Freigabe des Ports 5000 f  r Flask
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]