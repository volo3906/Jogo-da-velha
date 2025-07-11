# -*- coding: utf-8 -*-
from random import choice
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        self.oponente = Tabuleiro.JOGADOR_X if tipo == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0
            
    def getJogada(self) -> (int, int):
        disponiveis = [(l, c) for l in range(3) for c in range(3) 
                      if self.matriz[l][c] == Tabuleiro.DESCONHECIDO]
        
        # R1
        jogada = self.verificar_sequencia(self.tipo) or self.verificar_sequencia(self.oponente)
        if jogada and jogada in disponiveis:
            return jogada

        # R2
        jogada = self.encontrar_jogada_com_duas_sequencias()
        if jogada and jogada in disponiveis:
            return jogada

        # R3
        if (1, 1) in disponiveis:
            return (1, 1)

        # R4
        jogada = self.marcar_canto_oposto()
        if jogada and jogada in disponiveis:
            return jogada

        # R5
        jogada = self.encontrar_canto_vazio()
        if jogada:
            return jogada

        # R6
        return choice(disponiveis) if disponiveis else (0, 0)

    def verificar_sequencia(self, jogador):
        for i in range(3):
            linha = self.matriz[i]
            if linha.count(jogador) == 2 and linha.count(Tabuleiro.DESCONHECIDO) == 1:
                return (i, linha.index(Tabuleiro.DESCONHECIDO))
            
            coluna = [self.matriz[j][i] for j in range(3)]
            if coluna.count(jogador) == 2 and coluna.count(Tabuleiro.DESCONHECIDO) == 1:
                return (coluna.index(Tabuleiro.DESCONHECIDO), i)
        
        diagonal1 = [self.matriz[i][i] for i in range(3)]
        if diagonal1.count(jogador) == 2 and diagonal1.count(Tabuleiro.DESCONHECIDO) == 1:
            pos = diagonal1.index(Tabuleiro.DESCONHECIDO)
            return (pos, pos)
        
        diagonal2 = [self.matriz[i][2-i] for i in range(3)]
        if diagonal2.count(jogador) == 2 and diagonal2.count(Tabuleiro.DESCONHECIDO) == 1:
            pos = diagonal2.index(Tabuleiro.DESCONHECIDO)
            return (pos, 2-pos)
        
        return None
    
    def encontrar_jogada_com_duas_sequencias(self):
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                    
                    self.matriz[i][j] = self.tipo
                    contagem = 0
                    
                    linha = self.matriz[i]
                    if linha.count(self.tipo) == 2 and linha.count(Tabuleiro.DESCONHECIDO) == 1:
                        contagem += 1
                    
                    coluna = [self.matriz[x][j] for x in range(3)]
                    if coluna.count(self.tipo) == 2 and coluna.count(Tabuleiro.DESCONHECIDO) == 1:
                        contagem += 1
                    
                    if i == j:
                        diagonal = [self.matriz[x][x] for x in range(3)]
                        if diagonal.count(self.tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
                            contagem += 1
                    
                    if i + j == 2:
                        diagonal = [self.matriz[x][2-x] for x in range(3)]
                        if diagonal.count(self.tipo) == 2 and diagonal.count(Tabuleiro.DESCONHECIDO) == 1:
                            contagem += 1
                    
                    self.matriz[i][j] = Tabuleiro.DESCONHECIDO
                    
                    if contagem >= 2:
                        return (i, j)
        return None


    def marcar_canto_oposto(self):
        cantos = [(0,0), (0,2), (2,0), (2,2)]
        opostos = {(0,0):(2,2), (0,2):(2,0), (2,0):(0,2), (2,2):(0,0)}
        
        for canto in cantos:
            i, j = canto
            if self.matriz[i][j] == self.oponente:
                oposto_i, oposto_j = opostos[canto]
                if self.matriz[oposto_i][oposto_j] == Tabuleiro.DESCONHECIDO:
                    return (oposto_i, oposto_j)
        return None

    def encontrar_canto_vazio(self):
        for i, j in [(0,0), (0,2), (2,0), (2,2)]:
            if self.matriz[i][j] == Tabuleiro.DESCONHECIDO:
                return (i, j)
        return None