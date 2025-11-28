# 📊 Book Store API - Admin Dashboard

Dashboard interativo de monitoramento e métricas usando Streamlit, com acesso restrito a administradores.

## 🎯 Funcionalidades

### 🏥 Health & Status
- Status geral da API (healthy/degraded/unhealthy)
- Verificação de componentes (database, storage, config, dependencies)
- Métricas detalhadas de cada componente
- Timestamp de última verificação

### 📚 Books Analytics
- Total de livros no catálogo
- Preço médio dos livros
- Distribuição por categoria
- Gráficos de pizza (distribuição de categorias)
- Histograma de preços
- Tabela de categorias com contagem
- Lista de livros recentes

### 🕷️ Scraping Jobs Monitor
- Lista de todos os jobs de scraping
- Status de cada job (running/completed/failed)
- Métricas de jobs (total, em execução, concluídos, falhados)
- Gráfico de distribuição de status
- Interface para disparar novos jobs de scraping

### 🔐 Auth Metrics
- Informações da sessão atual
- Estatísticas de usuários
- Refresh de token
- Métricas de autenticação

### 📈 Real-time Monitor
- Status do sistema em tempo real
- Métricas atualizadas
- Timeline de atividade
- Auto-refresh configurável

## 🚀 Como Usar

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements-dashboard.txt
```

### Executar Localmente

```bash
# A partir da raiz do projeto
cd dashboard
streamlit run app.py
```

O dashboard estará disponível em: **http://localhost:8501**

### Login

1. Acesse o dashboard
2. Selecione o ambiente (Production/Staging/Local)
3. Use as credenciais de admin:
   - **Username**: `admin`
   - **Password**: `admin123`

> ⚠️ **Importante**: Apenas usuários com role `admin` podem acessar o dashboard.

## 🌐 Ambientes Disponíveis

| Ambiente | URL |
|----------|-----|
| **Production** | https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com |
| **Staging** | https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com |
| **Local** | http://localhost:5000 |

## 📁 Estrutura de Arquivos

```
dashboard/
├── app.py              # Aplicação Streamlit principal
├── auth.py             # Módulo de autenticação
├── api_client.py       # Cliente da API
├── README.md           # Esta documentação
└── requirements-dashboard.txt  # Dependências
```

## 🔧 Arquivos

### `app.py`
Aplicação principal do dashboard com todas as visualizações e funcionalidades.

**Componentes:**
- Autenticação obrigatória
- Seletor de ambiente
- 5 tabs principais (Health, Analytics, Scraping, Auth, Monitor)
- Auto-refresh opcional
- Gráficos interativos (Plotly)

### `auth.py`
Gerenciamento de autenticação.

**Funções:**
- `check_authentication()` - Verifica se usuário está autenticado
- `show_login_form()` - Exibe formulário de login
- `authenticate()` - Autentica usuário na API
- `logout()` - Faz logout e limpa sessão

### `api_client.py`
Cliente HTTP para interagir com a API.

**Métodos:**
- `get_health()` - Health check
- `get_books()` - Lista de livros
- `get_stats()` - Estatísticas
- `get_scraping_jobs()` - Jobs de scraping
- `trigger_scraping()` - Disparar novo job
- E mais...

## 🎨 Personalização

### Alterar Cores

Edite o CSS em `app.py`:

```python
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;  /* Cor do título */
    }
    .status-healthy {
        color: #28a745;  /* Verde */
    }
</style>
""", unsafe_allow_html=True)
```

### Adicionar Novas Métricas

1. Adicione método no `api_client.py` se necessário
2. Crie nova tab ou seção em `app.py`
3. Implemente visualização usando Streamlit/Plotly

## 📊 Gráficos Disponíveis

### Plotly Charts
- **Pie Chart**: Distribuição de categorias
- **Histogram**: Distribuição de preços
- **Bar Chart**: Status de jobs
- **Line Chart**: Timeline de atividade

### Métricas
- **st.metric()**: Cards de métricas
- **st.dataframe()**: Tabelas interativas
- **st.json()**: Visualização de JSON

## 🔒 Segurança

### Autenticação
- Login obrigatório com credenciais de admin
- Sessão gerenciada pelo Streamlit
- Token JWT armazenado em session_state
- Logout disponível a qualquer momento

### Restrições
- ✅ Apenas usuários com role `admin`
- ✅ Token JWT necessário para todas as chamadas
- ✅ Timeout de 10 segundos em requisições
- ✅ Validação de ambiente antes de conectar

## 🐛 Troubleshooting

### Dashboard não carrega
```bash
# Verificar se API está rodando
curl http://localhost:5000/health

# Verificar dependências
pip install -r requirements-dashboard.txt
```

### Erro de autenticação
- Verifique se a API está rodando
- Confirme as credenciais (admin/admin123)
- Verifique o ambiente selecionado
- Tente fazer login diretamente na API

### Erro ao disparar scraping
- Certifique-se de estar logado como admin
- Verifique se o token não expirou
- Confirme os parâmetros do scraping

### Gráficos não aparecem
```bash
# Reinstalar plotly
pip install --upgrade plotly
```

## 🚀 Deploy do Dashboard

### Streamlit Cloud

1. Crie conta em [share.streamlit.io](https://share.streamlit.io)
2. Conecte seu repositório GitHub
3. Selecione `dashboard/app.py` como main file
4. Configure secrets (se necessário)
5. Deploy!

### Heroku

```bash
# Criar Procfile na pasta dashboard/
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create fiap-bookstore-dashboard
git subtree push --prefix dashboard heroku main
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-dashboard.txt .
RUN pip install -r requirements-dashboard.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build e run
docker build -t bookstore-dashboard .
docker run -p 8501:8501 bookstore-dashboard
```

## 📝 Variáveis de Ambiente

Opcionais para configurar defaults:

```bash
# .env
DEFAULT_API_URL=https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com
DEFAULT_ENVIRONMENT=Production
STREAMLIT_SERVER_PORT=8501
```

## 🎯 Próximas Funcionalidades

- [ ] Alertas em tempo real
- [ ] Exportar relatórios em PDF
- [ ] Dashboard de logs
- [ ] Configurações de notificações
- [ ] Histórico de métricas (banco de dados)
- [ ] Múltiplos usuários admin
- [ ] Permissões granulares

## 📚 Recursos

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Requests Docs](https://docs.python-requests.org/)

---

**🎨 Desenvolvido com Streamlit | 📊 FIAP MLE Tech Challenge**

