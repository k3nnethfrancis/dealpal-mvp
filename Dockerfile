# Usa un'immagine base che ha sia Python che Node.js
FROM nikolaik/python-nodejs:latest

# Installa supervisord
RUN apt-get update && apt-get install -y supervisor

# Crea una directory per i file di configurazione di supervisord
RUN mkdir -p /etc/supervisor/conf.d

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file dei requisiti Python e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il frontend e installa le dipendenze NPM
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN cd frontend && npm install

# Copia il resto del codice sorgente
COPY . .

# Copia la configurazione di supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Imposta le porte esposte corrispondenti ai servizi
EXPOSE 9090 8001

# Comando per avviare supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
