# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o projeto Book Store!

## 🚀 Como Começar

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/giulianogimenez/FIAP-MLE-book-store.git
cd FIAP-MLE-book-store
```

### 2. Configure o Ambiente

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
pip install pytest black flake8  # Ferramentas de desenvolvimento
```

### 3. Crie uma Branch

```bash
git checkout -b feature/minha-nova-feature
# ou
git checkout -b fix/correcao-de-bug
```

## 📝 Padrões de Código

### Estilo Python

- Seguimos [PEP 8](https://pep8.org/)
- Usamos [Black](https://github.com/psf/black) para formatação
- Linha máxima de 100 caracteres

```bash
# Formatar código
black api scraper tests

# Verificar estilo
flake8 api scraper tests --max-line-length=100
```

### Documentação

- Docstrings em todas as funções e classes
- Comentários explicativos quando necessário
- README atualizado para novas features

```python
def minha_funcao(param1: str, param2: int) -> dict:
    """
    Breve descrição da função.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
        
    Returns:
        Descrição do retorno
    """
    pass
```

## 🧪 Testes

### Escrever Testes

- Teste toda nova funcionalidade
- Mantenha cobertura de testes > 80%
- Use nomes descritivos para testes

```python
def test_create_book_success():
    """Teste de criação de livro com dados válidos"""
    # Arrange
    book_data = {...}
    
    # Act
    result = create_book(book_data)
    
    # Assert
    assert result['status'] == 'success'
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=api --cov=scraper

# Testes específicos
pytest tests/test_api.py::test_create_book
```

## 📋 Tipos de Contribuição

### 🐛 Reportar Bugs

Ao reportar um bug, inclua:

1. Descrição clara do problema
2. Passos para reproduzir
3. Comportamento esperado vs. atual
4. Versão do Python e dependências
5. Logs de erro (se houver)

### ✨ Sugerir Features

Para sugerir novas funcionalidades:

1. Explique o problema que a feature resolve
2. Descreva a solução proposta
3. Considere alternativas
4. Adicione exemplos de uso

### 💻 Contribuir com Código

#### API REST

Adicionar novos endpoints:

```python
# Em api/routes.py
@api_bp.route('/nova-rota', methods=['GET'])
def nova_funcionalidade():
    """Documentação do endpoint"""
    pass

# Em api/controllers/
class NovoController:
    """Implementar lógica de negócio"""
    pass

# Em tests/test_api.py
def test_nova_funcionalidade():
    """Testar novo endpoint"""
    pass
```

#### Web Scraper

Criar novos scrapers:

```python
# Em scraper/
from scraper.base_scraper import BaseScraper

class MeuScraper(BaseScraper):
    def scrape(self, *args, **kwargs):
        """Implementar lógica de scraping"""
        pass
    
    def parse_item(self, element):
        """Parser de items"""
        pass

# Adicionar testes
def test_meu_scraper():
    """Testar novo scraper"""
    pass
```

## 🔄 Processo de Pull Request

### 1. Antes de Submeter

- [ ] Código segue padrões do projeto
- [ ] Testes passando (`pytest`)
- [ ] Código formatado (`black`)
- [ ] Sem erros de linting (`flake8`)
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado (se aplicável)

### 2. Commit Messages

Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário.

Closes #123
```

Tipos:
- `feat`: Nova feature
- `fix`: Correção de bug
- `docs`: Apenas documentação
- `style`: Formatação, sem mudança de código
- `refactor`: Refatoração de código
- `test`: Adicionar/modificar testes
- `chore`: Tarefas de manutenção

Exemplos:
```
feat(api): adicionar endpoint de busca de livros

Implementa busca de livros por título, autor e ISBN.
Inclui paginação e ordenação.

Closes #45
```

```
fix(scraper): corrigir parsing de preços

Preços com formato especial não eram processados corretamente.
Adiciona tratamento para múltiplos formatos de moeda.

Fixes #78
```

### 3. Criar Pull Request

1. Push sua branch
```bash
git push origin feature/minha-feature
```

2. Abra PR no GitHub
3. Preencha o template de PR
4. Aguarde review
5. Faça ajustes se solicitado
6. Aguarde merge

## 📚 Recursos Úteis

### Documentação
- [Flask](https://flask.palletsprojects.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://requests.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/docs/)

### Ferramentas
- [Black](https://black.readthedocs.io/)
- [Flake8](https://flake8.pycqa.org/)
- [Pytest](https://docs.pytest.org/)

## ❓ Dúvidas?

- Abra uma [Issue](https://github.com/FIAP/FIAP-MLE-book-store/issues)
- Entre em contato com os mantenedores
- Consulte a documentação existente

## 📜 Código de Conduta

- Seja respeitoso e profissional
- Aceite críticas construtivas
- Foque no melhor para o projeto
- Ajude outros contribuidores

---

**Obrigado por contribuir! 🎉**

