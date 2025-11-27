# 📑 Índice da Documentação

## 🎯 Por Onde Começar?

### Se você é novo no projeto:
1. 👉 **[QUICKSTART.md](QUICKSTART.md)** - Comece aqui! 5 minutos para rodar tudo
2. 📖 **[README.md](README.md)** - Documentação completa do projeto
3. 🔧 **[SETUP.md](SETUP.md)** - Guia detalhado de configuração

### Se você quer contribuir:
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia de contribuição

## 📚 Documentação

### Guias Principais

| Documento | Descrição | Quando Usar |
|-----------|-----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Início rápido em 5 min | Primeira vez no projeto |
| [README.md](README.md) | Documentação completa | Referência geral |
| [SETUP.md](SETUP.md) | Setup detalhado | Problemas de instalação |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Como contribuir | Vai fazer PR ou adicionar código |
| [INDEX.md](INDEX.md) | Este arquivo | Navegação na documentação |

## 🏗️ Estrutura do Projeto

### Módulos Principais

#### 📡 API REST (`api/`)
- `api/app.py` - Aplicação Flask principal
- `api/config.py` - Configurações da API
- `api/routes.py` - Definição de rotas/endpoints
- `api/controllers/` - Lógica de negócio

**Documentação:**
- Endpoints: Ver [README.md#Endpoints](README.md#endpoints-disponíveis)
- Exemplos: Ver [examples/api_examples.py](examples/api_examples.py)
- Testes: Ver [tests/test_api.py](tests/test_api.py)

#### 🕷️ Web Scraper (`scraper/`)
- `scraper/base_scraper.py` - Classe base abstrata
- `scraper/book_scraper.py` - Scraper de livros
- `scraper/data_processor.py` - Processamento de dados
- `scraper/main.py` - Script principal CLI

**Documentação:**
- Como usar: Ver [README.md#Scraper](README.md#usando-o-web-scraper)
- Exemplos: Ver [examples/scraper_examples.py](examples/scraper_examples.py)
- Testes: Ver [tests/test_scraper.py](tests/test_scraper.py)

#### 🧪 Testes (`tests/`)
- `tests/test_api.py` - Testes da API
- `tests/test_scraper.py` - Testes do scraper

### Arquivos de Configuração

| Arquivo | Propósito |
|---------|-----------|
| `requirements.txt` | Dependências Python |
| `setup.py` | Configuração do pacote (legacy) |
| `pyproject.toml` | Configuração do pacote (moderno) |
| `Makefile` | Comandos úteis |
| `Dockerfile` | Container Docker |
| `docker-compose.yml` | Orquestração Docker |
| `.gitignore` | Arquivos ignorados pelo Git |
| `.dockerignore` | Arquivos ignorados pelo Docker |

### Scripts de Execução

| Script | Comando | Descrição |
|--------|---------|-----------|
| `run_api.py` | `python run_api.py` | Inicia a API |
| `run_scraper.py` | `python run_scraper.py` | Inicia o scraper |

## 🎓 Tutoriais e Exemplos

### Exemplos Práticos

#### API
```bash
# Rodar exemplos da API
python examples/api_examples.py
```

Arquivo: [examples/api_examples.py](examples/api_examples.py)

Inclui exemplos de:
- Health check
- Listar livros
- Buscar livro por ID
- Criar novo livro
- Atualizar livro
- Deletar livro
- Buscar livros
- Estatísticas

#### Scraper
```bash
# Rodar exemplos do scraper
cd examples && python scraper_examples.py
```

Arquivo: [examples/scraper_examples.py](examples/scraper_examples.py)

Inclui exemplos de:
- Scraping básico
- Salvar dados (JSON/CSV)
- Scraping detalhado
- Criar scraper customizado
- Análise de dados

### Tutoriais no QUICKSTART

O [QUICKSTART.md](QUICKSTART.md) inclui:
- Tutorial 1: Adicionar livro via API
- Tutorial 2: Fazer scraping de páginas
- Tutorial 3: Testar com Python

## 🛠️ Comandos Úteis (Makefile)

```bash
make help          # Ver todos os comandos
make install       # Instalar dependências
make setup         # Setup completo
make env           # Criar arquivo .env
make run-api       # Rodar API
make run-scraper   # Rodar scraper
make test          # Rodar testes
make test-cov      # Testes com cobertura
make lint          # Verificar código
make format        # Formatar código
make clean         # Limpar temporários
make tree          # Ver estrutura
make status        # Status do projeto
```

Ver arquivo: [Makefile](Makefile)

## 🐳 Docker

### Arquivos Docker

- `Dockerfile` - Imagem Docker
- `docker-compose.yml` - Orquestração
- `.dockerignore` - Arquivos ignorados

### Comandos Docker

```bash
# Rodar API
docker-compose up api

# Rodar API + Scraper
docker-compose up

# Build
docker-compose build

# Logs
docker-compose logs -f
```

Mais em: [README.md#Docker](README.md)

## 📊 Estrutura de Diretórios

```
FIAP-MLE-book-store/
├── api/                    # Módulo API REST
│   ├── controllers/        # Lógica de negócio
│   ├── app.py             # App Flask
│   ├── config.py          # Configurações
│   └── routes.py          # Rotas
├── scraper/               # Módulo Web Scraper
│   ├── base_scraper.py    # Classe base
│   ├── book_scraper.py    # Scraper de livros
│   ├── data_processor.py  # Processamento
│   └── main.py            # CLI
├── tests/                 # Testes unitários
├── examples/              # Exemplos de uso
├── data/                  # Dados (criado em runtime)
│   └── output/            # Dados processados
├── docs/                  # Documentação
└── [arquivos de config]   # requirements.txt, etc.
```

## 🔍 Busca Rápida

### "Como faço para...?"

| Pergunta | Resposta |
|----------|----------|
| Instalar o projeto | [QUICKSTART.md](QUICKSTART.md) ou [SETUP.md](SETUP.md) |
| Rodar a API | `python run_api.py` ou ver [README.md](README.md#iniciar-o-servidor) |
| Rodar o scraper | `python run_scraper.py` ou ver [README.md](README.md#executar-scraping-básico) |
| Testar a API | `curl` exemplos em [README.md](README.md#exemplo-com-curl) |
| Criar novo endpoint | Ver [CONTRIBUTING.md](CONTRIBUTING.md#api-rest) |
| Criar novo scraper | Ver [CONTRIBUTING.md](CONTRIBUTING.md#web-scraper) |
| Rodar testes | `pytest` ou ver [README.md](README.md#executar-testes) |
| Ver exemplos | Diretório [examples/](examples/) |
| Contribuir | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Usar Docker | Ver [README.md](README.md) seção Docker |

### "Onde está...?"

| O que | Onde |
|-------|------|
| Código da API | [api/](api/) |
| Código do scraper | [scraper/](scraper/) |
| Testes | [tests/](tests/) |
| Exemplos | [examples/](examples/) |
| Dados coletados | [data/output/](data/output/) |
| Configurações | [api/config.py](api/config.py) e `.env` |
| Dependências | [requirements.txt](requirements.txt) |
| Documentação | Arquivos `.md` na raiz |

## 📖 Referência da API

### Endpoints

| Método | Endpoint | Descrição | Documentação |
|--------|----------|-----------|--------------|
| GET | `/health` | Health check | [README.md](README.md) |
| GET | `/api/v1/books` | Listar livros | [README.md](README.md) |
| GET | `/api/v1/books/:id` | Buscar livro | [README.md](README.md) |
| POST | `/api/v1/books` | Criar livro | [README.md](README.md) |
| PUT | `/api/v1/books/:id` | Atualizar | [README.md](README.md) |
| DELETE | `/api/v1/books/:id` | Deletar | [README.md](README.md) |
| GET | `/api/v1/stats` | Estatísticas | [README.md](README.md) |

Detalhes completos: [README.md - Endpoints](README.md#endpoints-disponíveis)

## 🔗 Links Externos

### Documentação de Dependências

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Parser HTML
- [Requests](https://requests.readthedocs.io/) - Cliente HTTP
- [Pandas](https://pandas.pydata.org/) - Análise de dados
- [Pytest](https://docs.pytest.org/) - Framework de testes

### Recursos de Aprendizado

- [Python.org](https://www.python.org/)
- [Real Python](https://realpython.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

## 🆘 Suporte

### Encontrou um problema?

1. Verifique o [SETUP.md](SETUP.md) - Troubleshooting
2. Verifique o [QUICKSTART.md](QUICKSTART.md) - Problemas?
3. Busque nas [Issues](https://github.com/FIAP/FIAP-MLE-book-store/issues)
4. Crie uma nova Issue se necessário

### Quer contribuir?

Leia o [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Última atualização:** 2025-11-27

**Versão:** 1.0.0

