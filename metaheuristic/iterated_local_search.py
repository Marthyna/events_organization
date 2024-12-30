""" O entregável meta-heurística consiste em:
    a) Um código-fonte em qualquer linguagem (com instruções claras
    para compilação/instalação/execução em Linux) que toma um
    arquivo no formato de entrada dado e outros parâmetros (veja
    abaixo) e executa a meta-heurística. (preencher README.md)

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
    relatório. FEITO (fazer gráfico?)

    c) Além do nome do arquivo de entrada, o programa deve tomar
    na linha de comando quaisquer outros parâmetros cujos valores
    foram variados nos experimentos (idealmente por meio de argumentos 
    posicionais na linha de comando). Dentre esses argumentos, 
    obrigatoriamente, para todas as meta-heurísticas, devem se encontrar
    a semente de aleatoriedade (exceto se completamente determinística)
    e o valor que controla o critério de parada (número de iterações, ou 
    qualquer outro escolhido). FEITO

    d) O código não pode suportar somente o critério de parada por tempo. 
    Os experimentos exigem rodar o código por 5s e 300s, e para isso é útil
    um critério por tempo, porém nesse caso é necessário entregar algum outro
    critério determinístico (como número de iterações) que retorne exatamente
    a mesma solução.

    e) O código deve implementar a meta-heurística escolhida. Cada meta-heurística
    tem lacunas que variam com o problema e decisões de implementação que ficam
    a critério dos alunos, mas também tem partes que caracterizam ela como aquela
    meta-heurística (estas devem estar presentes no código). FEITO

    f) São critérios de avaliação da implementação da meta-heurística: a sua
    corretude, a sua legibilidade, a adequação a meta-heurística escolhida 
    (vide item acima), e a sua performance (especialmente no que tange a escolha
    de representação da solução, a exagerada criação novos objetos de solução ao
    invés de sua alteração, e o recálculo do valor da função objetivo do a partir
    zero ao invés de por delta).

    g) Esse programa deve ser exatamente o mesmo utilizado para escrita do 
    entregável relatório/experimentos.
"""

# ILS tries to avoid the disavantages of random restart by exploring S*
# using a walk that steps from s* to a "nearby" one.
# Given the current s*, we first apply a perturbation that leads to an
# intermediate state s' (which belongs to S). Then, LocalSearch is applied
# to s' and we reach a solution s*'. If s*' passes an acceptance test, then
# it becomes the next element of the walk in S*. Otherwise, one returns to
# s*.

# procedure IteratedLocalSearch:
#   s0 = GenerateInitialSolution
#   s* = LocalSearch(s0)
#   repeat
#     s' = Perturbation(s*, history)
#     s*' = LocalSearch(s')
#     s* = AcceptanceCriterion(s*, s*', history)
#   until TerminationCriterion
# end

# Much of the potential complexity of ILS lies in the history dependence.
# If there is none, the walk has no memory and perturbation and acceptance
# criterion do not depend on previously visited solution. One accepts or not
# s*' with a fixed rule. This is a random walk in S* that is Markovian, with
# the property that the probability of going from s1* to s2* depends only
# on them. Using memory enhances performance, but also increases complexity.

# GenerateInitialSolution: random
# LocalSearch
# Perturbation: random move to neighborhood of higher order than LocalSearch
# AcceptanceCriterion: force cost to decrease

import random
import time
from collections import defaultdict
import argparse


class IteratedLocalSearch:
    def __init__(self, file_path, seed, max_iterations=None, max_time=None) -> None:
        self.file_path = file_path
        self.seed = seed
        self.max_iterations = max_iterations
        self.max_time = max_time
        random.seed(self.seed)

    def __read_instance(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        self.n = int(lines[0].strip())  # number of spaces
        self.M = int(lines[1].strip())  # space size
        self.T = int(lines[2].strip())  # number of themes
        self.m = int(lines[3].strip())  # number of attractions

        attractions = []
        for i in range(4, 4 + self.m):
            theme_j, dim_j = map(int, lines[i].strip().split())
            attractions.append((theme_j, dim_j))

        self.themes = [attr[0] for attr in attractions]
        self.dimensions = [attr[1] for attr in attractions]

    def _termination_criterion(self, iteration, start_time=None):
        if self.max_iterations is not None:
            return iteration >= self.max_iterations
        elif self.max_time is not None:
            return time.time() - start_time >= self.max_time
        else:
            raise ValueError("No termination criterion specified.")

    def __calculate_dispersion(self, solution):
        theme_to_spaces = defaultdict(set)
        for space_idx, attractions in enumerate(solution):
            for attraction in attractions:
                theme_to_spaces[self.themes[attraction]].add(space_idx)
        return sum(len(spaces) for spaces in theme_to_spaces.values())

    def __is_feasible(self, solution):
        for space in solution:
            if sum(self.dimensions[attraction] for attraction in space) > self.M:
                return False
        return True

    def __generate_initial_solution(self):
        solution = [[] for _ in range(self.n)]
        used_space = [0] * self.n

        for idx, dimension in enumerate(self.dimensions):
            for space_idx in range(self.n):
                if used_space[space_idx] + dimension <= self.M:
                    solution[space_idx].append(idx)
                    used_space[space_idx] += dimension
                    break

        return solution

    def __generate_initial_solution_greedy(self):
        solution = [[] for _ in range(self.n)]
        attractions_by_theme = defaultdict(list)

        # group attractions by theme
        for attraction in range(self.m):
            attractions_by_theme[self.themes[attraction]].append(attraction)

        # allocate attractions prioritizing the same theme in the same space
        for theme, attractions in attractions_by_theme.items():
            for attraction in attractions:
                for space in solution:
                    if sum(self.dimensions[att] for att in space) + self.dimensions[attraction] <= self.M:
                        space.append(attraction)
                        break

        return solution

    def __local_search(self, solution):
        best_solution = solution
        best_dispersion = self.__calculate_dispersion(solution)

        for space_idx in range(len(solution)):
            for attraction in list(best_solution[space_idx]):
                for target_space in range(len(solution)):
                    if target_space != space_idx:

                        # Try moving an attraction
                        new_solution = [list(space) for space in best_solution]
                        if attraction in new_solution[space_idx]:
                            new_solution[space_idx].remove(attraction)
                        new_solution[target_space].append(attraction)

                        if self.__is_feasible(new_solution):
                            new_dispersion = self.__calculate_dispersion(new_solution)
                            if new_dispersion < best_dispersion:
                                best_solution = new_solution
                                best_dispersion = new_dispersion
        return best_solution

    def __perturbation(self, solution):
        perturbed_solution = [list(space) for space in solution]
        num_changes = random.randint(2, max(2, self.m // 3))

        for _ in range(num_changes):
            a = random.choice(range(self.m))  # random attraction

            src_space = next(
                (i for i, space in enumerate(perturbed_solution) if a in space), None
            )
            if src_space is None:
                continue

            dest_space = random.choice(range(self.n))

            # remove from current space
            perturbed_solution[src_space].remove(a)

            # try adding to the destination space
            if (
                    sum(self.dimensions[att] for att in perturbed_solution[dest_space])
                    + self.dimensions[a]
                    <= self.M
            ):
                perturbed_solution[dest_space].append(a)
            else:
                perturbed_solution[src_space].append(a)

        return perturbed_solution

    def __acceptance_criterion(self, current, new):
        return (
            new
            if self.__calculate_dispersion(new) < self.__calculate_dispersion(current)
            else current
        )

    def __termination_criterion(self, iteration):
        return iteration >= self.max_iterations

    def __format_solution(self, solution):
        formatted = "\n".join(
            f"  Espaço {i + 1}: {', '.join(map(str, attractions))}"
            for i, attractions in enumerate(solution)
        )
        return formatted

    def iterated_local_search(self):
        self.__read_instance()

        start_time = time.time()

        current_solution = self.__generate_initial_solution_greedy()
        current_solution = self.__local_search(current_solution)
        best_solution = current_solution
        best_dispersion = self.__calculate_dispersion(current_solution)
        print("Dispersão inicial:")
        print(best_dispersion)

        iteration = 0

        while not self._termination_criterion(iteration, start_time):
            perturbed_solution = self.__perturbation(current_solution)
            local_solution = self.__local_search(perturbed_solution)
            local_dispersion = self.__calculate_dispersion(local_solution)

            if local_dispersion < best_dispersion:
                best_solution = local_solution
                best_dispersion = local_dispersion
                elapsed_time = time.time() - start_time
                formatted_solution = self.__format_solution(best_solution)
                print(f"\n{elapsed_time:.2f}s | Dispersão: {best_dispersion}")
                print("Solução Atual:")
                print(formatted_solution)

            current_solution = self.__acceptance_criterion(current_solution, local_solution)
            iteration += 1

        return best_solution, best_dispersion


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Iterated Local Search for event organization."
    )
    parser.add_argument("file_path", type=str, help="Path to the instance file.")
    parser.add_argument("seed", type=int, help="Random seed for reproducibility.")
    parser.add_argument(
        "--termination-criterion",
        type=str,
        choices=["iterations", "time"],
        required=True,
        help="Choose termination criterion: 'iterations' or 'time'.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        help="Maximum number of iterations (required if termination criterion is 'iterations').",
    )
    parser.add_argument(
        "--max-time",
        type=float,
        help="Maximum time in seconds (required if termination criterion is 'time').",
    )

    args = parser.parse_args()

    if args.termination_criterion == "iterations" and args.max_iterations is None:
        parser.error("You must specify --max-iterations if termination criterion is 'iterations'.")
    if args.termination_criterion == "time" and args.max_time is None:
        parser.error("You must specify --max-time if termination criterion is 'time'.")

    ils = IteratedLocalSearch(
        file_path=args.file_path,
        seed=args.seed,
        max_iterations=args.max_iterations,
        max_time=args.max_time,
    )

    solution, dispersion = ils.iterated_local_search()
    formatted_solution = ils._IteratedLocalSearch__format_solution(solution)
    print("\nSolução Final:")
    print(formatted_solution)
    print(f"Dispersão Final: {dispersion}")
