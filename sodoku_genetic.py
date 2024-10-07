import numpy as np
import random

BOARD_SIZE = 9  # 9x9 Sudoku

given_board = [0, 0, 0, 0, 0, 8, 0, 0, 0,
               0, 9, 0, 0, 0, 0, 6, 0, 0,
               0, 0, 4, 0, 6, 0, 3, 0, 0,
               7, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 3, 0, 0, 2, 6, 0, 0, 5,
               0, 0, 1, 0, 9, 5, 2, 0, 0, 
               8, 0, 0, 0, 4, 7, 5, 9, 0,
               0, 0, 0, 0, 0, 0, 0, 3, 0,
               0, 5, 2, 0, 0, 0, 0, 7, 8]
given_values = np.array(given_board).reshape(BOARD_SIZE, BOARD_SIZE)

class Board:
    def __init__(self, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
            for i in range(BOARD_SIZE):
                row = list(range(1, 10))
                for j in range(BOARD_SIZE):
                    if given_values[i, j] != 0:
                        row.remove(given_values[i, j])
                np.random.shuffle(row)
                for j in range(BOARD_SIZE):
                    if given_values[i, j] != 0:
                        self.board[i, j] = given_values[i, j]
                    else:
                        self.board[i, j] = row.pop()
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        fitness = 0
        for i in range(BOARD_SIZE):
            fitness += len(set(self.board[i])) + len(set(self.board[:, i]))
        for i in range(0, BOARD_SIZE, 3):
            for j in range(0, BOARD_SIZE, 3):
                fitness += len(set(self.board[i:i+3, j:j+3].flatten()))
        return fitness

    def mutate(self):
        for _ in range(5):  # Perform multiple mutations
            row = random.randint(0, BOARD_SIZE - 1)
            col1, col2 = random.sample(range(BOARD_SIZE), 2)
            while given_values[row, col1] != 0 or given_values[row, col2] != 0:
                col1, col2 = random.sample(range(BOARD_SIZE), 2)
            self.board[row, col1], self.board[row, col2] = self.board[row, col2], self.board[row, col1]
        self.fitness = self.calculate_fitness()

def crossover(parent1, parent2):
    child = Board()
    for i in range(BOARD_SIZE):
        if random.random() < 0.5:
            child.board[i] = parent1.board[i]
        else:
            child.board[i] = parent2.board[i]
    child.fitness = child.calculate_fitness()
    return child

def genetic_algorithm(population_size=10000, num_generations=1000, mutation_rate=0.2):
    population = [Board() for _ in range(population_size)]
    for generation in range(num_generations):
        population.sort(key=lambda x: x.fitness, reverse=True)
        best = population[0]
        if best.fitness == 27 * BOARD_SIZE:
            print(f"Solution found in generation {generation}")
            return best
        
        if generation % 10 == 0:
            print(f"Generation {generation}: Best fitness = {best.fitness}")
        
        new_population = population[:population_size // 10]  # Keep top 10%
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:population_size // 2], 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child.mutate()
            new_population.append(child)
        population = new_population
    
    print("No solution found")
    return population[0]

best_solution = genetic_algorithm()
print("Best solution:")
print(best_solution.board)
print(f"Fitness: {best_solution.fitness}")