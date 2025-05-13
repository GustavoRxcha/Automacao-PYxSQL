import pyodbc
from pathlib import *
import paramiko
import time
from dotenv import load_dotenv
import os

load_dotenv()
usuario_putty = os.getenv("USER_PUTTY")
senha_putty = os.getenv("PASS_PUTTY")
usuario_linux = os.getenv("USER_LINUX")
senha_linux = os.getenv("PASS_LINUX")
senha_root = os.getenv("PASS_ROOT")

# --------------------------------------------------------------------------------

# def limpeza_log_caixa(conn):

#     cursor = conn.cursor()
#     select_nfg_log = cursor.execute("SELECT * FROM NFCE_LOG WITH WHERE MOVIMENTO <= '01-01-2025'").fetchone()

#     if select_nfg_log:
#         cursor.execute("DELETE NFCE_LOG FROM NFCE_LOG WITH (NOLOCK) WHERE MOVIMENTO <= '01-01-2025'") 
#         return "Feita a limpeza de Log's"
#     else:
#             return "Não há arquivos para limpar."
#     cursor.close()

# --------------------------------------------------------------------------------

def habilitar_cartao_presente_caixa(conn):
       
    cursor = conn.cursor()  

    try:
        cursor.execute("USE PDV; UPDATE A SET INCOMM_HABILITAR = 'S', INCOMM_TOKEN = '/TbAwcZADNX+VZEtEsovaMJOhZ305T6oiKP0CyLzmdFXgCKG', INCOMM_ACCOUNT = 'acct_farmacias-nissei', INCOMM_TERMINAL_ID = CAST((SELECT LOJA FROM PARAMETROS) AS VARCHAR) + CAST((SELECT CAIXA FROM PARAMETROS) AS VARCHAR), INCOMM_STORE_ID = '000' + CAST(LOJA AS VARCHAR) + 'IBR31940BZ', INCOMM_URL = 'https://connect-api.todoincomm.com.br' FROM PARAMETROS AS A;")
        conn.commit()

        return "Foi habilitada a venda de cartão presente no caixa!"
    except:
        return "!ERRO: Não foi possível habilitar a opção!\n Acessar Banco e verificar."
    cursor.close()

# --------------------------------------------------------------------------------

def atualizar_biometria_caixa(conn):
     
    cursor = conn.cursor()

    try:
        cursor.execute("TRUNCATE TABLE OPERADORES; INSERT INTO OPERADORES SELECT * FROM [BALCAO].LOJA.DBO.OPERADORES; TRUNCATE TABLE BIOMETRIAS; INSERT INTO BIOMETRIAS(BIOMETRIA, DATA_HORA, TIPO, CODIGO, STATUS, NITGEN_ISDB, VENDEDOR) SELECT BIOMETRIA, DATA_HORA, TIPO, CODIGO, STATUS, NITGEN_ISDB, VENDEDOR FROM [BALCAO].LOJA.DBO.BIOMETRIAS;")
        conn.commit()
        
        return f"Feito atualização de Biometrias no caixa selecionado!\nTRUNCATE - Ctrl + T"
    except:
        return f"!ERRO: Não foi possível atualizar Biometrias!\n Acessar Banco e verificar."

    cursor.close()

# --------------------------------------------------------------------------------

def tabela_zero_caixa(conn):
     
    dir_atual = Path(__file__).parent  
    caminho_tabela_zero = 'ScriptsSQL\\script_tabela_zero.sql'
    with open(caminho_tabela_zero, 'r', encoding='utf-8') as file:
        tabela_zero = file.read()

    dir_atual = Path(__file__).parent  
    caminho_tabela_zero_1 = 'ScriptsSQL\\tabela_zero_1.sql'
    with open(caminho_tabela_zero_1, 'r', encoding='utf-8') as file:
        tabela_zero_1 = file.read()

    dir_atual = Path(__file__).parent  
    caminho_tabela_zero_2 = 'ScriptsSQL\\tabela_zero_2.sql'
    with open(caminho_tabela_zero_2, 'r', encoding='utf-8') as file:
        tabela_zero_2 = file.read()

    cursor = conn.cursor()

    try:
        cursor.execute(tabela_zero)
        return f"Erro de Tabela 0 corrigido utilizando a USP"
    except:
        cursor.execute(tabela_zero_1)
        cursor.execute(tabela_zero_2)
        cursor.execute("exec USP_SINCRONIZA_TABELAS_PDV_LOJA")
        return f"feito a criação da USP e correção de Tabela 0"
    finally:
        return f"ERRO, não foi possível fazer a correção de Tabela 0"

    cursor.close()

# --------------------------------------------------------------------------------


def verificar_vendas_caixa(conn, data, valor, status_venda):

    cursor = conn.cursor()

    try:
        dir_atual = Path(__file__).parent  
        caminho_script_vendas = 'ScriptsSQL\\script_verificar_vendas.sql'
        with open(caminho_script_vendas, 'r', encoding='utf-8') as file:
            vendas_caixa = file.read()


        cursor.execute(vendas_caixa, (data, valor, status_venda))
        linha = cursor.fetchone()

        if linha:
            (forma_pagamento, status, valor, troco, cupom, nsu, numero_venda) = linha

            if status_venda == 'A':
                return f"Pagamento em: {forma_pagamento}\nSTATUS: {status}\nValor: {valor}\nTroco: {troco}\nCUPOM: {cupom}\nNSU: {nsu}\nN° Venda: {numero_venda}"
            elif status_venda == 'C':
                return f"Pagamento em: {forma_pagamento}\nSTATUS: {status}\nValor: {valor}\nTroco: {troco}\nCUPOM: {cupom}\nNSU: {nsu}\nN° Venda: {numero_venda}"
        else:
            return "Não há informação."

    except Exception as e:
        return f"Utilizar '.' ao invés de ','"

    cursor.close()

# --------------------------------------------------------------------------------

def iniciar_vnc(ip_servidor):

    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
        cliente_ssh.connect(ip_servidor, username=usuario_linux, password=senha_linux)

        # Abre um shell
        shell = cliente_ssh.invoke_shell()
        time.sleep(1)

        shell.send('su root\n')
        time.sleep(1)

        shell.send(senha_root + '\n')
        time.sleep(2)

        # Inicia o serviço VNC
        shell.send('service x11vnc start\n')
        time.sleep(2)

    except Exception as e:
        print(f"Erro ao conectar ou executar o comando: {e}")
    finally:
        cliente_ssh.close()

# --------------------------------------------------------------------------------

def mount_a(ip_servidor):

    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
        cliente_ssh.connect(ip_servidor, username=usuario_linux, password=senha_linux)

        # Abre um shell
        shell = cliente_ssh.invoke_shell()
        time.sleep(1)

        shell.send('su root\n')
        time.sleep(1)

        shell.send(senha_root + '\n')
        time.sleep(2)

        # Inicia o serviço VNC
        shell.send('mount -a\n')
        time.sleep(2)

    except Exception as e:
        return f"Erro ao conectar ou executar o comando: \n\n{e}"
    finally:
        cliente_ssh.close()

# --------------------------------------------------------------------------------

#def erro_6f(ip_servidor):
#
#    usuario = 'prevenda'
#    senha = 'Nissei@2018'
#    senha_root = 'F@RM4C1A'
#
#    try:
#        # Cria a conexão SSH
#        cliente_ssh = paramiko.SSHClient()
#        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
#        cliente_ssh.connect(ip_servidor, username=usuario, password=senha)
#
#        # Abre um shell interativo
#        shell = cliente_ssh.invoke_shell()
#        time.sleep(1)
#
#        shell.send('su root\n')
#        time.sleep(1)                                   #LOGIN NO SU ROOT
#        shell.send(senha_root + '\n')
#        time.sleep(2)
#
#        #INICIO DO 6F
#        shell.send('mv /var/opt/mssql/data/PDV.mdf /opt\n')
#        time.sleep(3)
#        shell.send('mv /var/opt/mssql/data/PDV_log.ldf /opt\n')
#        time.sleep(3)
#        shell.send('cd /var/opt/\n')
#        time.sleep(3)
#        shell.send('rm -rf mssql\n')
#        time.sleep(3)
#        shell.send('/opt/mssql/bin/mssql-conf setup\n')
#        time.sleep(5)
#        shell.send('3\n')                                      #CONFIGURANDO SQL
#        time.sleep(3)
#        shell.send('Y\n')
#        time.sleep(3)
#        shell.send('8\n')
#        time.sleep(3)
#        shell.send('ERPM@2017\n')
#        time.sleep(4)
#        shell.send('ERPM@2017\n')
#        time.sleep(10)
#
#        shell.send('mv /opt/PDV.mdf /var/opt/mssql/data\n')
#        time.sleep(4)
#        shell.send('mv /opt/PDV_log.ldf /var/opt/mssql/data\n')
#        time.sleep(4)
#
#        #ANEXANDO BANCO
#        #shell.send(f"/opt/mssql-tools/bin/sqlcmd -S {ip_servidor} -U sa -P 'ERPM@2017' -Q \"CREATE DATABASE PDV ON (FILENAME = '/var/opt/mssql/data/PDV.mdf'), (FILENAME = '/var/opt/mssql/data/PDV_log.ldf') FOR ATTACH;\"\n")
#        #time.sleep(5)
#
#    except Exception as e:
#        return f"Erro ao conectar ou executar o comando: \n\n{e}"
#    finally:
#        cliente_ssh.close()

# --------------------------------------------------------------------------------

def leitura_gravação(ip_servidor):

    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
        cliente_ssh.connect(ip_servidor, username=usuario_putty, password=senha_putty)

        # Abre um shell
        shell = cliente_ssh.invoke_shell()
        time.sleep(1)

        shell.send('su root\n')
        time.sleep(1)

        shell.send(senha_root + '\n')
        time.sleep(2)

        # Inicia o serviço VNC
        shell.send('chmod -R a+rwx /opt/pdv/\n')
        time.sleep(2)

    except Exception as e:
        return f"Erro ao conectar ou executar o comando: \n\n{e}"
    finally:
        cliente_ssh.close()

# --------------------------------------------------------------------------------

# conn.close()