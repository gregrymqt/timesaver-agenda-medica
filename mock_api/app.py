import os
from flask import Flask, jsonify
from flask_cors import CORS

MOCK_DATA = [
    {"id": 1, "paciente": "Carlos Silva", "cpf": "111.222.333-44", "medico": "Dr. House", "especialidade": "Clínico Geral", "data_hora": "2026-08-10 14:30", "status": "Confirmado"},
    {"id": 2, "paciente": "Maria Oliveira", "cpf": "222.333.444-55", "medico": "Dra. Grey", "especialidade": "Cardiologia", "data_hora": "2026-08-10 15:00", "status": "Pendente"},
    {"id": 3, "paciente": "João Pereira", "cpf": "333.444.555-66", "medico": "Dr. Shepherd", "especialidade": "Neurologia", "data_hora": "2026-08-11 09:00", "status": "Cancelado"},
    {"id": 4, "paciente": "Ana Souza", "cpf": "444.555.666-77", "medico": "Dr. House", "especialidade": "Clínico Geral", "data_hora": "2026-08-11 10:30", "status": "Confirmado"},
    {"id": 5, "paciente": "Lucas Martins", "cpf": "555.666.777-88", "medico": "Dra. Yang", "especialidade": "Cirurgia", "data_hora": "2026-08-12 11:00", "status": "Confirmado"},
]

app = Flask(__name__)
CORS(app)

@app.route('/api/agendamentos', methods=['GET'])
def get_agendamentos():
    return  jsonify(MOCK_DATA), 200 

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status":"healthy", "service":"Mock API"}),200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)