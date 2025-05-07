import subprocess
import paramiko
import time



def executar_script_powershell(ip_maquina_remota):
    # Caminho do PsExec
    psexec_path = r"C:\caminho\para\PSTools\PsExec.exe"
    
    usuario = "svc_procfitjob"
    senha = "ruqaBAvU7?g6!T"
    caminho_script = r"testescript.ps1"

    comando = [
        psexec_path,
        f"\\\\{ip_maquina_remota}",
        "-u", usuario, 
        "-p", senha,
        "powershell.exe", 
        "-ExecutionPolicy", "Bypass",  # Ignorar a política de execução
        "-File", caminho_script 
    ]
    
    try:
       
        resultado = subprocess.run(comando, capture_output=True, text=True)

        # Verificando a saída e erros do comando
        if resultado.returncode == 0:
            print("Script executado com sucesso.")
            print(f"Saída do PowerShell:\n{resultado.stdout}")
        else:
            print(f"Erro ao executar o script:\n{resultado.stderr}")

    except Exception as e:
        print(f"Erro ao executar o PsExec: {e}")

######################################################################################################################################

def limpar_temp_remoto(ip_maquina_remota):
    psexec_path = r"C:\PSTools\PsExec.exe"

    usuario = "svc_procfitjob"
    senha   = "ruqaBAvU7?g6!T"

    # Montar o comando do PsExec com PowerShell
    comando = [
        psexec_path,
        f"\\\\{ip_maquina_remota}",
        "-u", usuario, 
        "-p", senha,
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",  # Ignorar a política de execução
        "-Command",
        (
            "ipconfig"
        )
    ]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)

        # Verificar saída
        if resultado.returncode == 0:
            print("Comando executado com sucesso.")
            print("Saída do PowerShell:", resultado.stdout)
        else:
            print("Erro ao executar o comando.")
            print("Erros:", resultado.stderr)

    except Exception as e:
        print(f"Erro ao executar PsExec: {e}")


limpar_temp_remoto('192.168.153.52')

################################################################################################

def erro_6f(ip_servidor):

    usuario = 'prevenda'
    senha = 'Nissei@2018'
    senha_root = 'F@RM4C1A'

    try:
        # Cria a conexão SSH
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
        cliente_ssh.connect(ip_servidor, username=usuario, password=senha)

        # Abre um shell interativo
        shell = cliente_ssh.invoke_shell()
        time.sleep(1)

        shell.send('su root\n')
        time.sleep(1)                                   #LOGIN NO SU ROOT
        shell.send(senha_root + '\n')               
        time.sleep(2)

        #INICIO DO 6F
        shell.send('mv /var/opt/mssql/data/PDV.mdf /opt\n')
        time.sleep(2)
        shell.send('mv /var/opt/mssql/data/PDV_log.ldf /opt\n')
        time.sleep(2)
        shell.send('cd /var/opt/\n')
        time.sleep(2)
        shell.send('rm -rf mssql\n')
        time.sleep(2)
        shell.send('3\n')                                      #CONFIGURANDO SQL 
        time.sleep(3)
        shell.send('Y\n')
        time.sleep(3)
        shell.send('8\n')
        time.sleep(3)
        shell.send('ERPM@2017\n')
        time.sleep(2)
        shell.send('ERPM@2017\n')
        time.sleep(10)

        shell.send('mv /opt/PDV.mdf /var/opt/mssql/data\n')
        time.sleep(2)
        shell.send('mv /opt/PDV_log.ldf /var/opt/mssql/data\n')
        time.sleep(2)

        #ANEXANDO BANCO
        #shell.send(f"/opt/mssql-tools/bin/sqlcmd -S {ip_servidor} -U sa -P 'ERPM@2017' -Q \"CREATE DATABASE PDV ON (FILENAME = '/var/opt/mssql/data/PDV.mdf'), (FILENAME = '/var/opt/mssql/data/PDV_log.ldf') FOR ATTACH;\"\n")
        #time.sleep(5)

        output = shell.recv(9999).decode('utf-8')
        print("Saída do terminal:\n", output)

    except Exception as e:
        print(f"Erro ao conectar ou executar o comando: {e}")
    finally:
        cliente_ssh.close()

#erro_6f('10.17.196.3')