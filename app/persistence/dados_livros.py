# Camada de Persistência - Dados de Livros
# Responsabilidade: armazenar e recuperar livros. Nenhuma regra de negócio aqui.
# Optei por seguir o desenvolvimento de dentro para fora, conforme recomendação do professor.

livros = [
    {
        "id": 1,
        "titulo": "Harry Potter e a Pedra Filosofal",
        "autor": "J.K. Rowling",
        "editora": "Rocco",
        "estoque": {
            "Loja Centro": 3,
            "Loja Norte": 0,
            "Loja Sul": 5
        }
    },
    {
        "id": 2,
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "editora": "Martins Fontes",
        "estoque": {
            "Loja Centro": 2,
            "Loja Norte": 1,
            "Loja Sul": 0
        }
    },
    {
        "id": 3,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "editora": "Globo",
        "estoque": {
            "Loja Centro": 0,
            "Loja Norte": 4,
            "Loja Sul": 2
        }
    }
]


def listar_todos_livros():
    return livros

def buscar_livro_por_id(livro_id):
    for livro in livros:
        if livro["id"] == livro_id:
            return livro
    return None