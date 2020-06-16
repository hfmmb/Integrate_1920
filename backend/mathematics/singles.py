import math
from decimal import Decimal #Mehor precisao que o buitin float do python
import time
#Função para processar, mudada pelo que o utilizador insere
def f(x:Decimal):
    return  x*x

def trapezoidal_simpson( lower:Decimal, upper:Decimal, numero_total_trapezios):
    """'
    Utiliza o algoritmo trapezoidal de Simpson para calcular 
    o valor aproximado de uma integral com o auxilio de trapezios

    Arguments:
        lower {float} -- [description]
        upper {float} -- [description]
        numero_total_trapezios {int} -- Número total de trapezios utilizados no algoritmo de calculo

    Returns:
        Decimal -- valor aproximado da integral
    """
    x = Decimal(0.0)
    h = Decimal(0.0)
    soma = Decimal(0.0)
    h=Decimal(math.fabs(upper-lower)/numero_total_trapezios)
    j=1
    while j < numero_total_trapezios:
        x=Decimal(lower+j*h)
        soma = soma + f(x)
        print("x: ", x, "h: ", h, "Soma: ", soma)
        j+=1
    integral = Decimal((h/2)*(f(lower)+f(upper)+2*soma))
    return integral


def simpson(lower:Decimal, upper:Decimal, precision:Decimal):
    """Calculates and returns the value of an integral using the trapezoidal Simpson method aproximation calculation

    Arguments:
        lower {Decimal} -- Limite inferior
        upper {Decimal} -- Limite superior
        precision {Decimal} -- Precisao (largura trapezoides utilizador no calculo)
    """
    start_time = time.time()
    intervalos=2
    limite_inferior = Decimal(lower)
    limite_superior = Decimal(upper)
    precisao = Decimal(precision)

    integral = trapezoidal_simpson(limite_inferior, limite_superior, intervalos)

    while True:
        integral_temp = integral
        intervalos+=1
        integral = trapezoidal_simpson(limite_inferior, limite_superior, intervalos)
        if math.fabs(integral-integral_temp) >= precisao:
            break

    print("A integral tem o valor de: ", integral)
    print("A integral tem ", intervalos, " intervalos")

    print("Tempo de execução: %s" % (time.time() - start_time))

    return integral, intervalos