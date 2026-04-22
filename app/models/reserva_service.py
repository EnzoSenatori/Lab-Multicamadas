# o sufixo '_service' é uma  uma convenção comum em arquitetura multicamadas — módulos que contêm regras de negócio costumam se chamar "services"
# Camada de Negócio - Regras sobre Reservas
# Responsabilidade: aplicar regras de domínio. Não conhece HTTP nem Flask.
# Só pode chamar a camada de Persistência, a camada adjacente.

# imports organizados conforme convenção PEP 8 - não sabia que tinha isso.
import io
import base64
from datetime import date

import qrcode # biblioteca externa -> instalar via pip

from app.persistence.dados_reservas import adicionar_reserva, listar_todas_reservas

def gerar_conteudo_qr_code(livro_id, unidade):
    unidade_formatada = unidade.replace(" ", "").upper()
    return f"RESERVA-{livro_id}-{unidade_formatada}"

def gerar_imagem_qr_code(conteudo): # feature nova -> vai gerar um QR Code por reserva.
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(conteudo)
    qr.make(fit=True)
    imagem = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO() # cria um arquivo em memória. Assim, a imagem é salva nele em vez de no disco.
    imagem.save(buffer, format="PNG")
    bytes_png = buffer.getvalue()
    base64_str = base64.b64encode(bytes_png).decode("utf-8") # bytes convertidos para texto Base64
    return f"data:image/png;base64,{base64_str}"

def criar_reserva(livro, unidade, usuario=None, data=None):
    if data is not None and data != "":
        data_reserva = date.fromisoformat(data)
        data_hoje = date.today()
        if data_reserva < data_hoje:
            raise ValueError("A data da reserva não pode ser anterior à data atual.")
    conteudo_qr = gerar_conteudo_qr_code(livro["id"], unidade)
    imagem_qr = gerar_imagem_qr_code(conteudo_qr)
    reserva = {
        "livro_id": livro["id"],
        "unidade": unidade,
        "status": "reservado",
        "usuario": usuario,
        "data": data,
        "qr_code": conteudo_qr,
        "qr_code_imagem": imagem_qr,
    }
    adicionar_reserva(reserva)
    return reserva

def listar_reservas():
    return listar_todas_reservas()

def unidade_tem_estoque(livro, unidade):
    estoque = livro["estoque"]
    quantidade = estoque.get(unidade, 0)
    return quantidade > 0