# Arquivo: aspirador.py
# Estado do mundo: (posição do aspirador, sujeira em A, sujeira em B)

ACOES = ['Esquerda', 'Direita', 'Aspirar']

def resultado(estado, acao):
    """Modelo de transição: devolve o estado que resulta de executar a ação."""
    local, sujo_a, sujo_b = estado
    if acao == 'Esquerda':
        return ('A', sujo_a, sujo_b)
    if acao == 'Direita':
        return ('B', sujo_a, sujo_b)
    if acao == 'Aspirar':
        if local == 'A':
            return ('A', False, sujo_b)
        return ('B', sujo_a, False)
    return estado

def atualizar_estado(estado, percepcao):
    """Junta o que o agente já sabia com a percepção atual (local, situação)."""
    local, situacao = percepcao
    _, sujo_a, sujo_b = estado
    if local == 'A':
        sujo_a = (situacao == 'Sujo')
    else:
        sujo_b = (situacao == 'Sujo')
    return (local, sujo_a, sujo_b)


# Agente baseado em objetivos

def objetivo_atingido(estado):
    """Teste de objetivo: os dois quadrados limpos."""
    return not estado[1] and not estado[2]

def buscar_plano(estado):
    """Busca em largura por uma sequência de ações que leva ao objetivo."""
    fronteira = [(estado, [])]
    visitados = set()
    while fronteira:
        atual, plano = fronteira.pop(0)
        if objetivo_atingido(atual):
            return plano
        if atual not in visitados:
            visitados.add(atual)
            for acao in ACOES:
                fronteira.append((resultado(atual, acao), plano + [acao]))
    return []

class AgenteObjetivo:
    def __init__(self):
        # No início ele não sabe nada do outro quadrado, então assume que pode estar sujo
        self.estado = ('A', True, True)
        self.plano = []

    def agir(self, percepcao):
        self.estado = atualizar_estado(self.estado, percepcao)
        if objetivo_atingido(self.estado):
            return 'NoOp'
        if not self.plano:
            self.plano = buscar_plano(self.estado)
        acao = self.plano.pop(0)
        self.estado = resultado(self.estado, acao)  # atualiza o modelo com o efeito esperado
        return acao


# Agente baseado em utilidade

PREMIO_LIMPO = 10     # cada quadrado limpo vale pontos a cada passo
CUSTO_MOVER = 1       # cada movimento gasta energia
CUSTO_ASPIRAR = 0.5   # ligar o aspirador também gasta energia
HORIZONTE = 2         # quantos passos à frente o agente olha

def utilidade(estado, acao):
    """Mede o quão bom é o estado: pontos por quadrado limpo menos a energia gasta na ação."""
    _, sujo_a, sujo_b = estado
    pontos = PREMIO_LIMPO * ((not sujo_a) + (not sujo_b))
    if acao in ('Esquerda', 'Direita'):
        pontos -= CUSTO_MOVER
    elif acao == 'Aspirar':
        pontos -= CUSTO_ASPIRAR
    return pontos

def valor(estado, acao, profundidade):
    """Utilidade de executar a ação e depois continuar escolhendo as melhores ações."""
    proximo = resultado(estado, acao)
    total = utilidade(proximo, acao)
    if profundidade > 1:
        total += max(valor(proximo, a, profundidade - 1) for a in ACOES + ['NoOp'])
    return total

class AgenteUtilidade:
    def __init__(self):
        self.estado = ('A', True, True)

    def agir(self, percepcao):
        self.estado = atualizar_estado(self.estado, percepcao)
        opcoes = ACOES + ['NoOp']
        acao = max(opcoes, key=lambda a: valor(self.estado, a, HORIZONTE))
        self.estado = resultado(self.estado, acao)
        return acao


# Simulação

def simular(agente, mundo, passos=6):
    """mundo = {'local': 'A', 'A': 'Sujo', 'B': 'Sujo'}"""
    for passo in range(1, passos + 1):
        percepcao = (mundo['local'], mundo[mundo['local']])
        acao = agente.agir(percepcao)
        if acao == 'Aspirar':
            mundo[mundo['local']] = 'Limpo'
        elif acao == 'Esquerda':
            mundo['local'] = 'A'
        elif acao == 'Direita':
            mundo['local'] = 'B'
        print(f'passo {passo}: percepção={percepcao} -> ação={acao:8} | mundo={mundo}')

if __name__ == '__main__':
    print('\nAgente baseado em OBJETIVOS:')
    simular(AgenteObjetivo(), {'local': 'A', 'A': 'Sujo', 'B': 'Sujo'})

    print('\nAgente baseado em UTILIDADE:')
    simular(AgenteUtilidade(), {'local': 'A', 'A': 'Sujo', 'B': 'Sujo'})
