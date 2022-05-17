from mpi4py import MPI
from utils import primeCheck, cantPrimos
import sys
import time

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')

# Recibe el k número hasta donde llegara a comprobar primos
k = int(sys.argv[1])

paquetes = []

# número de paquetes de 100 en 100 números que se repartiran entre los workers
num_paquetes = int(k/100)

for i in range(1, num_paquetes + 1):
    paquete = 100 * i
    paquetes.append(paquete)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()   # get MPI status object

paquetes_verificados = 0
numero_primos = 0

if rank == 0:
    inicio = time.perf_counter()
    task_index = 0
    num_workers = size - 1
    closed_workers = 0

    print("Se utilizaran {} workers".format(num_workers))
    print("Se utilizaran {} paquetes para dividir el trabajo".format(num_paquetes))
    while closed_workers < num_workers:
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == tags.READY:
                # Worker is ready, so send it a task
                if task_index < len(paquetes):
                    comm.send(paquetes[task_index], dest=source, tag=tags.START)
                    print("Enviando paquete {} al worker {}".format(task_index, source))
                    task_index += 1
                else:
                    comm.ssend(None, dest=source, tag=tags.EXIT)
        elif tag == tags.DONE:
            numero_primos += data
        elif tag == tags.EXIT:
            closed_workers += 1

    fin = time.perf_counter()
    print("Administrador reportando resultados totales!!")
    print("Cantidad de números primos encontrados {}".format(numero_primos))
    print("El tiempo tomado para finalizar el proceso fue de {:.4f} s".format(fin - inicio))
else:
    # Worker processes execute code below
    print("Worker {} listo para trabajar!!".format(rank))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        task = comm.recv(source=0, tag=MPI.ANY_SOURCE, status=status)
        tag = status.Get_tag()

        if tag == tags.START:
            # Do the work here
            result = cantPrimos(task - 100, task +1)
            paquetes_verificados += 1
            comm.send(result, dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            print("Worker {} reportando resultados de trabajo!!".format(rank))
            print("Verifique {} paquetes".format(paquetes_verificados))
            break

    comm.send(None, dest=0, tag=tags.EXIT)
