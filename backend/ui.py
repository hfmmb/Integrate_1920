import sympy as s
import pathlib
import webbrowser

from backend.mathematics.singles import simpson as trap_simpson
from backend.utilities.string import StringHandler
from backend.mathematics.logic import Diferencial
from os import name
from sys import version_info, exit
from screeninfo import get_monitors
from sympy import S, Symbol, Derivative, Integral, Limit, sin, cos, tan, cot, sinh, cosh, cot, plot, solve, diff, integrate, ln, plot_implicit, evalf, SympifyError, symbols, lambdify


#from decimal import Decimal, DecimalException

if version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import END, Frame, Button, Text, Label, Canvas, Checkbutton, IntVar
    from tkinter.font import Font
    from Tkinter.ttk import Combobox, tkMessageBox
else:
    import tkinter as Tk
    from tkinter import END, Frame, Button, Text, Label, Canvas, Checkbutton, messagebox, IntVar
    from tkinter.font import Font
    from tkinter.ttk import Combobox

class UI(Frame):
    master=Tk.Tk()
    reserved_symbol_dict = {'arcsen':'arcsen','arcsin':'arcsen','arccos':'arccos','arctg':'arctg',
                            'cosen':'cosen'  ,'cosin':'cosen'  ,'cocos':'cocos'}

    def __init__(self, master=master):

        Frame.__init__(self, master)

        self.master.wm_title("Integrate - Derivação e Integração")
        self.master.wm_iconphoto(False, Tk.PhotoImage(file="./icon.png"))

        #Obtem resolução do ecra atual
        resolution = get_monitors()
        screen_width = resolution[0].width
        screen_height = resolution[0].height

        window_width = round(0.50 * screen_width)
        window_height = round(0.28 * screen_height)

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
        funcao_text = "-6*x⁴+2*log(5*x³)+sen(x²)+sqrt(x)"
        self.frame_master_row = Frame(master=self.master, highlightbackground="black", highlightthickness=2)
        self.frame_master_row.pack(side = Tk.TOP)

        self.frame_input_funcao = Frame(master=self.frame_master_row, highlightbackground="black", highlightthickness=1)
        self.frame_input_funcao.pack( side = Tk.TOP )
        self.lbl_function = Label(self.frame_input_funcao, text="f(x)= ", font=fonte)
        self.tbx_input = Text(self.frame_input_funcao, height=2, width=60, font=fonte)
        self.btn_apagar = Button(master=self.frame_input_funcao, command=self.listener_btn_apagar, text='Apagar')
        self.lbl_function.pack(side=Tk.LEFT)
        self.tbx_input.insert(END, funcao_text)
        self.tbx_input.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.btn_apagar.pack(side=Tk.LEFT, fill=Tk.BOTH)

        #Combobox e campos de input do modo selecionado
        self.frame_modo = Frame(master=self.frame_master_row, highlightbackground="black", highlightthickness=1)
        self.lbl_modo = Label(self.frame_modo, text = "Modo: ")
        self.cb_modo = Combobox(self.frame_modo, state='readonly', font=fonte , 
            values=[ "f(x)", "f'(x)", "f''(x)", u"\u222B"+" f(x)dx (Indefinida)", 
                    u"\u222B"+"ab f(x)dx (Definida)" ,u"\u222B"+" f(x)dx Algoritmo Simpson", 
                    "Minimos e Máximos", "Limite"], width=25)
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

        self.lbl_reta_tangente_x = Label(self.frame_reta_tangente_x, text="x:")
        self.lbl_reta_tangente_y = Label(self.frame_reta_tangente_y, text="y:")
        self.tbx_reta_tangente_x = Text(self.frame_reta_tangente_x, height=1, width=10)
        self.tbx_reta_tangente_y = Text(self.frame_reta_tangente_y, height=1, width=10)

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
        self.frame_operacoes = Frame(master=self.frame_master_row, highlightbackground="black", highlightthickness=1, padx=4, pady=6)
        self.lbl_operations = Label(self.frame_operacoes, text="Operações: ")

        self.frame_operacoes_linha_1 = Frame(master=self.frame_operacoes)
        self.btn_soma = Button(self.frame_operacoes_linha_1, command=self.listener_btn_soma, text='+', width=WIDTH_OPER)
        self.btn_subtracao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_subtracao, text='-', width=WIDTH_OPER)
        self.btn_multiplicacao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_multiplicacao, text='*', width=WIDTH_OPER)
        self.btn_divisao = Button(self.frame_operacoes_linha_1, command=self.listener_btn_divisao, text='/', width=WIDTH_OPER)

        self.frame_operacoes_linha_2 = Frame(master=self.frame_operacoes)
        self.btn_sin = Button(self.frame_operacoes_linha_2, command=self.listener_btn_sin, text='sin(x)', width=WIDTH_OPER)
        self.btn_cos = Button(self.frame_operacoes_linha_2, command=self.listener_btn_cos, text='cos(x)', width=WIDTH_OPER)
        self.btn_tg = Button(self.frame_operacoes_linha_2, command=self.listener_btn_tg, text='tang(x)', width=WIDTH_OPER)
        self.btn_cotg = Button(self.frame_operacoes_linha_2, command=self.listener_btn_cotg, text='cotang(x)', width=WIDTH_OPER)

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
        self.btn_abs = Button(self.frame_operacoes_linha_5, command=self.listener_btn_abs, text='Abs(x)', width=WIDTH_OPER)

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
        self.btn_abs.pack(side=Tk.LEFT, fill=Tk.BOTH)

        self.frame_btn_comandos = Frame(master=self.frame_master_row)
        self.btn_resolver = Button(master=self.frame_btn_comandos, text='Resolver', command=self.listener_btn_resolver)
        self.btn_info = Button(master=self.frame_btn_comandos, command=self.listener_btn_info, text='Info')
        self.btn_sair = Button(master=self.frame_btn_comandos, command=self.listener_btn_sair, text='Sair', )

        self.frame_btn_comandos.pack(side=Tk.TOP)
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
            cb_index = self.cb_modo.current()
            x, y = symbols('x y', real=True)


            if(len(self.get_txb_input_text())<=1):
                messagebox.showerror("Erro!", "Escreva a função na caixa de texto!")
            else:
                    
                handler = StringHandler()
                funcao = handler.process_ready(str(self.get_txb_input_text()))

                #f(x)
                if cb_index == 0:
                    funcao_pretty = "f(x)="+ handler.pretty_ready(funcao)
                    funcao_plot = plot(funcao, title=funcao_pretty, show=False)
                    funcao_plot.legend=True
                    funcao_plot[0].label=funcao_pretty

                    #Reta tangente no ponto da função
                    if self.chkbx_reta_toggle_state.get() == 1:
                        try:
                            coordenada_x = None
                            coordenada_y = None
                            try:
                                coordenada_x = float(self.tbx_reta_tangente_x.get("1.0",END))
                            except Exception:
                                messagebox.showerror("Erro","O valor da coordenada x não é valido!")
                            try:
                                coordenada_y = float(self.tbx_reta_tangente_y.get("1.0",END))
                            except Exception:
                                messagebox.showerror("Erro","O valor da coordenada y não é valido!")
                            m, a, b = symbols("m a b")
                            #Obtem a derivada da funcao
                            funcao_deriv = diff(funcao)
                            funcao_deriv = str(funcao_deriv)
                            #Tranforma a funcao em ordem a "m" para obter o declive
                            funcao_deriv = funcao_deriv + "-y"
                            g=lambdify((x, y), funcao_deriv)
                            #Substitui as coordenadas do ponto na funcao
                            m_value=g(float(coordenada_x), float(coordenada_y))

                            print("Derivada: ", funcao_deriv)
                            print("m=", m_value)


                            f_r_tangente = lambdify((m, x, a, b), "m*(x-a)-b")
                            f_final = f_r_tangente(m_value, x, float(coordenada_x), float(coordenada_y))
                            reta_tangente = str(f_final)
                            
#                            sp.plot(str(f_final))

                            reta_tangente_pretty = "Reta tangente no ponto ("+str(coordenada_x)+", "+str(coordenada_y)+") de f(x)="+handler.pretty_ready(reta_tangente)
                            funcao_deriv_plot = plot(reta_tangente, show=False)
                            funcao_plot.append(funcao_deriv_plot[0])
                            funcao_plot[1].label=reta_tangente_pretty
                            funcao_plot[1].line_color = 'firebrick'

                            print("Reta tangente: ", reta_tangente)

                        except Exception:
                            messagebox.showerror("Erro!", "Não foi possivel calcular a reta tangente no ponto ("+str(coordenada_x)+", "+str(coordenada_y)+") da funçao inserida!")

                    funcao_plot.show()

                #f'(x)
                elif cb_index == 1:
                    funcao_deriv = diff(funcao)

                    funcao_deriv_pretty = "f'(x)="+handler.pretty_ready(str(funcao_deriv))
                    messagebox.showinfo("Derivate", handler.pretty_ready(str(funcao_deriv_pretty)))
                    funcao_plot = plot(funcao_deriv, title=funcao_deriv_pretty)

                #f''(x)
                elif cb_index == 2:
                    derivada = diff(funcao)

                    segunda_derivada = diff(derivada)
                    funcao_segunda_derivada_pretty = "f''(x)="+handler.pretty_ready(str(segunda_derivada))
                    plot(segunda_derivada, title=funcao_segunda_derivada_pretty)

                #Integral sem intervalos (Indefinida) (Primitivas)
                elif cb_index == 3:
    #                messagebox.showinfo("Integrate", handler.pretty_ready(str(j)))
                    try:
                        primitiva = integrate(funcao)
                        integral_calculo_zeros = solve(integrate(funcao).doit())
                        primitiva_pretty = u"\u222B"+"f(x)dx="+handler.pretty_ready(str(primitiva))
                        messagebox.showinfo("Resultado Primitiva / Integral Definida!", str(primitiva_pretty)+"\nZeros: "+ str(integral_calculo_valor))
                        plot(primitiva, title=primitiva_pretty)

                    except Exception as e:
                        messagebox.showerror("Erro!", "Não foi possivel calcular a integral desta função!\n" + e)

                #Integral com intervalos (definida)
                elif cb_index == 4:

                    valor_inferior, valor_superior = str(self.tbx_input_inferior.get("1.0", END)), str(self.tbx_input_superior.get("1.0", END))
                    if(len(valor_inferior) > 1 and len(valor_superior) > 1):
                        try:
                            if valor_inferior != "-00":
                                valor_inferior = int(valor_inferior)
                            if valor_superior != "00" and valor_superior != "+00" :
                                valor_superior = int(valor_superior)

                            if(valor_inferior > valor_superior):
                                aux = int(valor_superior)
                                valor_superior = int(valor_inferior)
                                valor_inferior = int(aux)
                            try:
                                funcao_integral = integrate(funcao, (x, valor_inferior, valor_superior))
                                integral = str(funcao_integral.doit())
                                try:
                                    integral_aproximada = funcao_integral.evalf()
                                    messagebox.showinfo("Resultado integral definida","O valor da integral calculada é de aproximadamente: "+ str(integral_aproximada))
                                except Exception:
                                    messagebox.showinfo("Resultado integral definida","O valor em fracção da integral calculada é de: "+ integral)
                            except Exception:
                                messagebox.showerror("Erro!","Não foi possivel calcular o valor da integral dada no intervalo de limites ["+valor_inferior+", "+valor_superior+"]!")        
                        except Exception:
                            messagebox.showerror("Erro!","Apenas numeros são permitidos!")
                    else:
                        messagebox.showerror("Erro!","Preencha os campos de valores inferior e superior!")

                #Integral Simpson (Valor)
                elif cb_index == 5:
                    valor_inferior = 0
                    valor_superior = 100

                    total_subintervalos=int(100)
#                    integral_valor = integral_valor.as_sum(total_subintervalos).n(100)

#                    e = Integral("1/sqrt(x)", (x, 0, 1)).as_sum(10, evaluate=True).n(4)
                    diferencial=Diferencial()

                    try:
                        if valor_inferior == None and valor_superior == None:
                            valor = diferencial.Intergral_Valor(funcao)
                        else:
                            valor = diferencial.Intergral_Valor(funcao, 0, 1)
                        messagebox.showinfo("Resultado Integral!", "Valor: "+ str(valor))
                    except Exception as err:
                        print(err)
#                    messagebox.showinfo("Resultado Integral!", "Valor: "+ str(integral_valor))

                    precisao = 64
                    resultado_calculo = trap_simpson(valor_inferior, valor_superior, precisao)
                    resultado_integral , resultado_intervalo = resultado_calculo

                    messagebox.showinfo("Integral Algoritmo Simpson", 
                                        "Valor calculado: " + str(resultado_integral)+
                                        "\n\nIntervalos encontrados: "+ str(resultado_intervalo))

                #Minimos e maximos da função
                elif cb_index == 6: 
                    try:
                        solucao = solve(Derivative(funcao, x).doit())
                        messagebox.showinfo("Minimos e Maximos", "Minimo / Maximo absoluto: " +  str(solucao))

                    except Exception:
                        messagebox.showerror("Erro!", "Não foi possivel calcular os minimos e maximos da função!")

                #Limites
                elif cb_index == 7:
#                    print(solve(Limit(funcao, x, S.Infinity).doit(), dict=True))
                    #plot(funcao, title=funcao)

                    valor_tendencia_limite = str(self.tbx_input_valor_limite.get("1.0", END))
                    if valor_tendencia_limite == '00' or valor_tendencia_limite == '+00':
                        valor_tendencia_limite = S.Infinity
                    elif valor_tendencia_limite == '-00':
                        valor_tendencia_limite = S.NegativeInfinity

                    mensagem = ""
                    sinal = str(self.tbx_input_sinal_limite.get("1.0", END)) #Limite a esquerda ou direita da funcao
                    if sinal=='+':
                        mensagem = "direita"
                    elif sinal=='-':
                        mensagem = "esquerda"
                    else:
                        sinal=None
                        messagebox.showwarning("Sinal invalido!", "Sinal do limite não definido! (-) esquerda (+) direita.")

                        limite = None
                        if sinal == None:
                            try:
                                limite = solve(Limit(funcao, x, valor_tendencia_limite).doit())
                                messagebox.showinfo("Limite da função", 
                                                    "O limite da função para x->"+valor_tendencia_limite+"é: "+ str(limite))
                            except Exception:
                                messagebox.showerror("Erro!", "Não foi possivel calcular o limite de x->"+valor_tendencia_limite+" para a função dada!")                                
                        else:
                            try:
                                limite = Limit(funcao, x, valor_tendencia_limite , dir=sinal).doit()
                                messagebox.showinfo("Limite da função à"+mensagem+" ("+sinal+")", 
                                                    "O limite à "+mensagem+" ("+sinal+") da função é: "+ str(limite))
                            except Exception as e:
                                messagebox.showerror("Erro!", "Não foi possivel calcular o limite à "+mensagem+" ("+sinal+") para a função dada!")
                    plot(Limit(funcao, x, valor_tendencia_limite).doit(), title=Limit(funcao, x, valor_tendencia_limite))

        except Exception:
            messagebox.showerror("ERRO!", "Não foi possivel resolver a expressao inserida, está bem escrita?")

    def listener_btn_apagar(self):
        self.tbx_input.delete('1.0', END)
        print('Limpando texto...')

    def listener_btn_info(self):
        path = str(pathlib.Path(__file__).parent.absolute().parent)
        if "nt" in name:
            path = path + '\manual.html'
        else:
            path = path + '/manual.html'
        
        try:
            try:
                webbrowser.open_new_tab(path)
            except Exception :
                messagebox.showerror("Erro!", "Não foi possivel aceder ao browser do sistema operativo!\n")
        except FileNotFoundError as e:
            messagebox.showerror("Erro!", "Não foi possivel aceder aos ficheiros da documentação!\n" + e)

    def listener_btn_sair(self):
        exit()

    def listener_cb_modo(self, event):
        '''
        Change listener da combobox
        '''
        selected_index = self.cb_modo.current()

        # f(x) e reta tangente no ponto
        if(selected_index == 0):
            self.frame_reta_tangente.pack(side=Tk.LEFT)
            self.chkbx_reta_tg.pack(side=Tk.LEFT)

        #Integral Definida
        elif(selected_index == 4):
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
            self.lbl_reta_tangente_y.pack(side=Tk.LEFT)
            self.tbx_reta_tangente_y.pack(side=Tk.LEFT)
        else:
            self.frame_reta_tangente_x.pack_forget()
            self.frame_reta_tangente_y.pack_forget()

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
            self.tbx_input.insert(END, "*root(a, x)")
        else:
            self.tbx_input.insert(END, "root(a, x)")

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
    """
    def listener_btn_abs(self):
        if (len(self.tbx_input.get('1.0', END))-1>0):
            self.tbx_input.insert(END, "*Abs(x)")
        else:
            self.tbx_input.insert(END, "Abs(x)")
    """