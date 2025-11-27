# 🐛 Troubleshooting

Soluções para problemas comuns do Book Store API.

## 📋 Índice

- [Problemas de Instalação](#problemas-de-instalação)
- [Problemas com a API](#problemas-com-a-api)
- [Problemas de Autenticação](#problemas-de-autenticação)
- [Problemas com Deploy](#problemas-com-deploy)
- [Problemas com Web Scraping](#problemas-com-web-scraping)

---

## Problemas de Instalação

### Erro: "Module not found"

**Sintoma:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solução:**
```bash
# Verificar se o ambiente virtual está ativado
which python  # Deve apontar para o venv

# Reinstalar dependências
pip install -r requirements.txt

# ou forçar reinstalação
pip install -r requirements.txt --force-reinstall
```

### Erro ao instalar dependências no Windows

**Sintoma:**
```
error: Microsoft Visual C++ 14.0 is required
```

**Solução:**
1. Instale o [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/)
2. Ou use versões pré-compiladas: `pip install --only-binary :all: -r requirements.txt`

### Erro: "Permission denied" ao instalar pacotes

**Solução:**
```bash
# Use ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## Problemas com a API

### Porta 5000 já está em uso

**Sintoma:**
```
OSError: [Errno 48] Address already in use
```

**Solução 1:** Mudar porta
```bash
export API_PORT=5001
python run_api.py
```

**Solução 2:** Matar processo na porta 5000
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### API não responde ou demora muito

**Diagnóstico:**
```bash
# Verificar se a API está rodando
curl http://localhost:5000/health

# Ver logs
tail -f logs/api.log  # se logging configurado
```

**Soluções:**
- Verificar se há processos consumindo muita CPU/memória
- Reiniciar a API
- Verificar logs para erros

### Erro 500 (Internal Server Error)

**Diagnóstico:**
- Verificar logs da aplicação
- Verificar stack trace no terminal onde a API está rodando

**Soluções Comuns:**
- Verificar se `data/users.csv` existe
- Verificar permissões de arquivos
- Verificar configurações em `api/config.py`

### CORS Errors no Frontend

**Sintoma:**
```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solução:**

CORS já está configurado em `api/app.py`. Se ainda houver problemas:

```python
# api/app.py
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "https://seu-dominio.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## Problemas de Autenticação

### Token Expirado

**Sintoma:**
```json
{
  "msg": "Token has expired"
}
```

**Solução:**
```bash
# Usar refresh token
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

### Token Inválido

**Sintoma:**
```json
{
  "msg": "Invalid token"
}
```

**Soluções:**
1. Verificar formato do header:
```bash
# Correto
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Errado (faltando "Bearer")
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

2. Fazer login novamente para obter token válido

### Credenciais Inválidas

**Sintoma:**
```json
{
  "error": "Invalid credentials"
}
```

**Soluções:**
1. Verificar username e password
2. Verificar se usuário existe em `data/users.csv`
3. Usar usuários padrão: `admin`/`admin123` ou `user`/`user123`

### Acesso Negado (403 Forbidden)

**Sintoma:**
```json
{
  "error": "Admin access required"
}
```

**Solução:**

Endpoint requer role `admin`. Faça login com usuário admin:

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Arquivo users.csv corrompido

**Sintoma:**
```
Error reading users.csv
```

**Solução:**

Restaurar arquivo de exemplo:

```bash
cp data/users.csv.example data/users.csv

# Ou recriar usuários
python scripts/create_user.py create -u admin -p admin123 -r admin
python scripts/create_user.py create -u user -p user123
```

---

## Problemas com Deploy

### Heroku: Application Error

**Diagnóstico:**
```bash
heroku logs --tail --app seu-app
```

**Soluções Comuns:**

1. **Dynos desligados (H14 error)**:
```bash
heroku ps:scale web=1 --app seu-app
```

2. **Erro no Procfile**:

Verificar se `Procfile` está correto:
```
web: gunicorn api.wsgi:app
```

3. **Porta incorreta**:

Certifique-se que a app usa `$PORT`:
```python
# api/wsgi.py ou run_api.py
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
```

4. **Dependências faltando**:
```bash
# Verificar requirements.txt
heroku run pip list --app seu-app
```

### Heroku: Build Failed

**Diagnóstico:**
```bash
heroku logs --tail --app seu-app
```

**Soluções:**

1. **Python version**:

Verificar `runtime.txt` ou criar `.python-version`:
```
3.11
```

2. **Dependencies error**:
```bash
# Testar instalação local
pip install -r requirements.txt
```

3. **Rollback se necessário**:
```bash
heroku rollback --app seu-app
```

### Deploy Staging OK mas Production com erro

**Diagnóstico:**

Comparar configurações:
```bash
heroku config --app fiap-mle-bookstore-staging > staging.txt
heroku config --app fiap-mle-bookstore-prod > prod.txt
diff staging.txt prod.txt
```

**Solução:**

Sincronizar variáveis de ambiente necessárias.

---

## Problemas com Web Scraping

### Scraping retorna dados vazios

**Diagnóstico:**
```bash
python run_scraper.py --pages 1 --format json
cat data/output/books_*.json
```

**Soluções:**

1. Verificar se o site está acessível:
```bash
curl -I http://books.toscrape.com
```

2. Verificar logs do scraper
3. Site pode ter mudado estrutura HTML (atualizar seletores)

### Erro: "Connection timeout"

**Solução:**

Aumentar timeout em `scraper/base_scraper.py`:

```python
response = requests.get(url, timeout=30)  # Aumentar timeout
```

### Scraping muito lento

**Soluções:**

1. Reduzir número de páginas:
```bash
python run_scraper.py --pages 2  # Menos páginas
```

2. Verificar conexão de internet
3. Site pode estar com rate limiting

### Erro ao salvar arquivo

**Sintoma:**
```
PermissionError: [Errno 13] Permission denied
```

**Solução:**
```bash
# Verificar permissões da pasta data/output
chmod 755 data/output

# Criar pasta se não existir
mkdir -p data/output
```

---

## Problemas com Docker

### Container não inicia

**Diagnóstico:**
```bash
docker logs book-store-api
```

**Soluções:**

1. Rebuild imagem:
```bash
docker-compose build --no-cache
docker-compose up
```

2. Verificar Docker Compose file
3. Verificar se portas estão livres

### Erro: "Port already allocated"

**Solução:**
```bash
# Parar containers existentes
docker-compose down

# Ou mudar porta no docker-compose.yml
ports:
  - "5001:5000"  # Mapear para porta 5001
```

---

## Problemas com Testes

### Testes falhando

**Diagnóstico:**
```bash
pytest -v  # Modo verbose
pytest --lf  # Rodar apenas testes que falharam
```

**Soluções:**

1. Verificar dependências de teste:
```bash
pip install pytest pytest-cov
```

2. Limpar cache:
```bash
pytest --cache-clear
```

3. Verificar se API está rodando (para testes de integração):
```bash
# Parar API antes de testes
pkill -f run_api.py
```

### Erro de import nos testes

**Solução:**
```bash
# Adicionar diretório ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

---

## Problemas Gerais

### Git: "fatal: unable to access"

**Solução:**
```bash
# Verificar configuração
git config --global http.sslVerify false  # Temporário

# ou configurar proxy se necessário
git config --global http.proxy http://proxy:porta
```

### Swagger UI não carrega

**Diagnóstico:**
```bash
curl http://localhost:5000/api/v1/docs
```

**Soluções:**

1. Verificar se Flasgger está instalado:
```bash
pip install flasgger
```

2. Verificar configuração em `api/app.py`
3. Limpar cache do navegador

### Performance ruim

**Soluções:**

1. Verificar uso de memória/CPU
2. Implementar cache (Redis)
3. Otimizar queries de banco
4. Usar Gunicorn com múltiplos workers:
```bash
gunicorn -w 4 api.wsgi:app  # 4 workers
```

---

## 🆘 Ainda com Problemas?

Se o problema persistir:

1. **Verifique Issues no GitHub**: [Issues](https://github.com/giulianogimenez/FIAP-MLE-book-store/issues)
2. **Abra uma nova Issue** com:
   - Descrição detalhada do problema
   - Logs completos
   - Passos para reproduzir
   - Ambiente (OS, Python version, etc)

3. **Consulte a documentação**:
   - [Quick Start](QUICK_START.md)
   - [Autenticação](AUTHENTICATION.md)
   - [API](../api/README.md)
   - [Deploy](../DEPLOYMENT.md)

---

**📞 Suporte**: Para dúvidas ou problemas, abra uma [Issue no GitHub](https://github.com/giulianogimenez/FIAP-MLE-book-store/issues).

