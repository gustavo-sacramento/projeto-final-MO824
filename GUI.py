import time
import parameters
import genetic_algorithm as ga
import matplotlib.pyplot as plt

def plot(start, obstacles, points, population, path_lengths, generation, is_last_generation, optimal_solution_time): 
    for i, chromosome in enumerate(population):
        refresh(obstacles, points)
        x, y = [], []

        for j, gene in enumerate(chromosome):
            if gene == '1':
                x.append(points[j][0])
                y.append(points[j][1])

        current_time = time.time()

        plt.plot(x, y, '-')
        plt.text(1, parameters.y_end + 1, f"Geração: {generation}, Cromossomo: {i + 1}\nDistância: {round(path_lengths[i], 3)}\nTempo de execução total: {round(current_time - start, 3)} s")

        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(0.02)
    
    if is_last_generation:
        plot_final(start, obstacles, points, population, path_lengths, generation, optimal_solution_time)

def plot_final(start, obstacles, points, population, path_lengths, generation, optimal_solution_time):
    min_valid_length = 10**5
    min_index = 0
    x, y = [], []

    for i in range(len(path_lengths)):
        if ga.is_valid_chromosome(population[i], obstacles, points) and min_valid_length > path_lengths[i]:
            min_valid_length = path_lengths[i]
            min_index = i

    plt.ioff()
    refresh(obstacles, points)
    
    chromosome = population[min_index]

    for j, gene in enumerate(chromosome):
        if gene == '1':
            x.append(points[j][0])
            y.append(points[j][1])
    
    end = time.time()

    plt.plot(x, y, '-')
    plt.text(1, parameters.y_end+1, f"Última geração: {generation}\nCaminho mínimo encontrado: {round(path_lengths[min_index], 3)}\nTempo de execução total: {round(end - start, 3)} s")
    plt.pause(1)
    
    print("Tempo de execução total: ", round(end - start, 3), " s")
    print("Solução ótima encontrada em: ", round(optimal_solution_time, 3), " s")
    plt.show()

def refresh(obstacles, points):
    plt.clf()
    plt.axis([parameters.x_start, parameters.x_end, parameters.y_start, parameters.y_end])

    plot_obstacles(obstacles)
    plot_points(points)
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.subplots_adjust(top=0.8)

def plot_obstacles(obstacles):
    # Gera os retângulos no plano
    for obstacle in obstacles:
        x, y = [], []

        for i,j in obstacle:
            x.append(i)
            y.append(j)
        
        plt.fill(x, y, 'p')

def plot_points(points):
    # Gera os pontos no plano
    x, y = [], []

    for i,j in points:
        x.append(i)
        y.append(j)

    plt.plot(x[1:-1], y[1:-1], "k.")
    plt.plot(x[0], y[0], "bo", label='Origem')
    plt.plot(x[-1], y[-1], "go", label='Destino')
    plt.legend(loc="upper left")

plt.ion()