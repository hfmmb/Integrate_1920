import sympy as sp

x, y, m, a, b = sp.symbols('x y m a b')

# Finding maximum and minimum (critical points)
#sp.solve(sp.Derivative(x**2 - 2*x - 15, x).doit())

# Integrals - with interval
#sp.Integral(sp.sin(x) * x, (x, 0, 1)).doit()

coordenada_x = str(1)
coordenada_y = str(1)

#Obtem a derivada da funcao
f_deriv = sp.diff("x**2")
#f_deriv = sp.diff("0.5*(x)**2+3*(x)**(-1)")

f_deriv = str(f_deriv)
#Tranforma a funcao em ordem a "m" para obter o declive
f_deriv = f_deriv + "-y"
#f_deriv = f_deriv + "-(y)"

g=sp.lambdify((x, y),f_deriv)
#Substitui as coordenadas do ponto na funcao
m_val=g(float(coordenada_x), float(coordenada_y))

print(m_val)

f_r_tangente = sp.lambdify((m, x, a, b), "m*(x-a)-b")
f_final = f_r_tangente(m_val, x, float(coordenada_x), float(coordenada_y))
print(f_final)
sp.plot(str(f_final))