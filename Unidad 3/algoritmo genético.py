import random
import numpy as np

# Parámetros
tam = 100
p_c = 0.9
p_m = 0.1
gens = 150

# Datos base
nodos = [
    "Bilbao", "Celta", "Vigo", "Valladolid", "Jaen", "Sevilla", "Granada", "Murcia",
    "Valencia", "Barcelona", "Gerona", "Zaragoza", "Madrid", "Albacete"
]
idx = {n: i for i, n in enumerate(nodos)}

# Matriz de pesos
mat = np.inf * np.ones((len(nodos), len(nodos)))

# Aristas
conex = [
    ("Bilbao", "Celta", 378), ("Bilbao", "Zaragoza", 324), ("Celta", "Vigo", 171), ("Celta", "Valladolid", 235),
    ("Vigo", "Valladolid", 356), ("Vigo", "Sevilla", 245), ("Valladolid", "Madrid", 193),
    ("Valladolid", "Zaragoza", 390), ("Valladolid", "Jaen", 411),
    ("Jaen", "Sevilla", 125), ("Jaen", "Granada", 207), ("Sevilla", "Granada", 211),
    ("Granada", "Murcia", 257), ("Murcia", "Albacete", 150), ("Murcia", "Valencia", 241),
    ("Valencia", "Albacete", 191), ("Valencia", "Barcelona", 349), ("Barcelona", "Zaragoza", 296),
    ("Barcelona", "Gerona", 100), ("Zaragoza", "Gerona", 289), ("Zaragoza", "Madrid", 190),
    ("Zaragoza", "Albacete", 215), ("Madrid", "Albacete", 251), ("Albacete", "Granada", 244)
]

# Grafo
g = {i: [] for i in range(len(nodos))}

for a, b, d in conex:
    i, j = idx[a], idx[b]
    mat[i][j] = mat[j][i] = d
    g[i].append(j)
    g[j].append(i)

# Evaluación
def f(x):
    s = 0
    for i in range(len(x)):
        a = x[i]
        b = x[(i + 1) % len(x)]
        if b not in g[a]:
            return np.inf
        s += mat[a][b]
    return s

# Generación de individuo válido
def gen_ind():
    while True:
        r = [random.choice(list(g.keys()))]
        v = set(r)
        while len(r) < len(nodos):
            cands = [n for n in g[r[-1]] if n not in v]
            if not cands:
                break
            n = random.choice(cands)
            r.append(n)
            v.add(n)
        if len(r) == len(nodos) and r[0] in g[r[-1]]:
            return r

# Población inicial
def gen_pop(n):
    return [gen_ind() for _ in range(n)]

# Aptitud
def eval_pop(p):
    return [1 / f(ind) for ind in p]

# Selección
def sel(pop, fits, k=3):
    s = random.sample(list(zip(pop, fits)), k)
    s.sort(key=lambda x: x[1], reverse=True)
    return s[0][0]

# Cruce
def crz(x, y):
    if random.random() > p_c:
        return x[:], y[:]
    i, j = sorted(random.sample(range(len(x)), 2))
    h = [-1]*len(x)
    h[i:j] = x[i:j]
    rem = [n for n in y if n not in h]
    it = iter(rem)
    for k in range(len(h)):
        if h[k] == -1:
            h[k] = next(it)
    if chk(h):
        return h, crz(y, x)[0]
    return x[:], y[:]

# Mutación
def mut(x):
    if random.random() < p_m:
        i, j = random.sample(range(len(x)), 2)
        y = x[:]
        y[i], y[j] = y[j], y[i]
        if chk(y):
            return y
    return x

# Validez
def chk(r):
    for i in range(len(r)):
        if r[(i + 1) % len(r)] not in g[r[i]]:
            return False
    return True

# Algoritmo principal
P = gen_pop(tam)
for it in range(gens):
    F = eval_pop(P)
    best = min(P, key=lambda x: f(x))
    d = f(best)
    ruta = [nodos[i] for i in best]
    print(f"Gen {it+1}: Dist = {d} | Ruta: {' -> '.join(ruta)}")
    nueva = []
    while len(nueva) < tam:
        a = sel(P, F)
        b = sel(P, F)
        h1, h2 = crz(a, b)
        nueva.append(mut(h1))
        if len(nueva) < tam:
            nueva.append(mut(h2))
    P = nueva

# Final
final = min(P, key=lambda x: f(x))
final_dist = f(final)
ruta_final = [nodos[i] for i in final]

print("\nRuta final:")
print(" -> ".join(ruta_final))
print(f"Distancia: {final_dist}")
