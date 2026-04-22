# Ponto de entrada da aplicação
# Responsabilidade: instanciar a aplicação via factory e iniciar o servidor.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)