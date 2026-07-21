import sqlite3
import os
from flask import g

# Caminho do banco
DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite')

def get_db():
    """
    Retorna a conexão SQLite para a requisição atual.
    Se a conexão ainda não existir para esta requisição, abre uma nova.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        # Permite acessar colunas pelo nome (ex: user['email']) em vez de índice (user[0])
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Fecha a conexão do banco ao final de cada requisição HTTP."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Registra o hook de teardown no ciclo de vida do Flask."""
    app.teardown_appcontext(close_db)