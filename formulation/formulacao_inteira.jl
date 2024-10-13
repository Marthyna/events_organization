# O entregável formulação inteira consiste em:
#    a) Um código-fonte em qualquer linguagem (com instruções claras 
#    para compilação/instalação/execução em Linux) que toma um 
#    arquivo no formato de entrada dado, a semente de aleatoriedade 
#    (para passar ao solucionador (no caso de Julia/JuMP/HiGHS, a 
#    semente de aleatoriedade do solucionador pode ser definida com 
#    set attribute(model, "random seed", seed parametro)), não para
#    a RNG da linguagem), e o limite de tempo (em segundos), e 
#    utiliza uma formulação inteira e o solucionador HiGHS para 
#    resolver o problema.

#    b) O HiGHS é o solucionador recomendado mas outros solucionadores
#    podem ser utilizados caso seja a preferância dos alunos.

#    c) Uma execução deve escrever na saída padrão as informações 
#    usadas para montar a tabela do relatório (melhor solução 
#    encontrada, tempo, etc...).

#    d) São critérios de avaliação da implementação da formulação 
#    inteira: a sua corretude, a sua legibilidade, o emprego do que
#    aprendido na disciplina, e decisões que levam a formulação a ter
#    mais ou menos variáveis e ser mais apertada ou mais frouxa.

#    e) Essa formulação deve ser exatamente a mesma utilizada para 
#    escrita do entregável relatório/experimentos.

using JuMP
using HiGHS
m = Model(HiGHS.Optimizer)
set_attribute(m, "random seed", seed_parametro)