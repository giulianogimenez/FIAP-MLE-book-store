# 🚀 Deploy Workflow - Local → Staging → Production

## Workflow Canônico

Este documento define o processo obrigatório para deploy de todas as mudanças.

---

## 🏠 TESTES LOCAIS (Obrigatório para Scraping)

### ⚠️ IMPORTANTE: Teste Localmente ANTES do Deploy

Para mudanças relacionadas ao **scraping**, **SEMPRE** teste localmente primeiro:

**Razões:**
- 🚀 **Feedback imediato** (segundos vs minutos)
- 💰 **Reduz custos de cloud** (menos builds no Heroku)
- 🐛 **Detecta bugs rapidamente** (sem poluir logs de staging)
- ⏱️ **Economiza tempo** (sem esperar builds)

### 📝 Quando Testar Localmente

| Tipo de Mudança | Teste Local? | Razão |
|-----------------|-------------|-------|
| **Scraping (parser, extração)** | ✅ **OBRIGATÓRIO** | Validar extração de dados |
| **Lógica de negócio** | ✅ Recomendado | Validar comportamento |
| **Endpoints novos/modificados** | ✅ Recomendado | Testar contratos |
| **Configuração/deploy** | ⚠️ Opcional | Depende de infra cloud |
| **Documentação apenas** | ❌ Não necessário | Sem código executável |

---

## 🧪 Como Testar Scraping Localmente

### 1. Teste Rápido (Scraper Isolado)

```bash
cd /path/to/project

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Executar scraper standalone
python run_scraper.py --pages 2 --format json --output test_local

# Verificar output
ls -lh data/output/test_local.json
cat data/output/test_local.json | python3 -m json.tool | head -50
```

### 2. Teste Completo (Via API Local)

```bash
# Terminal 1: Iniciar API local
python run_api.py
# ou
flask run

# Terminal 2: Testar endpoint de scraping
LOCAL_URL="http://localhost:5000"

# Login
curl -s "$LOCAL_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' > /tmp/local_token.json

TOKEN=$(cat /tmp/local_token.json | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Trigger scraping (2 páginas para teste rápido)
curl -s "$LOCAL_URL/api/v1/scraping/trigger" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"url": "http://books.toscrape.com", "pages": 2, "format": "json", "output": "test_local"}'

# Aguardar 1-2 minutos
sleep 120

# Verificar resultado
curl -s "$LOCAL_URL/api/v1/books?limit=1" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### 3. Validar Dados Extraídos

```python
# Verificar estrutura dos dados localmente
import json

with open('data/output/test_local.json', 'r') as f:
    books = json.load(f)
    
first_book = books[0]
print("Campos extraídos:")
print(f"  ✅ title: {first_book.get('title')}")
print(f"  ✅ price: {first_book.get('price')}")
print(f"  ✅ upc: {first_book.get('upc', '❌ MISSING')}")
print(f"  ✅ category: {first_book.get('category', '❌ MISSING')}")
print(f"  ✅ isbn: {first_book.get('isbn', '❌ MISSING')}")
print(f"  ✅ description: {first_book.get('description', '❌ MISSING')[:50]}...")
```

### ✅ Definition of Done (Testes Locais)

Antes de fazer commit, validar:

- [ ] ✅ Scraper executa sem erros
- [ ] ✅ Todos os campos esperados estão presentes (UPC, category, ISBN, etc.)
- [ ] ✅ Dados estão no formato correto (tipos, valores)
- [ ] ✅ Arquivo JSON/CSV foi gerado corretamente
- [ ] ✅ Performance aceitável (tempo razoável para N páginas)
- [ ] ✅ Logs não mostram erros críticos

### 💡 Dica: Use Páginas Pequenas para Teste

```bash
# ✅ BOM: Teste rápido local
python run_scraper.py --pages 2  # ~40 books, ~2 minutos

# ❌ EVITAR: Teste longo local
python run_scraper.py --pages 30  # ~600 books, ~15 minutos
```

---

## 📋 Checklist de Deploy Completo

### 0️⃣ Testes Locais (Scraping/Lógica)
- [ ] **Testar scraper localmente** (se aplicável)
- [ ] Validar estrutura de dados
- [ ] Verificar performance
- [ ] Confirmar todos os campos necessários

### 1️⃣ Desenvolvimento
- [ ] Implementar mudanças localmente
- [ ] **Testar localmente** (especialmente scraping)
- [ ] Commit no GitHub (`git push origin main`)

#### 2️⃣ Staging
- [ ] Deploy em staging: `git push staging main`
- [ ] ⏳ Aguardar build do Heroku (~30-60s)
- [ ] 🧪 Executar testes com `curl` em staging
- [ ] ✅ Validar Definition of Done (DoD)

#### 3️⃣ Production (Somente após validação em Staging)
- [ ] Deploy em produção: `git push production main`
- [ ] ⏳ Aguardar build do Heroku (~30-60s)
- [ ] 🔍 Validação final em produção

---

## 🧪 Testes Obrigatórios em Staging

### Para Endpoints Novos/Modificados

```bash
STAGING_URL="https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com"

# 1. Health Check
curl -s $STAGING_URL/health | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])"

# 2. Obter token admin
curl -s "$STAGING_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  > /tmp/staging_token.json

TOKEN=$(cat /tmp/staging_token.json | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 3. Testar endpoint específico
# Exemplo: GET /api/v1/books
curl -s "$STAGING_URL/api/v1/books" -H "Authorization: Bearer $TOKEN" | head -20

# 4. Verificar status HTTP
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/api/v1/books" -H "Authorization: Bearer $TOKEN")
echo "Status: $HTTP_CODE"

# 5. Validar resposta
# Adicionar testes específicos conforme necessário
```

### Critérios de DoD (Definition of Done)

Antes de promover para produção, validar:

- [ ] ✅ Endpoint retorna status HTTP esperado
- [ ] ✅ Autenticação funciona corretamente
- [ ] ✅ Autorização (roles) funciona corretamente
- [ ] ✅ Resposta tem estrutura JSON/HTML esperada
- [ ] ✅ Sem erros 500 (Internal Server Error)
- [ ] ✅ Health check está "healthy" ou "degraded" (não "unhealthy")
- [ ] ✅ Logs do Heroku não mostram erros críticos

---

## 🚫 O QUE NÃO FAZER

### ❌ Deploy scraping sem teste local
```bash
# NUNCA fazer isso para mudanças no scraper:
git commit -m "feat: modify scraper"
git push staging main  # ❌ SEM testar localmente primeiro

# Consequências:
# - Gasta tempo de build do Heroku (~1-2 min)
# - Polui logs de staging com erros evitáveis
# - Aumenta custos de infraestrutura
# - Feedback lento (minutos vs segundos)
```

### ❌ Deploy direto em produção
```bash
# NUNCA fazer isso sem testar em staging primeiro:
git push production main  # ❌ SEM validação em staging
```

### ❌ Deploy simultâneo
```bash
# NUNCA fazer isso:
git push staging main && git push production main  # ❌ Deploy em paralelo
```

### ❌ Pular testes em staging
```bash
# NUNCA fazer isso:
git push staging main
# ... sem executar curl tests ...
git push production main  # ❌ SEM validar DoD
```

### ❌ Testar com muitas páginas localmente
```bash
# EVITAR: Testes longos desnecessários
python run_scraper.py --pages 30  # ❌ 15 minutos localmente

# PREFERIR: Testes rápidos
python run_scraper.py --pages 2   # ✅ 2 minutos localmente
```

---

## ✅ Exemplo de Fluxo Correto

### Fluxo Completo (com Testes Locais)

```bash
# 0. Testar Localmente (OBRIGATÓRIO para scraping)
echo "🧪 Testing LOCALLY first..."
python run_scraper.py --pages 2 --format json --output test_local

# Validar resultado
python3 << EOF
import json
with open('data/output/test_local.json', 'r') as f:
    books = json.load(f)
    book = books[0]
    assert 'upc' in book, "UPC missing!"
    assert 'category' in book, "Category missing!"
    print(f"✅ Local test PASSED - {len(books)} books with all fields")
EOF

# 1. Commit
git add -A
git commit -m "feat: enhance scraper to extract UPC and category"
git push origin main

# 2. Deploy Staging
echo "🚀 Deploying to STAGING..."
git push staging main

# 3. Aguardar build
echo "⏳ Waiting for Heroku build..."
sleep 30

# 4. Testar em Staging
echo "🧪 Testing in STAGING..."
STAGING_URL="https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com"

# Login
curl -s "$STAGING_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' > /tmp/staging_token.json

TOKEN=$(cat /tmp/staging_token.json | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Testar endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_URL/api/v1/new-endpoint" -H "Authorization: Bearer $TOKEN")

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Staging tests PASSED"
else
  echo "❌ Staging tests FAILED - HTTP $HTTP_CODE"
  exit 1
fi

# 5. Deploy Production (somente se passou)
echo "🚀 Deploying to PRODUCTION..."
git push production main

# 6. Validação final
sleep 30
echo "🔍 Validating PRODUCTION..."
PROD_URL="https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com"
# ... repetir testes ...

echo "✅ DEPLOYMENT COMPLETE"
```

---

## 🔧 Scripts Auxiliares

### `scripts/deploy.sh`
Script automatizado que segue o workflow correto.

```bash
# Usage
./scripts/deploy.sh staging    # Deploy + test staging
./scripts/deploy.sh production # Deploy + test production (após staging)
```

### `scripts/test_env.sh`
Script para executar testes de validação.

```bash
# Usage
./scripts/test_env.sh staging    # Test staging
./scripts/test_env.sh production # Test production
```

---

## 📌 URLs de Referência

| Ambiente | URL | Git Remote |
|----------|-----|------------|
| **Staging** | https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com | `staging` |
| **Production** | https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com | `production` |

---

## 🎯 Lembretes Importantes

### 🏠 Teste localmente PRIMEIRO (scraping)

**Para mudanças no scraper, SEMPRE teste localmente antes de fazer deploy!**

Benefícios:
- ⚡ **Feedback instantâneo** (segundos)
- 💰 **Reduz custos** (menos builds em nuvem)
- 🐛 **Detecta bugs cedo** (desenvolvimento local)
- 🚀 **Aumenta produtividade** (iteração rápida)

### 🧪 NUNCA pule os testes em staging!

**Staging NÃO é opcional!**

Staging existe para:
- 🛡️ Proteger produção de bugs
- 🧪 Validar mudanças em ambiente real
- 📊 Verificar performance e comportamento
- 🔍 Detectar problemas antes dos usuários
- 🔐 Validar autenticação/autorização
- 🌐 Testar integrações reais

### 📊 Workflow em Resumo

```
🏠 LOCAL → 📦 GITHUB → 🧪 STAGING → ✅ DoD → 🚀 PRODUCTION
   ↑                        ↑               ↑
   |                        |               |
Testes rápidos       Testes reais    Validação final
(scraping)           (curl)          (smoke test)
```

---

_Última atualização: 2025-11-28_

