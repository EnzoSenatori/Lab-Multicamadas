# Camada de Rotas - Endpoints de Reservas
# Responsabilidade: mapear URL/método HTTP para funções do Controller.

from flask import Blueprint, request, jsonify

from app.controllers.reserva_controller import reservar

reserva_routes = Blueprint("reserva_routes", __name__) # BluePrint é ideal para caso o projeto cresça

@reserva_routes.post("/api/reservas")
def rota_reservar(): # deixei "rota_ [...]" para facilitar depuração em caso de erros --> deixa explícito que a função só existe na camada de rotas
    dados = request.get_json(silent=True) or {}
    resposta, status = reservar(dados)
    return jsonify(resposta), status