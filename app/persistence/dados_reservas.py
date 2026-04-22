# Camada de Persistência - Dados de Reservas
# Responsabilidade: armazenar e recuperar reservas. Nenhuma regra de negócio aqui também.
# A Persistência só "coloca na gaveta" o que chegou pronto. Reitero: não há regras de negócio em persistência.

reservas = []
def adicionar_reserva(reserva):
    reservas.append(reserva)
    return reserva

def listar_todas_reservas():
    return reservas