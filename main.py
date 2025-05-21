from tkinter import *
from PIL import Image, ImageTk
from Funcoes.funcoesloja import *
from Funcoes.funcoescaixa import *
from Funcoes.funcoeslinux import *
from style.cores import *
from dotenv import load_dotenv

load_dotenv()
#########################################################################################

class Aplicacao(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("ExecFlow")
        self.iconbitmap("style/EFico.ico")
        self.geometry("400x500")
        self.configure(bg=fundo)

        self.filial = ""

        logo = Image.open("style/EFlogo.png")  # pode ser .jpg, .png etc
        logo = logo.resize((420,87))  # redimensiona, se quiser
        self.logo_tk = ImageTk.PhotoImage(logo)

        # Container principal
        container = Frame(self, bg=fundo)
        container.pack(fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.telas = {}
                                                                                               
        for T in (Homepage, MenuProblemas, DataHub, AtualizarEstoque, AtualizarBiometria, IntegrarNota, AtualizarVersaoLoja, LimparTemp,                                    #<--LOJA
                  HomepageCaixa, MenuProblemasCaixa, HabilitarCartaoPresente, AtualizarBiometriaCaixa, AtualizarVersaoCaixa, TabelaZeroCaixa, ConsultarVendaCaixa,          #<--CAIXA                                                                           #<--CAIXA
                  MenuProblemasLinux, HabilitarVNCCaixa, ErroMount_a, LeituraGravacao,):                                                                                    #<--LINUX                                                  #<--LINUX
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
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller
        self.criar_widgets()
    
    def criar_widgets(self):


        topo_frame = Frame(self, bg=fundo)
        topo_frame.pack(pady=(50,10))

        Label(topo_frame, text="Informe o número da ", fg=cor_texto, bg=fundo, font=("Arial", 13, "bold")).pack(side=LEFT)
        Label(topo_frame, text="FILIAL", fg=cor_texto, bg=fundo, font=("Arial", 13, "underline", "bold")).pack(side=LEFT)
    
        self.texto_aviso_bio = Label(self, text="Realizar o PRIMEIRO acesso em um 'Menu LOJA'\nNecessário para liberar conexão com 'Menu CAIXA'", bg=fundo, fg=botao1, font=("Arial", 9, "bold"), bd=1, relief="solid")
        self.texto_aviso_bio.pack(pady=15)

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=13)

        self.botao_menu_loja = Button(self, text="Menu LOJA", width=15, height=1, bg=botao1, fg="#ffffff", bd=4, relief="ridge", font=("Arial", 10), command=lambda: self.conectar_banco_loja()).pack(pady=10)
        self.botao_menu_caixa = Button(self, text="Menu CAIXA SQL", width=15, height=1, bg=botao1, fg="#ffffff", bd=4, relief="ridge", font=("Arial", 10), command=lambda: self.conectar_banco_caixa()).pack(pady=10)
        self.botao_menu_linux = Button(self, text="Menu LINUX", width=15, height=1, bg=botao1, fg="#ffffff", bd=4, relief="ridge", font=("Arial", 10), command=lambda: self.controller.mostrar_tela(MenuProblemasLinux)).pack(pady=10)

        self.texto_erro_selecionar_filial = Label(self, text="", fg=vermelho, bg=fundo, font=("Arial", 13, "bold"))
        self.texto_erro_selecionar_filial.pack(pady=5, padx=40)

        aplicar_hover_em_todos(self, hover, botao1)
               
        Label(self, image=self.controller.logo_tk).pack(pady=(20, 10))

    def confirmar_filial(self):
        self.filial_digitada = self.entrada.get()
        self.controller.filial = self.filial_digitada
        self.entrada.delete(0, END)

        if self.filial_digitada.strip() == "" or self.filial_digitada == "Digite aqui..." or self.filial_digitada == '0':
            return
        
        self.controller.ip = gerar_ip(self.filial_digitada)

    def conexao_servidor(self):    
        ip_loja = self.controller.ip + "24"
        print(ip_loja)

        self.controller.usuario_sql = os.getenv("USER_SQL")
        self.controller.senha_sql = os.getenv("PASS_SQL")

        if len(ip_loja) > 5:
            self.controller.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={ip_loja};'
                f'DATABASE=LOJA;'
                f'UID={self.controller.usuario_sql};'
                f'PWD={self.controller.senha_sql};'
                'Connection Timeout=3;'
            )
            print("Conectado com sucesso ao banco!")
            self.controller.mostrar_tela(MenuProblemas)
            self.controller.ip = ""
            self.texto_erro_selecionar_filial.config(text="")
        else:
            self.texto_erro_selecionar_filial.config(text="Falha na conexão")
            return


    def conectar_banco_loja(self):
        self.confirmar_filial()
        self.conexao_servidor()

    def conectar_banco_caixa(self):
        self.confirmar_filial()
        if self.controller.ip.strip() == "" or self.controller.ip == "Digite aqui..." or self.controller.ip == '0':
            return
        self.controller.mostrar_tela(HomepageCaixa)
        self.texto_erro_selecionar_filial.config(text="")
    
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
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        # Widget estático
        self.texto_menu = Label(self, text="", font=("Arial", 12, "bold"), bg=fundo, fg=cor_texto)
        self.texto_menu.pack(pady=(40, 30))

        botoes_frame = Frame(self, bg=fundo)
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

            Button(botoes_frame, text=texto, width=20, height=2, bg=botao1, fg="white", bd=3, relief="ridge", font=("Arial", 9, "bold"), command=comando).grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")
            aplicar_hover_em_todos(botoes_frame, hover, botao1)

        #ajuste proporção
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)

        botao_alterar_filial = Button(self, text="Alterar filial", width=25, height=2, bg=vermelho, fg="white", bd=3, relief="ridge", font=("Arial", 10, "bold"), command=lambda: alterar_filial(self, Homepage))
        aplicar_hover(botao_alterar_filial, hover, vermelho)
        botao_alterar_filial.pack(pady=(15, 5))

        Label(self, image=self.controller.logo_tk).pack(pady=(15, 10))

    def atualizar(self):
        filial = self.controller.filial
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS\n\nFILIAL: {filial}")
#########################################################################################

class DataHub(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_status = Label(self, text="STATUS DO DATAHUB:", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_status.pack(pady=(90, 30))

        botao_habilitar_datahub = Button(self, text="Habilitar DataHub", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.habilitar_db)
        botao_habilitar_datahub.pack(pady=10)
        aplicar_hover(botao_habilitar_datahub, hover, verde)

        botao_desabilitar_datahub = Button(self, text="Desabilitar DataHub", width=15, height=1, bg=vermelho, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.desabilitar_db)
        botao_desabilitar_datahub.pack(pady=10)
        aplicar_hover(botao_desabilitar_datahub, hover, vermelho)

        botao_voltar_menu = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_status.config(text="STATUS DO DATAHUB:")])
        botao_voltar_menu.pack(pady=5)
        aplicar_hover(botao_voltar_menu, hover, botao2)

        Label(self, image=self.controller.logo_tk).pack(pady=(100, 10))

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
#         Frame.__init__(self, parent, bg=fundo)
#         self.controller = controller

#         self.texto_primary_cheio = Label(self, text="Deseja realizar a limpeza de Log's?", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
#         self.texto_primary_cheio.pack(pady=13)

#         self.texto_primary_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=fundo, fg=cor_texto, font=("Arial", 9))
#         self.texto_primary_confirmacao.pack(pady=5)

#         self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 10))
#         self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
#         self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
#         self.confirmar_limpeza.pack(pady=13)

#         Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_log, font=("Arial", 10)).pack(pady=5)
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
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_matricula_titulo = Label(self, text="Informe a matrícula", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_matricula_titulo.pack(pady=(40,10))
    
        self.matricula = Entry(self, fg='grey', width=30, font=("Arial", 10))
        self.matricula.insert(0, 'Informe a matrícula...')
        self.matricula.bind('<FocusIn>', self.quando_clicar)
        self.matricula.pack(pady=13)

        botao_confirmar = Button(self, text="Confirmar", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.atualizar_bio)
        botao_confirmar.pack(pady=5)
        aplicar_hover(botao_confirmar, hover, verde)

        botao_voltar_menu = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_matricula_infos.config(text="")])
        botao_voltar_menu.pack(pady=5)
        aplicar_hover(botao_voltar_menu, hover, botao2)

        self.texto_matricula_infos = Label(self, text="", bg="#292929", fg=cor_texto, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_matricula_infos.pack(pady=10, fill='x')

        Label(self, image=self.controller.logo_tk).pack(pady=(20, 10))

    def atualizar_bio(self):
        matricula_digitada = self.matricula.get()
        self.matricula.delete(0, END)

        if not matricula_digitada.isdigit():
            self.texto_matricula_infos.config(text="Matrícula inválida! Use apenas números.", fg=vermelho)
            return
        else:
            status_colaborador = atualizar_biometria(self.controller.conn, matricula_digitada)
            self.texto_matricula_infos.config(text=status_colaborador, fg=cor_texto)

    def quando_clicar(self, event):
        if self.matricula.get() == 'Informe a matrícula...':
            self.matricula.delete(0, END)
            self.matricula.config(fg='black')

#########################################################################################

class IntegrarNota(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_integrar_titulo = Label(self, text="Informe a CHAVE NFE para integração", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_integrar_titulo.pack(pady=(80,20))

        self.aviso = Label(self, text="EM TESTES", bg=fundo, fg=vermelho, font=("Arial", 13, "bold"))
        self.aviso.pack(pady=1)
    
        self.chave_nfe = Entry(self, fg='grey', width=30, font=("Arial", 10))
        self.chave_nfe.insert(0, 'Informe a chave...')
        self.chave_nfe.bind('<FocusIn>', self.quando_clicar)
        self.chave_nfe.pack(pady=13)

        #botao_confirmar = Button(self, text="Confirmar", width=15, height=1, bg="green", fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.integrar_nf)
        #botao_confirmar.pack(pady=5)
        #aplicar_hover(botao_confirmar, hover, verde)

        botao_voltar_menu = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_integrar_infos.config(text="", fg='black')])
        botao_voltar_menu.pack(pady=5)
        aplicar_hover(botao_voltar_menu, hover, botao2)

        self.texto_integrar_infos = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_integrar_infos.pack(pady=13, fill='x')

        Label(self, image=self.controller.logo_tk).pack(pady=(60, 10))

    def integrar_nf(self):
        chave_digitada = self.chave_nfe.get()
        self.chave_nfe.delete(0, END)

        if not chave_digitada.isdigit():
            self.texto_integrar_infos.config(text="CHAVE inválida! Use apenas números.", fg=vermelho)
            return
        else:
            integracao_nota = integrar_nota(self.controller.conn, chave_digitada)
            self.texto_integrar_infos.config(text=integracao_nota, fg=cor_texto)

    def quando_clicar(self, event):
        if self.chave_nfe.get() == 'Informe a chave...':
            self.chave_nfe.delete(0, END)
            self.chave_nfe.config(fg='black')

#########################################################################################

class AtualizarEstoque(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_titulo_estoque = Label(self, text="Atualizar estoque da Filial", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_titulo_estoque.pack(pady=(90,20))
        self.texto_resultado_estoque = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_resultado_estoque.pack(pady=13)

        botao_atualizar = Button(self, text="Atualizar estoque", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.atualizar_estoque_loja)
        botao_atualizar.pack(pady=5)
        aplicar_hover(botao_atualizar, hover, verde)

        botao_voltar_menu = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_resultado_estoque.config(text="")])
        botao_voltar_menu.pack(pady=5)
        aplicar_hover(botao_voltar_menu, hover, botao2)

        Label(self, image=self.controller.logo_tk).pack(pady=(90, 7))

    def atualizar_estoque_loja(self):
        resultado_atualizacao = atualizar_estoque(self.controller.conn)
        self.texto_resultado_estoque.config(text=resultado_atualizacao)

#########################################################################################

class AtualizarVersaoLoja(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_versao = Label(self, text="Versão atual PREVENDA:", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_versao.pack(pady=(60,10))

        self.inserir_versao = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_versao.insert(0, 'Informe a versão...')
        self.inserir_versao.bind('<FocusIn>', self.quando_clicar)
        self.inserir_versao.pack(pady=(30, 20))

        botao_atualizar = Button(self, text="Atualizar Versão", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.atualiza_versao)
        botao_atualizar.pack(pady=5)
        aplicar_hover(botao_atualizar, hover, verde)

        botao_consultar = Button(self, text="Consultar Versão", width=15, height=1, bg=botao1, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.consulta_de_versao)
        botao_consultar.pack(pady=5)
        aplicar_hover(botao_consultar, hover, botao1)

        botao_voltar_menu_versao = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemas), self.texto_versao.config(text="Versão atual:")])
        botao_voltar_menu_versao.pack(pady=5)
        aplicar_hover(botao_voltar_menu_versao, hover, botao2)

        self.info_versao = Label(self, text="| Versões que utilizamos atualmente |\n\nPDV: 3.0.0.281            \nPREVENDA: 1.102.081", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"), bd=2, relief="solid")
        self.info_versao.pack(pady=13)

        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

    def consulta_de_versao(self):
        resultado_versao = consultar_versao(self.controller.conn)
        self.texto_versao.config(text=f"Versão atual PREVENDA: {resultado_versao}")
    
    def atualiza_versao(self):
        versao_digitada = self.inserir_versao.get()
        self.inserir_versao.delete(0, END)

        if len(versao_digitada) > 6:
            atualizar_versao(self.controller.conn, versao_digitada)
            resultado_versao = consultar_versao(self.controller.conn)
            self.texto_versao.config(text=f"Versão atual PREVENDA: {resultado_versao}")
        else:
            return

    def quando_clicar(self, event):
        if self.inserir_versao.get() == 'Informe a versão...':
            self.inserir_versao.delete(0, END)
            self.inserir_versao.config(fg='black')

#########################################################################################

class LimparTemp(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_informar_ip = Label(self, text="Informe o IP do terminal\npara limpar a %Temp%", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_informar_ip.pack(pady=(70,20))

        self.aviso = Label(self, text="EM CONSTRUÇÃO", bg=fundo, fg=vermelho, font=("Arial", 13, "bold"))
        self.aviso.pack(pady=13)
    
        self.entry_ip = Entry(self, fg='grey', width=30, font=("Arial", 10))
        self.entry_ip.insert(0, 'Informe o IP...')
        self.entry_ip.bind('<FocusIn>', self.quando_clicar)
        self.entry_ip.pack(pady=13)

        #Button(self, text="Limpar %Temp%", width=15, height=1, bg="green", fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.limpar_temp).pack(pady=5)
        botao_voltar_menu = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: self.controller.mostrar_tela(MenuProblemas))
        botao_voltar_menu.pack(pady=5)
        aplicar_hover(botao_voltar_menu, hover, botao2)

        self.texto_limpeza_status = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"), anchor="center", justify="center")
        self.texto_limpeza_status.pack(pady=13, fill='x')

        Label(self, image=self.controller.logo_tk).pack(pady=(70, 10))

    def limpar_temp(self):
        ip_digitado = self.entry_ip.get()
        self.entry_ip.delete(0, END)

        try:
            status_limpeza = limpar_temp_ps1(self.controller.conn, ip_digitado)
            self.texto_limpeza_status.config(text=status_limpeza, fg=cor_texto)
        except:
            self.texto_limpeza_status.config(text="ERRO na execução do PowerShell\nIP incorreto.", fg=vermelho)


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
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_selecionar_caixa = Label(self, text=f"", fg=cor_texto, bg=fundo, font=("Arial", 13, "bold"))
        self.texto_selecionar_caixa.pack(pady=(80,30), padx=40)

        self.entrada = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.entrada.insert(0, 'Digite aqui...')
        self.entrada.bind('<FocusIn>', self.quando_clicar)
        self.entrada.pack(pady=13)

        botao_confirmar_caixa = Button(self, text="Confirmar", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=lambda: self.confirmar_caixa())
        botao_confirmar_caixa.pack(pady=5)
        aplicar_hover(botao_confirmar_caixa, hover, verde)

        botao_alterar_filial = Button(self, text="Alterar filial", width=15, height=1, bg=botao2, fg='#ffffff', bd=3, relief="ridge", font=("Arial", 10),command=lambda: [self.controller.mostrar_tela(Homepage), self.texto_erro_selecionar_caixa.config(text="")])
        botao_alterar_filial.pack(pady=5)
        aplicar_hover(botao_alterar_filial, hover, vermelho)

        self.texto_erro_selecionar_caixa = Label(self, text="", fg=vermelho, bg=fundo, font=("Arial", 13, "bold"))
        self.texto_erro_selecionar_caixa.pack(pady=10, padx=40)

        Label(self, image=self.controller.logo_tk).pack(pady=(60, 10))

    def confirmar_caixa(self):
        self.controller.caixa_selecionado = self.entrada.get()
        self.entrada.delete(0, END)

        if self.controller.caixa_selecionado.strip() == "" or self.controller.caixa_selecionado == "Digite aqui..." or self.controller.caixa_selecionado == '0':
            return
        
        self.controller.ip_caixa = self.controller.ip + self.controller.caixa_selecionado
        print(self.controller.ip_caixa)

        try:
            if len(self.controller.caixa_selecionado) < 2 and len(self.controller.ip_caixa) > 5 and self.controller.caixa_selecionado != None:
                self.controller.conn = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={self.controller.ip_caixa};'
                    f'DATABASE=PDV;'
                    f'UID={self.controller.usuario_sql};'
                    f'PWD={self.controller.senha_sql};'
                    'Connection Timeout=3;'
                )
                print("Conectado com sucesso ao banco!")
                self.controller.mostrar_tela(MenuProblemasCaixa)
                self.texto_erro_selecionar_caixa.config(text="")
            else:
                self.texto_erro_selecionar_caixa.config(text="Número de CAIXA ou FILIAL inválido!")
                return
        except:
            self.texto_erro_selecionar_caixa.config(text="Falha na conexão com o banco.")
    
    def atualizar(self):
        filial = self.controller.filial
        self.texto_selecionar_caixa.config(text=f"Qual CAIXA será feita a conexão?\n\nFilial: {filial}")

    def quando_clicar(self, event):
        if self.entrada.get() == 'Digite aqui...':
            self.entrada.delete(0, END)
            self.entrada.config(fg='black')

#########################################################################################

class MenuProblemasCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_menu = Label(self, text="", font=("Arial", 10, "bold"), bg=fundo, fg=cor_texto)
        self.texto_menu.pack(pady=(40, 10))

        botoes_frame = Frame(self, bg=fundo)
        botoes_frame.pack()

        botoes = [
            ("Atualizar Biometrias", lambda: self.controller.mostrar_tela(AtualizarBiometriaCaixa)),
            ("Tabela 0", lambda: self.controller.mostrar_tela(TabelaZeroCaixa)),
            ("Habilitar\ncartão presente", lambda: self.controller.mostrar_tela(HabilitarCartaoPresente)),
            ("Atualizar Versão\nPDV", lambda: self.controller.mostrar_tela(AtualizarVersaoCaixa)),
            ("Verificar Vendas", lambda: self.controller.mostrar_tela(ConsultarVendaCaixa)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasCaixa)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasCaixa)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasCaixa)),
        ]

        for i, (texto, comando) in enumerate(botoes):
            linha = i // 2
            coluna = i % 2

            Button(botoes_frame, text=texto, width=20, height=2, bg=botao1, fg="white", bd=3, relief="ridge", font=("Arial", 8, "bold"), command=comando).grid(row=linha, column=coluna, padx=13, pady=6, sticky="nsew")
            aplicar_hover_em_todos(botoes_frame, hover, botao1)
        #ajuste proporção
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)

        frame_alteracoes = Frame(self, bg=fundo)
        frame_alteracoes.pack(pady=(13, 6))

        botao_alterar_filial = Button(frame_alteracoes, text="Alterar filial", width=21, height=3, bg=vermelho, fg="white", bd=3, relief="ridge", font=("Arial", 9, "bold"), command=lambda: alterar_filial(self, Homepage))
        aplicar_hover(botao_alterar_filial, hover, vermelho)
        botao_alterar_filial.pack(side="left", padx=6)

        botao_alterar_caixa = Button(frame_alteracoes, text="Alterar caixa", width=21, height=3, bg=vermelho, fg="white", bd=3, relief="ridge", font=("Arial", 9, "bold"), command=lambda: self.controller.mostrar_tela(HomepageCaixa))
        aplicar_hover(botao_alterar_caixa, hover, vermelho)
        botao_alterar_caixa.pack(side="left", padx=6)

        Label(self, image=self.controller.logo_tk).pack(pady=(5, 20))
        
    def atualizar(self):
        filial = self.controller.filial
        caixa = self.controller.caixa_selecionado
        self.texto_menu.config(text=f"CORREÇÕES DE PROBLEMAS CAIXA\n\nFILIAL: {filial}\nCAIXA: {caixa}")

#########################################################################################

#ADICIONAR A CLASSE NO DICIONARIO DE TELAS

# class LimpezaCaixa(Frame):
#     def __init__(self, parent, controller):
#         Frame.__init__(self, parent, bg=fundo)
#         self.controller = controller

#         self.texto_limpeza_caixa = Label(self, text="Deseja realizar a limpeza de Log's?", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
#         self.texto_limpeza_caixa.pack(pady=13)

#         self.texto_limpeza_confirmacao = Label(self, text="(Digite 'S' no campo para realizar)", bg=fundo, fg=cor_texto, font=("Arial", 9))
#         self.texto_limpeza_confirmacao.pack(pady=5)

#         self.confirmar_limpeza = Entry(self, fg='grey', width=30, font=("Arial", 10))
#         self.confirmar_limpeza.insert(0, "Digite 'S' no campo para realizar...")
#         self.confirmar_limpeza.bind('<FocusIn>', self.quando_clicar)
#         self.confirmar_limpeza.pack(pady=13)

#         Button(self, text="Confirmar", width=15, height=1, bg='green', fg="#ffffff", command=self.limpar_caixar, font=("Arial", 10)).pack(pady=5)
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
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_titulo_habilitar = Label(self, text="HABILITAR CARTÃO PRESENTE", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_titulo_habilitar.pack(pady=(90,20))
        self.texto_status_cartao = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_status_cartao.pack(pady=13)

        botao_habilitar_venda = Button(self, text="Habilitar Venda", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.habilitar_cartao_presente)
        botao_habilitar_venda.pack(pady=5)
        aplicar_hover(botao_habilitar_venda, hover, verde)
        
        botao_voltar_menu_cartao = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_cartao.config(text="")])
        botao_voltar_menu_cartao.pack(pady=5)
        aplicar_hover(botao_voltar_menu_cartao, hover, botao2)

        Label(self, image=self.controller.logo_tk).pack(pady=(100, 10))

    def habilitar_cartao_presente(self):
        resultado_habilitar = habilitar_cartao_presente_caixa(self.controller.conn)
        self.texto_status_cartao.config(text=resultado_habilitar)

#########################################################################################

class AtualizarBiometriaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_titulo_bio_caixa = Label(self, text="Atualização de Biometrias no CAIXA", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_titulo_bio_caixa.pack(pady=(90,5))
        self.texto_aviso_bio = Label(self, text="| Utilizar este menu após ter atualizado no menu LOJA |", bg=fundo, fg=botao1, font=("Arial", 9, "bold"), bd=1, relief="solid")
        self.texto_aviso_bio.pack(pady=15)
        self.texto_status_truncate = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_status_truncate.pack(pady=13)

        botao_atualizar_bio = Button(self, text="Atualizar Biometrias", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.atualizar_bio_caixa)
        botao_atualizar_bio.pack(pady=5)
        aplicar_hover(botao_atualizar_bio, hover, verde)

        botao_voltar_menu_bio = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_truncate.config(text="")])
        botao_voltar_menu_bio.pack(pady=13)
        aplicar_hover(botao_voltar_menu_bio, hover, botao2)

        Label(self, image=self.controller.logo_tk).pack(pady=(90, 10))

    def atualizar_bio_caixa(self):
        resultado_truncate = atualizar_biometria_caixa(self.controller.conn)
        self.texto_status_truncate.config(text=resultado_truncate)

#########################################################################################

class AtualizarVersaoCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_versao = Label(self, text="Versão atual do PDV:", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_versao.pack(pady=(60,10))

        self.inserir_versao = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_versao.insert(0, 'Informe a versão...')
        self.inserir_versao.bind('<FocusIn>', self.quando_clicar)
        self.inserir_versao.pack(pady=(30, 20))

        botao_atualizar_caixa = Button(self, text="Atualizar Versão", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.atualiza_versao)
        botao_atualizar_caixa.pack(pady=5)
        aplicar_hover(botao_atualizar_caixa, hover, verde)

        botao_consultar_versao_caixa = Button(self, text="Consultar Versão", width=15, height=1, bg=botao1, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.consulta_de_versao)
        botao_consultar_versao_caixa.pack(pady=5)
        aplicar_hover(botao_consultar_versao_caixa, hover, botao1)

        botao_voltar_menu_versao = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_versao.config(text="Versão atual:")])
        botao_voltar_menu_versao.pack(pady=5)
        aplicar_hover(botao_voltar_menu_versao, hover, botao2)

        self.info_versao = Label(self, text="| Versões que utilizamos atualmente |\n\nPDV: 3.0.0.281             \nPREVENDA: 1.102.081", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"), bd=2, relief="solid")
        self.info_versao.pack(pady=10)

        
        Label(self, image=self.controller.logo_tk).pack(pady=(30, 10))

    def consulta_de_versao(self):
        resultado_versao = consultar_versao(self.controller.conn)
        self.texto_versao.config(text=f"Versão atual PDV: {resultado_versao}")
    
    def atualiza_versao(self):
        versao_digitada = self.inserir_versao.get()
        self.inserir_versao.delete(0, END)

        atualizar_versao(self.controller.conn, versao_digitada)
        resultado_versao = consultar_versao(self.controller.conn)
        self.texto_versao.config(text=f"Versão atual PDV: {resultado_versao}")

    def quando_clicar(self, event):
        if self.inserir_versao.get() == 'Informe a versão...':
            self.inserir_versao.delete(0, END)
            self.inserir_versao.config(fg='black')

#########################################################################################

class TabelaZeroCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_titulo_tabelazero = Label(self, text="Corrigir PDV com TABELA 0", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_titulo_tabelazero.pack(pady=(90,20))
        self.texto_status_tabelazero = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.texto_status_tabelazero.pack(pady=13)

        botao_executar_usp = Button(self, text="Executar USP", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.corrigir_tabela_zero)
        botao_executar_usp.pack(pady=5)
        aplicar_hover(botao_executar_usp, hover, verde)

        botao_voltar_menu_tabela = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.texto_status_tabelazero.config(text="")])
        botao_voltar_menu_tabela.pack(pady=13)
        aplicar_hover(botao_voltar_menu_tabela, hover, botao2)
        
        Label(self, image=self.controller.logo_tk).pack(pady=(100, 10))

    def corrigir_tabela_zero(self):
        resultado_tabela = tabela_zero_caixa(self.controller.conn)
        self.texto_status_tabelazero.config(text=resultado_tabela)

#########################################################################################

class ConsultarVendaCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.titulo_consulta = Label(self, text="Consulta de vendas no Caixa", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.titulo_consulta.pack(pady=(20,0))

        self.titulo_consulta = Label(self, text="Utilize a parametrização", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold", "underline"))
        self.titulo_consulta.pack(pady=5)

        self.titulo_consulta = Label(self, text="Data: DD/MM/AAAA", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold", "underline"))
        self.titulo_consulta.pack(padx=(0,120), pady=0)

        self.inserir_data = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_data.insert(0, 'Informe a data...')
        self.inserir_data.bind('<FocusIn>', self.quando_clicar)
        self.inserir_data.pack(pady=(1, 1))

        self.titulo_consulta = Label(self, text="&", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"))
        self.titulo_consulta.pack(pady=0)

        self.inserir_valor = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_valor.insert(0, 'Informe o Valor, Ex: 9.99')
        self.inserir_valor.bind('<FocusIn>', self.quando_clicar)
        self.inserir_valor.pack(pady=(1, 1))

        self.titulo_consulta = Label(self, text="Valor: 9.99", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold", "underline"))
        self.titulo_consulta.pack(padx=(0,175), pady=0)

        self.erro_preenchimento = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.erro_preenchimento.pack(pady=3, fill='x')

        botao_consultar_venda = Button(self, text="Consultar Venda", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.consultar_vendas)
        botao_consultar_venda.pack(pady=3)
        aplicar_hover(botao_consultar_venda, hover, verde)

        botao_voltar_menu_consulta = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasCaixa), self.erro_preenchimento.config(text="", fg="black"), self.historico_vendas_aprovadas.config(text=""), self.historico_vendas_canceladas.config(text="")])
        botao_voltar_menu_consulta.pack(pady=(5,5))
        aplicar_hover(botao_voltar_menu_consulta, hover, botao2)

        frame_historico = Frame(self)
        frame_historico.pack(pady=(5,1), padx=10, fill="x")

        self.historico_vendas_aprovadas = Label(frame_historico, text="", bg=verde, fg=cor_texto, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.historico_vendas_aprovadas.pack(side="left", expand=True, fill='both')

        self.historico_vendas_canceladas = Label(frame_historico, text="", bg=vermelho, fg=cor_texto, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.historico_vendas_canceladas.pack(side="left", expand=True, fill='both')

        Label(self, image=self.controller.logo_tk).pack(pady=(1, 10))

    def consultar_vendas(self):
        data_digitada = self.inserir_data.get()
        self.inserir_data.delete(0, END)

        valor_digitado = self.inserir_valor.get()
        self.inserir_valor.delete(0, END)

        if data_digitada and valor_digitado:
            self.erro_preenchimento.config(text="", fg=vermelho)
            vendas_aprovadas = verificar_vendas_caixa(self.controller.conn, data_digitada, valor_digitado, 'A')
            self.historico_vendas_aprovadas.config(text=vendas_aprovadas, fg=cor_texto)

            vendas_canceladas = verificar_vendas_caixa(self.controller.conn, data_digitada, valor_digitado, 'C')
            self.historico_vendas_canceladas.config(text=vendas_canceladas, fg=cor_texto)

        else:
            self.erro_preenchimento.config(text="Preencha os campos corretamente.", fg=vermelho)

    def quando_clicar(self, event):
        if self.inserir_data.get() == 'Informe a data...':
            self.inserir_data.delete(0, END)
            self.inserir_data.config(fg='black')

        if self.inserir_valor.get() == 'Informe o Valor, Ex: 9.99':
            self.inserir_valor.delete(0, END)
            self.inserir_valor.config(fg='black')

#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################
#########################LINUX - LINUX - LINUX################################################################

class MenuProblemasLinux(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_menu_linux = Label(self, text="CORREÇÕES DE PROBLEMAS LINUX", font=("Arial", 10, "bold"), bg=fundo, fg=cor_texto)
        self.texto_menu_linux.pack(pady=(40, 10))

        botoes_frame = Frame(self, bg=fundo)
        botoes_frame.pack()

        botoes = [
            ("Leitura e Gravação", lambda: self.controller.mostrar_tela(LeituraGravacao)),
            ("Mount -a", lambda: self.controller.mostrar_tela(ErroMount_a)),
            ("Habilitar VNC", lambda: self.controller.mostrar_tela(HabilitarVNCCaixa)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasLinux)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasLinux)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasLinux)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasLinux)),
            ("---------", lambda: self.controller.mostrar_tela(MenuProblemasLinux)),      
        ]

        for i, (texto, comando) in enumerate(botoes):
            linha = i // 2
            coluna = i % 2

            Button(botoes_frame, text=texto, width=20, height=2, bg=botao1, fg="white", bd=3, relief="ridge", font=("Arial", 8, "bold"), command=comando).grid(row=linha, column=coluna, padx=13, pady=6, sticky="nsew")
            aplicar_hover_em_todos(botoes_frame, hover, botao1)
        #ajuste proporção
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)

        frame_alteracoes = Frame(self, bg=fundo)
        frame_alteracoes.pack(pady=(13, 6))

        botao_alterar_filial = Button(frame_alteracoes, text="Alterar filial", width=21, height=3, bg=vermelho, fg="white", bd=3, relief="ridge", font=("Arial", 9, "bold"), command=lambda: alterar_filial(self, Homepage))
        aplicar_hover(botao_alterar_filial, hover, vermelho)
        botao_alterar_filial.pack(side="left", padx=6)

        Label(self, image=self.controller.logo_tk).pack(pady=(20, 20))
        

#########################################################################################

class HabilitarVNCCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_titulo_habilitar = Label(self, text="Habilitar conexão VNC no Caixa", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_titulo_habilitar.pack(pady=(90,20))

        self.inserir_ip_vnc = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_ip_vnc.insert(0, 'Informe o IP...')
        self.inserir_ip_vnc.bind('<FocusIn>', self.quando_clicar)
        self.inserir_ip_vnc.pack(pady=(1, 5))

        botao_habilitar_vnc = Button(self, text="Habilitar VNC", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.habilitar_vnc)
        botao_habilitar_vnc.pack(pady=5)
        aplicar_hover(botao_habilitar_vnc, hover, verde)

        botao_voltar_menu_vnc = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasLinux), self.texto_status_vnc.config(text="")])
        botao_voltar_menu_vnc.pack(pady=13)
        aplicar_hover(botao_voltar_menu_vnc, hover, botao2)

        self.texto_status_vnc = Label(self, text="", bg=fundo, font=("Arial", 11, "bold"))
        self.texto_status_vnc.pack(pady=13)
  
        Label(self, image=self.controller.logo_tk).pack(pady=(100, 10))

    def habilitar_vnc(self):
        ip_digitado = self.inserir_ip_vnc.get().strip()
            
        if not ip_digitado or ip_digitado == "Informe o IP...":
            self.texto_status_vnc.config(text="IP inválido.", fg="red")
            return

        try:
            resultado = iniciar_vnc(ip_digitado)
            self.texto_status_vnc.config(text=resultado, fg=cor_texto)
            self.inserir_ip_vnc.delete(0, END)
        except Exception as e:
            self.texto_status_vnc.config(text=f"Erro inesperado: \n{str(e)}", fg="red")

    def quando_clicar(self, event):
        if self.inserir_ip_vnc.get() == 'Informe o IP...':
            self.inserir_ip_vnc.delete(0, END)
            self.inserir_ip_vnc.config(fg='black')

#########################################################################################

class ErroMount_a(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_mount = Label(self, text="Erro de diretório PBM\n(Mount -a)", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_mount.pack(pady=(90,20))

        self.inserir_ip_mount = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_ip_mount.insert(0, 'Informe o IP...')
        self.inserir_ip_mount.bind('<FocusIn>', self.quando_clicar)
        self.inserir_ip_mount.pack(pady=(1, 5))

        botao_mount = Button(self, text="Corrigir", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.corrigir_mount_a)
        botao_mount.pack(pady=5)
        aplicar_hover(botao_mount, hover, verde)

        botao_voltar_menu_mount = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasLinux), self.texto_status_mount.config(text="")])
        botao_voltar_menu_mount.pack(pady=13)
        aplicar_hover(botao_voltar_menu_mount, hover, botao2)

        self.texto_status_mount = Label(self, text="", bg=fundo, font=("Arial", 10, "bold"))
        self.texto_status_mount.pack(pady=13)

        
        Label(self, image=self.controller.logo_tk).pack(pady=(80, 10))

    def corrigir_mount_a(self):
        ip_digitado = self.inserir_ip_mount.get().strip()
            
        if not ip_digitado or ip_digitado == "Informe o IP...":
            self.texto_status_mount.config(text="IP inválido.", fg="red")
            return

        try:
            resultado = mount_a(ip_digitado)
            self.texto_status_mount.config(text=resultado, fg=cor_texto)
            self.inserir_ip_mount.delete(0, END)
        except Exception as e:
            self.texto_status_mount.config(text=f"Erro inesperado: \n{str(e)}", fg="red")

    def quando_clicar(self, event):
        if self.inserir_ip_mount.get() == 'Informe o IP...':
            self.inserir_ip_mount.delete(0, END)
            self.inserir_ip_mount.config(fg='black')

#########################################################################################

class LeituraGravacao(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.texto_permissao = Label(self, text="Ativar permissões no PDV\nLeitura e Gravação", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.texto_permissao.pack(pady=(70,20))

        self.inserir_ip_permissao = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_ip_permissao.insert(0, 'Informe o IP...')
        self.inserir_ip_permissao.bind('<FocusIn>', self.quando_clicar)
        self.inserir_ip_permissao.pack(pady=(1, 5))

        botao_permissao = Button(self, text="Ativar", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.ativar_permissao)
        botao_permissao.pack(pady=5)
        aplicar_hover(botao_permissao, hover, verde)

        botao_voltar_menu_permissao = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasLinux), self.texto_status_permissao.config(text="")])
        botao_voltar_menu_permissao.pack(pady=13)
        aplicar_hover(botao_voltar_menu_permissao, hover, botao2)

        self.texto_status_permissao = Label(self, text="", bg=fundo, font=("Arial", 10, "bold"))
        self.texto_status_permissao.pack(pady=10)
  
        Label(self, image=self.controller.logo_tk).pack(pady=(80, 10))

    def ativar_permissao(self):
            ip_digitado = self.inserir_ip_permissao.get().strip()
            
            if not ip_digitado or ip_digitado == "Informe o IP...":
                self.texto_status_permissao.config(text="IP inválido.", fg="red")
                return
        
            try:
                resultado = leitura_gravação(ip_digitado)
                self.texto_status_permissao.config(text=resultado, fg=cor_texto)
                self.inserir_ip_permissao.delete(0, END)
            except Exception as e:
                self.texto_status_permissao.config(text=f"Erro inesperado: \n{str(e)}", fg="red")

    def quando_clicar(self, event):
        if self.inserir_ip_permissao.get() == 'Informe o IP...':
            self.inserir_ip_permissao.delete(0, END)
            self.inserir_ip_permissao.config(fg='black')

#########################################################################################

class ConfigurarCaixa(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=fundo)
        self.controller = controller

        self.titulo_configurar_caixa = Label(self, text="Configurar Caixas", bg=fundo, fg=cor_texto, font=("Arial", 13, "bold"))
        self.titulo_configurar_caixa.pack(pady=(20,0))

        self.inserir_ip = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_ip.insert(0, 'Informe o IP...')
        self.inserir_ip.bind('<FocusIn>', self.quando_clicar)
        self.inserir_ip.pack(pady=(1, 1))

        self.inserir_uf = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_uf.insert(0, 'Informe a UF...')
        self.inserir_uf.bind('<FocusIn>', self.quando_clicar)
        self.inserir_uf.pack(pady=(1, 1))

        self.inserir_caixa = Entry(self, fg='grey', width=30, font=("Arial", 11))
        self.inserir_caixa.insert(0, 'Informe o número do Caixa...')
        self.inserir_caixa.bind('<FocusIn>', self.quando_clicar)
        self.inserir_caixa.pack(pady=(1, 1))

        self.informacoes_config = Label(self, text="", bg=fundo, fg=cor_texto, font=("Arial", 10, "bold"), anchor="center", justify="center")
        self.informacoes_config.pack(pady=3, fill='x')

        botao_consultar_venda = Button(self, text="Consultar Venda", width=15, height=1, bg=verde, fg="#ffffff", bd=3, relief="ridge", font=("Arial", 10), command=self.consultar_vendas)
        botao_consultar_venda.pack(pady=3)
        aplicar_hover(botao_consultar_venda, hover, verde)

        botao_voltar_menu_consulta = Button(self, text="Voltar para Menu", width=15, height=1, bg=botao2, fg=cor_texto, bd=3, relief="ridge", font=("Arial", 11), command=lambda: [self.controller.mostrar_tela(MenuProblemasLinux), self.informacoes_config.config(text="")])
        botao_voltar_menu_consulta.pack(pady=(5,5))
        aplicar_hover(botao_voltar_menu_consulta, hover, botao2)

        Label(self, image=self.controller.logo_tk).pack(pady=(1, 10))

    def quando_clicar(self, event):
        if self.inserir_data.get() == 'Informe o IP...':
            self.inserir_data.delete(0, END)
            self.inserir_data.config(fg='black')

        if self.inserir_valor.get() == 'Informe a UF...':
            self.inserir_valor.delete(0, END)
            self.inserir_valor.config(fg='black')

        if self.inserir_valor.get() == 'Informe o número do Caixa...':
            self.inserir_valor.delete(0, END)
            self.inserir_valor.config(fg='black')

#########################################################################################

app = Aplicacao()
app.mainloop()