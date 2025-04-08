import random

def generate_individual(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def fitness(individual):
    # Cuenta cuántos pares de reinas se atacan
    n = len(individual)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if individual[i] == individual[j] or abs(individual[i] - individual[j]) == abs(i - j):
                attacks += 1
    return attacks

def mutate(x1, x2, x3, F, n):
    # Mutación adaptada al dominio discreto
    mutant = []
    for i in range(n):
        val = int(x1[i] + F * (x2[i] - x3[i]))
        val = max(0, min(n - 1, val))  # Clamp
        mutant.append(val)
    return mutant

def crossover(target, mutant, CR):
    n = len(target)
    trial = []
    for i in range(n):
        if random.random() < CR or i == random.randint(0, n - 1):
            trial.append(mutant[i])
        else:
            trial.append(target[i])
    return trial

def differential_evolution(n, pop_size=100, F=0.5, CR=0.9, max_gen=1000):
    population = [generate_individual(n) for _ in range(pop_size)]

    for gen in range(max_gen):
        for i in range(pop_size):
            idxs = list(range(pop_size))
            idxs.remove(i)
            r1, r2, r3 = random.sample(idxs, 3)

            mutant = mutate(population[r1], population[r2], population[r3], F, n)
            trial = crossover(population[i], mutant, CR)

            if fitness(trial) <= fitness(population[i]):
                population[i] = trial

            if fitness(population[i]) == 0:
                print(f"Solución encontrada en la generación {gen}: {population[i]}")
                return population[i]

    print("No se encontró solución exacta.")
    return min(population, key=fitness)

# Ejemplo: resolver el problema de las 8 reinas
solution = differential_evolution(n=8)
print("Solución final:", solution)
