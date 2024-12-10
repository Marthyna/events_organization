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

FILE_1 = "../inf05010_2024-2_B_TP_instances_organizacao-de-eventos/01.txt"

function ler_arquivo(path)
    open(path, r) do file
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
    mo = Model(HiGHS.Optimizer)

    # n espaços com M tamanho
    # m atrações
    # tj: temática da atração j, j = 1, ..., m
    # dj: dimensão da atração j, j = 1, ..., m
    n, M, T, m, atracoes = ler_arquivo(FILE_1)

    # xij: 1 se a atração j é alocada no espaço i, 0 caso contrário
    @variable(mo, x[1:n, 1:m], Bin)

    # a dispersão de uma temática j é o número de espaços distintos que têm ao menos uma atração de j
    @variable(mo, dispersao[1:T])

    # TODO: definir a dispersão

    # cada atração só pode ser alocada em um espaço
    @constraint(mo, [j = 1:m], sum(x[i, j] for i in 1:n) == 1)

    # sum dj * xij <= M, para todo i = 1, ..., n
    @constraint(mo, [i = 1:n], sum(atracoes[j][2] * x[i, j] for j in 1:m) <= M)

    # minimizar a dispersão somada de todas as tematicas
    @objective(mo, Min, sum(dispersao))

end


#   1 2 3 4 atracoes
# 1 0 1 0 0
# 2 0 0 1 0
# 3 1 0 0 1
# espaços

# 