from database.db import get_db
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

        # 2. Insere o usuário padrão de forma atômica e segura para múltiplos processos.
        # O 'INSERT OR IGNORE' tenta inserir, mas não faz nada (e não gera erro)
        # se um registro com o mesmo 'email' (UNIQUE) já existir.
        email_admin = "admin@timesaver.com"
        senha_admin = "admin123"
        senha_hash = generate_password_hash(senha_admin)

        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (email, senha_hash, nome)
            VALUES (?, ?, ?)
        ''', (email_admin, senha_hash, "Administrador TimeSaver"))

        conn.commit()

        # A propriedade 'rowcount' do cursor nos diz se a última operação afetou alguma linha.
        # Se for > 0, a inserção ocorreu. Se for 0, o usuário já existia.
        if cursor.rowcount > 0:
            print(f"✅ Banco de dados inicializado e usuário padrão criado: {email_admin}")
        else:
            print("ℹ️ Banco de dados já inicializado.")