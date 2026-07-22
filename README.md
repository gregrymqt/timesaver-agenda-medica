# 🩺 TimeSaver - Sistema de Agenda Médica

Um sistema web moderno e robusto para visualização e gerenciamento de agendamentos médicos. O projeto possui autenticação de usuários com **Flask + SQLite**, dashboard dinâmico alimentado por **Tabulator.js**, e consumo de uma **API Mock** externa via **HTTPX (Async)**, totalmente containerizado com **Docker e Docker Compose**.

---

## ✨ Funcionalidades Principais

- **🔒 Autenticação e Segurança:** Tela de login protegida por sessão criptografada, suporte a senhas seguras (Pbkdf2:sha256) e middleware de proteção de rotas (`@login_required`).
- **📊 Dashboard Dinâmico:** Interface responsiva construída com **Bootstrap 5** e **Tabulator.js 5.5**, contando com:
  - Busca e filtragem global em tempo real (por Paciente, CPF ou Médico).
  - Ordenação por colunas e paginação de resultados.
  - Indicadores de status visuais (Confirmado, Pendente, Cancelado).
- **⚡ Arquitetura Assíncrona & Resiliente:** Comunicação assíncrona com a API externa usando `httpx.AsyncClient` com tratamento nativo de *timeouts*, falhas de rede e tratamento gracioso de erros (sem derrubar o frontend).
- **🐳 Multi-Stage Docker Builds:** Containers otimizados, seguros (executados como usuário `nonroot`) e orquestrados por servidor de produção **Gunicorn (gthread)**.

---

## 🛠️ Arquitetura e Tecnologias

A aplicação é organizada no modelo de microsserviços/serviços desacoplados orquestrados pelo Docker Compose:

```text
┌────────────────────────────────┐         ┌─────────────────────────────────┐
│     Aplicação Web (app)        │  HTTP   │       Mock API (mock_api)       │
│  Flask (Porta 5000)            │ ──────> │   Flask (Porta 5001)            │
│  - Auth & SQLite Database      │ (Async) │   - Fornece dados simulados     │
│  - Dashboard HTML/JS/Tabulator │         │     de agendamentos médicos     │
└────────────────────────────────┘         └─────────────────────────────────┘
```

### Tecnologias Utilizadas:

- **Backend:** Python 3.11+, Flask 3.0, Gunicorn (Worker `gthread`)
- **Cliente HTTP Assíncrono:** HTTPX (`httpx.AsyncClient`)
- **Banco de Dados:** SQLite (com gerenciamento de conexões por requisição)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Tabulator.js 5.5
- **Testes Automatizados:** Pytest, Pytest-Flask, Pytest-Asyncio
- **Containerização:** Docker (Multi-stage build), Docker Compose

---

## 📁 Estrutura do Projeto

```text
desafio_time_saver/
├── app/                        # Aplicação Web Principal
│   ├── database/               # Conexão SQLite e Seeds de dados iniciais
│   ├── repositories/           # Camada de acesso aos dados de usuários
│   ├── services/               # Serviços de Negócio e Consumo Assíncrono da API
│   ├── static/                 # Arquivos Estáticos (CSS, JavaScript)
│   ├── templates/              # Templates Jinja2 (HTML)
│   ├── main.py                 # Ponto de entrada do Flask App
│   └── Dockerfile              # Build da imagem da aplicação principal
├── mock_api/                   # Serviço Mock de Agendamentos
│   ├── app.py                  # API Mock com dados sintéticos
│   └── Dockerfile              # Build da imagem da API Mock
├── tests/                      # Testes Automatizados (Unitários e de Integração)
├── docker-compose.yml          # Orquestração dos Containers
├── requirements.txt            # Dependências Python do projeto
└── README.md                   # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto com Docker

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado.
- [Docker Compose](https://docs.docker.com/compose/) instalado.

### Passos para Inicialização

1. **Clone o repositório:**
   ```bash
   git clone [<URL_DO_SEU_REPOSITORIO>](https://github.com/gregrymqt/timesaver-agenda-medica)
   cd desafio_time_saver
   ```

2. **Suba os containers:**
   Execute o comando abaixo na raiz do projeto para construir e iniciar os serviços:
   ```bash
   docker-compose up --build -d
   ```
   *(Ou `docker compose up --build -d` para Docker V2)*

3. **Acesse no Navegador:**
   - **Dashboard Principal:** [http://localhost:5000](http://localhost:5000)
   - **API Mock Direct Healthcheck:** [http://localhost:5001/api/health](http://localhost:5001/api/health)

4. **Credenciais Padrão de Acesso:**
   - **E-mail:** `admin@timesaver.com`
   - **Senha:** `admin123`

---

## 🧪 Como Rodar os Testes Automatizados

A suíte de testes cobre a autenticação, integridade do banco SQLite, proteção de rotas e resiliência da integração HTTP.

### Executando dentro do Container Docker:

```bash
docker-compose exec web pytest
```

### Executando em Ambiente Local (Virtualenv):

```bash
# Ative seu ambiente virtual e instale as dependências
pip install -r requirements.txt

# Execute os testes especificando o PYTHONPATH
PYTHONPATH=".;app" pytest
```

---

## 🔌 Endpoints da Aplicação

### 🌐 Aplicação Principal (`http://localhost:5000`)
- `GET /` - Redireciona para `/dashboard` se autenticado, caso contrário para `/login`.
- `GET /login` & `POST /login` - Exibe e processa o formulário de login.
- `GET /logout` - Encerra a sessão do usuário.
- `GET /dashboard` - Interface gráfica do sistema (Protegida).
- `GET /api/agendamentos` - Endpoint interno (Protegido) que consome assincronamente a Mock API e fornece os dados formatados para o Tabulator.js.

### 🤖 Mock API (`http://localhost:5001`)
- `GET /api/agendamentos` - Retorna a lista de consultas médicas sintéticas em formato JSON.
- `GET /api/health` - Healthcheck do serviço da API Mock.
