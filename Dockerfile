# Dockerfile para o projeto Book Store

FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para lxml
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

# Criar diretórios necessários
RUN mkdir -p data/output

# Expor porta da API
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=api.app
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV API_PORT=5000
ENV API_HOST=0.0.0.0

# Comando padrão (rodar API)
CMD ["python", "run_api.py"]

