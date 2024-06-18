from random import randint
import time
import parameters
import math
from shapely.geometry import Polygon, LineString
from GUI import plot

def start(path_validity):
    # Define um caminho minimo inicial grande
    start = time.time()
    shortest_path = 10**5
    optimal_solution_time = start
    lock_count = 0
    population = create_population(parameters.points, path_validity)
    path_lengths = []
    new_index = 0

    for chromosome in population:
        path_lengths.append(get_path_length(chromosome, parameters.points))

    plot(start, parameters.obstacles, parameters.points, population, path_lengths, 1, False, optimal_solution_time)

    for generation in range(parameters.max_generations - 1):
        if lock_count > 10:
            if is_valid_chromosome(population[new_index], parameters.obstacles, parameters.points):
                plot(start, parameters.obstacles, parameters.points, new_population, path_lengths, generation, True, optimal_solution_time)
                break
            else:
                lock_count = 0
                new_index = 0

        new_population = []
        path_lengths.clear()

        fitness_list = fitness_sort(population, parameters.obstacles, parameters.points)
        
        for i in range(len(population)):
            chromosome = population[i]

            # while not is_valid_chromosome(str(chromosome), obstacles, points):
            #     chromosome = create_chromosome(points, path_validity)
            
            # population[i] = chromosome

            if parameters.move_obstacles:
                parent1 = get_random_chromosome(fitness_list)
                parent2 = get_random_chromosome(fitness_list)

                child = crossover(parent1, parent2)

                if randint(1, 10) <= parameters.mutation_prob * 10:
                    child = mutation(child)
                
                path_lengths.append(get_path_length(child, parameters.points))
                new_population.append(child)

            else:
                while True:
                    parent1 = get_random_chromosome(fitness_list)
                    parent2 = get_random_chromosome(fitness_list)

                    child = crossover(parent1, parent2)

                    if randint(1, 10) <= parameters.mutation_prob * 10:
                        child = mutation(child)

                    if is_valid_chromosome(child, parameters.obstacles, parameters.points):
                        break
                    
                path_lengths.append(get_path_length(child, parameters.points))
                new_population.append(child)

        if parameters.num_obstacles > 0 and parameters.move_obstacles:
            move_obstacles(parameters.obstacles)

        population = new_population 

        if generation == parameters.max_generations - 2:
            plot(start, parameters.obstacles, parameters.points, new_population, path_lengths, generation + 2, True, optimal_solution_time)
        else:
            plot(start, parameters.obstacles, parameters.points, new_population, path_lengths, generation + 2, False, optimal_solution_time)

        for i in range(len(path_lengths)):
            if is_valid_chromosome(population[i], parameters.obstacles, parameters.points) and shortest_path > path_lengths[i]:
                new_shortest_path = path_lengths[i]
                new_index = i

        if new_shortest_path == shortest_path:
            lock_count += 1
        else:
            lock_count = 0
            shortest_path = new_shortest_path
            optimal_solution_time = time.time() - start

def move_obstacles(obstacles):
    index = randint(0, parameters.num_obstacles - 1)
    direction = randint(0, 3)
    factor = 0

    if parameters.x_end > 50:
        factor = randint(0, 3)
    else:
        factor = randint(0, 1)

    # 0 para esquerda, 1 para a direita, 2 para cima e 3 para baixo
    if factor > 0:
        if direction == 0:
            for i in range(4):
                if obstacles[index][i][0] - factor > 1:
                    obstacles[index][i] = (obstacles[index][i][0] - factor, obstacles[index][i][1])
                else:
                    break  
        
        elif direction == 1:
            for i in range(4):
                if obstacles[index][i][0] + factor < parameters.x_end:
                    obstacles[index][i] = (obstacles[index][i][0] + factor, obstacles[index][i][1]) 
                else:
                    break
        
        elif direction == 2:
            for i in range(4):
                if obstacles[index][i][1] + factor < parameters.y_end:
                    obstacles[index][i] = (obstacles[index][i][0], obstacles[index][i][1] + factor)
                else:
                    break 
        
        elif direction == 3:
            for i in range(4):
                if obstacles[index][i][1] - factor > 1:
                    obstacles[index][i] = (obstacles[index][i][0], obstacles[index][i][1] - factor)
                else:
                    break

def mutation(chromosome):
    index = randint(1, len(chromosome) - 2)
    chromosome = list(chromosome)

    if chromosome[index] == '0':
        chromosome[index] = '1'
    else:
        chromosome[index] = '0'

    return ''.join(chromosome)

def get_fitness(chromosome, obstacles, points):
    if not is_valid_chromosome(chromosome, obstacles, points):
        return 0
    
    length = get_path_length(chromosome, points)
    
    if length == 0:
        return 0
    else:
        return 1 / length

def get_random_chromosome(fitness_list):
    candidates_cut_index = len(fitness_list) * parameters.top_percentage
    candidates_cut_index = math.floor(candidates_cut_index)

    return fitness_list[randint(0, candidates_cut_index)][0]

def fitness_sort(population, obstacles, points):
    sorted = []

    for chromosome in population:
        sorted.append((chromosome, get_fitness(chromosome, obstacles, points)))

    sorted.sort(reverse=True, key=lambda tuple: tuple[1])

    return sorted

def crossover(parent1, parent2):
    index = math.floor(parameters.cross_point * len(parent1))

    return ''.join([parent1[:index], parent2[index:]])

def _crossover2(parent1, parent2, points, obstacles):
    size_p1 = len(parent1)
    crossover_points = []
    match_points = []
    children = []

    for i in range(1, size_p1 - 2):
        for j in range(1, size_p1 - 2):
            if (parent1[i+1] == '1' and parent2[j] == '1') and (parent1[i] == '1' and parent2[j+1] == '1'):
                if not is_valid_path(points[i+1], points[j], obstacles) and not is_valid_path(points[i], points[j+1], obstacles):
                    crossover_points.append(i)
                    match_points.append(j)

    print(crossover_points, match_points)
    return parent1

def create_population(points, path_validity):
    population = []
   
    for _ in range(parameters.population_size):
        # Gera uma população de caminhos válidos
        while True:
            chromosome = create_chromosome(points, path_validity)

            if chromosome:
                break
            
        population.append(chromosome)

    return population

def create_chromosome(points, path_validity):
    # Sempre começamos visitando a origem
    chromosome = '1'
    previous_point = points[0]
    
    for i in range(1, len(points)):
        point = points[i]

        if i == (len(points) - 1) and not path_validity[previous_point][i]:
            return False

        if path_validity[previous_point][i]:

            if i == (len(points) - 1):
                gene = '1'
            else:
                gene = '0' if randint(1, 10) > 5 else '1'

            if gene == '1':
                previous_point = point
            
            chromosome += gene

        else:
            chromosome += '0'

    return chromosome

def is_valid_chromosome(chromosome, obstacles, points):
    point1, point2 = (), ()

    # Usamos o fato de que todos os cromossomos tem o mesmo tamanho
    # Para ter uma referência do indíce de cada ponto em points
    for i, gene in enumerate(chromosome):
        if gene == '1':

            if not point1:
                point1 = points[i] 
            else:
                point2 = points[i]

            if point1 and point2:

                if is_valid_path(point1, point2, obstacles):
                    return False

                point1 = point2
                point2 = ()
    
    return True

def is_valid_path(point1, point2, obstacles):
    path = LineString([point1, point2])

    for obstacle in obstacles:
        obstacle = Polygon(obstacle)

        if path.intersects(obstacle):
            return True

    return False


def get_path_length(chromosome, points):
    point1, point2 = (), ()
    length = 0

    for i, gene in enumerate(chromosome):
        if gene == '1':
            if not point1:
                point1 = points[i] 
            else:
                point2 = points[i]

            if point1 and point2:

                length += get_distance(point1, point2)

                point1 = point2
                point2 = ()

    return length

def get_distance(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]

    return math.sqrt((x_diff ** 2) + (y_diff ** 2))