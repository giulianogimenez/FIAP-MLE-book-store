# 🚀 Deploy Workflow - Staging → Production

## Workflow Canônico

Este documento define o processo obrigatório para deploy de todas as mudanças.

### 📋 Checklist de Deploy

#### 1️⃣ Desenvolvimento
- [ ] Implementar mudanças localmente
- [ ] Testar localmente (se aplicável)
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

### ❌ Pular testes
```bash
# NUNCA fazer isso:
git push staging main
# ... sem executar curl tests ...
git push production main  # ❌ SEM validar DoD
```

---

## ✅ Exemplo de Fluxo Correto

```bash
# 1. Commit
git add -A
git commit -m "feat: add new endpoint"
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

## 🎯 Lembrete

**NUNCA pule os testes em staging!**

Staging existe para:
- 🛡️ Proteger produção de bugs
- 🧪 Validar mudanças em ambiente real
- 📊 Verificar performance e comportamento
- 🔍 Detectar problemas antes dos usuários

---

_Última atualização: 2025-11-28_

