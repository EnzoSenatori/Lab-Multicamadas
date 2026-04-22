# Camada de Controllers - Requisições sobre Livros
# Responsabilidade: validar entrada, orquestrar Negócio, montar resposta.
# Só pode chamar a camada de Negócio (Model) --> atenção ao Import.

from app.models.livro_service import (
    buscar_livros_por_termo,
    obter_livro_por_id,
    obter_estoque,
    listar_unidades_disponiveis,
    calcular_total_estoque,
    classificar_disponibilidade,
)

def serializar_livro(livro):
    return {
        "id": livro["id"],
        "titulo": livro["titulo"],
        "autor": livro["autor"],
        "editora": livro["editora"],
        "total_estoque": calcular_total_estoque(livro),
        "badge": classificar_disponibilidade(livro),
        "unidades_disponiveis": listar_unidades_disponiveis(livro),
    }

def buscar_livros(termo):
    if not termo or termo.strip() == "": # verificação rápida
        return {"erro": "Digite um termo de busca."}, 400
    resultados = buscar_livros_por_termo(termo.strip())
    if resultados == "erro":
        return {"erro": "Digite um termo de busca."}, 400
    livros_serializados = []
    for livro in resultados:
        livros_serializados.append(serializar_livro(livro))
    resposta = {
        "termo": termo.strip(),
        "total": len(livros_serializados),
        "livros": livros_serializados,
    }
    return resposta, 200

def detalhar_livro(livro_id): # busca um livro específico por IP. Caso não encontre, retorna 404 Not Found.
    livro = obter_livro_por_id(livro_id)
    if livro is None:
        return {"erro": "Livro não encontrado."}, 404
    estoque = obter_estoque(livro)
    unidades = []
    for loja, quantidade in sorted(estoque.items(), key=lambda item: item[1], reverse=True):
        if quantidade > 0:
            unidades.append({"nome": loja, "quantidade": quantidade})
    resposta = {
        "livro": serializar_livro(livro),
        "unidades": unidades,
    }
    return resposta, 200