import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

from database.db import init_app as init_db_app
from database.seed import DBInit
from services.auth_service import AuthService
from services.agenda_service import AgendaService

# 1. Inicializa a aplicação Flask
app = Flask(__name__)

# Chave secreta para criptografia de cookies de sessão
app.secret_key = os.environ.get('SECRET_KEY', 'timesaver-secret-key-2026')

# Registra o hook de fechamento automático do banco SQLite
init_db_app(app)

# Executa a migration/seed do banco na inicialização da aplicação
with app.app_context():
    DBInit.init_db()

# Instância do serviço que consome a API mock de agendamentos
agenda_service = AgendaService()


# 2. Decorator Middleware para Proteção de Rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Sessão expirada ou não encontrada. Faça login para continuar.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# 3. Definição das Rotas do Sistema

@app.route('/')
def index():
    """Rota raiz: redireciona para o dashboard se logado, senão para o login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tela de Login e processamento do formulário de autenticação."""
    # Se já estiver logado, redireciona direto pro dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    error = None

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()

        if not email or not senha:
            error = "Por favor, preencha todos os campos."
        else:
            # Chama o serviço de autenticação
            user = AuthService.authenticate(email, senha)
            
            if user:
                # Salva dados essenciais na sessão criptografada
                session['user_id'] = user['id']
                session['user_nome'] = user['nome']
                session['user_email'] = user['email']
                return redirect(url_for('dashboard'))
            else:
                error = "E-mail ou senha incorretos."

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Encerra a sessão do usuário e limpa os cookies."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Interface principal da Agenda Médica (Dashboard)."""
    return render_template('index.html', user_nome=session.get('user_nome', 'Usuário'))


@app.route('/api/agendamentos', methods=['GET'])
@login_required
async def api_agenda():
    """
    Endpoint interno consumido pelo Tabulator.js via Front-end.
    Retorna a lista de agendamentos consumida da Mock API.
    """
    result = await agenda_service.get_agendamentos()
    
    if result['success']:
        return jsonify({
            "status": "success",
            "data": result['data']
        }), 200
    else:
        # Se a API externa falhar, retorna o erro tratado com status 502 (Bad Gateway)
        return jsonify({
            "status": "error",
            "message": result['error'],
            "data": []
        }), 502


# 4. Inicialização do Servidor Web
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)