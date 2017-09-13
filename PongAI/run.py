import random
import plotly
import numpy as np
from PongAI.game import game
from PongAI.ai import always_goes_up, random_direction, follows_ball, neural_network
from PongAI.gui import display

DISPLAY = display.Display()

POPULATION_SIZE = 100
MUTATION_CHANCE = 0.05

# Generate initial population
POPULATION = []
for i in range(POPULATION_SIZE):
    POPULATION.append(neural_network.NeuralNetwork())

GENERATION = 0
while 1:
    # Tournament
    NEXT_POPULATION = []
    FITNESSES = []
    for i, v in enumerate(POPULATION):
        if i % 2 == 0:
            left_player = POPULATION[i]
            right_player = POPULATION[i + 1]
            current_game = game.PongGame(left_player, right_player, GENERATION)
            winner = current_game.start(DISPLAY)
            if winner[0] == game.Players.Left:
                NEXT_POPULATION.append(left_player)
            else:
                NEXT_POPULATION.append(right_player)
            FITNESSES.append(winner[1] ** 2)
    BEST_NETWORK = NEXT_POPULATION[FITNESSES.index(max(FITNESSES))]

    #  Refill Population
    CHILDREN = []
    HIGHEST_FITNESS = max(FITNESSES)
    DISPLAY.highest_fitnesses.append(HIGHEST_FITNESS)
    AVERAGE_FITNESS = sum(FITNESSES) / len(FITNESSES)
    DISPLAY.average_fitnesses.append(AVERAGE_FITNESS)

    print("Generation: " + str(GENERATION))
    print("Highest fitness: " + str(HIGHEST_FITNESS))
    print("Average fitness: " + str(AVERAGE_FITNESS))

    while len(NEXT_POPULATION) + len(CHILDREN) < POPULATION_SIZE - 5:
        s = sum(FITNESSES)
        selection_probabilities = [float(i) / s for i in FITNESSES]

        # Select two parents
        parent_a = np.random.choice(NEXT_POPULATION, p=selection_probabilities)
        parent_b = np.random.choice(NEXT_POPULATION, p=selection_probabilities)

        child = neural_network.NeuralNetwork()
        child.syn0 = np.array(parent_a.syn0)
        child.syn1 = np.array(parent_b.syn1)
        child.syn2 = np.array(parent_a.syn2)

        CHILDREN.append(child)
    NEXT_POPULATION.extend(CHILDREN)
    for i in range(5):
        NEXT_POPULATION.append(neural_network.NeuralNetwork())

    # Mutate
    for network in POPULATION:
        for row, _ in enumerate(network.syn0):
            for synapse, _ in enumerate(network.syn0[row]):
                if random.random() < MUTATION_CHANCE:
                    network.syn0[row][synapse] = 2 * random.random() - 1
        for row, _ in enumerate(network.syn1):
            for synapse, _ in enumerate(network.syn0[row]):
                if random.random() < MUTATION_CHANCE:
                    network.syn1[row][synapse] = 2 * random.random() - 1
        for row, _ in enumerate(network.syn0):
            for synapse, _ in enumerate(network.syn2[row]):
                if random.random() < MUTATION_CHANCE:
                    network.syn2[row][synapse] = 2 * random.random() - 1

    NEXT_POPULATION[0] = BEST_NETWORK

    GENERATION += 1
    POPULATION = list(NEXT_POPULATION)
