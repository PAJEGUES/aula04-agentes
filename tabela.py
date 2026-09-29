# Arquivo: tabela.py
import math

BITS_POR_PERCEPCAO = 10
PERCEPCOES_POR_SEGUNDO = 1
DURACAO_SEGUNDOS = 60 * 60  # uma hora

percepcoes_possiveis = 2 ** BITS_POR_PERCEPCAO     # |P| = 1024
T = PERCEPCOES_POR_SEGUNDO * DURACAO_SEGUNDOS      # T = 3600 percepções

# A tabela precisa de uma linha para cada sequência possível de percepções de tamanho 1 até T:
# soma de |P|^t para t = 1 .. T. O último termo domina, então a soma é praticamente |P|^T.
expoente_base10 = T * math.log10(percepcoes_possiveis)

print(f'Percepções diferentes por segundo: 2^{BITS_POR_PERCEPCAO} = {percepcoes_possiveis}')
print(f'Número de percepções em uma hora: T = {T}')
print(f'Entradas da tabela ~ {percepcoes_possiveis}^{T} = 2^{BITS_POR_PERCEPCAO * T}')
print(f'Ordem de grandeza: 10^{expoente_base10:.0f}')
print('Comparação: átomos no universo observável ~ 10^80')
