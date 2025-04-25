import pyodbc
from tkinter import *
from funcoesloja import *
from funcoescaixa import *
from cores import *

#########################################################################################

class Aplicacao(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Comandos SQL Nissei")
        self.geometry("550x550")
        self.configure(bg=amarelo_nissei)

        self.filial = ""

        # Container principal
        container = Frame(self, bg=amarelo_nissei)
        container.pack(fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.telas = {}
        
                                                                                        #<--loja|caixa-->
        for T in (Homepage, MenuProblemas, DataHub, PrimaryCheio, AtualizarBiometria, IntegrarNota, Homepage_caixa, MenuProblemas_caixa, LimpezaCaixa, HabilitarCartaoPresente, AtualizarBiometriaCaixa):
            tela = T(container, self)
            self.telas[T] = tela
            tela.grid(row=0, column=0, sticky="nsew")
        
        # Mostra a Home
        self.mostrar_tela(Homepage)
    
    def mostrar_tela(self, tela_class):
        tela = self.telas[tela_class]

        if hasattr(tela, 'atualizar'):
            tela.atualizar()

        tela.tkraise()

##############################CONEXÃO-CONEXÃO-CONEXÃO###########################################################

class Homepage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):

        topo_frame = Frame(self, bg=amarelo_nissei)
        topo_frame.pack(pady=30)
        Label(topo_frame, text="Informe o número da ", fg=azul_nissei, bg=amarelo_nissei, font=("Arial", 20, "bold")).pack(side=LEFT)
        Label(topo_frame, text="FILIAL", fg=azul_nissei, bg=amarelo_nissei, font=("Arial", 20, "underline", "bold")).pack(side=LEFT)
    

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 17))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=20)

        Button(self, text="Menu LOJA", width=15, height=1, bg=azul_nissei, fg="#ffffff", font=("Arial", 14), command=lambda: self.conectar_banco_loja()).pack(pady=10)
        Button(self, text="Menu CAIXA", width=15, height=1, bg=azul_nissei, fg="#ffffff", font=("Arial", 14), command=lambda: self.conectar_banco_caixa()).pack(pady=10)

    def confirmar_filial(self):
        filial_digitada = self.entrada.get()
        self.controller.filial = filial_digitada
        self.entrada.delete(0, END)

        if filial_digitada.strip() == "" or filial_digitada == "Digite aqui..." or filial_digitada == '0':
            return
        
        self.controller.ip = gerar_ip(filial_digitada)

    def conexao_servidor(self):    
        ip_loja = self.controller.ip + "24"
        print(ip_loja)

        ip_loja = r'localhost\SQLEXPRESS' #APAGAR

        if len(ip_loja) > 5:
            self.controller.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={ip_loja};'
                f'DATABASE=LOJA;'
                'Trusted_Connection=yes;' #APAGAR
                # f'UID=sa;'
                # f'PWD=ERPM@2017;'
            )
            print("Conectado com sucesso ao banco!")
            self.controller.mostrar_tela(MenuProblemas)
            self.controller.ip = ""
        else:
            return

    def conectar_banco_loja(self):
        self.confirmar_filial()
        self.conexao_servidor()

    def conectar_banco_caixa(self):
        self.confirmar_filial()
        if self.controller.ip.strip() == "" or self.controller.ip == "Digite aqui..." or self.controller.ip == '0':
            return
        self.controller.mostrar_tela(Homepage_caixa)
    
    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

########################LOJA-LOJA-LOJA-LOJA#################################################################

class MenuProblemas(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        
        # Widget estático
        self.texto_menu = Label(self, text="", font=("Arial", 15, "bold"), bg=amarelo_nissei, fg=azul_nissei)
        self.texto_menu.pack(pady=30)

        Button(self, text="DATA HUB", width=15, height=2, command=lambda: self.controller.mostrar_tela(DataHub)).pack(pady=5)
        Button(self, text="Primary Cheio", width=15, height=2, command=lambda: self.controller.mostrar_tela(PrimaryCheio)).pack(pady=5)
        Button(self, text="Atualizar Matrícula", width=15, height=2, command=lambda: self.controller.mostrar_tela(AtualizarBiometria)).pack(pady=5)
        Button(self, text="Alterar filial", width=15, height=2, bg=azul_nissei, fg="white", command=lambda: alterar_filial(self, Homepage)).pack(pady=5)

    def atualizar(self):
        filial = self.controller.filial
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS\n\nFILIAL: {filial}") 
#########################################################################################

class DataHub(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_status = Label(self, text="STATUS DO DATAHUB:", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status.pack(pady=30)

        Button(self, text="Habilitar DataHub", width=15, height=2, bg='green', fg="white", command=self.habilitar_db).pack(pady=5)
        Button(self, text="Desabilitar DataHub", width=15, height=2, bg='red', fg="white", command=self.desabilitar_db).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="white", command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_status.config(text="STATUS DO DATAHUB:")]).pack(pady=5)

    def habilitar_db(self):
        resultado = habilitar_datahub(self.controller.conn)
        self.texto_status.config(text="Data Hub HABILITADO")
    
    def desabilitar_db(self):
        resultado = desabilitar_datahub(self.controller.conn)
        self.texto_status.config(text="Data Hub DESABILITADO")
        
#########################################################################################

class PrimaryCheio(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_primary_cheio = Label(self, text="Deseja realizar a limpeza de Log's?", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_primary_cheio.pack(pady=20)

        self.texto_primary_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 9))
        self.texto_primary_confirmacao.pack(pady=5)

        self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
        self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
        self.confirmar_limpeza.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_log, font=("Arial", 14)).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="#ffffff", command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

    def limpar_log(self):
        confirmacao = self.confirmar_limpeza.get().strip()
        
        if confirmacao.lower() == 's':
            limpeza_concluida = primary_cheio(self.controller.conn)
            self.texto_primary_confirmacao.config(text=limpeza_concluida, fg='green', font=("Arial", 13, "bold"))
        else:
            self.texto_primary_confirmacao.config(text="Digito de confirmação INCORRETO!\n\nDigite 'S' para confirmar a limpeza!", fg='red', font=("Arial", 10, "bold"))

    def quando_clicar(self, event):
        if self.confirmar_limpeza.get() == "Digite 'S' no campo para realizar...":
            self.confirmar_limpeza.delete(0, END)
            self.confirmar_limpeza.config(fg='black')

#########################################################################################

class AtualizarBiometria(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
    
        self.texto_matricula_titulo = Label(self, text="Informe a matrícula", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_matricula_titulo.pack(pady=30)
    
        self.matricula = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.matricula.insert(0, 'Informe a matrícula...')
        self.matricula.bind('<FocusIn>', self.quando_clicar)
        self.matricula.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.atualizar_bio, font=("Arial", 14)).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="#ffffff", command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

        self.texto_matricula_infos = Label(self, text="", bg="#ffffff", fg=azul_nissei, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_matricula_infos.pack(pady=30, fill='x')

    def atualizar_bio(self):
        matricula_digitada = self.matricula.get()
        self.matricula.delete(0, END)

        if not matricula_digitada.isdigit():
            self.texto_matricula_infos.config(text="Matrícula inválida! Use apenas números.", fg="red")
            return
        else:
            status_colaborador = atualizar_biometria(self.controller.conn, matricula_digitada)
            self.texto_matricula_infos.config(text=status_colaborador, fg=azul_nissei)

    def quando_clicar(self, event):
        if self.matricula.get() == 'Informe a matrícula...':
            self.matricula.delete(0, END)
            self.matricula.config(fg='black')

#########################################################################################

class IntegrarNota(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller









#########################CAIXA-CAIXA-CAIXA################################################################

class Homepage_caixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_selecionar_caixa = Label(self, text="Qual CAIXA será feita a conexão?", fg=azul_nissei, bg=amarelo_nissei, font=("Arial", 20, "bold"))
        self.texto_selecionar_caixa.pack(pady=30, padx=40)

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 17))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", font=("Arial", 14), command=lambda: self.confirmar_caixa()).pack(pady=5)
        Button(self, text="Alterar filial", width=15, height=1, bg=azul_nissei, fg="white", font=("Arial", 14),command=lambda: self.controller.mostrar_tela(Homepage)).pack(pady=5)

        self.texto_erro_selecionar_caixa = Label(self, text="", fg="red", bg=amarelo_nissei, font=("Arial", 20, "bold"))
        self.texto_erro_selecionar_caixa.pack(pady=30, padx=40)

    def confirmar_caixa(self):
        caixa_selecionado = self.entrada.get()
        self.entrada.delete(0, END)

        if caixa_selecionado.strip() == "" or caixa_selecionado == "Digite aqui..." or caixa_selecionado == '0':
            return
        
        ip_caixa = self.controller.ip + caixa_selecionado
        print(ip_caixa)

        ip_caixa = r'localhost\SQLEXPRESS' #APAGAR

        if len(caixa_selecionado) < 2 or caixa_selecionado == None:
            self.controller.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={ip_caixa};'
                f'DATABASE=LOJA;'
                'Trusted_Connection=yes;' #APAGAR
                # f'UID=sa;'
                # f'PWD=ERPM@2017;'
            )
            print("Conectado com sucesso ao banco!")
            self.controller.mostrar_tela(MenuProblemas_caixa)
            self.texto_erro_selecionar_caixa.config(text="")
        else:
            self.texto_erro_selecionar_caixa.config(text="Número de CAIXA inválido!")
            return
    
    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

#########################################################################################

class MenuProblemas_caixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        
        # Widget estático
        self.texto_menu = Label(self, text="", font=("Arial", 15, "bold"), bg=amarelo_nissei, fg=azul_nissei)
        self.texto_menu.pack(pady=30)

        Button(self, text="Atualizar Biometrias", width=15, height=2, command=lambda: self.controller.mostrar_tela(AtualizarBiometriaCaixa)).pack(pady=5)
        Button(self, text="Habilitar\ncartão presente", width=15, height=2, command=lambda: self.controller.mostrar_tela(HabilitarCartaoPresente)).pack(pady=5)
        Button(self, text="Limpeza de LOG", width=15, height=2, command=lambda: self.controller.mostrar_tela(LimpezaCaixa)).pack(pady=5)
        Button(self, text="Alterar caixa", width=15, height=2, bg=azul_nissei, fg="white", command=lambda: self.controller.mostrar_tela(Homepage_caixa)).pack(pady=5)
        Button(self, text="Alterar filial", width=15, height=2, bg=azul_nissei, fg="white", command=lambda: self.controller.mostrar_tela(Homepage)).pack(pady=5)

    def atualizar(self):
        filial = self.controller.filial
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS CAIXA\n\nFILIAL: {filial}")

#########################################################################################

class LimpezaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_limpeza_caixa = Label(self, text="Deseja realizar a limpeza de Log's?", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_limpeza_caixa.pack(pady=20)

        self.texto_limpeza_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 9))
        self.texto_limpeza_confirmacao.pack(pady=5)

        self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
        self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
        self.confirmar_limpeza.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_caixar, font=("Arial", 14)).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="#ffffff", command=lambda: self.controller.mostrar_tela(MenuProblemas_caixa)).pack(pady=5)

    def limpar_caixar(self):
        confirmacao = self.confirmar_limpeza.get().strip()
        
        if confirmacao.lower() == 's':
            limpeza_concluida = limpeza_log_caixa(self.controller.conn)
            self.texto_limpeza_confirmacao.config(text=limpeza_concluida, fg='green', font=("Arial", 13, "bold"))
        else:
            self.texto_limpeza_confirmacao.config(text="Digito de confirmação INCORRETO!\n\nDigite 'S' para confirmar a limpeza!", fg='red', font=("Arial", 10, "bold"))

    def quando_clicar(self, event):
        if self.confirmar_limpeza.get() == "Digite 'S' no campo para realizar...":
            self.confirmar_limpeza.delete(0, END)
            self.confirmar_limpeza.config(fg='black')

#########################################################################################

class HabilitarCartaoPresente(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_titulo_habilitar = Label(self, text="HABILITAR CARTÃO PRESENTE", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_titulo_habilitar.pack(pady=30)
        self.texto_status_cartao = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_cartao.pack(pady=30)

        Button(self, text="Habilitar Venda", width=20, height=3, bg='green', fg="white", command=self.habilitar_cartao_presente).pack(pady=5)
        Button(self, text="Voltar para Menu", width=20, height=3, bg='#015b90', fg="white", command=lambda: [self.controller.mostrar_tela(MenuProblemas_caixa), self.texto_status_cartao.config(text="")]).pack(pady=30)

    def habilitar_cartao_presente(self):
        resultado_habilitar = habilitar_cartao_presente_caixa(self.controller.conn)
        self.texto_status_cartao.config(text=resultado_habilitar)

#########################################################################################

class AtualizarBiometriaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_titulo_bio_caixa = Label(self, text="Atualização de Biometrias no CAIXA", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_bio_caixa.pack(pady=5)
        self.texto_aviso_bio = Label(self, text="| Utilizar este menu após ter atualizado no menu LOJA |", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 10))
        self.texto_aviso_bio.pack(pady=15)
        self.texto_status_truncate = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_truncate.pack(pady=30)

        Button(self, text="Atualizar Biometrias", width=20, height=3, bg='green', fg="white", command=self.atualizar_bio_caixa).pack(pady=5)
        Button(self, text="Voltar para Menu", width=20, height=3, bg='#015b90', fg="white", command=lambda: [self.controller.mostrar_tela(MenuProblemas_caixa), self.texto_status_truncate.config(text="")]).pack(pady=30)

    def atualizar_bio_caixa(self):
        resultado_truncate = atualizar_biometria_caixa(self.controller.conn)
        self.texto_status_truncate.config(text=resultado_truncate)

#########################################################################################


app = Aplicacao()
app.mainloop()