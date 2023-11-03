from collections import deque
from mip import Model, xsum, maximize

def retorna_conteudo_arquivo():
    with open('teste1.txt', 'r') as arquivo:
        conteudo_arquivo = arquivo.readlines()
        conteudo_arquivo = [x.split() for x in conteudo_arquivo]
        conteudo_arquivo = [[int(x) for x in y] for y in conteudo_arquivo]
        numvariaveis = conteudo_arquivo[0][0]
        numrestricoes = conteudo_arquivo[0][1]
        funcaoobjetivo = conteudo_arquivo[1]
        restricoes = conteudo_arquivo[2:]

        return numvariaveis, numrestricoes, funcaoobjetivo, restricoes

def criar_modelo_mip(numvariaveis, numrestricoes, funcaoobjetivo, restricoes):
    m = Model()

    # Cria variáveis de decisão
    x = [m.add_var(name=f'x_{i}', var_type='I') for i in range(numvariaveis)]

    # Define a função objetivo
    m.objective = maximize(
        xsum(funcaoobjetivo[i] * x[i] for i in range(numvariaveis))
    )

    # Adiciona as restrições
    for i in range(numrestricoes):
        m += xsum(restricoes[i][j] * x[j] for j in range(numvariaveis)) <= restricoes[i][-1]

    return m, x

numvariaveis, numrestricoes, funcaoobjetivo, restricoes = retorna_conteudo_arquivo()
modelo_mip, x = criar_modelo_mip(numvariaveis, numrestricoes, funcaoobjetivo, restricoes)

def branch_and_bound(problema, x):
    fila = deque()
    fila.append(problema)
    melhor_solucao = float('-inf')

    while fila:
        prob_atual = fila.popleft()
        prob_atual.optimize(max_seconds=60)  # Defina o tempo limite desejado

        if prob_atual.objective_value <= melhor_solucao:
            continue

        mais_perto_meio = 1.0
        variavel_fracao = None
        for var in x:
            distancia_meio = abs(var.x - 0.5)
            if 0 < var.x < 1 and distancia_meio < mais_perto_meio:
                variavel_fracao = var
                mais_perto_meio = distancia_meio

        if variavel_fracao is None:
            if prob_atual.objective_value > melhor_solucao:
                melhor_solucao = prob_atual.objective_value
            continue

        pro_zero = prob_atual.copy()
        prob_um = prob_atual.copy()

        pro_zero += variavel_fracao == 0  # Adiciona a restrição xj = 0
        prob_um += variavel_fracao == 1  # Adiciona a restrição xj = 1

        fila.append(pro_zero)
        fila.append(prob_um)

    return melhor_solucao

# Exemplo de uso:
solucao = branch_and_bound(modelo_mip, x)
print("Melhor solução encontrada:", solucao)
#print o valor de cada variavel na solução otima
for var in x:
    print(var.name, '=', var.x)
    