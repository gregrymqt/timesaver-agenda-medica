import pytest
import os
import tempfile
from app.main import app as flask_app
from app.database.seed import DBInit

@pytest.fixture
def client():
    """
    Fixture que configura o ambiente de testes do Flask e injeta
    um banco SQLite temporário isolado.
    """
    # Cria um arquivo temporário no sistema para o banco de dados de teste
    db_fd, db_path = tempfile.mkstemp()
    
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key-123',
        'DATABASE': db_path, # Aponta o app para o banco de dados de teste
    })

    # Sobrescreve o caminho do banco para o arquivo temporário durante os testes
    with flask_app.app_context():
        DBInit.init_db()
        yield flask_app.test_client()

    # Limpeza (Teardown): Fecha e remove o banco temporário após rodar os testes
    os.close(db_fd)
    os.unlink(db_path)