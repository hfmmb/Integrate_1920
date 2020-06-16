import numpy as np
from sympy import Symbol, lambdify
from matplotlib import pyplot

def sympy_to_numpy(e):
    x = Symbol("x")
    a = np.arange(10) 

    expr = str(e)
    f = lambdify(x, expr, "numpy") 
    print(f(a))
    pyplot.plot(f(a))


sympy_to_numpy("sin(x)+x**3")