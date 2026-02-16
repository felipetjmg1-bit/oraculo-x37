FROM python:3.11-slim

WORKDIR /app

# Instalar dependências de sistema se necessário
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Garantir que os modelos iniciais existam (opcional, ou rodar train no build)
RUN python -m scripts.train --samples 100 --features 10

EXPOSE 5000

ENV HOST=0.0.0.0
ENV PORT=5000

CMD ["python", "-m", "app.main"]
