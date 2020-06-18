from sympy.parsing.latex import parse_latex
import sympy.plotting

from backend.utilities.string import StringHandler
import sympy as s
import matplotlib
import matplotlib.pyplot as mplot
class Diferencial(object):
    def __init__(self):
        self.handler = StringHandler()

    def show_plot(self, funcao, xmin=None, xmax=None, ymin=None, ymax=None):
        x, y = s.symbols("x y")
        if xmin==None or xmax == None:
            s.plot(funcao)
        elif xmin!=None or xmax != None:
            if xmin== None:
                xmin=xmax-5
            if xmax== None:
                xmax=xmin+5
            s.plot(funcao,(x, xmin, xmax))
        elif ymin!=None or ymax != None:
            if ymin== None:
                ymin=ymax-5
            if ymax== None:
                ymax=ymin+5
            s.plot(funcao,(y, ymin, ymax))
        else:
            xmin=5
            xmax=5
            ymin=5
            ymax=5
            s.plot(funcao,(x,xmin,xmax),(y,ymin,ymax))
        funcao="(x**3+2*x)/(2*x**2)"
        funcao = s.sympify(funcao)
        funcao = s.integrate(funcao).doit()
        s.plot_implicit(y < funcao)

    def Intergral_Valor(self, funcao, limite_inferior=None, limite_superior=None):
        """Retorna o valor aproximado da integral da função dada

        Args:
            funcao ([type]): [description]
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

    def retaTangentePonto(self, funcao, coord_x=0.0, coord_y=0.0, show_tangente=False, legenda="f(x)="):
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
        
        funcao_plot = s.plot(funcao, show=False)

        if show_tangente == True:
            m = self.DecliveValor(funcao, coord_x)
            y=s.sympify(m*(x-coord_x)+coord_y)

            rt = s.plot(y, show=False)
            funcao_plot.append(rt[0])

            reta_tangente_pretty = "Reta tangente no ponto ("+str(coord_x)+", "+str(coord_y)+") de f(x)="+self.handler.pretty_ready(funcao)
            funcao_plot[1].label=reta_tangente_pretty
            funcao_plot[1].line_color = 'firebrick'

            low = coord_y * 0.5
            high = coord_y * 1.5
#            bound = bool()
            p1 = s.plot_implicit(s.Eq(x**2 + y**2, 5))
            #ponto = s.plot_implicit(s.And((y > y-k),(y+i > y)), y_var=y)

        funcao_latex = self.sympyLatexify(funcao)
        funcao_plot.title = f"${funcao_latex}$"
        funcao_plot.show()


    def LimiteValor(self, funcao, valor_tendencia, sinal=None, margem_erro=0.1):
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
        #Limite a esquerda da função
        if(sinal=="-"):
            if(funcao.subs(x, valor_tendencia-1e-8).is_real):
                return s.limit(funcao, x, valor_tendencia)
            else:
                return None #Limite não existe
        #Limite a direita da função
        elif(sinal=="+"):
            if(funcao.subs(x, valor_tendencia+1e-8).is_real):
                return s.limit(funcao, x, valor_tendencia)
            else:
                return None #Limite não existe
        else:
            sinal_esquerda=funcao.subs(x, valor_tendencia-1e-8)
            sinal_direita=funcao.subs(x, valor_tendencia+1e-8)
            #Assume-se que o limite seja um valor pequeno, 
            #se este for pequeno o suficiente, 
            #assumimos que este existe e tentamos calcula-lo
            if(abs(sinal_esquerda-sinal_direita)<margem_erro):
                return s.limit(funcao, x, valor_tendencia)
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
            print("Erro! Não foi possivel transformar a função em formato <<LaTex>>")
        return func_latex

"""

dif = Diferencial()
print(dif.LimiteValor("sqrt(x)", 0.1, '-'))
print(dif.LimiteValor("sqrt(x)", 0, '-'))
print(dif.LimiteValor("sqrt(x)", 0, '+'))
print(dif.LimiteValor("sqrt(x)", 0))
print(dif.LimiteValor("x/Abs(x)", 0, '-'))
print(dif.LimiteValor("x/Abs(x)", 0, '+'))
print(dif.LimiteValor("x/Abs(x)", 0))

print(dif.LimiteValor("2000/(1+199*E**(-0.001*E))", s.S.Infinity, "+"))

dif.show_plot("((5+x)**4)-1")
"""