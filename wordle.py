import numpy as np
import random
random.seed()

# Set the target word in uppercase
WORD = "WORDLE"

def fitness(guess):
    # +1 for each letter in the word, +2 for each letter in the right position
    # Total of 2*len(WORD) for a perfect match + len(WORD) for each letter in the right position
    return 2*len([1 for i in range(len(WORD)) if guess[i] == WORD[i]]) + len([1 for i in guess if guess.count(i) <= WORD.count(i)])

def mutate(guess):
    # Randomly swap two letters in the guess 
    # Or randomly change one letter in the guess
    guess = list(guess)
    if random.random() < 0.5:
        i, j = random.sample(range(len(guess)), 2)
        guess[i], guess[j] = guess[j], guess[i]
    else:
        i = random.randint(0, len(guess)-1)
        guess[i] = chr(random.randint(65, 90))
        
    return "".join(guess)

def crossover(guess1, guess2):
    # Randomly select a crossover point and swap the two guesses at that point
    i = random.randint(0, len(guess1)-1)
    return guess1[:i] + guess2[i:]

def genetic_algorithm():
    # Generate a random population of 100 guesses using only uppercase letters
    population = ["".join([chr(random.randint(65, 90)) for _ in range(len(WORD))]) for _ in range(100)]
    
    # Run the genetic algorithm for 1000 generations
    for generation in range(1000):
        # Calculate the fitness of each guess
        scores = [fitness(guess) for guess in population]
        
        # Select the top 10% of guesses
        top = [population[i] for i in np.argsort(scores)[-10:]]
        
        # Generate the next generation
        new_population = []
        for i in range(100):
            # Randomly select two guesses from the top 10% of guesses
            guess1, guess2 = random.sample(top, 2)
            
            # Crossover the two guesses
            new_guess = crossover(guess1, guess2)
            
            # Mutate the new guess
            new_guess = mutate(new_guess)
            
            # Add the new guess to the new population
            new_population.append(new_guess)
        
        # Update the population
        population = new_population
        
        # Print the best guess in each generation
        print("Generation", generation, "Best guess:", max(population, key=fitness), "Fitness:", max(scores))
        
        # Check if the best guess is the target word
        if max(scores) == 2*len(WORD) + len(WORD):
            print("Found the word in", generation, "generations")
            break
        
    # Print the best guess after 1000 generations
    print("Best guess after 1000 generations:", max(population, key=fitness), "Fitness:", max(scores))
    
genetic_algorithm()