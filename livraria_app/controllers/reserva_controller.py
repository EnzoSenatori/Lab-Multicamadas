# Camada de Controllers - Requisições sobre Reservas
# Responsabilidade: validar entrada, orquestrar Negócio, montar resposta.
# Só pode chamar a camada de Negócio (Model) --> Atenção aos imports.

from livraria_app.models.livro_service import obter_livro_por_id
from livraria_app.models.reserva_service import criar_reserva, unidade_tem_estoque

def reservar(dados):
    livro_id_bruto = dados.get("livro_id")
    unidade = (dados.get("unidade") or "").strip()
    usuario = (dados.get("usuario") or "").strip() or None
    data = (dados.get("data") or "").strip() or None

    if livro_id_bruto is None or unidade == "":
        return {"erro": "Informe livro_id e unidade."}, 400
    try:
        livro_id = int(livro_id_bruto)
    except (TypeError, ValueError):
        return {"erro": "livro_id inválido."}, 400

    livro = obter_livro_por_id(livro_id)
    if livro is None:
        return {"erro": "Livro não encontrado."}, 404
    if not unidade_tem_estoque(livro, unidade): # controller não sabe o que esta regra significa, apenas pergunta para o model; se por ventura mudar, não é necessário alterar a lógica.
        return {"erro": "Unidade sem estoque disponível."}, 400

    reserva = criar_reserva(livro, unidade, usuario=usuario, data=data)
    resposta = {"reserva": reserva}
    return resposta, 201