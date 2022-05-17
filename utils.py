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

def cantPrimos(limiteInferior, Limitesuperior):
    cant_primos = 0

    for i in range(limiteInferior, Limitesuperior):
        if primeCheck(i):
            cant_primos += 1

    return cant_primos