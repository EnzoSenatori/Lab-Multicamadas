# App Factory -> Cria e configura a instância Flask, registrando todos os Blueprints de Rotas.

from flask import Flask

from app.routes.livro_routes import livro_routes
from app.routes.reserva_routes import reserva_routes

def create_app():
    livraria_app = Flask(__name__, static_folder="../frontend", static_url_path="")
    livraria_app.register_blueprint(livro_routes)
    livraria_app.register_blueprint(reserva_routes)

    @livraria_app.get("/")
    def servir_index():
        return livraria_app.send_static_file("index.html")

    return livraria_app