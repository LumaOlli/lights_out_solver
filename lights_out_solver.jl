using Random
using Gtk

function indice(i, j, n)
    return (i - 1) * n + j
end

function obter_direcoes(tipo)
    if tipo == 1
        return [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    elseif tipo == 2
        return [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    elseif tipo == 3
        return [
            (0, 0),
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
    else
        error("Tipo de vizinhança inválido.")
    end
end

function gerar_tabuleiro_automatico(n)
    return rand(0:1, n, n)
end

function construir_matriz_influencia(n, direcoes)
    tamanho = n * n
    A = zeros(Int, tamanho, tamanho)

    for i in 1:n
        for j in 1:n
            coluna = indice(i, j, n)

            for (di, dj) in direcoes
                ni = i + di
                nj = j + dj

                if 1 <= ni <= n && 1 <= nj <= n
                    linha = indice(ni, nj, n)
                    A[linha, coluna] = 1
                end
            end
        end
    end

    return A
end

function vetorizar_tabuleiro(tabuleiro)
    n = size(tabuleiro, 1)
    vetor = Int[]

    for i in 1:n
        for j in 1:n
            push!(vetor, tabuleiro[i, j] % 2)
        end
    end

    return vetor
end

function eliminacao_gaussiana_mod2(A, b)
    linhas = size(A, 1)
    colunas = size(A, 2)

    matriz = hcat(copy(A), b .% 2)

    linha_pivo = 1
    colunas_pivo = Int[]

    for coluna in 1:colunas
        pivo = 0

        for linha in linha_pivo:linhas
            if matriz[linha, coluna] == 1
                pivo = linha
                break
            end
        end

        if pivo == 0
            continue
        end

        if pivo != linha_pivo
            temp = copy(matriz[linha_pivo, :])
            matriz[linha_pivo, :] = matriz[pivo, :]
            matriz[pivo, :] = temp
        end

        for linha in (linha_pivo + 1):linhas
            if linha <= linhas && matriz[linha, coluna] == 1
                for k in coluna:(colunas + 1)
                    matriz[linha, k] =
                        (matriz[linha, k] + matriz[linha_pivo, k]) % 2
                end
            end
        end

        push!(colunas_pivo, coluna)
        linha_pivo += 1

        if linha_pivo > linhas
            break
        end
    end

    for linha in 1:linhas
        coeficientes_zeros = all(
            matriz[linha, coluna] == 0
            for coluna in 1:colunas
        )

        termo_um = matriz[linha, colunas + 1] == 1

        if coeficientes_zeros && termo_um
            return nothing, matriz, colunas_pivo
        end
    end

    solucao = zeros(Int, colunas)

    for i in length(colunas_pivo):-1:1
        coluna_pivo = colunas_pivo[i]
        soma = 0

        for coluna in (coluna_pivo + 1):colunas
            if coluna <= colunas
                soma = (
                    soma + matriz[i, coluna] * solucao[coluna]
                ) % 2
            end
        end

        solucao[coluna_pivo] = (
            matriz[i, colunas + 1] + soma
        ) % 2
    end

    return solucao, matriz, colunas_pivo
end

function resolver_tabuleiro(tabuleiro, tipo_vizinhanca)
    n = size(tabuleiro, 1)
    direcoes = obter_direcoes(tipo_vizinhanca)

    A = construir_matriz_influencia(n, direcoes)
    b = vetorizar_tabuleiro(tabuleiro)

    solucao, matriz_escalonada, colunas_pivo =
        eliminacao_gaussiana_mod2(A, b)

    return A, b, solucao, matriz_escalonada, colunas_pivo
end

function aplicar_jogada!(tabuleiro, i, j, direcoes)
    n = size(tabuleiro, 1)

    for (di, dj) in direcoes
        ni = i + di
        nj = j + dj

        if 1 <= ni <= n && 1 <= nj <= n
            tabuleiro[ni, nj] = (tabuleiro[ni, nj] + 1) % 2
        end
    end
end

function matriz_para_texto(matriz)
    texto = ""

    for i in 1:size(matriz, 1)
        linha = join(matriz[i, :], " ")
        texto *= linha * "\n"
    end

    return texto
end

function vetor_para_texto(vetor)
    return join(vetor, " ")
end

function vetor_como_tabuleiro(vetor, n)
    tabuleiro = zeros(Int, n, n)

    for i in 1:n
        for j in 1:n
            tabuleiro[i, j] = vetor[indice(i, j, n)]
        end
    end

    return tabuleiro
end

function gerar_tabuleiro_com_solucao(n, tipo_vizinhanca)
    tentativas = 0

    while true
        tentativas += 1
        tabuleiro = gerar_tabuleiro_automatico(n)

        _, _, solucao, _, _ =
            resolver_tabuleiro(tabuleiro, tipo_vizinhanca)

        if solucao !== nothing
            return tabuleiro, tentativas
        end
    end
end

mutable struct AppState
    n::Int
    tabuleiro::Matrix{Int}
    botoes::Vector{GtkButton}
    grid::GtkGrid
    saida::GtkTextView
    tamanho_combo::GtkComboBoxText
    vizinhanca_combo::GtkComboBoxText
end

function atualizar_botoes!(estado)
    for botao in estado.botoes
        destroy(botao)
    end

    empty!(estado.botoes)

    for i in 1:estado.n
        for j in 1:estado.n
            botao = GtkButton(string(estado.tabuleiro[i, j]))
            set_gtk_property!(botao, :width_request, 60)
            set_gtk_property!(botao, :height_request, 50)

            signal_connect(botao, "clicked") do widget
                estado.tabuleiro[i, j] =
                    (estado.tabuleiro[i, j] + 1) % 2

                set_gtk_property!(
                    widget,
                    :label,
                    string(estado.tabuleiro[i, j])
                )
            end

            push!(estado.botoes, botao)
            estado.grid[j - 1, i - 1] = botao
        end
    end

    showall(estado.grid)
end

function escrever_saida!(estado, texto)
    buffer = GtkTextBuffer()
    set_gtk_property!(buffer, :text, texto)
    set_gtk_property!(estado.saida, :buffer, buffer)
end

function criar_tabuleiro_vazio!(estado)
    tamanho_texto = Gtk.bytestring(
        GAccessor.active_text(estado.tamanho_combo)
    )

    estado.n = parse(Int, tamanho_texto)
    estado.tabuleiro = zeros(Int, estado.n, estado.n)

    atualizar_botoes!(estado)
    escrever_saida!(estado, "Tabuleiro vazio criado.\n")
end

function gerar_automatico!(estado)
    tamanho_texto = Gtk.bytestring(
        GAccessor.active_text(estado.tamanho_combo)
    )

    vizinhanca_texto = Gtk.bytestring(
        GAccessor.active_text(estado.vizinhanca_combo)
    )

    estado.n = parse(Int, tamanho_texto)
    tipo_vizinhanca = parse(Int, vizinhanca_texto[1])

    tabuleiro, tentativas =
        gerar_tabuleiro_com_solucao(estado.n, tipo_vizinhanca)

    estado.tabuleiro = tabuleiro
    atualizar_botoes!(estado)

    texto = "Tabuleiro solucionável gerado automaticamente.\n"
    texto *= "Tentativas: $tentativas\n"

    escrever_saida!(estado, texto)
end

function resolver_interface!(estado)
    vizinhanca_texto = Gtk.bytestring(
        GAccessor.active_text(estado.vizinhanca_combo)
    )

    tipo_vizinhanca = parse(Int, vizinhanca_texto[1])
    direcoes = obter_direcoes(tipo_vizinhanca)

    A, b, solucao, matriz_escalonada, colunas_pivo =
        resolver_tabuleiro(estado.tabuleiro, tipo_vizinhanca)

    texto = ""

    texto *= "==============================\n"
    texto *= "TABULEIRO INICIAL\n"
    texto *= "==============================\n"
    texto *= matriz_para_texto(estado.tabuleiro)

    texto *= "\n==============================\n"
    texto *= "MATRIZ DE INFLUÊNCIA A\n"
    texto *= "==============================\n"
    texto *= matriz_para_texto(A)

    texto *= "\n==============================\n"
    texto *= "VETOR b\n"
    texto *= "==============================\n"
    texto *= vetor_para_texto(b) * "\n"

    texto *= "\n==============================\n"
    texto *= "MATRIZ AUMENTADA ESCALONADA\n"
    texto *= "==============================\n"
    texto *= matriz_para_texto(matriz_escalonada)

    texto *= "\nPosto da matriz A: "
    texto *= string(length(colunas_pivo)) * "\n"

    if solucao === nothing
        texto *= "\nEste tabuleiro não possui solução.\n"
        texto *= "Não há combinação de jogadas capaz de zerar o jogo.\n"
        escrever_saida!(estado, texto)
        return
    end

    mapa = vetor_como_tabuleiro(solucao, estado.n)

    texto *= "\n==============================\n"
    texto *= "VETOR SOLUÇÃO x\n"
    texto *= "==============================\n"
    texto *= vetor_para_texto(solucao) * "\n"

    texto *= "\n==============================\n"
    texto *= "MAPA DE JOGADAS\n"
    texto *= "==============================\n"
    texto *= "1 = pressionar | 0 = não pressionar\n"
    texto *= matriz_para_texto(mapa)

    tabuleiro_atual = copy(estado.tabuleiro)
    contador = 1

    texto *= "\n==============================\n"
    texto *= "RESOLUÇÃO PASSO A PASSO\n"
    texto *= "==============================\n"

    for posicao in eachindex(solucao)
        if solucao[posicao] == 1
            i = div(posicao - 1, estado.n) + 1
            j = mod(posicao - 1, estado.n) + 1

            texto *= "\nJogada $contador\n"
            texto *= "Pressionar posição ($i, $j)\n"

            aplicar_jogada!(tabuleiro_atual, i, j, direcoes)

            texto *= "\nTabuleiro após a jogada:\n"
            texto *= matriz_para_texto(tabuleiro_atual)

            contador += 1
        end
    end

    texto *= "\n==============================\n"
    texto *= "TABULEIRO FINAL\n"
    texto *= "==============================\n"
    texto *= matriz_para_texto(tabuleiro_atual)

    if all(x -> x == 0, tabuleiro_atual)
        texto *= "\nValidação: todas as luzes foram apagadas.\n"
    else
        texto *= "\nValidação: a solução não zerou o tabuleiro.\n"
    end

    escrever_saida!(estado, texto)
end

function criar_interface()
    janela = GtkWindow(
        "Solucionador Lights Out - Julia",
        1200,
        900
    )

    caixa_principal = GtkBox(:v)
    push!(janela, caixa_principal)

    painel_superior = GtkBox(:h)
    push!(caixa_principal, painel_superior)

    push!(painel_superior, GtkLabel("Tamanho:"))

    tamanho_combo = GtkComboBoxText()
    push!(tamanho_combo, "3")
    push!(tamanho_combo, "4")
    push!(tamanho_combo, "5")
    set_gtk_property!(tamanho_combo, :active, 0)
    push!(painel_superior, tamanho_combo)

    push!(painel_superior, GtkLabel("Vizinhança:"))

    vizinhanca_combo = GtkComboBoxText()
    push!(vizinhanca_combo, "1 - Ortogonal")
    push!(vizinhanca_combo, "2 - Diagonal")
    push!(vizinhanca_combo, "3 - Completa")
    set_gtk_property!(vizinhanca_combo, :active, 0)
    push!(painel_superior, vizinhanca_combo)

    botao_vazio = GtkButton("Criar tabuleiro vazio")
    botao_auto = GtkButton("Gerar automático")
    botao_resolver = GtkButton("Resolver")

    push!(painel_superior, botao_vazio)
    push!(painel_superior, botao_auto)
    push!(painel_superior, botao_resolver)

    grid = GtkGrid()
    push!(caixa_principal, grid)

    saida = GtkTextView()

    set_gtk_property!(saida, :editable, false)
    set_gtk_property!(saida, :monospace, true)
    set_gtk_property!(saida, :wrap_mode, 0)

    scroll = GtkScrolledWindow()

    set_gtk_property!(scroll, :vexpand, true)
    set_gtk_property!(scroll, :hexpand, true)
    set_gtk_property!(scroll, :height_request, 420)
    set_gtk_property!(scroll, :width_request, 850)

    push!(scroll, saida)
    push!(caixa_principal, scroll)

    estado = AppState(
        3,
        zeros(Int, 3, 3),
        GtkButton[],
        grid,
        saida,
        tamanho_combo,
        vizinhanca_combo
    )

    signal_connect(botao_vazio, "clicked") do widget
        criar_tabuleiro_vazio!(estado)
    end

    signal_connect(botao_auto, "clicked") do widget
        gerar_automatico!(estado)
    end

    signal_connect(botao_resolver, "clicked") do widget
        resolver_interface!(estado)
    end

    criar_tabuleiro_vazio!(estado)

    showall(janela)
end

criar_interface()
Gtk.gtk_main()