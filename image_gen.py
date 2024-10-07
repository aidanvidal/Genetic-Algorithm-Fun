# A genetic algorithm to generate images from shapes using pygame
import numpy as np
import random
import pygame
random.seed()

# Set the number of shapes to draw
N_SHAPES = 300

# Set the target image
TARGET = pygame.image.load("goomba.webp")

# Get the dimensions of the target image
TARGET_WIDTH, TARGET_HEIGHT = TARGET.get_size()
WIDTH, HEIGHT = TARGET_WIDTH, TARGET_HEIGHT

# Get RGB values of the target image
TARGET = pygame.surfarray.array3d(TARGET)

# The Shape class represents a single shape in the image
class Shape:
    def __init__(self):
        # Randomly select the shape type (0 = circle, 1 = rectangle, 2 = triangle)
        self.type = random.randint(0, 2)
        
        # Randomly select the color of the shape
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Randomly select the position of the shape
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        
        # Randomly select the size of the shape
        self.size = random.randint(10, 50)
        
        # Randomly select the rotation of the shape
        self.rotation = random.randint(0, 360)
        
    def draw(self, screen):
        if self.type == 0:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        elif self.type == 1:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        elif self.type == 2:
            pygame.draw.polygon(screen, self.color, [(self.x, self.y), (self.x + self.size, self.y), (self.x + self.size // 2, self.y + self.size)])
            

class Chromosome:
    def __init__(self):
        # The genes is an array of shapes
        self.genes = [Shape() for _ in range(N_SHAPES)]
        
    def fitness(self):
        # Calculate the fitness of the chromosome
        # The fitness is the rgb difference between the target image and the generated image
        
        # Generate the image from the genes
        image = pygame.Surface((WIDTH, HEIGHT))
        image.fill((255, 255, 255))
        # Draw the shapes
        for shape in self.genes:
            shape.draw(image)
        # Convert the image to a numpy array
        image = pygame.surfarray.array3d(image)
        # Calculate the fitness
        return np.sum(np.abs(image - TARGET))
            
    def mutate(self):
        if random.random() < 0.5:
            return
        # Randomly mutate one of the genes 
        original_fitness = self.fitness()
        original_genes = self.genes.copy()
        while self.fitness() >= original_fitness:
            self.genes = original_genes.copy()
            i = random.randint(0, N_SHAPES-1)
            self.genes[i] = Shape()
    
    def save_image(self, filename):
        # Save the image to a file
        image = pygame.Surface((WIDTH, HEIGHT))
        image.fill((255, 255, 255))
        for shape in self.genes:
            shape.draw(image)
        pygame.image.save(image, filename)
        
# Create a population of chromosomes
population = [Chromosome() for _ in range(50)]
num_elites = 10
best = None
# Run the genetic algorithm for 1000 generations
for generation in range(1000):
    # Sort the population by fitness
    population.sort(key=lambda x: x.fitness())
    
    # Print the best fitness in each generation
    print(f"Generation {generation}: {population[0].fitness()}")
    best = population[0]
    # Break if the fitness is less than error tolerance
    if population[0].fitness() <= 100000:
        break
    
    # Select the elites
    elites = population[:num_elites]
    
    # Generate the children
    children = []
    for _ in range(len(population) - num_elites):
        # Randomly select two parents
        parent1, parent2 = random.sample(elites, 2)
        
        # Crossover the parents
        child = Chromosome()
        child.genes = parent1.genes.copy()
        for i in range(N_SHAPES):
            if random.random() < 0.5:
                child.genes[i] = parent1.genes[i]
            else:
                child.genes[i] = parent2.genes[i]
        
        # Mutate the child
        child.mutate()
        children.append(child)
    new_population = elites + children
    population = new_population
    
# Save the best image to a file
best_image = "best_image.png"
best_chromosome = population[0]
best_chromosome.save_image(best_image)

# Display the best image
screen = pygame.display.set_mode((WIDTH, HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255, 255, 255))
    for shape in best.genes:
        shape.draw(screen)
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
        