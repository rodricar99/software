# Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app_old.py" ] # Cambia app.py al nombre de tu script de la aplicación Flask