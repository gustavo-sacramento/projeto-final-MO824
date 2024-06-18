from genetic_algorithm import start, is_valid_path
import parameters

def main():
    # Mantém o valor inicial da validade dos caminhos
    # Será utilizado na hora de gerar a população inicial
    # para que ela só tenha cromossomos válidos

    for i, initial_point in enumerate(parameters.points):

        if initial_point not in path_validity:
            path_validity[initial_point] = [True] * parameters.num_points

        for j, final_point in enumerate(parameters.points):

            if final_point not in path_validity:
                path_validity[final_point] = [True] * parameters.num_points

            if is_valid_path(initial_point, final_point, parameters.obstacles):
                path_validity[initial_point][j] = False
                path_validity[final_point][i] = False

    start(path_validity)


path_validity = {}
main()
