<h1 align="center">Lights Out Solver</h1>

## Sobre o Projeto

<p align="justify">
Este repositório apresenta uma implementação do jogo <strong>Lights Out</strong> utilizando conceitos de <strong>Álgebra Linear</strong> e <strong>Cálculo Numérico</strong>. O objetivo do projeto é modelar o problema como um sistema linear binário e encontrar automaticamente a sequência de jogadas necessária para apagar todas as luzes do tabuleiro. O projeto foi desenvolvido como atividade acadêmica para demonstrar a aplicação prática da eliminação gaussiana em sistemas lineares definidos sobre o corpo finito GF(2), onde todas as operações são realizadas em módulo 2. Além de resolver o problema matematicamente, o sistema também apresenta uma simulação passo a passo das jogadas encontradas, permitindo visualizar todo o processo de resolução. </p>

## O Jogo Lights Out

<p align="justify">
Lights Out é um jogo de lógica composto por um tabuleiro de luzes que podem estar ligadas (1) ou desligadas (0). Ao pressionar uma célula, seu estado é invertido juntamente com o estado de algumas células vizinhas, dependendo da regra de vizinhança escolhida. O objetivo é apagar todas as luzes do tabuleiro. </p>

### Exemplo

**Tabuleiro inicial**

```text
1 0 1
0 1 0
1 1 0
```

**Objetivo**

```text
0 0 0
0 0 0
0 0 0
```

## Funcionalidades

O programa permite:

* Escolher o tamanho do tabuleiro;
* Informar manualmente um tabuleiro;
* Gerar automaticamente tabuleiros solucionáveis;
* Construir automaticamente a matriz de influência;
* Resolver o sistema utilizando eliminação gaussiana módulo 2;
* Exibir o vetor solução;
* Exibir o mapa de jogadas;
* Mostrar a resolução passo a passo;
* Validar o resultado final;
* Utilizar diferentes regras de vizinhança;
* Exportar automaticamente os resultados para arquivo TXT.

## Regras de Vizinhança

### Ortogonal

Afeta:

* própria célula;
* acima;
* abaixo;
* esquerda;
* direita.

### Diagonal

Afeta:

* própria célula;
* diagonais.

### Completa

Afeta:

* própria célula;
* vizinhos ortogonais;
* vizinhos diagonais.

# Implementação em Python

A versão em Python foi desenvolvida com foco em simplicidade, legibilidade e facilidade de execução.

## Principais Características

* Eliminação gaussiana módulo 2;
* Entrada manual de matrizes;
* Geração automática de tabuleiros;
* Resolução passo a passo;
* Regras alternativas de vizinhança;
* Compatível com Windows, Linux e macOS.

## Arquivo Principal

```text
lights_out_solver.py
```

## Pré-requisitos

Instalar Python 3.10 ou superior.

### Verificar instalação

```bash
python --version
```

ou

```bash
python3 --version
```

## Execução

No terminal:

```bash
python lights_out_solver.py
```

ou

```bash
python3 lights_out_solver.py
```

## Exemplo de Entrada

```text
Tamanho do tabuleiro: 3

Escolha a regra de vizinhança:
1 - Ortogonal padrão
2 - Diagonal
3 - Completa

Opção: 1

Escolha a forma de criação do tabuleiro:
1 - Digitar o tabuleiro manualmente
2 - Gerar o tabuleiro automaticamente com solução

Opção: 1

Linha 1: 1 0 1
Linha 2: 0 1 0
Linha 3: 1 1 0
```

## Exemplo de Saída

```text
TABULEIRO INICIAL
1 0 1
0 1 0
1 1 0

VETOR b
1 0 1 0 1 0 1 1 0

MAPA DE JOGADAS
1 = pressionar | 0 = não pressionar

0 1 1
0 0 1
0 1 0

TABULEIRO FINAL
0 0 0
0 0 0
0 0 0

Validação: todas as luzes foram apagadas.
```

# Implementação em Julia

A versão em Julia mantém a mesma lógica matemática da implementação em Python, explorando recursos voltados para computação científica e oferecendo interface gráfica.

## Principais Características

* Eliminação gaussiana módulo 2;
* Interface gráfica com Gtk.jl;
* Entrada manual de tabuleiros;
* Geração automática de tabuleiros solucionáveis;
* Resolução passo a passo;
* Exportação automática dos resultados para TXT;
* Regras alternativas de vizinhança.

## Arquivo Principal

```text
lights_out_solver.jl
```

## Pré-requisitos

Instalar Julia 1.10 ou superior.

### Verificar instalação

```bash
julia --version
```

## Instalação das Dependências

Abrir o terminal Julia:

```bash
julia
```

Executar:

```julia
import Pkg
Pkg.add("Gtk")
```

## Execução

No terminal:

```bash
julia lights_out_solver.jl
```

## Exemplo de Entrada

```text
Tamanho do tabuleiro: 3

Regra de vizinhança:
1 - Ortogonal
2 - Diagonal
3 - Completa

Opção: 1

Modo:
1 - Manual
2 - Automático

Opção: 2
```

## Exemplo de Saída

```text
TABULEIRO INICIAL
0 0 1
0 1 1
1 0 1

VETOR SOLUÇÃO x
1 1 0 0 0 0 1 0 1

MAPA DE JOGADAS
1 1 0
0 0 0
1 0 1

RESOLUÇÃO PASSO A PASSO

Jogada 1
Pressionar posição (1,1)

...

TABULEIRO FINAL
0 0 0
0 0 0
0 0 0

Validação: todas as luzes foram apagadas.

Resultado salvo automaticamente em resultado_lights_out.txt
```

## Método Matemático Utilizado

O problema é modelado pelo sistema linear:

```text
Ax = b (mod 2)
```

onde:

* **A** representa a matriz de influência;
* **x** representa o vetor de jogadas;
* **b** representa o estado inicial do tabuleiro.

A solução é obtida por meio da eliminação gaussiana módulo 2, utilizando:

1. Busca de pivô;
2. Troca de linhas;
3. Eliminação;
4. Retro-substituição.

Todas as operações são realizadas em módulo 2.


