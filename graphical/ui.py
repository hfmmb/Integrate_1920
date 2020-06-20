import tkinter as Tk
from tkinter import END, Frame, Button, Text, Label, Canvas, Checkbutton, messagebox, IntVar
from tkinter.font import Font
from tkinter.ttk import Combobox
from sys import version_info, exit
import pathlib
import sympy as s
from sympy import S, Symbol, Integral, Limit, sin, cos, tan, cot, sinh, cosh, cot, plot, solve, diff, integrate, ln, evalf, symbols
import webbrowser

from screeninfo import get_monitors
from logic.logic import Diferencial
from logic.standardify import StringHandler
from os import name

class UI(Frame):
    master=Tk.Tk()

    def __init__(self, master=master):

        Frame.__init__(self, master)

        self.master.wm_title("Integrate - Derivação e Integração")
        self.master.wm_iconphoto(False, Tk.PhotoImage(file="./icon.png"))

        #Obtem resolução do ecra atual
        resolution = get_monitors()
        screen_width = resolution[0].width
        screen_height = resolution[0].height

        window_width = round(0.66 * screen_width)
        window_height = round(0.38 * screen_height)

        #Aplica a resolução a janela
        resolution = str(window_width) + 'x' + str(window_height)
        master.geometry(resolution)

        # Gets both half the screen width/height and window width/height
        positionRight = int((screen_width)*0.25)
        positionDown = int((screen_height)*0.65)

        # Positions the window in the center of the page.
        master.geometry("+{}+{}".format(positionRight, positionDown))

        #Other elements

        fonte = Font(family="Helvetica", size=18)

        #Frame input função
        funcao_text = "x³/(x²+sen(pi^(x)/2)+ln(E+1)+sqrt(15))"
        self.frame_master_row = Frame(master=self.master, highlightbackground="black", highlightthickness=2)
        self.frame_master_row.pack(side = Tk.TOP)

#        self.master = Frame(master=self.master, highlightbackground="black", highlightthickness=2)
#        self.master.pack(side = Tk.TOP)

#        from PIL import Image, ImageTk

#        IMAGE_PATH = '01.jpg'
#        WIDTH, HEIGTH = 600, 600

#        self.frame_master_row = Tk.Canvas(master=self.master, width=WIDTH, height=HEIGTH)
#        self.frame_master_row.pack(side = Tk.TOP)

#        img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((window_width, window_height), Image.ANTIALIAS))
#        self.frame_master_row.background = img  # Keep a reference in case this code is put in a function.
#        bg = self.frame_master_row.create_image(0, 0, anchor=Tk.NW, image=img)


        self.frame_input_funcao = Frame(master=self.frame_master_row, highlightbackground="black", highlightthickness=1)
        self.frame_input_funcao.pack( side = Tk.TOP )
        self.lbl_function = Label(self.frame_input_funcao, text="f(x)= ", font=fonte)
        self.tbx_input = Text(self.frame_input_funcao, height=2, width=70, font=fonte)
        self.btn_apagar = Button(master=self.frame_input_funcao, command=self.listener_btn_apagar, text='Apagar')
        self.lbl_function.pack(side=Tk.LEFT)
        self.tbx_input.insert(END, funcao_text)
        self.tbx_input.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_apagar.pack(side=Tk.LEFT, fill=Tk.BOTH)

        #Combobox e campos de input do modo selecionado
        self.frame_modo = Frame(master=self.frame_master_row, highlightbackground="black", highlightthickness=1)
        self.lbl_modo = Label(self.frame_modo, text = "Modo: ")
        self.cb_modo = Combobox(self.frame_modo, state='readonly', font=fonte , 
            values=[ 
                "f(x)", 
                "f'(x)", 
                "f''(x)", 
                u"\u222B"+" f(x)dx (Indefinida)", 
                u"\u222B"+"ab f(x)dx (Definida)" ,
                u"\u222B"+"ab f(x)dx (Imprópria)", 
                "Minimos e Máximos",
                "Limite",
                u"\u222B"+" f(x)dx (Zeros)"], width=25)

        self.cb_modo.current(0)
        self.cb_modo.bind("<<ComboboxSelected>>", self.listener_cb_modo)

        self.frame_modo.pack( side = Tk.LEFT, fill=Tk.BOTH)
        self.lbl_modo.pack(side=Tk.LEFT)
        self.cb_modo.pack(side=Tk.LEFT)

        #Reta tangente há função
        self.frame_reta_tangente = Frame(master=self.frame_modo, highlightbackground="black", highlightthickness=1)
        self.chkbx_reta_toggle_state = IntVar()
        self.chkbx_reta_tg = Checkbutton(self.frame_reta_tangente, text='Reta Tangente no ponto', variable=self.chkbx_reta_toggle_state, onvalue=1, offvalue=0, command=self.listener_chkbx_reta_tg)
        self.chkbx_reta_tg.deselect()

        self.frame_reta_tangente_x = Frame(master=self.frame_reta_tangente)
        self.frame_reta_tangente_y = Frame(master=self.frame_reta_tangente)
        self.frame_reta_tangente_margem_erro = Frame(master=self.frame_reta_tangente)

        self.lbl_reta_tangente_x = Label(self.frame_reta_tangente_x, text="                  x:")
        self.lbl_reta_tangente_y = Label(self.frame_reta_tangente_y, text="y:")
        self.lbl_reta_tangente_margem_erro = Label(self.frame_reta_tangente_margem_erro, text="Margem erro:")

        self.tbx_reta_tangente_x = Text(self.frame_reta_tangente_x, height=1, width=10)
        self.tbx_reta_tangente_y = Text(self.frame_reta_tangente_y, height=1, width=10)
        self.tbx_reta_tangente_margem_erro = Text(self.frame_reta_tangente_margem_erro, height=1, width=10)

        self.frame_reta_tangente.pack( side=Tk.LEFT )        
        self.chkbx_reta_tg.pack( side=Tk.LEFT )

        #Contem os campos de input das integrais definidas com intervalo
        self.frame_integrais_definidas = Frame(master=self.frame_modo, highlightbackground="black", highlightthickness=1, width=20, height=10)
        self.frame_integrais_definidas_linha_1 = Frame(master=self.frame_integrais_definidas)
        self.frame_integrais_definidas_linha_2 = Frame(master=self.frame_integrais_definidas)
        self.lbl_input_inferior = Label(self.frame_integrais_definidas_linha_1, text="Limite inferior (a): ")
        self.tbx_input_inferior = Text(self.frame_integrais_definidas_linha_1, width=5, height=1)
        self.lbl_input_superior = Label(self.frame_integrais_definidas_linha_2, text="Limite superior (b): ")
        self.tbx_input_superior = Text(self.frame_integrais_definidas_linha_2, width=5, height=1)

        #Operações trigonometria, raizes, soma, sub, etc...
        WIDTH_OPER=8
        self.frame_operacoes = Frame(master=self.frame_master_row, padx=4, pady=6)
        self.lbl_operations = Label(self.frame_operacoes, text="Operações: ")

        self.frame_operacoes_linha_1 = Frame(master=self.frame_operacoes)
        self.btn_soma = Button(self.frame_operacoes_linha_1, command=self.listener_btn_soma, text='+', width=WIDTH_OPER)
        self.btn_subtracao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_subtracao, text='-', width=WIDTH_OPER)
        self.btn_multiplicacao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_multiplicacao, text='*', width=WIDTH_OPER)
        self.btn_divisao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_divisao, text='/', width=WIDTH_OPER)

        self.frame_operacoes_linha_2 = Frame(master=self.frame_operacoes)
        self.btn_sin = Button(self.frame_operacoes_linha_2, command=self.listener_btn_sin, text='sin(x)', width=WIDTH_OPER)
        self.btn_cos = Button(self.frame_operacoes_linha_2, command=self.listener_btn_cos, text='cos(x)', width=WIDTH_OPER)
        self.btn_tg = Button(self.frame_operacoes_linha_2, command=self.listener_btn_tg, text='tan(x)', width=WIDTH_OPER)
        self.btn_cotg = Button(self.frame_operacoes_linha_2, command=self.listener_btn_cotg, text='cotg(x)', width=WIDTH_OPER)

        self.frame_operacoes_linha_3 = Frame(master=self.frame_operacoes)
        self.btn_x_exp_y = Button(self.frame_operacoes_linha_3, command=self.listener_btn_x_exp_y, text='x^', width=WIDTH_OPER)
        self.btn_raiz = Button(self.frame_operacoes_linha_3, command=self.listener_btn_raiz, text='√', width=WIDTH_OPER)
        self.btn_parenteses_esquerdo = Button(self.frame_operacoes_linha_3, command=self.listener_btn_patenteses_esquerdo, text='(', width=WIDTH_OPER)
        self.btn_parenteses_direito = Button(self.frame_operacoes_linha_3, command=self.listener_btn_patenteses_direito, text=')', width=WIDTH_OPER)

        self.frame_operacoes_linha_4 = Frame(master=self.frame_operacoes)
        self.btn_x = Button(self.frame_operacoes_linha_4, command=self.listener_btn_x, text='x', width=WIDTH_OPER)
        self.btn_raiz_a_x = Button(self.frame_operacoes_linha_4, command=self.listener_btn_raiz_a_x, text='√(a,x)', width=WIDTH_OPER)
        self.btn_log = Button(self.frame_operacoes_linha_4, command=self.listener_btn_log, text='log(x)', width=WIDTH_OPER)
        self.btn_log_a_x = Button(self.frame_operacoes_linha_4, command=self.listener_btn_log_a_x, text='log_a(x)', width=WIDTH_OPER)

        self.frame_operacoes_linha_5 = Frame(master=self.frame_operacoes)
        self.btn_nepper = Button(self.frame_operacoes_linha_5, command=self.listener_btn_nepper, text='e', width=WIDTH_OPER)
        self.btn_nepper_exp = Button(self.frame_operacoes_linha_5, command=self.listener_btn_exp_nepper, text='e^', width=WIDTH_OPER)
        self.btn_log_nepper = Button(self.frame_operacoes_linha_5, command=self.listener_btn_log_nepper, text='ln(x)', width=WIDTH_OPER)
        self.btn_pi = Button(self.frame_operacoes_linha_5, command=self.listener_btn_pi, text='π', width=WIDTH_OPER)

        self.frame_operacoes_linha_6 = Frame(master=self.frame_operacoes)
        self.btn_secante = Button(self.frame_operacoes_linha_6, command=self.listener_btn_secante, text='sec(x)', width=WIDTH_OPER)
        self.btn_cosecante = Button(self.frame_operacoes_linha_6, command=self.listener_btn_cosecante, text='cosec(x)', width=WIDTH_OPER)
        self.btn_arcsen = Button(self.frame_operacoes_linha_6, command=self.listener_btn_arcsen, text='arcsen(x)', width=WIDTH_OPER)
        self.btn_arccos = Button(self.frame_operacoes_linha_6, command=self.listener_btn_arccos, text='arccos(x)', width=WIDTH_OPER)

        self.frame_operacoes_linha_7 = Frame(master=self.frame_operacoes)
        self.btn_arctan = Button(self.frame_operacoes_linha_7, command=self.listener_btn_arctan, text='arctan(x)', width=WIDTH_OPER)
        self.btn_arccotan = Button(self.frame_operacoes_linha_7, command=self.listener_btn_arccotan, text='arccotan(x)', width=WIDTH_OPER)
        self.btn_arcsecante = Button(self.frame_operacoes_linha_7, command=self.listener_btn_arcsecante, text='arcsec(x)', width=WIDTH_OPER)
        self.btn_arccosecante = Button(self.frame_operacoes_linha_7, command=self.listener_btn_arccosecante, text='arccosec(x)', width=WIDTH_OPER)

        self.frame_operacoes.pack( side=Tk.TOP )
        self.lbl_operations.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_1.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_soma.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_subtracao.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_multiplicacao.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_divisao.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_2.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_sin.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_cos.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_tg.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_cotg.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_3.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_x_exp_y.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_raiz.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_parenteses_esquerdo.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_parenteses_direito.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_4.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_x.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_raiz_a_x.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_log.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_log_a_x.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_5.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_nepper.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_nepper_exp.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_log_nepper.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_pi.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_6.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_secante.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_cosecante.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_arcsen.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_arccos.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_operacoes_linha_7.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_arctan.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_arccotan.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_arcsecante.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_arccosecante.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_btn_comandos = Frame(master=self.frame_master_row, padx=25, pady=6)
        self.btn_resolver = Button(master=self.frame_btn_comandos, text='Resolver', command=self.listener_btn_resolver)
        self.btn_info = Button(master=self.frame_btn_comandos, command=self.listener_btn_info, text='Info')
        self.btn_sair = Button(master=self.frame_btn_comandos, command=self.listener_btn_sair, text='Sair', )

        self.frame_btn_comandos.pack(side=Tk.RIGHT)
        self.btn_resolver.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_info.pack(side=Tk.TOP, fill=Tk.BOTH)
        self.btn_sair.pack(side=Tk.TOP, fill=Tk.BOTH)

        #Contem os campos de input do calculo de limites
        self.frame_limite = Frame(master=self.frame_modo, highlightbackground="black", highlightthickness=1, width=20, height=10)
        self.frame_sinal_limite = Frame(master=self.frame_limite)
        self.frame_valor_limite = Frame(master=self.frame_limite)
        self.lbl_input_sinal_limite = Label(self.frame_sinal_limite, text="Sinal: ")
        self.tbx_input_sinal_limite = Text(self.frame_sinal_limite, width=5, height=1)
        self.lbl_input_valor_limite = Label(self.frame_valor_limite, text="lim x->: ")
        self.tbx_input_valor_limite = Text(self.frame_valor_limite, width=5, height=1)


    # Functions
    def get_txb_input_text(self):
        textboxtext = self.tbx_input.get("1.0",END)
        return textboxtext

    #Event Listeners
    def listener_btn_resolver(self):
        try:

            if(len(self.get_txb_input_text()) <= 1):
                messagebox.showerror("Erro!", "Escreva a função na caixa de texto!")
            else:
                cb_index = self.cb_modo.current()
                x, y = symbols('x y', real=True)
                d = Diferencial()        
                handler = StringHandler()
                funcao = handler.process_ready(str(self.get_txb_input_text()))

                #f(x)
                if cb_index == 0:
                    self.get_coords(funcao)

                #f'(x)
                elif cb_index == 1:
                    try:
                        derivada = str(d.derivate(funcao))
                        self.get_coords(derivada)
                    except Exception as e:
                        messagebox.showerror("Erro!", 
                                            "Não foi possivel calcular a primeira derivada da função inserida!\n\n" + str(e))

                #f''(x)
                elif cb_index == 2:
                    try:
                        segunda_derivada = str(d.derivate(funcao, 2))
                        self.get_coords(segunda_derivada)
                    except Exception as e:
                        messagebox.showerror("Erro!", 
                                            "Não foi possivel calcular a segunda derivada da função inserida!\n\n" + str(e))

                #Integral sem intervalos (Indefinida) (Primitivas)
                elif cb_index == 3:

                    try:
                        primitiva = integrate(funcao)
                        d.plotIntegral(primitiva)

                    except Exception as e:
                        messagebox.showerror("Erro!", "Não foi possivel mostrar o grafico da integral desta função!\n\n" + str(e))

                #Integral com intervalos (definida)
                elif cb_index == 4:

                    valor_inferior, valor_superior = str(self.tbx_input_inferior.get("1.0", END)), str(self.tbx_input_superior.get("1.0", END))
                    valor_inferior_string, valor_superior_string = valor_inferior.strip('\n'), valor_superior.strip('\n')
                    if(len(valor_inferior) > 1 and len(valor_superior) > 1):
                        try:
                            valor_inferior = int(valor_inferior)

                            valor_superior = int(valor_superior)

                            if (valor_inferior_string != "-00") and (valor_superior_string != "00") and (valor_superior_string != "+00"):
                                if (valor_inferior > valor_superior):
                                    aux = int(valor_superior)
                                    valor_superior = int(valor_inferior)
                                    valor_inferior = int(aux)

                            try:
                                valor = d.Intergral_Valor(funcao, valor_inferior, valor_superior)
                                messagebox.showinfo("Resultado Integral!", "Valor: "+ str(valor))
                            except Exception:
                                messagebox.showerror("Erro!","Não foi possivel calcular o valor da integral dada no intervalo de limites ["+valor_inferior+", "+valor_superior+"]!")        
                        except Exception:
                            messagebox.showerror("Erro!","Apenas numeros são permitidos!")
                    else:
                        messagebox.showerror("Erro!","Preencha os campos de valores inferior e superior!")

                #Integrais Impróprias (Valor)
                elif cb_index == 5:

                    valor_inferior, valor_superior = str(self.tbx_input_inferior.get("1.0", END)), str(self.tbx_input_superior.get("1.0", END))
                    valor_inferior_string, valor_superior_string = valor_inferior.strip('\n'), valor_superior.strip('\n')
                    if(len(valor_inferior) > 1 and len(valor_superior) > 1):
                        if valor_inferior_string == "-00":
                            valor_inferior = s.S.NegativeInfinity()
                        else:
                            valor_inferior = int(valor_inferior)
                        if valor_superior_string == "00" or valor_superior == "+00" :
                            valor_inferior = s.S.Infinity()
                            
                        else:
                            valor_superior = int(valor_superior)

                        case_negative_infinity = valor_inferior_string == "-00" and ((valor_superior_string != "00") and (valor_superior_string != "+00"))
                        case_positive_infinity = valor_inferior_string != "-00" and ((valor_superior_string == "00") or (valor_superior_string == "+00"))
                        if case_negative_infinity and case_positive_infinity:
                            if (valor_inferior > valor_superior):
                                aux = int(valor_superior)
                                valor_superior = int(valor_inferior)
                                valor_inferior = int(aux)
                        case_all_infinity = valor_inferior_string == "-00" and ((valor_superior_string == "00") or (valor_superior_string == "+00"))

                        try:
                            if not case_all_infinity:
                                valor = d.Intergral_Valor(funcao, valor_inferior, valor_superior)
                                messagebox.showinfo("Resultado Integral!", "Valor: "+ str(valor))
                            else:
                                messagebox.showerror("Erro!","-00 e +00 em ambos os campos dos limites não é permitido! Integral Indefinida!")        

                        except Exception:
                            messagebox.showerror("Erro!","Não foi possivel calcular o valor da integral dada no intervalo de limites ["+valor_inferior+", "+valor_superior+"]!")        
                    else:
                        messagebox.showerror("Erro!","Preencha os campos de valores inferior e superior!")

                #Minimos e maximos da função
                elif cb_index == 6: 
                    try:
                        solucao = solve(d.derivate(funcao))
                        if len(solucao) == 0:
                            messagebox.showinfo("Minimos e Maximos", "A função não tem minimos nem máximos.")

                        else:
                            messagebox.showinfo("Minimos e Maximos", "Minimo(s) e maximo(s) encontrados: \n" +  str(solucao).replace(',','\n').replace('[','').replace(']',''))

                    except Exception as e:
                        messagebox.showerror("Erro!", "Não foi possivel calcular os minimos e maximos da função!\n\n"+str(e))

                #Limites
                elif cb_index == 7:
#                    print(solve(Limit(funcao, x, S.Infinity).doit(), dict=True))
                    #plot(funcao, title=funcao)

                    valor_tendencia_limite = str(self.tbx_input_valor_limite.get("1.0", END))

                    mensagem = ""
                    sinal = str(self.tbx_input_sinal_limite.get("1.0", END)) #Limite a esquerda ou direita da funcao
                    sinal = sinal.strip("\n")
                    if sinal == '+':
                        mensagem = "direita"
                    elif sinal == '-':
                        mensagem = "esquerda"
                    else:
                        sinal=None
                        messagebox.showwarning("Sinal indefinido!", "Sinal do limite não definido! (-) esquerda (+) direita.")

                    limite = None
                    if sinal == None:
                        try:
                            limite = d.LimiteValor(funcao, valor_tendencia_limite)
#                            limite = solve(Limit(funcao, x, valor_tendencia_limite).doit())
                            messagebox.showinfo("Limite da função", 
                                                "O limite da função para x->"+valor_tendencia_limite+"é: "+ str(limite))
                        except Exception as e:
                            messagebox.showerror("Erro!", "Não foi possivel calcular o limite de x->"+valor_tendencia_limite+" para a função dada!\n\n"+str(e))
                    else:
                        try:
#                                limite = Limit(funcao, x, valor_tendencia_limite , dir=sinal).doit()
                            limite = d.LimiteValor(funcao, valor_tendencia_limite, sinal)

                            messagebox.showinfo("Limite da função à"+mensagem+" ("+sinal+")", 
                                                "O limite à "+mensagem+" ("+sinal+") da função é: "+ str(limite))
                        except Exception as e:
                            messagebox.showerror("Erro!", "Não foi possivel calcular o limite à "+mensagem+" ("+sinal+") para a função dada!")
                    d.retaTangentePonto(str(Limit(funcao, x, valor_tendencia_limite).doit()))

                #Zeros integral
                elif cb_index == 8:
                        try:
                            integral_calculo_zeros = solve(primitiva)
                            primitiva_pretty = u"\u222B"+"f(x)dx="+handler.pretty_ready(str(primitiva))
                            messagebox.showinfo("Resultado Primitiva / Integral Definida!", str(primitiva_pretty)+"\nZeros: "+ str(integral_calculo_zeros))

                        except Exception as e:
                            messagebox.showerror("Erro!", "Não foi possivel calcular a integral desta função!\n" + str(e))

        except Exception as e:
            messagebox.showerror("ERRO!", "Não foi possivel resolver a expressao inserida, está bem escrita?\n\n"+ str(e))

    def listener_btn_apagar(self):
        self.tbx_input.delete('1.0', END)
        print('Limpando texto...')

    def listener_btn_info(self):


        from pathlib import Path
        root_folder = Path(__file__).parent.absolute().parent
        data_folder = Path("man/")
        data_folder = root_folder / data_folder 

        path = data_folder / "manual.html"

        try:
            try:
                webbrowser.open_new_tab(str(path))
            except Exception as e:
                messagebox.showerror("Erro!", "Não foi possivel aceder ao browser do sistema operativo!\n\n"+str(e))
        except FileNotFoundError as e:
            messagebox.showerror("Erro!", "Não foi possivel aceder aos ficheiros da documentação!\n\n" + str(e))

    def listener_btn_sair(self):
        exit()

    def listener_cb_modo(self, event):
        '''
        Change listener da combobox
        '''
        selected_index = self.cb_modo.current()
        self.chkbx_reta_tg.deselect()

        # f(x) e reta tangente no ponto
        if(selected_index < 3):
            self.frame_reta_tangente.pack(side=Tk.LEFT)
            self.chkbx_reta_tg.pack(side=Tk.LEFT)

        #Integral Definida
        elif(selected_index == 4 or selected_index == 5):
            self.frame_integrais_definidas.pack(side=Tk.LEFT)
            self.frame_integrais_definidas_linha_1.pack(side=Tk.TOP, fill=Tk.BOTH)
            self.frame_integrais_definidas_linha_2.pack(side=Tk.TOP, fill=Tk.BOTH)
            self.lbl_input_inferior.pack(side=Tk.LEFT, fill=Tk.BOTH)
            self.tbx_input_inferior.pack(side=Tk.RIGHT, fill=Tk.BOTH)
            self.lbl_input_superior.pack(side=Tk.LEFT, fill=Tk.BOTH)
            self.tbx_input_superior.pack(side=Tk.RIGHT, fill=Tk.BOTH)

        #Limites
        elif(selected_index == 7):
            self.frame_limite.pack(side=Tk.LEFT)
            self.frame_sinal_limite.pack(side=Tk.TOP, fill=Tk.BOTH)
            self.frame_valor_limite.pack(side=Tk.TOP, fill=Tk.BOTH)
            self.lbl_input_sinal_limite.pack(side=Tk.LEFT, fill=Tk.BOTH)
            self.tbx_input_sinal_limite.pack(side=Tk.RIGHT, fill=Tk.BOTH)
            self.lbl_input_valor_limite.pack(side=Tk.LEFT, fill=Tk.BOTH)
            self.tbx_input_valor_limite.pack(side=Tk.RIGHT, fill=Tk.BOTH)

        else:
            self.frame_reta_tangente.pack_forget()
            self.chkbx_reta_tg.deselect()
            self.frame_reta_tangente_x.pack_forget()
            self.frame_reta_tangente_y.pack_forget()

            self.frame_limite.pack_forget()
            self.chkbx_reta_tg.pack_forget()
            self.frame_integrais_definidas.pack_forget()

    def listener_chkbx_reta_tg(self):
        if(self.chkbx_reta_toggle_state.get() == 1):
            self.frame_reta_tangente_x.pack(side=Tk.TOP)
            self.lbl_reta_tangente_x.pack(side=Tk.LEFT)
            self.tbx_reta_tangente_x.pack(side=Tk.LEFT)
            self.frame_reta_tangente_y.pack(side=Tk.TOP)
            self.lbl_reta_tangente_y.pack(side=Tk.LEFT, fill=Tk.BOTH)
            self.tbx_reta_tangente_y.pack(side=Tk.RIGHT, fill=Tk.BOTH)
            self.frame_reta_tangente_margem_erro.pack(side=Tk.TOP)
            self.lbl_reta_tangente_margem_erro.pack(side=Tk.LEFT)
            self.tbx_reta_tangente_margem_erro.pack(side=Tk.LEFT)
        else:
            self.frame_reta_tangente_x.pack_forget()
            self.frame_reta_tangente_y.pack_forget()
            self.frame_reta_tangente_margem_erro.pack_forget()

    def listener_btn_x_exp_y(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*x**(1)")
        else:
            self.tbx_input.insert(END, "x**(1)")

    def listener_btn_raiz(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*sqrt(x)")
        else:
            self.tbx_input.insert(END, "sqrt(x)")

    def listener_btn_sin(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*sin(x)")
        else:
            self.tbx_input.insert(END, "sin(x)")

    def listener_btn_cos(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*cos(x)")
        else:
            self.tbx_input.insert(END, "cos(x)")

    def listener_btn_tg(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*tan(x)")
        else:
            self.tbx_input.insert(END, "tan(x)")

    def listener_btn_cotg(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*cot(x)")
        else:
            self.tbx_input.insert(END, "cot(x)")

    def listener_btn_soma(self):
            self.tbx_input.insert(END, "+")

    def listener_btn_subtracao(self):
            self.tbx_input.insert(END, "-")

    def listener_btn_multiplicacao(self):
            self.tbx_input.insert(END, "*")

    def listener_btn_divisao(self):
            self.tbx_input.insert(END, "/")

    def listener_btn_patenteses_esquerdo(self):
            self.tbx_input.insert(END, "(")

    def listener_btn_patenteses_direito(self):
            self.tbx_input.insert(END, ")")

    def listener_btn_raiz_a_x(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*root(x, 1)")
        else:
            self.tbx_input.insert(END, "root(x, 1)")

    def listener_btn_x(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*x")
        else:
            self.tbx_input.insert(END, "x")

    def listener_btn_log(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*log(x)")
        else:
            self.tbx_input.insert(END, "log(x)")

    def listener_btn_log_a_x(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*log(10, x)")
        else:
            self.tbx_input.insert(END, "log(10, x)")

    def listener_btn_nepper(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*E")
        else:
            self.tbx_input.insert(END, "E")

    def listener_btn_exp_nepper(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*E**(x)")
        else:
            self.tbx_input.insert(END, "E**(x)")

    def listener_btn_log_nepper(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*ln(x)")
        else:
            self.tbx_input.insert(END, "ln(x)")
    
    def listener_btn_pi(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*pi")
        else:
            self.tbx_input.insert(END, "pi")
    
    def listener_btn_arcsen(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*asin(x)")
        else:
            self.tbx_input.insert(END, "asin(x)")

    
    def listener_btn_arccot(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*acot(x)")
        else:
            self.tbx_input.insert(END, "acot(x)")

    
    def listener_btn_arctan(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*atan(x)")
        else:
            self.tbx_input.insert(END, "atan(x)")

    def listener_btn_secante(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*sec(x)")
        else:
            self.tbx_input.insert(END, "sec(x)")

    def listener_btn_cosecante(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*csc(x)")
        else:
            self.tbx_input.insert(END, "csc(x)")

    def listener_btn_arccos(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*acos(x)")
        else:
            self.tbx_input.insert(END, "acos(x)")

    
    def listener_btn_arcsecante(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*asec(x)")
        else:
            self.tbx_input.insert(END, "asec(x)")

    
    def listener_btn_arccosecante(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*acsc(x)")
        else:
            self.tbx_input.insert(END, "acsc(x)")

    
    def listener_btn_arccotan(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*acot(x)")
        else:
            self.tbx_input.insert(END, "acot(x)")

    def get_coords(self, funcao, show_tangente=False):

        d = Diferencial()

        if self.chkbx_reta_toggle_state.get() == 1:
            coordenada_x = self.tbx_reta_tangente_x.get("1.0",END)
            coordenada_x = coordenada_x.strip('\n')

            coordenada_y = self.tbx_reta_tangente_y.get("1.0",END)
            coordenada_y = coordenada_y.strip('\n')

            margem_erro = self.tbx_reta_tangente_margem_erro.get("1.0",END)
            margem_erro = margem_erro.strip('\n')
            if(len(coordenada_x) > 0 and len(coordenada_y) > 0):
                try:
                    try:
                        coordenada_x = float(coordenada_x)
                    except Exception as e:
                        messagebox.showerror("Erro","O valor da coordenada x não é valido!\n\n"+ str(e))

                    try:
                        coordenada_y = float(coordenada_y)
                    except Exception as e:
                        messagebox.showerror("Erro","O valor da coordenada y não é valido!\n\n"+ str(e))

                    validar=None
                    if len(margem_erro)>0:
                        try:
                            margem_erro = float(margem_erro)
                            validar = d.inFuncao(funcao, coordenada_x, coordenada_y, margem_erro=margem_erro)
                        except ValueError as e:
                            messagebox.showerror("Erro","O valor da margem de erro não é valido! Usando o valor default!\n\n"+ str(e))
                            validar = d.inFuncao(funcao, coordenada_x, coordenada_y)
                    else:
                        validar = d.inFuncao(funcao, coordenada_x, coordenada_y)
                    if not validar:
                        messagebox.showwarning("Atenção", "Os pontos inseridos não fazem parte da função!")
                    else:
                        d.retaTangentePonto(funcao, coordenada_x, coordenada_y, show_tangente=True)
                except Exception as e:
                    messagebox.showerror("Erro!", 
                                        "Não foi possivel calcular a reta tangente no ponto ("
                                        +str(coordenada_x)+", "+str(coordenada_y)+") da funçao inserida!\n\n" + str(e))
            else:
                messagebox.showerror("Erro!", "Os campos (x, y) não podem ser vazios!")

        else:
            d.retaTangentePonto(funcao)
