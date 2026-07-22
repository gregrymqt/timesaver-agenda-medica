from database.db import get_db

class UserRepository:
    @staticmethod
    def find_by_email(email: str):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?',(email,))
        user = cursor.fetchone()
        
        return dict(user) if user else None
    
    
    @staticmethod
    def create_user(email: str, senha_hash: str, nome: str):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''
            INSERT INTO usuarios (email, senha_hash, nome)
            VALUES (?, ?, ?)
            ''', (email, senha_hash, nome)
        )
        db.commit()
        cursor.lastrowid
        