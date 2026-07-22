from werkzeug.security import check_password_hash
from repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def authenticate(email: str, senha: str):
        """
        Valida o e-mail e a senha digitada pelo usuário.
        Retorna o dicionário do usuário se válido ou None se inválido.
        """
        
        user = UserRepository.find_by_email(email)
        if not user:
            return None
        
        if check_password_hash(user['senha_hash'], senha):
            return user
        
        return None