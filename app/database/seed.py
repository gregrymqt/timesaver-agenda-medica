import sqlite3
import os
from app.database.db import get_db
from werkzeug.security import generate_password_hash

class DBInit():
    @staticmethod
    def init_db():
        """Cria as tabelas e popula o usuário inicial caso o banco não exista."""
        # Conecta ao banco (o SQLite cria o arquivo .sqlite automaticamente se não existir)
        conn = get_db()
        cursor = conn.cursor()

        # 1. Criação da Tabela de Usuários para a Tela de Login
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                nome TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Verifica se já existe algum usuário cadastrado
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        total_usuarios = cursor.fetchone()[0]

        # 3. Se a tabela estiver vazia, insere o usuário padrão de teste
        if total_usuarios == 0:
            email_admin = "admin@timesaver.com"
            senha_admin = "admin123"
            
            # Gera o hash seguro da senha
            senha_hash = generate_password_hash(senha_admin)

            cursor.execute('''
                INSERT INTO usuarios (email, senha_hash, nome)
                VALUES (?, ?, ?)
            ''', (email_admin, senha_hash, "Administrador TimeSaver"))

            conn.commit()
            print(f"✅ Banco de dados inicializado com sucesso! Usuário criado: {email_admin}")
        else:
            print("ℹ️ Banco de dados já inicializado.")

    if __name__ == '__main__':
        init_db()