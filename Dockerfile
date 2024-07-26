# Basisimage
FROM python:3.12-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

COPY /database /app/database
COPY /templates /app/templates
COPY /testdata /app/testdata
COPY /utils /app/utils
COPY app.py .
COPY config.py .
COPY Dockerfile .
COPY forms.py .

# Kopieren und Installieren von Python-Abh  ngigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Setzen der Umgebungsvariable FLASK_APP
ENV FLASK_APP=app.py

# Freigabe des Ports 5000 f  r Flask
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]