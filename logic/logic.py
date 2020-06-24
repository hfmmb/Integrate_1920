from .standardify import StringHandler
from tkinter import messagebox
#import sympy.plotting

import sympy as s
from sympy import lambdify
import matplotlib as mt
import matplotlib.pyplot as mplot
import numpy as np
class Diferencial(object):
    def __init__(self):
        self.handler = StringHandler()

    def plotIntegralDefinida(self, funcao, a=1e-32 , b=None, plot_eixo_x_limites=(0, 20), plot_eixo_y_limites=(0, 20)):
        #Ajusta o eixo x minimo no grafico
        if(plot_eixo_x_limites[0] < 0):
            plot_eixo_x_limites[0] = 0
        #Ajusta o eixo y minimo no grafico
        if(plot_eixo_y_limites[0] < 0):
            plot_eixo_y_limites[0] = 0

        x = s.symbols("x")
        funcao = s.sympify(funcao)

        w = lambdify(x, funcao, "numpy")

        fig, aq = mplot.subplots()
        aq.set_ylim(bottom=0)

        # Make the shaded region
        iq = np.linspace(a, b)
        iw = w(iq)
        verts = [(a, 0), *zip(iq, iw), (b, 0)]
        poly = mt.patches.Polygon(verts, color='darkorange', edgecolor='black')
        aq.add_patch(poly)

        aq.text(0.5 * (a + b), 30, r"$\int_a^b f(q)\mathrm{d}q$",
                horizontalalignment='center', fontsize=20)

        aq.xaxis.set_ticks_position('bottom')

        aq.set_xticks((a, b))
        aq.set_xticklabels(('$a$'+'='+str(a), '$b$'+'='+str(b)))
        aq.set_yticks([])

        funcao_latex = self.sympyLatexify(funcao)

        mapa = {'a':str(int(a)), 'b':str(int(b)), 'f':funcao_latex}
        integral_string = r"\int_{a}^{b} \! f(x) \,dx= {f}".format_map(mapa)

        mplot.title(f"${integral_string}$")
        mplot.xlim(plot_eixo_x_limites[0], plot_eixo_x_limites[1])
        mplot.ylim(plot_eixo_y_limites[0], plot_eixo_y_limites[1])     

        mplot.show()

    def inFuncao(self, funcao, coord_x, coord_y, margem_erro=0.05):
        """Verifica se um ponto inserido faz parte de uma função tendo em conta uma margem de erro dada

        Args:
            funcao (string): Função a avaliar
            coord_x (float): Coordenada x da reta tangente a função
            coord_y (float): Coordenada y da reta tangente a função
            margem_erro (float, optional): #Margem de erro para considerar um ponto dentro da função. Defaults to 0.00001.

        Returns:
            [boolean]: True se faz parte da função, False caso nao faça
        """
        #Substitui x por valor da coordenada x
        func_point = funcao.replace('x', "("+str(coord_x)+")")

        #Resolve a função
        func_point = s.sympify(func_point)

        #Verifica se o ponto está na reta
        return (coord_y*(1-margem_erro) < func_point and func_point < coord_y*(1+margem_erro))


    def Intergral_Valor(self, funcao, limite_inferior=None, limite_superior=None):
        """Retorna o valor aproximado da integral da função dada

        Args:
            funcao (string): Função a integrar
        """
        x = s.Symbol('x')
        integral = s.Integral(funcao, (x, limite_inferior, limite_superior))
        try:
            funcao = s.sympify(funcao)
        except s.SympifyError as err:
            return None
        try:
            integral = float(integral.as_sum(10).n(4))
            return integral
        except Exception as err:
            print(err)
        return None

    def DecliveValor(self, funcao, coord_x):
        """Calcula o declive da reta num ponto de uma função recorrendo a derivada

        Args:
            funcao (string): Função para analizar
            coord_x (float): Coordenada do ponto x

        Returns:
            float: declive
        """
        x = s.Symbol('x')
        funcao_deriv = s.diff(funcao)

        m = funcao_deriv.subs(x, coord_x)
        return m

    def retaTangentePonto(self, funcao, coord_x=0.0, coord_y=0.0, show_tangente=False, legenda="f(x)=", plot_eixo_x_limites=(-10, 10), plot_eixo_y_limites=(-10, 10)):
        """Mostra o grafico de uma função, suporta mostrar a reta tangente num ponto (x, y) dadas as coordenadas

        Args:
            funcao (string): Função a mostrar em formato grafico
            coord_x (float, optional): Ponto x da reta tangente. Defaults to 0.0.
            coord_y (float, optional): Ponto y da reta tangente. Defaults to 0.0.
            show_tangente (bool, optional): Mostrar reta tangente da função, True para mostrar, False para omitir. Defaults to False.
            legenda (str, optional): Identificador do tipo de função, exemplos; f(x), f'(x), f''(x), etc. Defaults to "f(x)=".
        """

        m, x, y = s.symbols('m x y')

        funcao_pretty = self.handler.pretty_ready(funcao)

        funcao_plot = s.plot(funcao, show=False)
        funcao_plot.legend=True
        funcao_plot[0].label=legenda+ funcao_pretty
        funcao_plot.xlim = plot_eixo_x_limites
        funcao_plot.ylim = plot_eixo_y_limites

        #Reta tangente no ponto (x,y)
        if show_tangente == True:
            m = self.DecliveValor(funcao, coord_x)
            y=s.sympify(m*(x-coord_x)+coord_y)

            rt = s.plot(y, show=False)

            rt.xlim = plot_eixo_x_limites
            rt.ylim = plot_eixo_y_limites

            funcao_plot.append(rt[0])

            reta_tangente_pretty = "Reta tangente no ponto ("+str(coord_x)+", "+str(coord_y)+") de f(x)="+self.handler.pretty_ready(funcao)
            funcao_plot[1].label=reta_tangente_pretty
            funcao_plot[1].line_color = 'firebrick'

            #Ponto (x, y)
            ponto_tangente = s.plot_implicit(s.Eq(x**2 +y**2, 4), block = False, show=False)
            funcao_plot.append(ponto_tangente[0])
            funcao_plot[2].label="Ponto ("+str(coord_x)+", "+str(coord_y)+")"
            funcao_plot[2].line_color = 'darkorange'

        funcao_latex = self.sympyLatexify(funcao)
        funcao_plot.title = f"${funcao_latex}$"
        funcao_plot.show()

    def LimiteValor(self, funcao, valor_tendencia_limite, sinal=None, margem_erro=0.1):
        """Efectua o calculo de um limite e retorna o valor caso exista

        Args:
            funcao (string): Função a ser analizada para a existencia de limites
            valor_tendencia (float): Valor para qual o limite tende (lim f(x), x->y)
            sinal (string, optional): Limite a esquerda (-), direita (+) ou ambos (Campo vazio). Defaults to None.
            margem_erro (float): Valor de tolerancia usado para saber se o limite existe ou não, default é 0.1

        Returns:
            float: Retorna o valor do limite se este existe, None se este nao existe
        """

        x = s.Symbol('x')
        try:
            funcao = s.sympify(funcao)
        except s.SympifyError as e:
            print("Função em formato incorreto:\n", e)
        try:
            if(valor_tendencia_limite != "-00" and valor_tendencia_limite != "00" and valor_tendencia_limite != "+00"):
                valor_tendencia_limite = float(valor_tendencia_limite)
            
        except ValueError as e:
            print("Valor invalido: ", str(e))

        #Limite a esquerda da função
        if(sinal=="-"):
            if valor_tendencia_limite == "-00":
                return s.limit(funcao, x, "-00", dir=sinal)

            elif valor_tendencia_limite == "00" or valor_tendencia_limite == "+00":
                return s.limit(funcao, x, "+00", dir=sinal)

            elif(funcao.subs(x, valor_tendencia_limite-1e-8).is_real):
                return s.limit(funcao, x, valor_tendencia_limite, dir=sinal)
            else:
                return None #Limite não existe

        #Limite a direita da função
        elif(sinal=="+"):
            if valor_tendencia_limite == "-00":
                return s.limit(funcao, x, "-00", dir=sinal)

            elif valor_tendencia_limite == "00" or valor_tendencia_limite == "+00":
                return s.limit(funcao, x, "+00", dir=sinal)

            elif(funcao.subs(x, valor_tendencia_limite+1e-8).is_real):
                return s.limit(funcao, x, valor_tendencia_limite, dir=sinal)
            else:
                return None #Limite não existe
        else:
            sinal_esquerda=funcao.subs(x, str(valor_tendencia_limite-1e-8))
            sinal_direita=funcao.subs(x, valor_tendencia_limite+1e-8)
            #Assume-se que o limite seja um valor pequeno, 
            #se este for pequeno o suficiente, 
            #assumimos que este existe e tentamos calcula-lo
            if(abs(sinal_esquerda-sinal_direita)<margem_erro):
                return s.limit(funcao, x, valor_tendencia_limite)
            else:
                return None #Limite não existe

    def sympyLatexify(self, funcao):
        """Transforma uma função em formato string ou sympy para formato LaTex e retorna o resultado

        Args:
            funcao (string): Função a ser analizada para a existencia de limites

        Returns:
            float: Retorna a função em formato latex
        """
        try:
            funcao = s.sympify(funcao)
            func_latex = s.latex(funcao)

        except Exception as e:
            print("Erro! Não foi possivel transformar a função em formato <<LaTex>>\n\n"+ str(e))
        return func_latex

    def derivate(self, funcao, ordem=1):
        """Calcula a derivada de ordem n e retorna a sua expressao

        Args:
            funcao (string): Função a derivar
            ordem (int, optional): Order da derivada, 1 para f'(x), 2 para f''(x), etc... Defaults to 1.

        Returns:
            [Derivative]: Expressao da derivada de ordem n
        """
        derivada_ordem_n = s.diff(funcao)
        for i in range(ordem-1):
            try:
                if(str(derivada_ordem_n) == "0"):
                    return derivada_ordem_n
                derivada_ordem_n = s.diff(derivada_ordem_n)
                derivada_ordem_n = str(derivada_ordem_n)

            except Exception as e:
                messagebox.showerror("Erro!", 
                                    "Não foi possivel calcular a derivada de ordem "+ str(ordem) + " da funçao inserida!\n\n" + str(e))
        return derivada_ordem_n
