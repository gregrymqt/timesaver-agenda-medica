from app.services.auth_service import AuthService

def test_auth_service_sucesso(client):
    """Testa a autenticação com credenciais corretas do usuário admin."""
    user = AuthService.authenticate("admin@timesaver.com", "admin123")
    assert user is not None
    assert user['email'] == "admin@timesaver.com"
    assert user['nome'] == "Administrador TimeSaver"


def test_auth_service_senha_invalida(client):
    """Testa a autenticação com senha incorreta."""
    user = AuthService.authenticate("admin@timesaver.com", "senha_errada_123")
    assert user is None


def test_auth_service_usuario_inexistente(client):
    """Testa a autenticação com um e-mail não cadastrado."""
    user = AuthService.authenticate("naoexiste@timesaver.com", "admin123")
    assert user is None


def test_rota_login_get(client):
    """Garante que a página de login carrega com status HTTP 200 OK."""
    response = client.get('/login')
    assert response.status_code == 200


def test_rota_login_post_sucesso(client):
    """Testa o envio do formulário de login válido com redirecionamento (302) para o dashboard."""
    response = client.post('/login', data={
        'email': 'admin@timesaver.com',
        'senha': 'admin123'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers['Location'] == '/dashboard'


def test_rota_login_post_falha(client):
    """Testa o envio de login inválido (deve permanecer no login)."""
    response = client.post('/login', data={
        'email': 'admin@timesaver.com',
        'senha': 'senha_errada'
    })

    assert response.status_code == 200
    assert b"E-mail ou senha incorretos." in response.data


def test_protecao_rota_dashboard_sem_login(client):
    """Garante que usuários não autenticados são redirecionados para a tela de login."""
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']