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
            "$temp = $env:TEMP; "
            "if (Test-Path $temp) { "
            "    Remove-Item -Path \"$temp\\*\" -Recurse -Force; "
            "} "
            "New-Item -Path $temp -ItemType Directory; "
            "Write-Output 'Temp limpado'"
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

######################################################################################################################################


def iniciar_vnc(ip_servidor):

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
        time.sleep(1)

        shell.send(senha_root + '\n')
        time.sleep(2)

        # Inicia o serviço VNC
        shell.send('service x11vnc start\n')
        time.sleep(2)

        # Lê a saída do shell
        output = shell.recv(9999).decode('utf-8')
        print("Saída do terminal:\n", output)

    except Exception as e:
        print(f"Erro ao conectar ou executar o comando: {e}")
    finally:
        cliente_ssh.close()


#iniciar_vnc('10.18.52.3')

################################################################################################

def mount_a(ip_servidor):

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
        time.sleep(1)

        shell.send(senha_root + '\n')
        time.sleep(2)

        # Inicia o serviço VNC
        shell.send('mount -a\n')
        time.sleep(2)

        # Lê a saída do shell
        output = shell.recv(9999).decode('utf-8')
        print("Saída do terminal:\n", output)

    except Exception as e:
        print(f"Erro ao conectar ou executar o comando: {e}")
    finally:
        cliente_ssh.close()

mount_a('10.18.52.3')
