import mip  
from leitura import retorna_conteudo_arquivo as rca # Função que retorna o conteúdo do arquivo de entrada

numvariaveis, numrestricoes, funcaoobjetivo, restricoes = rca()

# Crie um modelo de programação linear
def cria_modelo():
    m = mip.Model(sense=mip.MAXIMIZE) # MAXIMIZE ou MINIMIZE

    # Crie as variáveis de decisão
    x = [m.add_var(name='x{}'.format(i), var_type=mip.CONTINUOUS) for i in range(numvariaveis)]

    # Crie a função objetivo
    m.objective = mip.xsum(funcaoobjetivo[i] * x[i] for i in range(numvariaveis))

    # Crie as restrições
    for i in range(numrestricoes):
        m += mip.xsum(restricoes[i][j] * x[j] for j in range(numvariaveis)) <= restricoes[i][-1]
    return m

    

    
branchbound()
