import requests
import os

class AgendaService:
    def __int__(self):
        self.mock_api_url = os.environ.get(
                'MOCK_API_URL', 
                'http://mock-api:5001/api/agendamentos'
            )
        
    async def get_agendamentos(self):
        """
        Consome a API de agendamentos com tratamento de erros e timeout.
        Evita que falhas na API externa derrubem o front-end.
        """    
        
        try:
            
            response = await requests.get(self.mock_api_url, timeout=3.0)
            
            if response.status_code == 200:
                return{
                    "success":True,
                    "data": response.json(),
                    "error": None
                } 
                
            return {
                    "success": False, 
                    "data": [], 
                    "error": f"API de agendamentos respondeu com status {response.status_code}"
                }
        
        except requests.Exception.TimeoutError as e:
            return{
                "success":False,
                "data":[],
                "error": "Tempo limite excedido ao conectar à API de agendamentos (Timeout)."
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False, 
                "data": [], 
                "error": "Não foi possível conectar ao serviço de agendamentos."
            }
    