import random
import time

def seed(n):
    random.seed(n)

# Etapa 1: Leitura do mapa
def leitura_mapa(arquivo):
    start_time = time.time() 
    
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

        mapa_lido = []
        for linha in linhas:
            if not linha[0].isdigit():
                continue
            mapa_lido.append(linha.split())
            
    end_time = time.time()  
    print(f"Tempo de leitura do mapa: {end_time - start_time:.4f} segundos")
    
    return mapa_lido

# Etapa 2: Extração das coordenadas
def extrair_coordenadas(mapa_lido):
    start_time = time.time()
    
    coordenadas = {}

    for linha in mapa_lido:
        ponto = int(linha[0])
        x = float(linha[1])
        y = float(linha[2])

        coordenadas[ponto] = (x, y)
        
    end_time = time.time()  
    print(f"Tempo de extração das coordenadas: {end_time - start_time:.4f} segundos")

    return coordenadas

# Etapa 3: Calcular a distância de Chebyshev
def calcular_distancia(coordenadas):
    start_time = time.time()

    distancias = {}

    # 1) Ler cada par da lista
    for primeiro_ponto in coordenadas:
        for segundo_ponto in coordenadas:

            # 2) Comparar x com x e y com y = resulta um par de distâncias
            if primeiro_ponto != segundo_ponto:
                x1, y1 = coordenadas[primeiro_ponto]
                x2, y2 = coordenadas[segundo_ponto]

                # Distância de Chebyshev: máximo das diferenças absolutas
                distancia = max(abs(x1 - x2), abs(y1 - y2))

                # 3) Salvar a distância num novo par
                distancias[(primeiro_ponto, segundo_ponto)] = distancia
                distancias[(segundo_ponto, primeiro_ponto)] = distancia

    end_time = time.time()  
    print(f"Tempo de cálculo das distâncias: {end_time - start_time:.4f} segundos")
    
    return distancias

# Etapa 4: Construir a rota inicial

def rota_inicial(coordenadas, distancias, rclSize):
    start_time = time.time()
    
    pontos = list(coordenadas.keys())

    # 1 Define ponto inicial aleatório
    ponto_inicial = pontos.pop(random.randint(0, len(pontos) - 1))
    rota = [ponto_inicial]

    # 2 Construção da rota
    while pontos:
        ultimo_ponto = rota[-1]

        # 3 Gera candidatos a partir das cidades restantes
        candidatos = []
        for cidade in pontos:
            distancia = distancias[(ultimo_ponto, cidade)]
            candidatos.append((cidade, distancia))
            
        candidatos.sort(key=lambda x: x[1])  # Ordena de acordo com a distância

        # 4 Lista Restrita de Candidatos (RCL)
        rcl = []
        for tupla in candidatos[:rclSize]:
            rcl.append(tupla[0]) # adiciona apenas a cidade

        # Escolhe a próxima cidade aleatoriamente da RCL
        proxima_cidade = random.choice(rcl)
        rota.append(proxima_cidade)
        pontos.remove(proxima_cidade)

    # Retorna à cidade inicial para completar o ciclo
    rota.append(rota[0])
    
    end_time = time.time()  # Marca o fim da construção da rota inicial
    print(f"Tempo de construção da rota inicial: {end_time - start_time:.4f} segundos")

    return rota

def gerar_vizinhos(rota, distancias):
  start_time = time.time()
    
  vizinhos = []

  for i in range(1, (len(rota) - 1)):
    for j in range(i + 1, len(rota)):
           
        ## LEMBRETE: CONDENSAR DEPOIS
      frag_inicio = rota[:i]
      frag_invertido = rota[i:j][::-1]
      frag_final = rota[j:]

      novo_vizinho = frag_inicio + frag_invertido + frag_final
      vizinhos.append(novo_vizinho)

      #print(f"Nova rota: (combinação {i} e {j}): {novo_vizinho}")

  return vizinhos

def calc_distancia_tabu(rota, distancias):
    start_time = time.time()
    
    total = 0

    # Itera sobre os pares consecutivos de cidades na rota
    for i in range(len(rota) - 1):
        # Obtém a distância diretamente ou a simétrica, com um fallback de 0
        dist = distancias.get((rota[i], rota[i + 1]), distancias.get((rota[i + 1], rota[i]), 0))
        total += dist
        #print(f"Cálculo {i}: {dist}")

    # Adiciona a distância de retorno do último ponto ao ponto inicial
    retorno = distancias.get((rota[-1], rota[0]), distancias.get((rota[0], rota[-1]), 0))
    total += retorno
    #print(f"Distância de retorno: {retorno}")

    return total

def verificar_convergencia(hist_distancias, tolerancia):
    start_time = time.time()
    
    if len(hist_distancias) < 2:
        return False
    convergencia = abs(hist_distancias[-1] - hist_distancias[-2]) < tolerancia
    return convergencia

def busca_tabu(rota_inicial, distancias, max_iteracoes, tabuSize, tolerancia):
    start_time = time.time()
    
    melhor_rota = rota_inicial
    melhor_distancia = calc_distancia_tabu(melhor_rota, distancias)

    lista_tabu =[]  #aramzena resultados proibidos

    solucao_Atual = melhor_rota
    distancia_atual = melhor_distancia
    
    hist_distancias = [melhor_distancia]

    for iteracao in range(max_iteracoes):
        vizinhos = gerar_vizinhos(solucao_Atual, distancias)
        
        melhor_vizinho = None
        dist_melhor_vizinho = float('inf')
        
        for item in vizinhos:
            if item in lista_tabu:
                continue
            
            dist_vizinho = calc_distancia_tabu(item, distancias)
            
            if dist_vizinho < dist_melhor_vizinho:
                melhor_vizinho = item
                dist_melhor_vizinho = dist_vizinho
                
        if melhor_vizinho and dist_melhor_vizinho < distancia_atual:
            solucao_Atual = melhor_vizinho
            distancia_atual = dist_melhor_vizinho
            
            if distancia_atual < melhor_distancia:
                melhor_rota = solucao_Atual
                melhor_distancia = distancia_atual
                
        if verificar_convergencia(hist_distancias, tolerancia):
            print("Convergiu")
            break
                
        # Atualizando a tabu
        if solucao_Atual not in lista_tabu:     
            lista_tabu.append(solucao_Atual)
        
        if len(lista_tabu) > tabuSize: # limita o tamanho da lista a x
            lista_tabu.pop(0)
            
        hist_distancias.append(distancia_atual)
            
        print(f"Iteração {iteracao + 1}: Melhor distância atual: {melhor_distancia}")
    
    end_time = time.time()  
    print(f"Tempo total da busca Tabu: {end_time - start_time:.4f} segundos")
    
    return melhor_rota, melhor_distancia


def main():
    n = random.randint(1, 30)
    seed(n)
    
    arquivo = "berlin52.txt"
    mapa_lido = leitura_mapa(arquivo)
    coordenadas = extrair_coordenadas(mapa_lido)
    distancias = calcular_distancia(coordenadas)
    
    rclSize = 5
    rota = rota_inicial(coordenadas, distancias, rclSize)
    print(f"Rota Inicial (cidades): {rota}")

    max_iteracoes = 100
    tabuSize = 100
    tolerancia = 0.1
    melhor_rota, melhor_distancia = busca_tabu(rota, distancias, max_iteracoes, tabuSize, tolerancia)
    
    print(f"Seed: {n}")
    print(f"Melhor rota: {melhor_rota}")
    print(f"Distância: {melhor_distancia}")

if __name__ == "__main__":
    main()