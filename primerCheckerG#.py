import sys

# Recibe el k número hasta donde llegara a comprobar primos
k = int(sys.argv[1])

paquetes = []

# número de paquetes de 100 en 100 números que se repartiran entre los workers
num_paquetes = int(k/100)

for i in range(1, num_paquetes + 1):
    paquete = 100 * i
    paquetes.append(paquete)

def primeCheck(num):
    divisores = 0
    for i in range(2, num):
        if num % i == 0:
            divisores += 1
            break

    if divisores == 0:
        return True
    else:
        return False