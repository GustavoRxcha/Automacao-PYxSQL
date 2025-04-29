import subprocess

def executar_script_powershell(ip_maquina_remota):
    # Caminho do PsExec
    psexec_path = r"C:\caminho\para\PSTools\PsExec.exe"
    
    usuario = "Administrador"
    senha = "senha_remota"
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


ip = "10.16.44.24"

executar_script_powershell(ip)
