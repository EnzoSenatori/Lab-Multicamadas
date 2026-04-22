# Camada de Rotas - Endpoints de Livros
# Responsabilidade: mapear URL/método HTTP para funções do Controller.
# Converte dados da requisição HTTP em argumentos Python, e a resposta do Controller em resposta HTTP.

from flask import Blueprint, request, jsonify

from app.controllers.livro_controller import buscar_livros, detalhar_livro

livro_routes = Blueprint("livro_routes", __name__)

@livro_routes.get("/api/livros")
def rota_buscar_livros(): # função que o Flask vai chamar quando chegar um GET /api/livros
    termo = request.args.get("termo", "")
    resposta, status = buscar_livros(termo) # lembrar de como os dados estão sendo tratados em controller
    return jsonify(resposta), status

@livro_routes.get("/api/livros/<int:livro_id>")
def rota_detalhar_livro(livro_id):
    resposta, status = detalhar_livro(livro_id)
    return jsonify(resposta), status