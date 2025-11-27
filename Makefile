# Makefile para facilitar comandos comuns

.PHONY: help install setup run-api run-scraper test clean lint format

help:  ## Mostrar esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependências
	pip install --upgrade pip
	pip install -r requirements.txt

setup: install  ## Configuração inicial completa
	mkdir -p data/output
	@echo "✅ Setup completo!"
	@echo "Próximo passo: Copie .env.example para .env e ajuste as configurações"

run-api:  ## Rodar a API Flask
	python run_api.py

run-scraper:  ## Rodar o scraper básico
	python run_scraper.py

test:  ## Executar todos os testes
	pytest -v

test-cov:  ## Executar testes com cobertura
	pytest --cov=api --cov=scraper --cov-report=html --cov-report=term

lint:  ## Verificar código com flake8
	flake8 api scraper tests --max-line-length=100 --exclude=venv

format:  ## Formatar código com black
	black api scraper tests

clean:  ## Limpar arquivos temporários
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

clean-data:  ## Limpar dados coletados
	rm -rf data/output/*
	@echo "✅ Dados limpos!"

env:  ## Criar arquivo .env a partir do exemplo
	@if [ ! -f .env ]; then \
		echo "# Flask Configuration" > .env; \
		echo "FLASK_APP=api.app" >> .env; \
		echo "FLASK_ENV=development" >> .env; \
		echo "FLASK_DEBUG=True" >> .env; \
		echo "API_PORT=5000" >> .env; \
		echo "API_HOST=0.0.0.0" >> .env; \
		echo "" >> .env; \
		echo "# Database Configuration" >> .env; \
		echo "DATABASE_URL=sqlite:///bookstore.db" >> .env; \
		echo "" >> .env; \
		echo "# Scraping Configuration" >> .env; \
		echo "SCRAPING_DELAY=1" >> .env; \
		echo "USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" >> .env; \
		echo "✅ Arquivo .env criado!"; \
	else \
		echo "⚠️  Arquivo .env já existe!"; \
	fi

venv:  ## Criar ambiente virtual
	python3 -m venv venv
	@echo "✅ Ambiente virtual criado!"
	@echo "Ative com: source venv/bin/activate"

dev:  ## Configuração completa para desenvolvimento
	@make venv
	@echo "\nAgora execute:"
	@echo "  source venv/bin/activate"
	@echo "  make setup"
	@echo "  make env"

api-test:  ## Testar API com curl
	@echo "Testing health endpoint..."
	@curl -s http://localhost:5000/health | python -m json.tool
	@echo "\nTesting books endpoint..."
	@curl -s http://localhost:5000/api/v1/books | python -m json.tool

scrape-demo:  ## Demo do scraper (2 páginas)
	python run_scraper.py --pages 2 --format both --output demo

scrape-full:  ## Scraping completo (5 páginas)
	python run_scraper.py --pages 5 --format both --output books_full

examples-api:  ## Rodar exemplos da API
	python examples/api_examples.py

examples-scraper:  ## Rodar exemplos do scraper
	cd examples && python scraper_examples.py

tree:  ## Mostrar estrutura do projeto
	tree -L 3 -I 'venv|__pycache__|*.pyc|.git|htmlcov|.pytest_cache' .

status:  ## Status do projeto
	@echo "📊 Status do Projeto"
	@echo "===================="
	@echo "\n📁 Estrutura:"
	@find . -name "*.py" -not -path "./venv/*" | wc -l | xargs echo "  Arquivos Python:"
	@echo "\n📦 Dependências:"
	@pip list | grep -E "(Flask|requests|beautifulsoup4|pandas)" || echo "  Instale dependências: make install"
	@echo "\n🧪 Testes:"
	@if [ -d "tests" ]; then find tests -name "test_*.py" | wc -l | xargs echo "  Arquivos de teste:"; fi
	@echo "\n💾 Dados:"
	@if [ -d "data/output" ]; then ls -1 data/output | wc -l | xargs echo "  Arquivos em data/output:"; fi

