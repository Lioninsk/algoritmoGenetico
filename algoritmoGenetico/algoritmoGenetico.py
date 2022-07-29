from random import randint
import colors

class AlgoritmoGenetico:
    # inicialização dos parametros
    def __init__(self, tamPopulacao, taxaMutacao, taxaCrossOver, numGeracoes) -> None:
        self.tamPopulacao = tamPopulacao
        self.taxaMutacao = taxaMutacao
        self.taxaCrossOver = taxaCrossOver
        self.numGeracoes = numGeracoes
        self.numGenes = 3
        self.maxMinMutacao = 50
        self.gerarPopulacao()


    def gerarPopulacao(self) -> None:
        # cria um vetor para cada besouro
        self.populacao = [[] for i in range(self.tamPopulacao)]
        # define os RGB's aleatorios para cada besouro
        for cromossomo in self.populacao:
            r,g,b = randint(0,255),randint(0,255),randint(0,255)
            cromossomo.append(r)
            cromossomo.append(g)
            cromossomo.append(b)
    


    def funcaoObjetivo(self, cromossomo) -> float:
        valor = 0
        for gene in cromossomo:
            # equação especifica da função fitness, dá valores maiores para besouros mais escuros com RGB proximos a 0 
            valor += (gene - 255) / -255
            # caso fosse besouros brancos seria:
            # valor += gene / 255 brancos
        return round(valor/3,2)


    
    def avaliarPopulacao(self) -> None:
        self.avaliacao = []
        for cromossomo in self.populacao:
            self.avaliacao.append(self.funcaoObjetivo(cromossomo))
    

# Seleção por torneio
    def selecionar(self) -> int:
        # Condensa a informação do besouro e sua fitness em uma lista
        participantesTorneio = list(zip(self.populacao, self.avaliacao))
        # escolhe os indices dos besouros sorteados
        indexEscolhido1 = randint(0,self.tamPopulacao-1)
        indexEscolhido2 = randint(0,self.tamPopulacao-1)
        # garante que o mesmo besouro não seja o mesmo escolhido
        while indexEscolhido2 == indexEscolhido1:
            indexEscolhido2 = randint(0,self.tamPopulacao-1)
        cromossomo1 = participantesTorneio[indexEscolhido1]
        cromossomo2 = participantesTorneio[indexEscolhido2]
        # retorna o indice do mais adaptado verificando o fitness
        return indexEscolhido1 if cromossomo1[1] >= cromossomo2[1] else indexEscolhido2
    
    def selecionarPais(self) -> (list):
        pai = self.selecionar()
        mae = self.selecionar()
        # garante que a mãe e o pai não sejam os mesmos besouros.
        while(mae == pai):
            mae = self.selecionar()
        return (self.populacao[pai], self.populacao[mae])




#   Cruzamento de um ponto
    def cruzamento(self, pai, mae) -> (list):
        # Se a taxa de cruzamento for maior ou igual ao valor aleatorio realiza reprodução
        if randint(1,100) <= self.taxaCrossOver:
            pontoDeCorte = randint(1, self.numGenes-1)
            filho1 = pai[:pontoDeCorte] + mae[pontoDeCorte:]
            filho2 = mae[:pontoDeCorte] + pai[pontoDeCorte:]
        # Caso contrario replica-se pai e mãe
        else:
            filho1 = pai[:]
            filho2 = mae[:]
        return (filho1,filho2)
    


    def mutar(self, cromossomo) -> None:
        # Se o valor sorteado for menor ou igual a taxa de mutação -> realiza mutação
        if randint(1,100) <= self.taxaMutacao:
            valorMutacao = self.maxMinMutacao
            # escolhe um valor aleatorio para mutação
            mudanca = randint(-valorMutacao, valorMutacao)
            # escolhe aleatoriamente um gene para sofrer mutação 
            geneEscolhido = randint(0,self.numGenes-1)
            # aplica mutação
            cromossomo[geneEscolhido] += mudanca
            self.ajustar(cromossomo, geneEscolhido)
    
    def ajustar(self, cromossomo, geneEscolhido) -> None:
        valorGeneAlterado = cromossomo[geneEscolhido]
        if valorGeneAlterado > 255:
            cromossomo[geneEscolhido] = 255
        elif valorGeneAlterado < 0:
            cromossomo[geneEscolhido] = 0
    
    def printColored(self):
        for cromossomo in list(zip(self.populacao, self.avaliacao)):
            print(colors.colored(cromossomo[0][0],cromossomo[0][1],cromossomo[0][2], cromossomo), end=' ')
        print('\n')




def main():
    # criação e avaliação da primeira geração
    gen = AlgoritmoGenetico(15, 5, 80, 100)
    gen.avaliarPopulacao()
    for _ in range(gen.numGeracoes):
        # printa os besouros e seus fitenss
        gen.printColored()
        novaPopulacao = []
        # enquanto a nova populacao não for gerada -> realiza seleção cruzamento e mutação
        while len(novaPopulacao) < gen.tamPopulacao:
            pai,mae = gen.selecionarPais()
            filho1, filho2 = gen.cruzamento(pai,mae)
            gen.mutar(filho1)
            gen.mutar(filho2)
            novaPopulacao.append(filho1)
            novaPopulacao.append(filho2)
        # atualiza a população
        gen.populacao = novaPopulacao
        # avalia a nova população
        gen.avaliarPopulacao()



main()