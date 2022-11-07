import random
import math

def hasil(populasi):

    for i in populasi:
        print("\n")
        print("Kromosom : ", i.bit)
        print("X : ", i.x)
        print("Y : ", i.y)
        print("fitness : ", h(i.x, i.y))

    print("====== Best Generation ======")

def h(x, y):
    return (math.cos(x) + math.sin(y))**2 / (x**2 + y**2)

batas_bawahX = -5
batas_atasX = 5
batas_bawahY = -5
batas_atasY = 5


class Chromosome:
    def __init__(self):
        self.bit = random.choices([0, 1], k=8)
        self.x = self.decoding(batas_atasX, batas_bawahX, self.bit[:4])
        self.y = self.decoding(batas_atasY, batas_bawahY, self.bit[4:])

    def decoding(self, ra, rb, g):
        tp = [2**-i for i in range(1, len(g)+1)]
        return rb + ((ra-rb)/sum(tp)*sum([g[i]*tp[i] for i in range(len(g))]))


def f(x, y):
    hasil = h(x, y)
    return 1 / (hasil + 0.00000001)


def exist(l, c):
    found = False
    for i in l:
        if i.bit == c.bit:
            found = True
            break
    return found


def seleksi_parent(k):
    parent = []
    arr_fitness = list(map(lambda c: f(c.x, c.y), populasi))
    arr_weight = [arr_fitness[i] / sum(arr_fitness)
                  for i in range(len(populasi))]
    while len(parent) != k:
        kandidat = random.choices(populasi, weights=arr_weight)[0]
        if not exist(parent, kandidat):
            parent.append(kandidat)
    return parent


def crossover(ortu1, ortu2):
    posisi = random.randint(1, len(ortu1.bit) - 2)

    bit_chro1 = ortu1.bit[:posisi] + ortu2.bit[posisi:]
    bit_chro2 = ortu2.bit[:posisi] + ortu1.bit[posisi:]

    rng_mutasi = random.uniform(0, 100)
    if rng_mutasi > (100 - 0.5):
        posisi_mutasi = random.randint(0, len(bit_chro1) - 1)
        if bit_chro1[posisi_mutasi] == 1:
            bit_chro1[posisi_mutasi] = 0
        else:
            bit_chro1[posisi_mutasi] = 1

    rng_mutasi = random.uniform(0, 100)
    if rng_mutasi > (100 - 0.5):
        posisi_mutasi = random.randint(0, len(bit_chro2) - 1)
        if bit_chro2[posisi_mutasi] == 1:
            bit_chro2[posisi_mutasi] = 0
        else:
            bit_chro2[posisi_mutasi] = 1


def seleksi_survivor():
    populasi.sort(key=lambda c: h(c.x, c.y))

    while len(populasi) != 100:
        populasi.pop()


populasi = []
generasi = 1
while len(populasi) != 100:
    c = Chromosome()
    if not exist(populasi, c):
        populasi.append(c)
seleksi_survivor()
hasil(populasi)


while generasi < 100:
    parent = seleksi_parent(2)
    crossover(parent[0], parent[1])
    seleksi_survivor()

    generasi += 1
    hasil(populasi)
