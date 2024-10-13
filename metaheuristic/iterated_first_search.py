""" O entregável meta-heurística consiste em:
    a) Um código-fonte em qualquer linguagem (com instruções claras
    para compilação/instalação/execução em Linux) que toma um
    arquivo no formato de entrada dado e outros parâmetros (veja
    abaixo) e executa a meta-heurística.

    b) Após a geração da solução inicial, e toda a vez que a
    implementação encontra uma solução melhor que a melhor conhecida
    até o momento, esta deve escrever na saída padrão: 
        (i) a quantidade de segundos (com duas casas após a vírgula)
        desde o começo da execução; 
        (ii) o valor dessa solução; 
        (iii) uma representação da mesma que seja possível de ser 
        compreendida por um ser humano. 
    Além disso, a implementação também deve escrever na saída padrão
    quaisquer outras informações usadas para montagem das tabelas do
    relatório.

    c) Além do nome do arquivo de entrada, o programa deve tomar
    na linha de comando quaisquer outros parâmetros os quais os valores
    foram variados nos experimentos (idealmente por meio de argumentos 
    posicionais na linha de comando). Dentre esses argumentos, 
    obrigatoriamente, para todas as meta-heurísticas, devem se encontrar
    a semente de aleatoriedade (exceto se completamente determinística)
    e o valor que controla o critério de parada (número de iterações, ou 
    qualquer outro escolhido).

    d) O código não pode suportar somente o critério de parada por tempo. 
    Os experimentos exigem rodar o código por 5s e 300s, e para isso é útil
    um critério por tempo, porém nesse caso é necessário entregar algum outro
    critério determinístico (como número de iterações) que retorne exatamente
    a mesma solução.

    e) O código deve implementar a meta-heurística escolhida. Cada meta-heurística
    tem lacunas que variam com o problema e decisões de implementação que ficam
    a critério dos alunos, mas também tem partes que caracterizam ela como aquela
    meta-heurística (estas devem estar presentes no código).

    f) São critérios de avaliação da implementação da meta-heurística: a sua
    corretude, a sua legibilidade, a adequação a meta-heurística escolhida 
    (vide item acima), e a sua performance (especialmente no que tange a escolha
    de representação da solução, a exagerada criação novos objetos de solução ao
    invés de sua alteração, e o recálculo do valor da função objetivo do a partir
    zero ao invés de por delta).

    g) Esse programa deve ser exatamente o mesmo utilizado para escrita do 
    entregável relatório/experimentos.
"""