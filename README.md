# TimeSaver - Sistema de Agenda Médica

Um sistema web para visualização de agendamentos médicos, construído com Flask e containerizado com Docker. A aplicação possui autenticação de usuário e um dashboard dinâmico que consome dados de uma API mock.

## ✨ Funcionalidades

- **Autenticação Segura:** Tela de login para proteger o acesso ao sistema.
- **Dashboard Dinâmico:** Interface principal que exibe os agendamentos em uma tabela interativa (usando Tabulator.js).
- **Arquitetura de Microsserviços:** A aplicação principal consome dados de um serviço de API mock separado, simulando um ambiente distribuído.
- **Ambiente Containerizado:** Totalmente configurado com Docker e Docker Compose para um setup de desenvolvimento e produção simplificado.

## 🛠️ Arquitetura e Tecnologias

O projeto é orquestrado pelo Docker Compose e dividido em dois serviços principais:

- `web`: A aplicação Flask principal que serve o frontend, a autenticação e um endpoint de API seguro. Utiliza **Gunicorn** como servidor WSGI para produção.
- `mock-api`: Um serviço Flask secundário que simula uma API externa, fornecendo os dados dos agendamentos.

**Tecnologias Utilizadas:**

- **Backend:** Python, Flask, Gunicorn
- **Comunicação HTTP:** Httpx (cliente assíncrono)
- **Frontend:** HTML, JavaScript, Tabulator.js
- **Database:** SQLite (para autenticação de usuários)
- **Testes:** Pytest
- **Containerização:** Docker, Docker Compose

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Docker
- Docker Compose

### Passos para Instalação

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DA_PASTA>
   ```

2. **Inicie os containers:**
   Execute o comando a seguir na raiz do projeto para construir as imagens e iniciar os serviços em background.
   ```bash
   docker-compose up --build -d
   ```

3. **Acesse a aplicação:**
   A aplicação estará disponível no seu navegador no endereço:
   - **URL:** http://localhost:5000

   **Credenciais de Acesso Padrão:**
   - **Email:** `admin@timesaver.com`
   - **Senha:** `admin123`

## 🧪 Como Rodar os Testes

Os testes automatizados foram escritos com Pytest e podem ser executados dentro do container da aplicação para garantir um ambiente consistente.

1. Certifique-se de que os containers estão em execução (`docker-compose up -d`).
2. Execute o comando abaixo para rodar a suíte de testes:
   ```bash
   docker-compose exec timesaver_web_app pytest
   ```