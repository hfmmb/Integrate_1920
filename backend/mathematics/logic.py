import sympy as s

class Diferencial:
    def __init__(self):
        pass

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

dif = Diferencial()
print(dif.LimiteValor("sqrt(x)", 0.1, '-'))
print(dif.LimiteValor("sqrt(x)", 0, '-'))
print(dif.LimiteValor("sqrt(x)", 0, '+'))
print(dif.LimiteValor("sqrt(x)", 0))
print(dif.LimiteValor("x/Abs(x)", 0, '-'))
print(dif.LimiteValor("x/Abs(x)", 0, '+'))
print(dif.LimiteValor("x/Abs(x)", 0))

print(dif.LimiteValor("2000/(1+199*E**(-0.001*E))", s.S.Infinity, "+"))