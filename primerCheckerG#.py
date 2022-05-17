from mpi4py import MPI
from utils import primeCheck, cantPrimos
import sys

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

if rank == 0:
    print("Estaremos repartiendo los siguientes paquetes: \n", paquetes)

def main(paquetes = paquetes):
    if rank == 0:
        
        data =  paquetes[0:size -1]
        paquetes = paquetes[size-1:]
        data.insert(0,0)
    else:
        data = 0
            
    data = comm.scatter(data, root = 0)

    if rank != 0:
        print('El Proceso ', rank, ' Trabajara con el paquete ', data)

        cant_primos = cantPrimos(data - 100, data + 1)

        #data = comm.gather({ cant_primos: cant_primos, rank: rank, paquete: paquete}, root = 0)
        data = comm.gather({"cant_primos": cant_primos, "Proceso": rank, "paquete": data}, root = 0)
    else:
        data = comm.gather({"cant_primos": 0, "rank": 0, "paquete": 0}, root = 0)
    
    if rank == 0:
        print(data[1:])
        print()

    if (len(paquetes) > 0):
        if (len(paquetes) < size-1):
            paquetes += [0] *  (size-1 -len(paquetes))  
            main(paquetes=paquetes)
        else:
            main(paquetes=paquetes)

main()
