# Basisimage
FROM python:3.12-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

COPY . .

# Kopieren und Installieren von Python-Abh  ngigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Setzen der Umgebungsvariable FLASK_APP
ENV FLASK_APP=app.py

# Freigabe des Ports 5000 f  r Flask
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]