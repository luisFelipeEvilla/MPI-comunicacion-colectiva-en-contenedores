from mpi4py import MPI
import sys

print(sys.argv)

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
