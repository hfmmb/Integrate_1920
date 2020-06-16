class StringHandler(object):
    PATTERN_DICT = {"gamma":u"\u0263","sen":"sin", "tg":"tan", "x²":"x**2", "x³":"x**3", 
                    "x⁴":"x**4", "x⁵":"x**5", "x⁶":"x**6", "x⁷":"x**7", "x⁸":"x**8","x⁹":"x**9", 
                    "raiz":"sqrt","√":"sqrt", "|":"mod","cotan":"cot","cotg":"cot","^":"**","e":"E"}
    def __init__(self):
        pass

    def process_ready(self, funcao):
        """Converte uma função "human readable" para "computer readable" de forma a ser possivel executar as operacções desejadas

        Arguments:
            funcao {string} -- Função da uma reta, parabola, integral, etc...

        Returns:
            string -- Função em formato "computed readable"
        """
        for key in StringHandler.PATTERN_DICT.keys():
            funcao = str(funcao.lower().replace(key, StringHandler.PATTERN_DICT[key]))
        return funcao


    def pretty_ready(self, funcao):
        """Converte uma função "computer readable" para "human readable" de forma a ser mais facil de ler

        Arguments:
            funcao {string} -- Função da uma reta, parabola, integral, etc...

        Returns:
            string -- Função em formato "human readable"
        """
        for key in StringHandler.PATTERN_DICT.keys():
            funcao = str(funcao.lower().replace(StringHandler.PATTERN_DICT[key], key))
        
        SPECIAL_PATTERN_DICT = {"*x":"x","*log":"log","*ln":"ln","*sen":"sen","*cos":"cos","*tg":"tg"}
        for key in SPECIAL_PATTERN_DICT.keys():
            funcao = str(funcao.lower().replace(key, SPECIAL_PATTERN_DICT[key]))
        return funcao

'''
    def extract_digits(self, funcao):
        lista = []
        for funcao in StringHandler.PATTERN_DICT.keys():
            funcao = str(funcao.lower().replace(StringHandler.PATTERN_DICT[key], key))
        return funcao
'''
#handler = StringHandler()
#handler.extract_digits
