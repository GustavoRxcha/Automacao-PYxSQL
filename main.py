import pyodbc
from tkinter import *
from funcoes import *
from cores import *

#########################################################################################

class Aplicacao(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Comandos SQL Nissei")
        
        self.filial = ""

        # Container principal
        container = Frame(self)
        container.pack(fill="both", expand=True)
        
        self.telas = {}
        
        # Adiciona telas ao dicionário
        for T in (Homepage, MenuProblemas, DataHub, PrimaryCheio, AtualizarBiometria, IntegrarNota):
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

#########################################################################################

class Homepage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):
        self.texto_homepage = Label(self, text="Informe o número da Filial", fg=azul_nissei, bg=amarelo_nissei, font=("Arial", 20))
        self.texto_homepage.pack(pady=30, padx=40)

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=20)

        Button(self, text="Confirmar", width=10, height=1, font=("Arial", 14), command=lambda: self.confirmar_filial()).pack(pady=5)

    def confirmar_filial(self):
        filial_digitada = self.entrada.get()
        self.controller.filial = filial_digitada
        self.entrada.delete(0, END)

        if filial_digitada.strip() == "" or filial_digitada == "Digite aqui..." or filial_digitada == '0':
            return
        
        ip = conectar_banco(filial_digitada)
        print(ip)
        ip = r'localhost\SQLEXPRESS'

        if ip:
            self.controller.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={ip};'
                f'DATABASE=LOJA;'
                'Trusted_Connection=yes;'
            )
            print("Conectado com sucesso ao banco!")
            self.controller.mostrar_tela(MenuProblemas)
    
    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

#########################################################################################

class MenuProblemas(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        
        # Widget estático
        self.texto_menu = Label(self, text="", font=("Arial", 15), bg=amarelo_nissei, fg=azul_nissei)
        self.texto_menu.pack(pady=30)

        Button(self, text="DATA HUB", width=15, height=2, command=lambda: self.controller.mostrar_tela(DataHub)).pack(pady=5)
        Button(self, text="Primary Cheio", width=15, height=2, command=lambda: self.controller.mostrar_tela(PrimaryCheio)).pack(pady=5)
        Button(self, text="Atualizar Matrícula", width=15, height=2, command=lambda: self.controller.mostrar_tela(AtualizarBiometria)).pack(pady=5)

    def atualizar(self):
        filial = self.controller.filial
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS\n\nFILIAL: {filial}")

#########################################################################################

class DataHub(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        self.texto_status = Label(self, text="STATUS DO DATAHUB:", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15))
        self.texto_status.pack(pady=30)

        Button(self, text="Habilitar DataHub", width=15, height=2, bg='green', command=self.habilitar_db).pack(pady=5)
        Button(self, text="Desabilitar DataHub", width=15, height=2, bg='red', command=self.desabilitar_db).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

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

        self.texto_primary_cheio = Label(self, text="Deseja realizar a limpeza de Log's?", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15))
        self.texto_primary_cheio.pack(pady=20)

        self.texto_primary_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 9, "bold"))
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
    
        self.texto_matricula_titulo = Label(self, text="Informe a matrícula", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15))
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

#########################################################################################
app = Aplicacao()
app.mainloop()