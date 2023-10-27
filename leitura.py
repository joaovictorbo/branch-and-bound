def retorna_conteudo_arquivo():
    with open('teste1.txt', 'r') as arquivo:
        conteudo_arquivo = arquivo.readlines()
        #divida as strings por espaço
        conteudo_arquivo = [x.split() for x in conteudo_arquivo]
        #transforme as strings em inteiros
        conteudo_arquivo = [[int(x) for x in y] for y in conteudo_arquivo]
        numvariaveis = conteudo_arquivo[0][0]
        numrestricoes = conteudo_arquivo[0][1]
        funcaoobjetivo = conteudo_arquivo[1]
        restricoes = conteudo_arquivo[2:]

        return numvariaveis, numrestricoes, funcaoobjetivo, restricoes
retorna_conteudo_arquivo()



