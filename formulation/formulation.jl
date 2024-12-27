""" O entregável formulação inteira consiste em:
(a) Um código-fonte em qualquer linguagem (com instruções claras
para compilação/instalação/execução em Linux) que toma um arquivo no
formato de entrada dado, a semente de aleatoriedade (para passar ao 
solucionador, não para a RNG da linguagem), e o limite de tempo 
(em segundos), e utiliza uma formulação inteira e o solucionador 
HiGHS para resolver o problema.

(b) O HiGHS é o solucionador recomendado mas outros solucionadores
podem ser utilizados caso seja a preferência dos alunos. 

(c) Uma execução deve escrever na saída padrão as informações usadas
para montar a tabela do relatório (melhor solução encontrada, tempo, etc...).

(d) São critérios de avaliação da implementação da formulação inteira: 
a sua corretude, a sua legibilidade, o emprego do que aprendido na
disciplina, e decisões que levam a formulação a ter mais ou menos
variáveis e ser mais apertada ou mais frouxa.

(e) Essa formulação deve ser exatamente a mesma utilizada para escrita
do entregável relatório/experimentos."""

import Pkg
Pkg.activate(@__DIR__)
Pkg.instantiate()

using JuMP
using HiGHS
using Dates

function ler_arquivo(path)
    open(path, "r") do file
        n = parse(Int, readline(file))
        M = parse(Int, readline(file))
        T = parse(Int, readline(file))
        m = parse(Int, readline(file))

        atracoes = []
        for i in 1:m
            line = split(readline(file))
            tematica = parse(Int, line[1])
            dimensao = parse(Int, line[2])
            push!(atracoes, (tematica, dimensao))
        end
        return n, M, T, m, atracoes
    end
end

function main()
    if length(ARGS) < 3
        println("Erro: Forneça o caminho do arquivo, a semente de aleatoriedade e o limite de tempo.")
        return
    end

    file_path = ARGS[1]
    seed = parse(Int, ARGS[2])
    time_limit = parse(Float64, ARGS[3])

    mo = Model(HiGHS.Optimizer)
    set_optimizer_attribute(mo, "random_seed", seed)
    set_optimizer_attribute(mo, "time_limit", time_limit)

    n, M, T, m, atracoes = ler_arquivo(file_path)

    # Variáveis:
    @variable(mo, x[1:m, 1:n], Bin)  # x[i, j] = 1 se a atração i está no espaço j
    @variable(mo, y[1:T, 1:n], Bin) # y[t, j] = 1 se temática t aparece no espaço j

    # Restrições:
    @constraint(mo, [i = 1:m], sum(x[i, j] for j in 1:n) == 1) # Cada atração é alocada em exatamente um espaço
    @constraint(mo, [j = 1:n], sum(atracoes[i][2] * x[i, j] for i in 1:m) <= M) # A soma das dimensões das atrações em um espaço não pode ultrapassar sua capacidade

    # y[t, j] = U x[i, j] para todo i em At, sendo At o conjunto de atrações da temática t
    # y[t, j] >= x[i, j] / |At| para todo i em At
    for t in 1:T
        atracoes_tem = [i for i in 1:m if atracoes[i][1] == t]
        @constraint(mo, [j = 1:n], y[t, j] >= sum(x[i, j] for i in atracoes_tem) / length(atracoes_tem))
    end

    # Obejtivo: minimizar a dispersão total
    @objective(mo, Min, sum(y[t, j] for t in 1:T, j in 1:n))

    start_time = now()
    optimize!(mo)
    end_time = now()
    tempo_usado = end_time - start_time
    println("Tempo de execução: $tempo_usado")

    if has_values(mo)
        melhor_solucao = objective_value(mo)

        println("Melhor solução encontrada: $melhor_solucao")

        println("Atrações alocadas por espaço:")
        for j in 1:n
            atracoes_alocadas = [i for i in 1:m if value(x[i, j]) > 0.5]
            println("Espaço $j: $atracoes_alocadas")
        end

        println("Dispersão por temática:")
        dispersao = [value(sum(y[t, j] for j in 1:n)) for t in 1:T]
        for t in 1:T
            println("Temática $t: dispersão = $(dispersao[t])")
        end
    else
        println("Não foi possível encontrar uma solução viável dentro do limite de tempo.")
    end

end

main()
