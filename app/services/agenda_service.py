import httpx
import os

class AgendaService:
    def __init__(self):
        self.mock_api_url = os.environ.get(
                'MOCK_API_URL',
                'http://mock-api:5001/api/agendamentos'
            )
        # Reutiliza o cliente HTTP para manter um pool de conexões, melhorando a performance.
        # Evita o custo de estabelecer uma nova conexão TCP/TLS para cada requisição.
        self._client = httpx.AsyncClient(timeout=3.0)

    async def get_agendamentos(self):
        """
        Consome a API de agendamentos com tratamento de erros e timeout.
        Evita que falhas na API externa derrubem o front-end.
        """
        try:
            response = await self._client.get(self.mock_api_url)
            response.raise_for_status()  # Lança exceção para status 4xx ou 5xx

            return {
                "success": True,
                "data": response.json(),
                "error": None
            }

        except httpx.TimeoutException as e:
            return {
                "success": False,
                "data": [],
                "error": "Tempo limite excedido ao conectar à API de agendamentos (Timeout)."
            }

        except httpx.RequestError as e:
            return {
                "success": False, 
                "data": [], 
                "error": f"Não foi possível conectar ao serviço de agendamentos: {e.__class__.__name__}"
            }