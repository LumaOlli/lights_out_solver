import random
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Tuple

Matrix = List[List[int]]
Vector = List[int]


def indice(i: int, j: int, n: int) -> int:
    return i * n + j


def obter_direcoes(tipo: int):
    if tipo == 1:
        return [
            (0, 0),
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

    if tipo == 2:
        return [
            (0, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

    if tipo == 3:
        return [
            (0, 0),
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

    raise ValueError("Regra de vizinhança inválida.")


def construir_matriz_influencia(n: int, direcoes) -> Matrix:
    tamanho = n * n
    matriz_a = [
        [0 for _ in range(tamanho)]
        for _ in range(tamanho)
    ]

    for i in range(n):
        for j in range(n):
            coluna = indice(i, j, n)

            for di, dj in direcoes:
                ni = i + di
                nj = j + dj

                if 0 <= ni < n and 0 <= nj < n:
                    linha = indice(ni, nj, n)
                    matriz_a[linha][coluna] = 1

    return matriz_a


def vetorizar_tabuleiro(tabuleiro: Matrix) -> Vector:
    return [
        valor % 2
        for linha in tabuleiro
        for valor in linha
    ]


def eliminacao_gaussiana_mod2(
    matriz_a: Matrix,
    vetor_b: Vector,
) -> Tuple[Optional[Vector], Matrix, List[int]]:
    quantidade_linhas = len(matriz_a)
    quantidade_colunas = len(matriz_a[0])

    matriz = [
        matriz_a[i][:] + [vetor_b[i] % 2]
        for i in range(quantidade_linhas)
    ]

    linha_pivo = 0
    colunas_pivo = []

    for coluna in range(quantidade_colunas):
        pivo = None

        for linha in range(linha_pivo, quantidade_linhas):
            if matriz[linha][coluna] == 1:
                pivo = linha
                break

        if pivo is None:
            continue

        if pivo != linha_pivo:
            matriz[linha_pivo], matriz[pivo] = (
                matriz[pivo],
                matriz[linha_pivo],
            )

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

    for linha in range(quantidade_linhas):
        coeficientes_zeros = all(
            matriz[linha][coluna] == 0
            for coluna in range(quantidade_colunas)
        )

        termo_um = matriz[linha][quantidade_colunas] == 1

        if coeficientes_zeros and termo_um:
            return None, matriz, colunas_pivo

    solucao = [0 for _ in range(quantidade_colunas)]

    for i in range(len(colunas_pivo) - 1, -1, -1):
        coluna_pivo = colunas_pivo[i]
        soma = 0

        for coluna in range(coluna_pivo + 1, quantidade_colunas):
            soma = (
                soma + matriz[i][coluna] * solucao[coluna]
            ) % 2

        solucao[coluna_pivo] = (
            matriz[i][quantidade_colunas] + soma
        ) % 2

    return solucao, matriz, colunas_pivo


def gerar_tabuleiro_automatico(n: int) -> Matrix:
    return [
        [random.randint(0, 1) for _ in range(n)]
        for _ in range(n)
    ]


def resolver_tabuleiro(tabuleiro: Matrix, tipo_vizinhanca: int):
    n = len(tabuleiro)
    direcoes = obter_direcoes(tipo_vizinhanca)
    matriz_a = construir_matriz_influencia(n, direcoes)
    vetor_b = vetorizar_tabuleiro(tabuleiro)

    solucao, matriz_escalonada, colunas_pivo = (
        eliminacao_gaussiana_mod2(matriz_a, vetor_b)
    )

    return matriz_a, vetor_b, solucao, matriz_escalonada, colunas_pivo


def aplicar_jogada(tabuleiro: Matrix, i: int, j: int, direcoes) -> None:
    n = len(tabuleiro)

    for di, dj in direcoes:
        ni = i + di
        nj = j + dj

        if 0 <= ni < n and 0 <= nj < n:
            tabuleiro[ni][nj] = (tabuleiro[ni][nj] + 1) % 2


def formatar_matriz(matriz: Matrix) -> str:
    return "\n".join(
        " ".join(str(valor) for valor in linha)
        for linha in matriz
    )


def formatar_vetor(vetor: Vector) -> str:
    return " ".join(str(valor) for valor in vetor)


def vetor_para_tabuleiro(vetor: Vector, n: int) -> Matrix:
    return [
        vetor[i * n:(i + 1) * n]
        for i in range(n)
    ]


class LightsOutApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Solucionador Lights Out")
        self.n = 3
        self.botoes = []
        self.tabuleiro = []

        self.tamanho_var = tk.IntVar(value=3)
        self.vizinhanca_var = tk.IntVar(value=1)

        self.criar_interface()

    def criar_interface(self):
        topo = tk.Frame(self.janela)
        topo.pack(pady=10)

        tk.Label(topo, text="Tamanho do tabuleiro:").grid(
            row=0,
            column=0,
            padx=5,
        )

        tk.OptionMenu(
            topo,
            self.tamanho_var,
            3,
            4,
            5,
        ).grid(row=0, column=1, padx=5)

        tk.Label(topo, text="Vizinhança:").grid(
            row=0,
            column=2,
            padx=5,
        )

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

        self.frame_tabuleiro = tk.Frame(self.janela)
        self.frame_tabuleiro.pack(pady=10)

        self.saida = tk.Text(
            self.janela,
            width=80,
            height=22,
        )
        self.saida.pack(padx=10, pady=10)

        self.criar_tabuleiro_vazio()

    def criar_tabuleiro_vazio(self):
        self.n = self.tamanho_var.get()
        self.tabuleiro = [
            [0 for _ in range(self.n)]
            for _ in range(self.n)
        ]
        self.atualizar_botoes()

    def atualizar_botoes(self):
        for widget in self.frame_tabuleiro.winfo_children():
            widget.destroy()

        self.botoes = []

        for i in range(self.n):
            linha_botoes = []

            for j in range(self.n):
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
        self.tabuleiro[i][j] = (self.tabuleiro[i][j] + 1) % 2
        self.botoes[i][j].config(text=str(self.tabuleiro[i][j]))

    def gerar_com_solucao(self):
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
        tipo = self.vizinhanca_var.get()
        direcoes = obter_direcoes(tipo)

        matriz_a, vetor_b, solucao, matriz_esc, colunas_pivo = (
            resolver_tabuleiro(self.tabuleiro, tipo)
        )

        self.saida.delete("1.0", tk.END)

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

        tabuleiro_atual = [
            linha[:]
            for linha in self.tabuleiro
        ]

        contador = 1

        self.saida.insert(tk.END, "RESOLUÇÃO PASSO A PASSO\n")

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

        zerado = all(
            valor == 0
            for linha in tabuleiro_atual
            for valor in linha
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


if __name__ == "__main__":
    root = tk.Tk()
    app = LightsOutApp(root)
    root.mainloop()