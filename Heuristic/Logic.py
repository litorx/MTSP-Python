import math
from distances import distances

class SolucionadorTSP:
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas
    
    def resolver(self, num_caixeiros, max_cidades_por_caixeiro):
        caminhos = [[] for _ in range(num_caixeiros)]
        cidades_nao_visitadas = set(range(1, len(self.coordenadas)))
        
        for caixeiro in range(num_caixeiros):
            caminho = caminhos[caixeiro]
            cidade_atual = 0
            caminho.append(cidade_atual)
            
            while len(caminho) < max_cidades_por_caixeiro and cidades_nao_visitadas:
                cidade_mais_proxima = min(cidades_nao_visitadas, key=lambda cidade: self._distancia(cidade_atual, cidade))
                caminho.append(cidade_mais_proxima)
                cidades_nao_visitadas.remove(cidade_mais_proxima)
                cidade_atual = cidade_mais_proxima
            
            caminho.append(0)
        
        cidades_restantes = set(range(1, len(self.coordenadas))) - set(cidade for caminho in caminhos for cidade in caminho)
        
        for cidade_restante in cidades_restantes:
            caminho_mais_proximo = min(caminhos, key=lambda caminho: self._calcular_custo_insercao(cidade_restante, caminho))
            indice_minimo = min(range(1, len(caminho_mais_proximo)), key=lambda i: self._calcular_custo_insercao_em_posicao(cidade_restante, caminho_mais_proximo, i))
            caminho_mais_proximo.insert(indice_minimo, cidade_restante)
        
        return caminhos 
    
    def _distancia(self, cidade1, cidade2):
        return math.dist(self.coordenadas[cidade1], self.coordenadas[cidade2])
    
    def _calcular_custo_insercao(self, cidade, caminho):
        return min(self._calcular_custo_insercao_em_posicao(cidade, caminho, i) for i in range(1, len(caminho)))
    
    def _calcular_custo_insercao_em_posicao(self, cidade, caminho, indice):
        if indice == len(caminho):
            return self._distancia(caminho[-1], cidade) + self._distancia(cidade, caminho[0]) - self._distancia(caminho[-1], caminho[0])
        else:
            return self._distancia(caminho[indice-1], cidade) + self._distancia(cidade, caminho[indice]) - self._distancia(caminho[indice-1], caminho[indice])

num_caixeiros = 5
max_cidades_por_caixeiro = 19

matriz_selecionada = "Matriz9"
coordenadas = distances[matriz_selecionada]

solucionador = SolucionadorTSP(coordenadas)
caminhos = solucionador.resolver(num_caixeiros, max_cidades_por_caixeiro)

for i, caminho in enumerate(caminhos):
    print(f"Caixeiro {i+1}: {caminho}")

distancia_total = round(sum(sum(solucionador._distancia(caminho[i], caminho[i+1]) for i in range(len(caminho) - 1)) for caminho in caminhos))
print(f"Distância total percorrida: {distancia_total}")
