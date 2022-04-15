from abc import ABC, abstractmethod
from random import random


class Avaliador(ABC):
    @abstractmethod
    def avaliar(self):
        pass


class Cromossomo:
    def __init__(self, tamanho: int, genes=[]):
        self.tamanho = tamanho
        self.genes = genes

    def mutacao(self, taxa):
        for n, gene in enumerate(self.genes):
            if random() <= taxa:
                if gene == 1:
                    self.genes[n] = 0
                else:
                    self.genes[n] = 1

    def aletorizar(self):
        self.genes = [round(random()) for c in range(self.tamanho)]


class Individuo:
    def __init__(self, id: str, cromossomo: Cromossomo):
        self.id = id
        self.cromossomo = cromossomo
        self.produtos = []
        self.nota: float = 0


class AvaliarCaminhao(Avaliador):
    def __init__(self, limite_caminhao, lista_produtos):
        self.limite_caminhao = limite_caminhao
        self.lista_produtos = lista_produtos

    def avaliar(self, individuo: Individuo):
        for n, gene in enumerate(individuo.cromossomo.genes):
            if gene == 1:
                individuo.produtos.append(self.lista_produtos[n])

        individuo.volume = sum([vol.volume for vol in individuo.produtos])
        individuo.preco = sum([cust.preco for cust in individuo.produtos])
        if individuo.volume <= self.limite_caminhao:
            individuo.nota = individuo.preco
        else:
            individuo.nota = 1

    def selecionar_adaptados(self, individuos, populacao):
        adaptados = []
        for c in range(int(populacao.quantidade_individuo)):
            pai = -1
            soma_notas = sum(preco.preco for preco in individuos)
            valor_sorteado = random() * soma_notas
            soma = 0
            i = 0
            while i < len(individuos) and soma < valor_sorteado:
                soma += individuos[i].nota
                pai += 1
                i += 1
            adaptados.append(individuos[pai])
        populacao.adaptados_da_geracao = adaptados
        populacao.melhor_da_geracao = individuos[0]

    def criar_filhos(self, adaptados):
        for n, individuo in enumerate(adaptados[:]):
            if n % 2 == 0:
                pai_1 = individuo
                pai_2 = adaptados[n + 1]
                filho_1, filho_2 = self.crossover(pai_1, pai_2)
                populacao.filhos.append(filho_1)
                populacao.filhos.append(filho_2)

    def crossover(self, pai_1, pai_2):
        corte = round(random() * len(pai_1.cromossomo.genes))
        filho_1 = Individuo(f'{pai_1.id}', Cromossomo(pai_1.cromossomo.tamanho,
                                                      pai_1.cromossomo.genes[:corte] + pai_2.cromossomo.genes[corte:]))
        filho_2 = Individuo(f'{pai_2.id}', Cromossomo(pai_1.cromossomo.tamanho,
                                                      pai_2.cromossomo.genes[:corte] + pai_1.cromossomo.genes[corte:]))
        return filho_1, filho_2


class Produto:
    def __init__(self, nome: str, volume: float, preco: float):
        self.nome = nome
        self.volume = volume
        self.preco = preco


class Populacao:
    def __init__(self, tam_cromossomo, tipo_individuo: Individuo, quantidade_individuo: int, avaliador: Avaliador,
                 geracao=1):
        self.tipo_individuo = tipo_individuo
        self.quantidade_individuo = quantidade_individuo
        self.avaliador = avaliador
        self.geracao = geracao
        self.individuos = []
        self.melhor_da_geracao = []
        self.adaptados_da_geracao = []
        self.filhos = []
        if self.geracao == 1:
            self.criar_inidividuos(tam_cromossomo)

    def avaliar_individuos(self):
        for individuo in self.individuos:
            self.avaliador.avaliar(individuo)
        self.individuos = sorted(self.individuos, key=lambda individuo: individuo.nota, reverse=True)

    def criar_inidividuos(self, tam_cromossomo):
        for i in range(self.quantidade_individuo):
            individuo = self.tipo_individuo(f'{i + 1}', Cromossomo(tam_cromossomo))
            individuo.cromossomo.aletorizar()
            self.individuos.append(individuo)

    def selecionar_adaptados(self):
        self.avaliador.selecionar_adaptados(self.individuos, self)

    def criar_filhos(self):
        self.avaliador.criar_filhos(self.adaptados_da_geracao)

    def mutacao_filhos(self, taxa):
        for filho in self.filhos:
            filho.cromossomo.mutacao(taxa)


if __name__ == '__main__':
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))

    quantidade_produtos = len(lista_produtos)
    avaliador = AvaliarCaminhao(3, lista_produtos)
    populacao_ant = []

    for c in range(0, 200):
        if c == 0:
            populacao = Populacao(quantidade_produtos, Individuo, 300, avaliador)
        else:
            populacao = Populacao(quantidade_produtos, Individuo, 300, avaliador, populacao_ant.geracao + 1)
            for filho in populacao_ant.filhos:
                populacao.individuos.append(filho)
        populacao.avaliar_individuos()
        populacao.selecionar_adaptados()
        populacao.criar_filhos()
        populacao.mutacao_filhos(0.05)
        populacao_ant = populacao

    print('melhor custo/beneficio de produtos para o caminhão\n')
    print(30*'-=')

    espaco = 0
    preco = 0
    for n, c in enumerate(lista_produtos):
        if populacao.individuos[0].cromossomo.genes[n] == 1:
            print(f'{c.nome} ocupando um espaço de {c.volume}m³ e custando R$ {c.preco:.2f}')
            espaco += c.volume
            preco += c.preco
    print(30 * '-=')
    print(f'\ntodos eles ocupam {espaco:.1f}m³ juntos por R$ {preco:.2f}')