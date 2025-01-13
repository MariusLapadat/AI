import random
import time
import numpy as np

import tsplib95


def flip(bit):
    return 1 if bit == 0 else 0


def readTxt():
    index_list = []
    value_list = []
    weight_list = []

    with open('rucsac-200.txt', 'r') as f:
        line_number = int(f.readline().strip())
        for _ in range(line_number):
            line = f.readline().strip().split()
            numbers = [int(x) for x in line]
            index_list.append(numbers[0])
            value_list.append(numbers[1])
            weight_list.append(numbers[2])
        data_list = [index_list, value_list, weight_list]

        #        for i in range(line_number):
        #            print(data_list[0][i], data_list[1][i], data_list[2][i])

        max_weight = int(f.readline().strip())
        # print(max_weight)
        return line_number, data_list, max_weight


def generate(len: int):
    random_list = []
    for _ in range(len):
        random_list.append(random.randint(0, 1))
    # print(random_list)
    return random_list


def validate(data_list: list, max_weight: int, random_list: list):
    current_weight = 0
    current_value = 0
    for i in range(len(random_list)):
        if random_list[i] == 1:
            # print(str(i)+" "+str(data_list[2][i]))
            current_weight += data_list[2][i]
            current_value += data_list[1][i]
    # print(current_weight)
    if current_weight <= max_weight:
        return current_value
    return -1


def population_value(data_list, max_weight, population):
    population_values = []
    for individual in population:
        individual_value = validate(data_list, max_weight, individual)
        population_values.append(individual_value)
    return population_values


def population_initialization(pop_size, line_number):
    population = []
    for _ in range(pop_size):
        solution = generate(line_number)
        population.append(solution)
    return population


def tournament_selection(population, tournament_size, popvalue):
    # Filtrăm lista de indivizi care au fitness diferit de -1
    individuals_with_valid_fitness = [i for i, value in enumerate(popvalue) if value != -1]

    # Selecția aleatorie a indivizilor din lista filtrată
    selected_individuals = random.sample(individuals_with_valid_fitness, tournament_size)

    best_guy = None
    best_value = float('-inf')  # Initializeaza cu un fitness negativ infinit
    for i in selected_individuals:
        if popvalue[i] > best_value:
            best_guy = population[i]
            best_value = popvalue[i]
    return best_guy


def crossover(parent1, parent2):
    # Selectăm un punct de tăiere aleator
    crossover_point = random.randint(1, len(parent1) - 1)

    # Combinăm genele părinților pentru a crea descendenții
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def mutation(individual, mutation_chance):
    mutated_individual = list(individual)
    for i in range(len(mutated_individual)):
        if random.randint(1, 100) <= mutation_chance:
            # Se efectuează mutația: inversarea valorii genei la un indice invers
            mutated_individual[i] = flip(mutated_individual[i])
    return mutated_individual


def get_smallest_non_negative(popvalue):
    for value in reversed(popvalue):
        if value != -1:
            return value
    return None


def evo_alg(pop_size, num_gen, mutation_chance):
    start_time = time.time()
    line_number, data_list, max_weight = readTxt()
    population = population_initialization(pop_size, line_number)
    popvalue = population_value(data_list, max_weight, population)
    for _ in range(num_gen):
        selected_parents = []
        # Selectarea părinților
        for _ in range(pop_size // 2):
            parent = tournament_selection(population, 5, popvalue)
            selected_parents.append(parent)
        # print('nr parinti',len(selected_parents))
        # Reproducerea (încrucișare și mutație)
        new_generation = []
        for i in range(len(selected_parents)):
            parent1 = selected_parents[i]
            parent2 = selected_parents[(i + 1) % len(
                selected_parents)]  # Utilizăm operația modulo pentru a accesa primul parinte în cazul ultimului parinte
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, mutation_chance)
            child2 = mutation(child2, mutation_chance)
            new_generation.append(child1)
            new_generation.append(child2)
        # print('nr indivizi noua gen',len(new_generation))

        # Evaluarea și selecția noii generații
        popvalue = population_value(data_list, max_weight, new_generation)
        for i in range(len(popvalue) - 1):
            for j in range(i + 1, len(popvalue)):
                if popvalue[i] < popvalue[j]:
                    popvalue[i], popvalue[j] = popvalue[j], popvalue[i]
                    new_generation[i], new_generation[j] = new_generation[j], new_generation[i]
        population = new_generation.copy()
    # print(len(popvalue))

    sum = 0
    for i in range(len(popvalue)):
        sum += popvalue[i]

    worst = get_smallest_non_negative(popvalue)
    end_time = time.time()
    runtime = end_time - start_time
    with open("rez1.txt", "a") as file:
        file.write("Marime populatie: " + str(pop_size) + "\n")
        file.write("Numar generatii: " + str(num_gen) + "\n")
        file.write("Sansa mutatie genetica: " + str(mutation_chance) + "\n")
        file.write("Best: " + str(popvalue[0]) + "\n")
        file.write("Avg: " + str(sum / len(popvalue)) + "\n")
        file.write("Worst: " + str(worst) + "\n")
        file.write("Timpul de rulare: " + str(runtime) + "\n\n")
    return popvalue


#######################################################################################


def calculate_distance(coords, node1, node2):
    x1, y1 = coords[node1]
    x2, y2 = coords[node2]
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluate_chromosome(chromosome, coords):
    dist = 0
    for i in range(len(chromosome)):
        dist += calculate_distance(coords, chromosome[i - 1], chromosome[i])
    return dist


def generate_random_chromosome(nodes):
    chromosome = list(nodes)
    random.shuffle(chromosome)
    return chromosome


def generate_initial_population(nodes, population_size):
    population = []
    for _ in range(population_size):
        chromosome = generate_random_chromosome(nodes)
        population.append(chromosome)
    return population


def evaluate_population(population, coords):
    distances = []
    for chromosome in population:
        distance = evaluate_chromosome(chromosome, coords)
        distances.append(distance)
    return distances


def selection(population, distances):
    selected_parents = []
    for _ in range(len(population)):
        # Selectează un părinte în funcție de distanța asociată
        index = distances.index(min(distances))
        selected_parents.append(population[index])
        # Setează distanța selectată ca infinit pentru a nu fi selectată din nou
        distances[index] = float('inf')
    return selected_parents


def crossovertsp(parents):
    offsprings = []
    for parent1, parent2 in zip(parents[::2], parents[1::2]):  # Iterăm prin părinții în perechi (de la 0 la lungimea listei, cu pasul 2)
        # Aplicăm crossover
        crossover_point = random.randint(0, len(parent1))
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        offsprings.extend([child1, child2])
    return offsprings


def mutationtsp(offsprings, mutation_chance):
    for offspring in offsprings:
        if random.randint(1, 100) <= mutation_chance:
            # Aplică o mutație asupra cromozomului (de exemplu, schimbând două orașe în rută)
            index1, index2 = random.sample(range(len(offspring)), 2)
            offspring[index1], offspring[index2] = offspring[index2], offspring[index1]
    return offsprings


def update_population(offsprings):
    # Înlocuiește populația veche cu noua populație (offsprings)
    return offsprings


def evo_alg_tsp(pop_size, num_gen, mutation_chance):
    start_time = time.time()
    problem = tsplib95.load_problem("eil76.tsp")
    best_solution = None
    best_distance = float('inf')
    all_distances = []

    nodes = list(problem.get_nodes())
    coords = problem.node_coords

    population = generate_initial_population(nodes, pop_size)
    distances = evaluate_population(population, coords)

    for _ in range(num_gen):
        parents = selection(population, distances)
        offsprings = crossovertsp(parents)
        offsprings = mutationtsp(offsprings, mutation_chance)
        population = update_population(offsprings)
        distances = evaluate_population(population, coords)

        best_solution_index = distances.index(min(distances))
        current_solution = population[best_solution_index]
        current_distance = min(distances)

        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance
            #print(best_distance)

        all_distances.append(current_distance)
    print(best_distance)
    avg_distance = sum(all_distances) / len(all_distances)
    end_time = time.time()
    runtime = end_time - start_time

    with open("rez2.txt", "a") as file:
        file.write("Marime populatie: " + str(pop_size) + "\n")
        file.write("Numar generatii: " + str(num_gen) + "\n")
        file.write("Sansa mutatie genetica: " + str(mutation_chance) + "\n")
        file.write("Best: " + str(best_distance) + "\n")
        file.write("Avg: " + str(avg_distance) + "\n")
        file.write("Timpul de rulare: " + str(runtime) + "\n\n")

    return best_distance, avg_distance


'''
def tsp_problem():
    start_time = time.time()
    tabu_percentage = 0.2
    max_tabu_size = int(k * tabu_percentage / 100)
    # print("Initial solution:")
    # initial_solution = generate_initial_solution(problem.get_nodes())
    # print(initial_solution)
    # print("Initial distance:", total_distance(initial_solution, problem.node_coords))

    best_solution, best_distance, avg_distance = tabu_search_tsp(problem, k, max_tabu_size)
    # print("\nBest solution found by Tabu Search:")
    # print(best_solution)
    # print("Total distance:", best_distance)

    end_time = time.time()
    runtime = end_time - start_time

    with open("rez2.txt", "a") as file:
        file.write("Parametru k numar iteratii: " + str(k) + "\n")
        file.write("Distanta maxima: " + str(best_distance) + "\n")
        file.write("Valoarea medie: " + str(avg_distance) + "\n")
        file.write("Timpul de rulare: " + str(runtime) + "\n\n")
'''
