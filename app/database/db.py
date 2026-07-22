import sqlite3
import os
from flask import g, current_app, Flask

def get_db():
    """
    Retorna a conexão SQLite para a requisição atual.
    Se a conexão ainda não existir para esta requisição, abre uma nova.
    Usa o caminho definido em app.config['DATABASE'].
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        # Permite acessar colunas pelo nome (ex: user['email']) em vez de índice (user[0])
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Fecha a conexão do banco ao final de cada requisição HTTP."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app: Flask):
    """Registra os hooks de gerenciamento do banco no ciclo de vida do Flask."""
    # Define o caminho padrão do banco se não estiver em modo de teste
    if not app.config.get('TESTING'):
        os.makedirs(app.instance_path, exist_ok=True)
        app.config.setdefault('DATABASE', os.path.join(app.instance_path, 'db.sqlite'))

    app.teardown_appcontext(close_db)