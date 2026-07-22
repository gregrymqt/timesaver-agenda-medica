import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from app.services.agenda_service import AgendaService

pytestmark = pytest.mark.asyncio


async def test_agenda_service_sucesso():
    """Simula resposta de sucesso (200 OK) da API externa de agendamentos."""
    mock_data = [
        {"id": 1, "paciente": "Paciente Teste", "medico": "Dr. House"}
    ]

    # Mock da resposta da API
    mock_response = MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status.return_value = None

    # Mock do cliente HTTP assíncrono
    async_client_mock = AsyncMock()
    async_client_mock.get.return_value = mock_response

    with patch('httpx.AsyncClient', return_value=async_client_mock):
        service = AgendaService()
        result = await service.get_agendamentos()

        assert result['success'] is True
        assert len(result['data']) == 1
        assert result['data'][0]['paciente'] == "Paciente Teste"


async def test_agenda_service_timeout():
    """Simula exceção de Timeout ao tentar conectar à API externa."""
    async_client_mock = AsyncMock()
    async_client_mock.get.side_effect = httpx.TimeoutException("Timeout error")

    with patch('httpx.AsyncClient', return_value=async_client_mock):
        service = AgendaService()
        result = await service.get_agendamentos()

        assert result['success'] is False
        assert result['data'] == []
        assert "Timeout" in result['error']


async def test_agenda_service_erro_conexao():
    """Simula falha genérica de conexão HTTP com a API externa."""
    async_client_mock = AsyncMock()
    async_client_mock.get.side_effect = httpx.RequestError("Connection error")

    with patch('httpx.AsyncClient', return_value=async_client_mock):
        service = AgendaService()
        result = await service.get_agendamentos()

        assert result['success'] is False
        assert result['data'] == []
        assert "Não foi possível conectar" in result['error']

def test_endpoint_api_agenda_protegido(client):
    """Garante que a rota interna `/api/agendamentos` exige autenticação prévia."""
    response = client.get('/api/agendamentos')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']