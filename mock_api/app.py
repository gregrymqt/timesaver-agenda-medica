from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

AGENDAMENTOS_MOCK = [
    {
        "id": 1,
        "paciente": "Ana Silva",
        "cpf": "123.456.789-00",
        "medico": "Dr. Carlos Eduardo",
        "especialidade": "Cardiologia",
        "data_hora": "2026-07-25 09:00",
        "status": "Confirmado"
    },
    {
        "id": 2,
        "paciente": "Bruno Costa",
        "cpf": "987.654.321-11",
        "medico": "Dra. Juliana Mendes",
        "especialidade": "Dermatologia",
        "data_hora": "2026-07-25 10:30",
        "status": "Pendente"
    },
    {
        "id": 3,
        "paciente": "Carla Souza",
        "cpf": "456.789.123-22",
        "medico": "Dr. Carlos Eduardo",
        "especialidade": "Cardiologia",
        "data_hora": "2026-07-25 14:00",
        "status": "Cancelado"
    }
]

@app.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    return jsonify(AGENDAMENTOS_MOCK), 200 

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status":"healthy", "service":"Mock API"}),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)