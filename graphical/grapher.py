import sympy as sp

x, y, m, a, b = sp.symbols('x y m a b')

# Integrals - with interval
sp.Integral(sp.sin(x) * x, (x, 0, 1)).doit()




