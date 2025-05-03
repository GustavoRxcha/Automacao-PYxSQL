import pyodbc
from tkinter import *
import subprocess
from PIL import Image, ImageTk
from funcoesloja import *
from funcoescaixa import *
from cores import *

#########################################################################################

class Aplicacao(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Comandos SQL Nissei")
        self.geometry("600x750")
        self.configure(bg=amarelo_nissei)

        self.filial = ""

        logo = Image.open("Logo_nissei.png")  # pode ser .jpg, .png etc
        logo = logo.resize((330, 180))  # redimensiona, se quiser
        self.logo_tk = ImageTk.PhotoImage(logo)

        # Container principal
        container = Frame(self, bg=amarelo_nissei)
        container.pack(fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.telas = {}
                                                                                               
        for T in (Homepage, MenuProblemas, DataHub, AtualizarEstoque, AtualizarBiometria, IntegrarNota, AtualizarVersaoLoja, LimparTemp,                                    #<--LOJA
                  HomepageCaixa, MenuProblemasCaixa, HabilitarCartaoPresente, AtualizarBiometriaCaixa, AtualizarVersaoCaixa, TabelaZeroCaixa,                               #<--CAIXA
                  ConsultarVendaCaixa, HabilitarVNCCaixa):                                                                                                                  #<--CAIXA
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
        
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        topo_frame = Frame(self, bg=amarelo_nissei)
        topo_frame.pack(pady=20)

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

        if len(ip_loja) > 5:
            self.controller.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={ip_loja};'
                f'DATABASE=LOJA;'
                f'UID=sa;'
                f'PWD=ERPM@2017;'
                'Connection Timeout=3;'
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
        self.controller.mostrar_tela(HomepageCaixa)
    
    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################
########################LOJA-LOJA-LOJA-LOJA#################################################################

class MenuProblemas(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        # Widget estático
        self.texto_menu = Label(self, text="", font=("Arial", 15, "bold"), bg=amarelo_nissei, fg=azul_nissei)
        self.texto_menu.pack(pady=(0, 30))

        botoes_frame = Frame(self, bg=amarelo_nissei)
        botoes_frame.pack()

        botoes = [
            ("Atualizar Matrícula", lambda: self.controller.mostrar_tela(AtualizarBiometria)),
            ("Atualizar Estoque", lambda: self.controller.mostrar_tela(AtualizarEstoque)),
            ("Integrar NF", lambda: self.controller.mostrar_tela(IntegrarNota)),
            ("DATA HUB", lambda: self.controller.mostrar_tela(DataHub)),
            ("Atualizar Versão\nPREVENDA", lambda: self.controller.mostrar_tela(AtualizarVersaoLoja)),
            ("Limpar %TEMP%", lambda: self.controller.mostrar_tela(LimparTemp)),
        ]

        for i, (texto, comando) in enumerate(botoes):
            linha = i // 2
            coluna = i % 2
            cor = "#ee3642" if "Alterar" in texto else azul_nissei

            Button(botoes_frame, text=texto, width=22, height=3, bg=cor, fg="white", font=("Arial", 13, "bold"), command=comando).grid(row=linha, column=coluna, padx=20, pady=10, sticky="nsew")

        #ajuste proporção
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)

        Button(self, text="Alterar filial", width=25, height=2, bg="#ee3642", fg="white", font=("Arial", 14, "bold"), command=lambda: alterar_filial(self, Homepage)).pack(pady=(30, 10))

    def atualizar(self):
        filial = self.controller.filial
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS\n\nFILIAL: {filial}")
#########################################################################################

class DataHub(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_status = Label(self, text="STATUS DO DATAHUB:", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status.pack(pady=30)

        Button(self, text="Habilitar DataHub", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.habilitar_db).pack(pady=10)
        Button(self, text="Desabilitar DataHub", width=15, height=1, bg="red", fg="#ffffff", font=("Arial", 14), command=self.desabilitar_db).pack(pady=10)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="white", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_status.config(text="STATUS DO DATAHUB:")]).pack(pady=5)

    def habilitar_db(self):
        resultado = habilitar_datahub(self.controller.conn)
        self.texto_status.config(text="Data Hub HABILITADO")
    
    def desabilitar_db(self):
        resultado = desabilitar_datahub(self.controller.conn)
        self.texto_status.config(text="Data Hub DESABILITADO")
        
#########################################################################################

#ADICIONAR A CLASSE NO DICIONARIO DE TELAS

# class PrimaryCheio(Frame):
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, bg=amarelo_nissei)
#         self.controller = controller

#         self.texto_primary_cheio = Label(self, text="Deseja realizar a limpeza de Log's?", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
#         self.texto_primary_cheio.pack(pady=20)

#         self.texto_primary_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 9))
#         self.texto_primary_confirmacao.pack(pady=5)

#         self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 14))
#         self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
#         self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
#         self.confirmar_limpeza.pack(pady=20)

#         Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_log, font=("Arial", 14)).pack(pady=5)
#         Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="#ffffff", command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

#     def limpar_log(self):
#         confirmacao = self.confirmar_limpeza.get().strip()
        
#         if confirmacao.lower() == 's':
#             limpeza_concluida = primary_cheio(self.controller.conn)
#             self.texto_primary_confirmacao.config(text=limpeza_concluida, fg='green', font=("Arial", 13, "bold"))
#         else:
#             self.texto_primary_confirmacao.config(text="Digito de confirmação INCORRETO!\n\nDigite 'S' para confirmar a limpeza!", fg='red', font=("Arial", 10, "bold"))

#     def quando_clicar(self, event):
#         if self.confirmar_limpeza.get() == "Digite 'S' no campo para realizar...":
#             self.confirmar_limpeza.delete(0, END)
#             self.confirmar_limpeza.config(fg='black')

#########################################################################################

class AtualizarBiometria(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
    
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_matricula_titulo = Label(self, text="Informe a matrícula", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_matricula_titulo.pack(pady=30)
    
        self.matricula = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.matricula.insert(0, 'Informe a matrícula...')
        self.matricula.bind('<FocusIn>', self.quando_clicar)
        self.matricula.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.atualizar_bio).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

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

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_integrar_titulo = Label(self, text="Informe a CHAVE NFE para integração", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_integrar_titulo.pack(pady=30)

        self.aviso = Label(self, text="EM TESTES", bg=amarelo_nissei, fg="red", font=("Arial", 20, "bold"))
        self.aviso.pack(pady=1)
    
        self.chave_nfe = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.chave_nfe.insert(0, 'Informe a chave...')
        self.chave_nfe.bind('<FocusIn>', self.quando_clicar)
        self.chave_nfe.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.integrar_nf).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_integrar_infos.config(text="", fg='black')]).pack(pady=5)

        self.texto_integrar_infos = Label(self, text="", bg="#ffffff", fg=azul_nissei, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_integrar_infos.pack(pady=30, fill='x')

    def integrar_nf(self):
        chave_digitada = self.chave_nfe.get()
        self.chave_nfe.delete(0, END)

        if not chave_digitada.isdigit():
            self.texto_integrar_infos.config(text="CHAVE inválida! Use apenas números.", fg="red")
            return
        else:
            integracao_nota = integrar_nota(self.controller.conn, chave_digitada)
            self.texto_integrar_infos.config(text=integracao_nota, fg=azul_nissei)

    def quando_clicar(self, event):
        if self.chave_nfe.get() == 'Informe a chave...':
            self.chave_nfe.delete(0, END)
            self.chave_nfe.config(fg='black')

#########################################################################################

class AtualizarEstoque(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_titulo_estoque = Label(self, text="Atualizar estoque da Filial", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_estoque.pack(pady=30)
        self.texto_resultado_estoque = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_resultado_estoque.pack(pady=30)

        Button(self, text="Atualizar estoque", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.atualizar_estoque_loja).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_resultado_estoque.config(text="")]).pack(pady=30)

    def atualizar_estoque_loja(self):
        resultado_atualizacao = atualizar_estoque(self.controller.conn)
        self.texto_resultado_estoque.config(text=resultado_atualizacao)

#########################################################################################

class AtualizarVersaoLoja(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_versao = Label(self, text="Versão atual PREVENDA:", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_versao.pack(pady=30)

        self.inserir_versao = Entry(self, fg='grey', width=30, font=("Arial", 16))
        self.inserir_versao.insert(0, 'Informe a versão...')
        self.inserir_versao.bind('<FocusIn>', self.quando_clicar)
        self.inserir_versao.pack(pady=(40, 20))

        Button(self, text="Atualizar Versão", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.atualiza_versao).pack(pady=5)
        Button(self, text="Consultar Versão", width=15, height=1, bg=azul_nissei, fg="#ffffff", font=("Arial", 14), command=self.consulta_de_versao).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="white", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_versao.config(text="Versão atual:")]).pack(pady=5)

        self.info_versao = Label(self, text="| Versões que utilizamos atualmente |\n\nPDV: 3.0.0.280            \nPREVENDA: 1.102.081", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.info_versao.pack(pady=30)

    def consulta_de_versao(self):
        resultado_versao = consultar_versao(self.controller.conn)
        self.texto_versao.config(text=f"Versão atual PREVENDA {resultado_versao}")
    
    def atualiza_versao(self):
        versao_digitada = self.inserir_versao.get()
        self.inserir_versao.delete(0, END)

        if len(versao_digitada) > 6:
            resultado_atualizacao = atualizar_versao(self.controller.conn, versao_digitada)
            self.texto_versao.config(text=f"Versão atual PREVENDA {resultado_atualizacao}")
        else:
            return

    def quando_clicar(self, event):
        if self.inserir_versao.get() == 'Informe a versão...':
            self.inserir_versao.delete(0, END)
            self.inserir_versao.config(fg='black')

#########################################################################################

class LimparTemp(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
    
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_informar_ip = Label(self, text="Informe o IP do terminal", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_informar_ip.pack(pady=30)

        self.aviso = Label(self, text="EM CONSTRUÇÃO", bg=amarelo_nissei, fg="red", font=("Arial", 20, "bold"))
        self.aviso.pack(pady=30)
    
        self.entry_ip = Entry(self, fg='grey', width=30, font=("Arial", 14))
        self.entry_ip.insert(0, 'Informe o IP...')
        self.entry_ip.bind('<FocusIn>', self.quando_clicar)
        self.entry_ip.pack(pady=20)

        #Button(self, text="Limpar %Temp%", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.limpar_temp).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: self.controller.mostrar_tela(MenuProblemas)).pack(pady=5)

        self.texto_limpeza_status = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_limpeza_status.pack(pady=30, fill='x')

    def limpar_temp(self):
        ip_digitado = self.entry_ip.get()
        self.entry_ip.delete(0, END)

        try:
            status_limpeza = limpar_temp_ps1(self.controller.conn, ip_digitado)
            self.texto_limpeza_status.config(text=status_limpeza, fg=azul_nissei)
        except:
            self.texto_limpeza_status.config(text="ERRO na execução do PowerShell\nIP incorreto.", fg="red")


    def quando_clicar(self, event):
        if self.entry_ip.get() == 'Informe o IP...':
            self.entry_ip.delete(0, END)
            self.entry_ip.config(fg='black')

#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################
#########################CAIXA-CAIXA-CAIXA################################################################

class HomepageCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_selecionar_caixa = Label(self, text="Qual CAIXA será feita a conexão?", fg=azul_nissei, bg=amarelo_nissei, font=("Arial", 20, "bold"))
        self.texto_selecionar_caixa.pack(pady=30, padx=40)

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 17))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=20)

        Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", font=("Arial", 14), command=lambda: self.confirmar_caixa()).pack(pady=5)
        Button(self, text="Alterar filial", width=15, height=1, bg="#ee3642", fg="white", font=("Arial", 14),command=lambda: self.controller.mostrar_tela(Homepage)).pack(pady=5)

        self.texto_erro_selecionar_caixa = Label(self, text="", fg="red", bg=amarelo_nissei, font=("Arial", 20, "bold"))
        self.texto_erro_selecionar_caixa.pack(pady=30, padx=40)

    def confirmar_caixa(self):
        self.controller.caixa_selecionado = self.entrada.get()
        self.entrada.delete(0, END)

        if self.controller.caixa_selecionado.strip() == "" or self.controller.caixa_selecionado == "Digite aqui..." or self.controller.caixa_selecionado == '0':
            return
        
        self.controller.ip_caixa = self.controller.ip + self.controller.caixa_selecionado
        print(self.controller.ip_caixa)

        try:
            if len(self.controller.caixa_selecionado) < 2 or self.controller.caixa_selecionado == None:
                self.controller.conn = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={self.controller.ip_caixa};'
                    f'DATABASE=PDV;'
                    f'UID=sa;'
                    f'PWD=ERPM@2017;'
                    'Connection Timeout=3;'
                )
                print("Conectado com sucesso ao banco!")
                self.controller.mostrar_tela(MenuProblemasCaixa)
                self.texto_erro_selecionar_caixa.config(text="")
            else:
                self.texto_erro_selecionar_caixa.config(text="Número de CAIXA inválido!")
                return
        except:
            self.texto_erro_selecionar_caixa.config(text="Falha na conexão com o banco.")
    
    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

#########################################################################################

class MenuProblemasCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller
        
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_menu = Label(self, text="", font=("Arial", 15, "bold"), bg=amarelo_nissei, fg=azul_nissei)
        self.texto_menu.pack(pady=(0, 30))

        botoes_frame = Frame(self, bg=amarelo_nissei)
        botoes_frame.pack()

        botoes = [
            ("Atualizar Biometrias", lambda: self.controller.mostrar_tela(AtualizarBiometriaCaixa), azul_nissei),
            ("Tabela 0", lambda: self.controller.mostrar_tela(TabelaZeroCaixa), azul_nissei),
            ("Habilitar\ncartão presente", lambda: self.controller.mostrar_tela(HabilitarCartaoPresente), azul_nissei),
            ("Atualizar Versão\nPDV", lambda: self.controller.mostrar_tela(AtualizarVersaoCaixa), azul_nissei),
            ("Verificar Vendas", lambda: self.controller.mostrar_tela(ConsultarVendaCaixa), azul_nissei),
            ("Habilitar VNC", lambda: self.controller.mostrar_tela(HabilitarVNCCaixa), azul_nissei),
            ("Alterar caixa", lambda: self.controller.mostrar_tela(HomepageCaixa), "#ee3642"),
            ("Alterar filial", lambda: self.controller.mostrar_tela(Homepage), "#ee3642"),
        ]

        for i, (texto, comando, cor) in enumerate(botoes):
            linha = i // 2
            coluna = i % 2

            Button(botoes_frame, text=texto, width=22, height=3, bg=cor, fg="white", font=("Arial", 13, "bold"), command=comando).grid(row=linha, column=coluna, padx=20, pady=10, sticky="nsew")

        #ajuste proporção
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)
        
    def atualizar(self):
        filial = self.controller.filial
        caixa = self.controller.caixa_selecionado
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS CAIXA\n\nFILIAL: {filial}\nCAIXA: {caixa}")

#########################################################################################

#ADICIONAR A CLASSE NO DICIONARIO DE TELAS

# class LimpezaCaixa(Frame):
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, bg=amarelo_nissei)
#         self.controller = controller

#         self.texto_limpeza_caixa = Label(self, text="Deseja realizar a limpeza de Log's?", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
#         self.texto_limpeza_caixa.pack(pady=20)

#         self.texto_limpeza_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 9))
#         self.texto_limpeza_confirmacao.pack(pady=5)

#         self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 14))
#         self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
#         self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
#         self.confirmar_limpeza.pack(pady=20)

#         Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_caixar, font=("Arial", 14)).pack(pady=5)
#         Button(self, text="Voltar para Menu", width=15, height=2, bg='#015b90', fg="#ffffff", command=lambda: self.controller.mostrar_tela(MenuProblemas_caixa)).pack(pady=5)

#     def limpar_caixar(self):
#         confirmacao = self.confirmar_limpeza.get().strip()
        
#         if confirmacao.lower() == 's':
#             limpeza_concluida = limpeza_log_caixa(self.controller.conn)
#             self.texto_limpeza_confirmacao.config(text=limpeza_concluida, fg='green', font=("Arial", 13, "bold"))
#         else:
#             self.texto_limpeza_confirmacao.config(text="Digito de confirmação INCORRETO!\n\nDigite 'S' para confirmar a limpeza!", fg='red', font=("Arial", 10, "bold"))

#     def quando_clicar(self, event):
#         if self.confirmar_limpeza.get() == "Digite 'S' no campo para realizar...":
#             self.confirmar_limpeza.delete(0, END)
#             self.confirmar_limpeza.config(fg='black')

#########################################################################################

class HabilitarCartaoPresente(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_titulo_habilitar = Label(self, text="HABILITAR CARTÃO PRESENTE", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_habilitar.pack(pady=30)
        self.texto_status_cartao = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_cartao.pack(pady=30)

        Button(self, text="Habilitar Venda", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.habilitar_cartao_presente).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_cartao.config(text="")]).pack(pady=30)

    def habilitar_cartao_presente(self):
        resultado_habilitar = habilitar_cartao_presente_caixa(self.controller.conn)
        self.texto_status_cartao.config(text=resultado_habilitar)

#########################################################################################

class AtualizarBiometriaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_titulo_bio_caixa = Label(self, text="Atualização de Biometrias no CAIXA", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_bio_caixa.pack(pady=5)
        self.texto_aviso_bio = Label(self, text="| Utilizar este menu após ter atualizado no menu LOJA |", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 13, "bold"))
        self.texto_aviso_bio.pack(pady=15)
        self.texto_status_truncate = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_truncate.pack(pady=30)

        Button(self, text="Atualizar Biometrias", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.atualizar_bio_caixa).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_truncate.config(text="")]).pack(pady=30)

    def atualizar_bio_caixa(self):
        resultado_truncate = atualizar_biometria_caixa(self.controller.conn)
        self.texto_status_truncate.config(text=resultado_truncate)

#########################################################################################

class AtualizarVersaoCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_versao = Label(self, text="Versão atual PDV:", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_versao.pack(pady=30)

        self.inserir_versao = Entry(self, fg='grey', width=30, font=("Arial", 16))
        self.inserir_versao.insert(0, 'Informe a versão...')
        self.inserir_versao.bind('<FocusIn>', self.quando_clicar)
        self.inserir_versao.pack(pady=(40, 20))

        Button(self, text="Atualizar Versão", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.atualiza_versao).pack(pady=5)
        Button(self, text="Consultar Versão", width=15, height=1, bg=azul_nissei, fg="#ffffff", font=("Arial", 14), command=self.consulta_de_versao).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="white", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_versao.config(text="Versão atual:")]).pack(pady=5)

        self.info_versao = Label(self, text="| Versões que utilizamos atualmente |\n\nPDV: 3.0.0.280             \nPREVENDA: 1.102.081", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.info_versao.pack(pady=30)

    def consulta_de_versao(self):
        resultado_versao = consultar_versao(self.controller.conn)
        self.texto_versao.config(text=f"Versão atual PDV {resultado_versao}")
    
    def atualiza_versao(self):
        versao_digitada = self.inserir_versao.get()
        self.inserir_versao.delete(0, END)

        resultado_atualizacao = atualizar_versao(self.controller.conn, versao_digitada)
        self.texto_versao.config(text=f"Versão atual PDV {resultado_atualizacao}")

    def quando_clicar(self, event):
        if self.inserir_versao.get() == 'Informe a versão...':
            self.inserir_versao.delete(0, END)
            self.inserir_versao.config(fg='black')

#########################################################################################

class TabelaZeroCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_titulo_tabelazero = Label(self, text="Corrigir PDV com TABELA 0", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_tabelazero.pack(pady=30)
        self.texto_status_tabelazero = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_tabelazero.pack(pady=30)

        Button(self, text="Executar USP", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.corrigir_tabela_zero).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_tabelazero.config(text="")]).pack(pady=30)

    def corrigir_tabela_zero(self):
        resultado_tabela = tabela_zero_caixa(self.controller.conn)
        self.texto_status_tabelazero.config(text=resultado_tabela)

#########################################################################################

class ConsultarVendaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.titulo_consulta = Label(self, text="Consulta de vendas no Caixa", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.titulo_consulta.pack(pady=(30,15))

        self.titulo_consulta = Label(self, text="Utilize a parametrização DD/MM/AAAA e 9.99", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold", "underline"))
        self.titulo_consulta.pack(pady=10)

        self.inserir_data = Entry(self, fg='grey', width=30, font=("Arial", 15))
        self.inserir_data.insert(0, 'Informe a data...')
        self.inserir_data.bind('<FocusIn>', self.quando_clicar)
        self.inserir_data.pack(pady=(5, 1))

        self.titulo_consulta = Label(self, text="&", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.titulo_consulta.pack(pady=1)

        self.inserir_valor = Entry(self, fg='grey', width=30, font=("Arial", 15))
        self.inserir_valor.insert(0, 'Informe o Valor, Ex: 9.99')
        self.inserir_valor.bind('<FocusIn>', self.quando_clicar)
        self.inserir_valor.pack(pady=(1, 10))

        self.erro_preenchimento = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"), anchor="center", justify="center")
        self.erro_preenchimento.pack(pady=5, fill='x')

        Button(self, text="Consultar Venda", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.consultar_vendas).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="white", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.erro_preenchimento.config(text="", fg="black")]).pack(pady=5)

        frame_labels = Frame(self, bg="#ffffff")
        frame_labels.pack(pady=5, padx=10, fill='x')

        self.historico_vendas_aprovadas = Label(self, text="", bg="#86fe94", fg=azul_nissei, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.historico_vendas_aprovadas.pack(side="left", expand=True, fill='both')

        self.historico_vendas_canceladas = Label(self, text="", bg="#ff9494", fg=azul_nissei, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.historico_vendas_canceladas.pack(side="left", expand=True, fill='both')

    def consultar_vendas(self):
        data_digitada = self.inserir_data.get()
        self.inserir_data.delete(0, END)

        valor_digitado = self.inserir_valor.get()
        self.inserir_valor.delete(0, END)

        if data_digitada and valor_digitado:
            self.erro_preenchimento.config(text="", fg="red")
            vendas_aprovadas = verificar_vendas_caixa(self.controller.conn, data_digitada, valor_digitado, 'A')
            self.historico_vendas_aprovadas.config(text=vendas_aprovadas, fg=azul_nissei)

            vendas_canceladas = verificar_vendas_caixa(self.controller.conn, data_digitada, valor_digitado, 'C')
            self.historico_vendas_canceladas.config(text=vendas_canceladas, fg=azul_nissei)

        else:
            self.erro_preenchimento.config(text="Preencha os campos corretamente.", fg="red")

    def quando_clicar(self, event):
        if self.inserir_data.get() == 'Informe a data...':
            self.inserir_data.delete(0, END)
            self.inserir_data.config(fg='black')

        if self.inserir_valor.get() == 'Informe o Valor, Ex: 9.99':
            self.inserir_valor.delete(0, END)
            self.inserir_valor.config(fg='black')

#########################################################################################

class HabilitarVNCCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=amarelo_nissei)
        self.controller = controller

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

        self.texto_titulo_habilitar = Label(self, text="Habilitar conexão VNC no Caixa", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 20, "bold"))
        self.texto_titulo_habilitar.pack(pady=20)

        self.aviso = Label(self, text="EM CONSTRUÇÃO", bg=amarelo_nissei, fg="red", font=("Arial", 20, "bold"))
        self.aviso.pack(pady=1)

        self.texto_status_vnc = Label(self, text="", bg=amarelo_nissei, fg=azul_nissei, font=("Arial", 15, "bold"))
        self.texto_status_vnc.pack(pady=20)

        #Button(self, text="Habilitar VNC", width=15, height=1, bg="green", fg="#ffffff", font=("Arial", 14), command=self.habilitar_vnc).pack(pady=5)
        Button(self, text="Voltar para Menu", width=15, height=1, bg="#ee3642", fg="#ffffff", font=("Arial", 16), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_vnc.config(text="")]).pack(pady=30)

    def habilitar_vnc(self):
        resultado_habilitar = iniciar_vnc(self.controller.conn, self.controller.ip_caixa)
        self.texto_status_vnc.config(text=resultado_habilitar)

#########################################################################################

app = Aplicacao()
app.mainloop()