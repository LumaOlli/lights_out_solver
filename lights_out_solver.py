# ==============================================================================
# Solucionador e Interface Gráfica para o Jogo "Lights Out" em Python
# Autor: [Seu Nome/GitHub]
# Descrição: Implementação do jogo Lights Out usando Tkinter.
#            O programa utiliza Álgebra Linear (Eliminação Gaussiana no corpo 
#            modular mod 2) para determinar as jogadas necessárias para resolver
#            o tabuleiro.
# ==============================================================================

import random
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Tuple

# Definição de apelidos de tipos para melhorar a legibilidade do código
Matrix = List[List[int]]
Vector = List[int]


def indice(i: int, j: int, n: int) -> int:
    """Converte coordenadas bidimensionais (i, j) de uma matriz n x n

    em um índice linear (1D) usado na vetorização.
    """
    return i * n + j


def obter_direcoes(tipo: int):
    """Retorna os vetores de deslocamento de acordo com o tipo de vizinhança:

    1: Ortogonal (Formato de Cruz)
    2: Diagonal (Formato de X)
    3: Completa (Bloco 3x3 completo)
    O par (0,0) representa a própria célula clicada.
    """
    if tipo == 1:
        return [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

    if tipo == 2:
        return [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if tipo == 3:
        return [
            (0, 0),
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),
        ]

    raise ValueError("Regra de vizinhança inválida.")


def construir_matriz_influencia(n: int, direcoes) -> Matrix:
    """Monta a matriz de adjacência/influência 'A' de tamanho (n² x n²).

    Cada coluna indica uma ação (clique) e cada linha mapeia quais lâmpadas
    são afetadas por essa respectiva ação.
    """
    tamanho = n * n
    matriz_a = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    for i in range(n):
        for j in range(n):
            coluna = indice(i, j, n)

            # Aplica o mapeamento nas posições vizinhas contidas nos limites do tabuleiro
            for di, dj in direcoes:
                ni = i + di
                nj = j + dj

                if 0 <= ni < n and 0 <= nj < n:
                    linha = indice(ni, nj, n)
                    matriz_a[linha][coluna] = 1

    return matriz_a


def vetorizar_tabuleiro(tabuleiro: Matrix) -> Vector:
    """Achata a matriz bidimensional do tabuleiro em um único vetor unidimensional (1D).

    Aplica a operação modular (% 2) para manter a consistência matemática.
    """
    return [valor % 2 for linha in tabuleiro for valor in linha]


def eliminacao_gaussiana_mod2(
    matriz_a: Matrix,
    vetor_b: Vector,
) -> Tuple[Optional[Vector], Matrix, List[int]]:
    """Resolve o sistema linear A * x = b usando eliminação gaussiana sob o corpo

    finito Z_2 (aritmética módulo 2). As somas mod 2 funcionam de forma idêntica
    à operação lógica XOR.
    """
    quantidade_linhas = len(matriz_a)
    quantidade_colunas = len(matriz_a[0])

    # Criação da matriz aumentada [A|b]
    matriz = [
        matriz_a[i][:] + [vetor_b[i] % 2]
        for i in range(quantidade_linhas)
    ]

    linha_pivo = 0
    colunas_pivo = []

    # --- Fase de Escalonamento (Foward Elimination) ---
    for coluna in range(quantidade_colunas):
        pivo = None

        # Busca pelo pivô de valor 1 na coluna atual
        for linha in range(linha_pivo, quantidade_linhas):
            if matriz[linha][coluna] == 1:
                pivo = linha
                break

        if pivo is None:
            continue  # Coluna livre / Variável livre

        # Permuta a linha atual com a linha do pivô encontrado se necessário
        if pivo != linha_pivo:
            matriz[linha_pivo], matriz[pivo] = (
                matriz[pivo],
                matriz[linha_pivo],
            )

        # Elimina os valores 1 localizados abaixo do pivô
        for linha in range(linha_pivo + 1, quantidade_linhas):
            if matriz[linha][coluna] == 1:
                for k in range(coluna, quantidade_colunas + 1):
                    matriz[linha][k] = (
                        matriz[linha][k] + matriz[linha_pivo][k]
                    ) % 2

        colunas_pivo.append(coluna)
        linha_pivo += 1

        if linha_pivo == quantidade_linhas:
            break

    # --- Análise de Consistência (Teorema de Rouché-Capelli) ---
    for linha in range(quantidade_linhas):
        coeficientes_zeros = all(
            matriz[linha][coluna] == 0 
            for coluna in range(quantidade_colunas)
        )

        termo_um = matriz[linha][quantidade_colunas] == 1

        # Linha de zeros resultando em termo independente igual a 1 indica sistema inconsistente
        if coeficientes_zeros and termo_um:
            return None, matriz, colunas_pivo

    # --- Fase de Substituição para Trás (Back Substitution) ---
    solucao = [0 for _ in range(quantidade_colunas)]

    for i in range(len(colunas_pivo) - 1, -1, -1):
        coluna_pivo = colunas_pivo[i]
        soma = 0

        for coluna in range(coluna_pivo + 1, quantidade_colunas):
            soma = (soma + matriz[i][coluna] * solucao[coluna]) % 2

        solucao[coluna_pivo] = (matriz[i][quantidade_colunas] + soma) % 2

    return solucao, matriz, colunas_pivo


def gerar_tabuleiro_automatico(n: int) -> Matrix:
    """Gera uma estrutura matricial n x n povoada aleatoriamente com zeros e uns."""
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]


def resolver_tabuleiro(tabuleiro: Matrix, tipo_vizinhanca: int):
    """Encapsula a geração do sistema e chama o solucionador matricial."""
    n = len(tabuleiro)
    direcoes = obter_direcoes(tipo_vizinhanca)
    matriz_a = construir_matriz_influencia(n, direcoes)
    vetor_b = vetorizar_tabuleiro(tabuleiro)

    solucao, matriz_escalonada, colunas_pivo = (
    eliminacao_gaussiana_mod2(matriz_a, vetor_b)
    )

    return matriz_a, vetor_b, solucao, matriz_escalonada, colunas_pivo


def aplicar_jogada(tabuleiro: Matrix, i: int, j: int, direcoes) -> None:
    """Modifica o estado do tabuleiro in-place, simulando as alterações provocadas

    pelo clique na coordenada (i, j).
    """
    n = len(tabuleiro)

    for di, dj in direcoes:
        ni = i + di
        nj = j + dj

        if 0 <= ni < n and 0 <= nj < n:
            tabuleiro[ni][nj] = (tabuleiro[ni][nj] + 1) % 2


# --- FUNÇÕES AUXILIARES DE FORMATAÇÃO TEXTUAL ---


def formatar_matriz(matriz: Matrix) -> str:
    return "\n".join(
        " ".join(str(valor) for valor in linha) for linha in matriz
    )


def formatar_vetor(vetor: Vector) -> str:
    return " ".join(str(valor) for valor in vetor)


def vetor_para_tabuleiro(vetor: Vector, n: int) -> Matrix:
    """Reconstrói o arranjo matricial n x n a partir de sua forma linearizada (1D)."""
    return [vetor[i * n : (i + 1) * n] for i in range(n)]


# --- CLASSE GERENCIADORA DA INTERFACE GRÁFICA (TKINTER) ---


class LightsOutApp:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Solucionador Lights Out")
        self.n = 3
        self.botoes = []
        self.tabuleiro = []

        # Variáveis de controle do Tkinter para monitorar seleções do usuário
        self.tamanho_var = tk.IntVar(value=3)
        self.vizinhanca_var = tk.IntVar(value=1)

        self.criar_interface()

    def criar_interface(self):
        """Instancia os widgets visuais da aplicação (menus, botões e terminais)."""
        # Contêiner Superior para Seleções de Configuração
        topo = tk.Frame(self.janela)
        topo.pack(pady=10)

        tk.Label(topo, text="Tamanho do tabuleiro:").grid(
            row=0, column=0, padx=5
        )

        tk.OptionMenu(
            topo,
            self.tamanho_var,
            3,
            4,
            5,
        ).grid(row=0, column=1, padx=5)

        tk.Label(topo, text="Vizinhança:").grid(row=0, column=2, padx=5)

        tk.OptionMenu(
            topo,
            self.vizinhanca_var,
            1,
            2,
            3,
        ).grid(row=0, column=3, padx=5)

        tk.Label(
            self.janela,
            text="1 = Ortogonal | 2 = Diagonal | 3 = Completa",
        ).pack()

        # Painel de Botões de Ações Gerais
        controles = tk.Frame(self.janela)
        controles.pack(pady=10)

        tk.Button(
            controles,
            text="Criar tabuleiro vazio",
            command=self.criar_tabuleiro_vazio,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            controles,
            text="Gerar automático com solução",
            command=self.gerar_com_solucao,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            controles,
            text="Resolver",
            command=self.resolver,
        ).grid(row=0, column=2, padx=5)

        # Grade Dedicada à Matriz de Botões Interativos
        self.frame_tabuleiro = tk.Frame(self.janela)
        self.frame_tabuleiro.pack(pady=10)

        # Console de Texto para Output dos Cálculos
        self.saida = tk.Text(
            self.janela,
            width=80,
            height=22,
        )
        self.saida.pack(padx=10, pady=10)

        # Inicialização do estado base do app
        self.criar_tabuleiro_vazio()

    def criar_tabuleiro_vazio(self):
        """Inicializa a matriz interna com zeros e força a atualização da grade física."""
        self.n = self.tamanho_var.get()
        self.tabuleiro = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.atualizar_botoes()

    def atualizar_botoes(self):
        """Limpa o contêiner visual anterior e renderiza a nova grade de botões."""
        # Limpa widgets filhos remanescentes
        for widget in self.frame_tabuleiro.winfo_children():
            widget.destroy()

        self.botoes = []

        for i in range(self.n):
            linha_botoes = []

            for j in range(self.n):
                # O parâmetro command utiliza closures (lambda com escopo local) para reter os índices i e j corretos
                botao = tk.Button(
                    self.frame_tabuleiro,
                    text=str(self.tabuleiro[i][j]),
                    width=6,
                    height=3,
                    command=lambda x=i, y=j: self.alternar_celula(x, y),
                )
                botao.grid(row=i, column=j, padx=2, pady=2)
                linha_botoes.append(botao)

            self.botoes.append(linha_botoes)

    def alternar_celula(self, i: int, j: int):
        """Gerencia o clique manual do usuário nas células, invertendo seu estado (0/1)."""
        self.tabuleiro[i][j] = (self.tabuleiro[i][j] + 1) % 2
        self.botoes[i][j].config(text=str(self.tabuleiro[i][j]))

    def gerar_com_solucao(self):
        """Loop iterativo que busca gerar uma configuração de tabuleiro inicial

        que possua solução válida garantida pelo algoritmo.
        """
        self.n = self.tamanho_var.get()
        tipo = self.vizinhanca_var.get()
        tentativas = 0

        while True:
            tentativas += 1
            tabuleiro = gerar_tabuleiro_automatico(self.n)
            _, _, solucao, _, _ = resolver_tabuleiro(tabuleiro, tipo)

            if solucao is not None:
                self.tabuleiro = tabuleiro
                break

        self.atualizar_botoes()
        self.saida.delete("1.0", tk.END)
        self.saida.insert(
            tk.END,
            f"Tabuleiro solucionável gerado em {tentativas} tentativa(s).\n",
        )

    def resolver(self):
        """Dispara a rotina matemática de resolução do sistema linear,

        exibindo de forma encadeada o passo a passo algébrico e as ações no console.
        """
        tipo = self.vizinhanca_var.get()
        direcoes = obter_direcoes(tipo)

        # Desestrutura o retorno com os dados do sistema
        matriz_a, vetor_b, solucao, matriz_esc, colunas_pivo = (
            resolver_tabuleiro(self.tabuleiro, tipo)
        )

        # Limpa o campo de log textual
        self.saida.delete("1.0", tk.END)

        # Escreve relatórios de estado do sistema na área de logs
        self.saida.insert(tk.END, "TABULEIRO INICIAL\n")
        self.saida.insert(tk.END, formatar_matriz(self.tabuleiro))
        self.saida.insert(tk.END, "\n\n")

        self.saida.insert(tk.END, "MATRIZ DE INFLUÊNCIA A\n")
        self.saida.insert(tk.END, formatar_matriz(matriz_a))
        self.saida.insert(tk.END, "\n\n")

        self.saida.insert(tk.END, "VETOR b\n")
        self.saida.insert(tk.END, formatar_vetor(vetor_b))
        self.saida.insert(tk.END, "\n\n")

        self.saida.insert(tk.END, "MATRIZ ESCALONADA\n")
        self.saida.insert(tk.END, formatar_matriz(matriz_esc))
        self.saida.insert(tk.END, "\n\n")

        self.saida.insert(
            tk.END,
            f"Posto da matriz A: {len(colunas_pivo)}\n\n",
        )

        # Interrupção em caso de sistema impossível
        if solucao is None:
            self.saida.insert(
                tk.END,
                "Este tabuleiro não possui solução.\n",
            )
            return

        mapa = vetor_para_tabuleiro(solucao, self.n)

        self.saida.insert(tk.END, "MAPA DE JOGADAS\n")
        self.saida.insert(tk.END, "1 = pressionar | 0 = não pressionar\n")
        self.saida.insert(tk.END, formatar_matriz(mapa))
        self.saida.insert(tk.END, "\n\n")

        # Cópia profunda para simulação visual da resolução
        tabuleiro_atual = [linha[:] for linha in self.tabuleiro]
        contador = 1

        self.saida.insert(tk.END, "RESOLUÇÃO PASSO A PASSO\n")

        # Simula a aplicação de cada bit '1' encontrado na resposta do vetor x
        for posicao, valor in enumerate(solucao):
            if valor == 1:
                i = posicao // self.n
                j = posicao % self.n

                self.saida.insert(
                    tk.END,
                    f"\nJogada {contador}: pressionar "
                    f"posição ({i + 1}, {j + 1})\n",
                )

                aplicar_jogada(tabuleiro_atual, i, j, direcoes)

                self.saida.insert(
                    tk.END,
                    formatar_matriz(tabuleiro_atual),
                )
                self.saida.insert(tk.END, "\n")

                contador += 1

        self.saida.insert(tk.END, "\nTABULEIRO FINAL\n")
        self.saida.insert(tk.END, formatar_matriz(tabuleiro_atual))

        # Teste lógico de verificação final
        zerado = all(
            valor == 0 for linha in tabuleiro_atual for valor in linha
        )

        if zerado:
            self.saida.insert(
                tk.END,
                "\n\nValidação: todas as luzes foram apagadas.",
            )
        else:
            self.saida.insert(
                tk.END,
                "\n\nValidação: a solução não zerou o tabuleiro.",
            )


# Ponto de entrada padrão para execução do script Python
if __name__ == "__main__":
    root = tk.Tk()
    app = LightsOutApp(root)
    root.mainloop()