# Stage 1: Builder - Instala as dependências em um ambiente temporário
FROM python:3.11-slim AS builder

# Variáveis de ambiente para otimização e boas práticas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Instala pacotes no diretório home do usuário, facilitando a cópia entre estágios
ENV PIP_USER=true

WORKDIR /app

# Instala dependências de sistema que podem ser necessárias para compilar pacotes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python. O contexto do build é a raiz do projeto.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Runner - A imagem final, leve e segura
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cria um usuário não-root por segurança
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot

# Copia os pacotes instalados do estágio 'builder'
COPY --from=builder /root/.local /home/nonroot/.local

# Copia apenas o código da aplicação (o conteúdo da pasta 'mock_api')
COPY mock_api/ .

# Adiciona o diretório de binários do usuário ao PATH (onde o gunicorn foi instalado)
ENV PATH=/home/nonroot/.local/bin:$PATH

# Adiciona o diretório de pacotes do usuário ao PYTHONPATH para que o interpretador encontre os módulos
ENV PYTHONPATH=/home/nonroot/.local/lib/python3.11/site-packages

# Troca para o usuário não-root
USER nonroot

EXPOSE 5001

# Usa Gunicorn como servidor WSGI de produção.
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5001", "app:app"]