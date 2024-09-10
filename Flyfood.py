import tsplib95, random, time

tsp = tsplib95.load("./berlin52.tsp")
restrooms = tsp.node_coords

# ========================================================

seed = None # Caso None gerara uma aleatoria
pais = 2  # Número de pais para seleção
prob_mutacao = 0.01  # Probabilidade de mutação
tamanho_populacao = 100  # Tamanho da população
geracoes = 250  # Número de gerações
type = 'roleta' # torneio | roleta

# ========================================================

def individuo():
    return random.sample(range(1, len(restrooms)+1), len(restrooms))

def criarPop():
    return [individuo() for _ in range(tamanho_populacao)]

def compareWith2(pointA, pointB):
    distanceH = abs(restrooms[pointA][0] - restrooms[pointB][0])
    distanceV = abs(restrooms[pointA][1] - restrooms[pointB][1])
    return distanceH + distanceV 
     
def compareWithMany(list):
    sumAll = 0
    tempList = list.copy()
    pointA = tempList.pop(0)
    for pointB in list:
        sumAll += compareWith2(pointA, pointB)
        pointA = pointB
    return sumAll

def selectFathers(population):
    # Roleta
    if type == 'roleta':
        total = 0
        value = 0
        
        # Inverter os valores de aptidão para que o menor valor tenha mais chance
        aptidoes_invertidas = [1 / i[0] for i in population]
        # Calcular o total das aptidões invertidas
        total = sum(aptidoes_invertidas)
        
        check = random.random()
        
        for i in range(len(population)):
            # Calcula a probabilidade de cada individuo
            probabilidade = aptidoes_invertidas[i] / total
            # Chega se o valor esta na faixa do individuo e o retorna caso sim 
            if value <= check < value + probabilidade:
                return population[i][1]
            value += probabilidade
    else:
        # Torneio
        candidateOne = random.choice(population)
        candidateTwo = random.choice(population)
        
        while candidateTwo == candidateOne:
            candidateTwo = random.choice(population)
        if candidateOne[0] < candidateTwo[0]:
            return candidateOne[1]
        return candidateTwo[1]

def reproduction(pop):
    pontuados = [(compareWithMany(i), i) for i in pop] # Atribui o valor da distancia a rota
    nova_pop = []
    while len(nova_pop) < tamanho_populacao:
        father = selectFathers(pontuados) 
        mother = selectFathers(pontuados)
        
        while father == mother:
            father = selectFathers(pontuados)
        
        chance = random.random()
        if chance <= 0.7:
            nova_pop.append(pmx_crossover(father, mother))
            nova_pop.append(pmx_crossover(mother, father))
        else:
            nova_pop.append(father.copy())
            nova_pop.append(mother.copy())
    return nova_pop[:tamanho_populacao]


def pmx_crossover(father, mother):
    # Obtemos o comprimento das permutações
    length = len(father)
    
    # Escolhe aleatoriamente dois pontos de crossover
    point1, point2 = sorted(random.sample(range(length), 2))
    if point2 - point1 < length // 4:  # Garante que a faixa de cruzamento seja significativa
        point2 = (point1 + length // 4) % length
    
    # Cria um filho com posições indefinidas
    child = [-1] * length

    # Copia o segmento entre os pontos de crossover do pai para o filho
    child[point1:point2] = father[point1:point2]
    
    # Cria o mapeamento entre os genes do segmento copiado
    mapping = {father[i]: mother[i] for i in range(point1, point2)}

    # Preenche os valores restantes do filho, garantindo a consistência
    for i in range(length):
        if child[i] == -1:  # Se ainda não foi preenchido
            value = mother[i]
            # Resolve possíveis conflitos com o mapeamento
            while value in mapping:
                value = mapping[value]
            child[i] = value

    return child
 
def getBestSolution(list):
    newList = [(compareWithMany(i), i) for i in list]
    return min(newList)[0],  min(newList)[1]

def mutacao(pop):
	for i in range(len(pop)):
		if random.random() <= prob_mutacao:
			ponto = random.sample(pop[i], 2)
			pop[i][ponto[0]-1], pop[i][ponto[1]-1] = pop[i][ponto[1]-1], pop[i][ponto[0]-1]
	return pop

def setSeed(seed):
    if seed:
        return seed
    return time.time()
	

def principal():
    # Inicialização da população
    random.seed(setSeed(seed))
    pop = criarPop()
    melhor_fitness = 0
    i = 0
    arquivo = open(f"{setSeed(seed)}.txt", "w")
    arquivo.write("INFORMATIONS\n")
    arquivo.write(f"\nseed = {None}")
    arquivo.write(f"\npais = {pais}")
    arquivo.write(f"\nprob_mutacao = {prob_mutacao}")
    arquivo.write(f"\ntamanho_populacao = {tamanho_populacao}")
    arquivo.write(f"\ngeracoes = {geracoes}")
    arquivo.write(f"\ntipo = {type}")
    arquivo.write("\n======================================\n")
    
    for i in range(geracoes):
        # Seleção e Reprodução
        pop = reproduction(pop)
        
        # Mutação
        pop = mutacao(pop)
        
        # Imprimir resultados
        melhor_fitness, melhor_individuo  = getBestSolution(pop)
        arquivo.write(f"GENERATION: {i}\n")
        arquivo.write("BEST ROUTE: [")
        arquivo.write(', '.join(str(x) for x in melhor_individuo))
        arquivo.write(f"]\nDISTANCE: {melhor_fitness}")
        arquivo.write("\n======================================\n")
    print(f"Melhor indivíduo: {melhor_individuo}, Aptidão: {melhor_fitness}")
    


if __name__ == "__main__":
    principal()

