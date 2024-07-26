# Basisimage
FROM python:3.12-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Installation von Git und anderen notwendigen Paketen
RUN apt-get update && apt-get install -y git && apt-get clean

# Klonen des Git-Repositories
RUN git clone https://github.com/K4esus/LSManagement.git .

WORKDIR /app/LSManagement
# Installation der Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Freigabe des Ports 5000 für Flask
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]