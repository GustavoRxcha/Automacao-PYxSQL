import pyodbc
from pathlib import *
import paramiko
import time
import os

#from dotenv import load_dotenv
#load_dotenv()
#usuario_putty = os.getenv("USER_PUTTY")
#senha_putty = os.getenv("PASS_PUTTY")
#usuario_linux = os.getenv("USER_LINUX")
#senha_linux = os.getenv("PASS_LINUX")
#senha_root = os.getenv("PASS_ROOT")

# --------------------------------------------------------------------------------

def iniciar_vnc(ip_servidor):

    usuario_putty = "suporte"
    senha_putty = "F@RM4C1A"
    senha_root = "F@RM4C1A"

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
        shell.send('service x11vnc start\n')
        time.sleep(2)

        return f"VNC habilitado para acessar terminal!"

    except Exception as e:
        print(f"Erro ao conectar ou executar o comando: {e}")
    finally:
        cliente_ssh.close()

# --------------------------------------------------------------------------------

def mount_a(ip_servidor):

    usuario_putty = "suporte"
    senha_putty = "F@RM4C1A"
    senha_root = "F@RM4C1A"

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
        shell.send('mount -a\n')
        time.sleep(2)

        return f"Efetuado 'mount -a', Caixa corrigido."

    except Exception as e:
        return f"Erro ao conectar ou executar o comando: \n\n{e}"
    finally:
        cliente_ssh.close()

# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------

def leitura_gravação(ip_servidor):

    usuario_putty = "suporte"
    senha_putty = "F@RM4C1A"
    senha_root = "F@RM4C1A"

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

        shell.send('chmod -R a+rwx /opt/pdv/\n')
        time.sleep(2)

        return f"Ativado as permissões no caixa\n\nLeitura e Gravação ✓ "

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