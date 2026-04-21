# O sufixo '_service' é uma  uma convenção comum em arquitetura multicamadas — módulos que contêm regras de negócio costumam se chamar "services"
# Camada de Negócio - Regras sobre Livros
# Responsabilidade: aplicar regras de domínio. Não conhece HTTP nem Flask.
# Só pode chamar a camada de Persistência.

from app.persistence.dados_livros import listar_todos_livros, buscar_livro_por_id

def buscar_livros_por_termo(termo):
    if termo == "":
        return "erro"
    resultados = []
    livros = listar_todos_livros()
    for livro in livros:
        titulo_contem = termo.lower() in livro["titulo"].lower()
        autor_contem = termo.lower() in livro["autor"].lower()
        editora_contem = termo.lower() in livro["editora"].lower()
        if titulo_contem or autor_contem or editora_contem: # Se alguma dessas "sentinelas" for True, é possível realizar o filtro.
            resultados.append(livro)
    return resultados

def obter_livro_por_id(livro_id):
    return buscar_livro_por_id(livro_id)

def obter_estoque(livro):
    return livro["estoque"]

def consultar_estoque_por_unidade(livro, unidade):
    estoque = obter_estoque(livro)
    return estoque.get(unidade, 0)

def listar_unidades_disponiveis(livro):
    unidades_com_estoque = []
    for loja, quantidade in livro["estoque"].items():
        if quantidade > 0:
            unidades_com_estoque.append((loja, quantidade))
    unidades_com_estoque.sort(key=lambda item: item[1], reverse=True) # ordena em ordem decrescente
    nomes_ordenados = []
    for loja, quantidade in unidades_com_estoque:
        nomes_ordenados.append(loja)
    return nomes_ordenados

def calcular_total_estoque(livro):
    estoque = obter_estoque(livro)
    return sum(estoque.values())

def classificar_disponibilidade(livro):
    total = calcular_total_estoque(livro)
    if total == 0:
        return "Indisponível"
    elif total <= 2:
        return "Estoque limitado"
    else:
        return "Em estoque"