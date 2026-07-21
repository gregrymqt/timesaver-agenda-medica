# 🩺 Agenda Médica — Processo Seletivo TimeSaver

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tabulator.js](https://img.shields.io/badge/Tabulator.js-5.5-Red?style=for-the-badge)](https://tabulator.info/)

Aplicação web completa para gestão e visualização de agenda médica, desenvolvida como solução ao teste técnico da **TimeSaver**. A solução conta com autenticação de usuários via SQLite, consumo de API remota de agendamentos com resiliência/fallback, interface interativa construída com Tabulator.js e ambiente totalmente containerizado via Docker Compose.

---

## 🏛️ Arquitetura e Estrutura do Projeto

O projeto adota uma estrutura modular e desacoplada, separando os serviços da aplicação principal (Flask Web App) e da API simulada de agendamentos (Mock API).

```text
agenda-medica-timesaver/
├── docker-compose.yml          # Orquestração dos serviços (App Web + Mock API)
├── .env.example                # Variáveis de ambiente de exemplo
├── README.md                   # Documentação do projeto
├── mock_api/                   # Serviço Mock da API de Agendamentos Médicos
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py                  # API REST com endpoints de consulta
└── app/                        # Aplicação Web Principal (Flask)
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py                 # Entrypoint e inicialização do Flask
    ├── database/
    │   ├── db.sqlite           # Banco de dados SQLite (auto-gerado)
    │   └── seed.py             # Script de migration e criação do usuário inicial
    ├── services/
    │   ├── auth_service.py     # Lógica de autenticação e verificação de hash
    │   └── agenda_service.py   # Consumo da API de agendamentos com resiliência
    ├── static/
    │   ├── css/style.css       # Estilização customizada e responsiva
    │   └── js/app.js           # Lógica do Tabulator.js, filtros e handlers
    ├── templates/
    │   ├── login.html          # Interface de autenticação
    │   └── index.html          # Dashboard e tabela da Agenda Médica
    └── tests/                  # Suíte de testes automatizados (Pytest)
        ├── test_auth.py
        └── test_agenda.py
```

---

## ⚡ Como Executar (Quick Start)

A aplicação foi projetada para execução simplificada com **um único comando**, sem necessidade de instalação local de dependências ou bancos de dados.

### Pré-requisitos
* [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/timesaver-agenda-medica.git
   cd timesaver-agenda-medica
   ```

2. **Suba o ambiente containerizado:**
   ```bash
   docker compose up --build
   ```

3. **Acesse a aplicação no navegador:**
   * **Aplicação Web:** `http://localhost:5000`
   * **Mock API de Agendamentos:** `http://localhost:5001/api/agendamentos`

---

## 🔐 Credenciais de Acesso (Ambiente de Teste)

Ao iniciar a aplicação pela primeira vez, o banco de dados SQLite é automaticamente inicializado e povoado com o usuário padrão de teste:

| Campo | Valor de Teste |
| :--- | :--- |
| **Usuário / E-mail** | `admin@timesaver.com` |
| **Senha** | `admin123` |

---

## 🧪 Executando os Testes Automatizados

Os testes automatizados cobrem os fluxos de autenticação, tratamento de falhas da API e renderização dos templates.

Para rodar a suíte de testes com `pytest` dentro do container:

```bash
docker compose exec web pytest -v
```

---

## 💡 Recursos e Boas Práticas Implementadas

* **Zero-Configuration DX:** Execução unificada com `docker compose up --build`.
* **Segurança na Autenticação:** Armazenamento seguro de senhas com hash (`werkzeug.security`).
* **Resiliência e Fallback:** Tratamento de *timeouts*, indisponibilidade de API ou dados malformatados com alertas visuais amigáveis no front-end.
* **Interface Dinâmica:** Tabela interativa via **Tabulator.js** com busca textual global (Paciente, CPF e Médico) e ordenação por colunas.
* **Isolamento de Ambientes:** Multi-stage Docker builds e rede privada no Docker Compose entre o Web App e a Mock API.

---

## 👤 Autor

Desenvolvido por **Lucas Vicente**  
* **LinkedIn:** [linkedin.com/in/lucasvicente](https://linkedin.com)  
* **GitHub:** [github.com/lucasvicente](https://github.com)
# timesaver-agenda-medica
