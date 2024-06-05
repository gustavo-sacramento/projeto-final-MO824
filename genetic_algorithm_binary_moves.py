import math
from config.parser import parser
from random import randint, choice
from utils.plotter import plot

def start(obstacles, path_points, grid):
    population = generate_population(grid)
    path_lengths = []

    for chromosome in population:
        path_lengths.append(len(chromosome))

    # plot(obstacles, path_points, population, path_lengths, 1, False)

    generations = int(parser['Genetic Algorithm']['max_generations'])

    for gen in range(generations - 1):
        new_population = []
        path_lengths.clear()

        fitness_list = sort_by_fitness(population, grid)

        for chromosome in population:
            while True:
                parent1 = choose_random_parent(fitness_list)
                parent2 = choose_random_parent(fitness_list)

                child = crossover(parent1, parent2)

                if randint(1, 10) <= 10 * float(parser['Genetic Algorithm']['mutation_probability']):
                    child = mutation(child)

                if chromosome_valid(child, grid):
                    break
            
            path_lengths.append(len(child))
            new_population.append(child)

        # move_obstacles(obstacles, path_points)
        population = new_population
        print(path_lengths) 
        # plot(obstacles, path_points, new_population, path_lengths, (gen+2), last_gen=True if gen == generations-2 else False)


def move_obstacles(obstacles, path_points):
    index = randint(0, int(parser['Obstacles']['number_of_obstacles']) - 1)
    direction = randint(0, 3)
    factor = randint(1, 4)

    # 0 for left, 1 for right, 2 for up and 3 for down
    if direction == 0:
        for i in range(4):
            if obstacles[index][i][1] - factor >= 0:
                obstacles[index][i] = (obstacles[index][i][0] - factor, obstacles[index][i][1])  
    
    elif direction == 1:
        for i in range(4):
            if obstacles[index][i][1] + factor <= int(parser['Plot Axes']['x_end']):
                obstacles[index][i] = (obstacles[index][i][0] + factor, obstacles[index][i][1]) 
    
    elif direction == 2:
        for i in range(4):
            if obstacles[index][i][1] + factor <= int(parser['Plot Axes']['y_end']):
                obstacles[index][i] = (obstacles[index][i][0], obstacles[index][i][1] + factor) 
    
    elif direction == 3:
        for i in range(4):
            if obstacles[index][i][1] - factor >= 0:
                obstacles[index][i] = (obstacles[index][i][0], obstacles[index][i][1] - factor)

def mutation(chromosome):
    index = randint(0, len(chromosome) - 2) # we won't mutate last move, given we will always reach our destination
    valid_moves = set(['00', '01', '10', '11'])
    valid_moves.remove(chromosome[index])

    chromosome[index] = choice(list(valid_moves))

    return chromosome

def fitness(chromosome, grid):
    length = len(chromosome)
    fitness = 1 / length if length != 0 else 0

    return fitness

def sort_by_fitness(population, grid):
    fitness_list = []

    for chromosome in population:
        chromosome_to_fitness = (chromosome, fitness(chromosome, grid))
        fitness_list.append(chromosome_to_fitness)

    fitness_list.sort(reverse=True, key=lambda tuple: tuple[1])

    return fitness_list

def choose_random_parent(fitness_list):
    till_index = len(fitness_list) * float(parser['Genetic Algorithm']['top_percentage'])
    till_index = math.floor(till_index)

    parent_to_fitness = fitness_list[randint(0, till_index)]

    return parent_to_fitness[0]

def crossover(parent1, parent2):

    if parser['Genetic Algorithm'].getboolean('crossover_split_random'):
        split_size = randint(0, len(parent1))

    else:
        fraction = float(parser['Genetic Algorithm']['crossover_split_size'])
        split_size = math.floor(fraction * len(parent1))

    return parent1[:split_size] + parent2[split_size:]

def generate_population(grid):
    population_size = int(parser['Genetic Algorithm']['population_size'])

    population = []
    print('Generating initial population, please wait ....')

    for _ in range(population_size):
        while True:
            chromosome = generate_chromosome(grid)
            if chromosome:
                break
            
        population.append(chromosome)

    print('Successfully created initial population')
    print('Simulating genetic algorithm for path planning .... (Press Ctrl+C to stop)')
    return population

def generate_chromosome(grid):
    chromosome = [] 
    visited = set()
    previous_path_point = (1, 1)
    visited.add((1, 1))

    while True:
        x, y = previous_path_point
        
        if grid[y][x] == 'F':
            break

        valid_moves = {}

        if x - 1 >= 1 and (x-1, y) not in visited and grid[y][x-1] != 'X':
            valid_moves['10'] = (x-1, y)
        if x + 1 < int(parser['Plot Axes']['x_end'])+1 and (x+1, y) not in visited and grid[y][x+1] != 'X':
            valid_moves['01'] = (x+1, y)
        if y - 1 >= 1 and (x, y-1) not in visited and grid[y-1][x] != 'X':
            valid_moves['00'] = (x, y-1)
        if y + 1 < int(parser['Plot Axes']['y_end'])+1 and (x, y+1) not in visited and grid[y+1][x] != 'X':
            valid_moves['11'] = (x, y+1)
        
        if not valid_moves:
            return False
        else:
            selected_move = choice(list(valid_moves.keys()))
            chromosome.append(selected_move)
            previous_path_point = valid_moves[selected_move]
            visited.add(previous_path_point)
    
    return chromosome

def chromosome_valid(chromosome, grid):
    path_point_1, path_point_2 = (1, 1), ()
    visited = set()
    visited.add((1, 1))

    for _, gene in enumerate(chromosome):
        x, y = path_point_1

        if gene == '00':    # move down
            y -= 1
        elif gene == '10':  # move left
            x -= 1
        elif gene == '01':  # move right
            x += 1
        else:               # move up
            y += 1

        #  If its in range and not looping
        if x > 0 and x < int(parser['Plot Axes']['x_end']) and y > 0 and y < int(parser['Plot Axes']['x_end']) and (x, y) not in visited:
            if grid[y][x] == 'X':
                return False
            
            path_point_2 = (x, y)
            visited.add(path_point_2)
            path_point_1 = path_point_2
            path_point_2 = ()
        else:
            return False
    
    return True

# def path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
#     path = LineString([path_point_1, path_point_2])

#     for obstacle in obstacles:

#         obstacle = Polygon(obstacle)
#         if path.intersects(obstacle):
#             return True

#     return False


def calculate_path_length(chromosome, path_points):  # We assume its a valid path
    path_point_1, path_point_2 = (1, 1), ()
    length = 0

    for i, gene in enumerate(chromosome):
        x, y = path_point_1

        if gene == '00':    # move down
            path_point_2 = (x, y-1)
        elif gene == '10':  # move left
            path_point_2 = (x-1, y)
        elif gene == '01':  # move right
            path_point_2 = (x+1, y)
        else:               # move up
            path_point_2 = (x, y+1)
        
        if path_point_1 and path_point_2:
            length += 1
            path_point_1 = path_point_2
            path_point_2 = ()

        return length

def _distance(path_point_1, path_point_2):
    return math.sqrt( (path_point_2[0] - path_point_1[0])**2 + (path_point_2[1] - path_point_1[1])**2 )