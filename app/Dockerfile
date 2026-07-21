FROM python:3.11-slim

# Evita gravação de arquivos .pyc no container e habilita log direto no stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Garante a existência do diretório do banco de dados
RUN mkdir -p /app/database

EXPOSE 5000

CMD ["python", "main.py"]