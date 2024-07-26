# Basisimage
FROM python:3.12-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

COPY /LSManagement /app/LSManagement

# Wechsel zum geklonten Repository-Verzeichnis
WORKDIR /app/LSManagement/

# Kopieren und Installieren von Python-Abh  ngigkeiten
# COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setzen der Umgebungsvariable FLASK_APP
ENV FLASK_APP=app.py

# Freigabe des Ports 5000 f  r Flask
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]