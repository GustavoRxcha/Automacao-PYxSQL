import subprocess
import paramiko



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

    usuario = 'su root' 
    senha = 'F@RM4C1A'

    try:
        # Cria a conexão SSH
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignora a verificação de chave do host
        cliente_ssh.connect(ip_servidor, username=usuario, password=senha)

        comando = 'sudo service x11vnc start'

        # Executa o comando
        stdin, stdout, stderr = cliente_ssh.exec_command(comando)

        stdin.write(senha + '\n')
        stdin.flush()

        saida = stdout.read().decode()
        erros = stderr.read().decode()

        if saida:
            print("Saída:", saida)

        if erros:
            print("Erros:", erros)
        else:
            print("Comando executado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Fecha a conexão SSH
        cliente_ssh.close()

# Exemplo de chamada da função:
iniciar_vnc('192.168.1.100')
