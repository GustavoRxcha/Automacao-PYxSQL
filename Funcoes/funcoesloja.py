import pyodbc
from pathlib import *
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()
usuario_proc = os.getenv("USER_PROC")
senha_proc = os.getenv("PASS_PROC")

def gerar_ip(filial):

        filial = int(filial)

        if 0 <= filial <= 199 or filial == 241:
            return f"10.16.{filial}."

        elif 200 <= filial <= 240:
            ultimos_digitos = filial % 100
            return f"10.17.{ultimos_digitos}."
        elif 242 <= filial <= 299:
            ultimos_digitos = filial % 100
            return f"10.17.{ultimos_digitos}."

        elif 300 <= filial <= 399:
            ultimos_digitos = filial % 100
            return f"10.17.1{ultimos_digitos}."

        elif 400 <= filial <= 499:
            ultimos_digitos = filial % 100
            return f"10.18.{ultimos_digitos}."

        else:
            return None

def alterar_filial(self, home):
    self.controller.filial = ""  # Zera a filial/IP
    self.controller.mostrar_tela(home)

# --------------------------------------------------------------------------------

def desabilitar_datahub(conn):

    cursor = conn.cursor()

    query = """
    UPDATE PARAMETROS SET 
    DATAHUB_HABILITAR = ?,
    DATAHUB_URL = ?,
    DATAHUB_USUARIO = ?,
    DATAHUB_SENHA = ?,
    DATAHUB_URL_CAD = ?,
    PRIORIZAR_CONSULTA_PROC_CLIENTES = ?
    """
    params = ('N', None, None, None, None, '0')

    cursor.execute(query, params)

    status_datahub = cursor.execute("SELECT DATAHUB_HABILITAR FROM PARAMETROS").fetchone()
    if status_datahub:
        resultado_select = status_datahub[0]
        print(f'STATUS ATUAL DO DATAHUB: {resultado_select}')

    conn.commit() #confirmar o comando

    cursor.close()

# --------------------------------------------------------------------------------

def habilitar_datahub(conn):

    cursor = conn.cursor()

    query = """
    UPDATE PARAMETROS SET 
    DATAHUB_HABILITAR = ?,
    DATAHUB_SENHA = ?,
    DATAHUB_URL = ?,
    DATAHUB_URL_CAD = ?,
    DATAHUB_USUARIO = ?,
    HABILITAR_PROPZ = ?
    """

    params = (
        'S',
        'V57Z$X7SAuD#dj',
        'https://datahub-api.nisseilabs.com.br',
        'https://vendamais.nisseilabs.com.br/clientes/cadastro/novo',
        'procfit',
        'S'
    )

    cursor.execute(query, params)

    status_datahub = cursor.execute("SELECT DATAHUB_HABILITAR FROM PARAMETROS").fetchone()
    if status_datahub:
        resultado_select = status_datahub[0]
        print(f'STATUS ATUAL DO DATAHUB: {resultado_select}')

    conn.commit()

    cursor.close()

# --------------------------------------------------------------------------------

# def primary_cheio(conn):

#         cursor = conn.cursor()

#         select_erpm_upload = cursor.execute("SELECT ENVIADO FROM ERPM_UPLOAD WITH WHERE ENVIADO = 'S'").fetchone()
#         if select_erpm_upload:
#             cursor.execute("DELETE ERPM_UPLOAD FROM ERPM_UPLOAD WITH WHERE ENVIADO = 'S'") 
#             conn.commit()
#             return "Feita a limpeza de Log's\n\nCorreção de Primary cheio!"
#         else:
#                 return "Não há arquivos para limpar."

#         cursor.close()

# --------------------------------------------------------------------------------

def atualizar_biometria(conn, matricula):

    dir_atual = Path(__file__).parent  
    caminho_script_atualizar_bio = 'ScriptsSQL\\script_atualizar_biometria.sql'

    with open(caminho_script_atualizar_bio, 'r', encoding='utf-8') as file:
        script = file.read()

    cursor = conn.cursor()

    cursor.execute(script, matricula)
    conn.commit()

    #cursor.execute("SELECT a.CARGO_DESCONTO FROM VENDEDORES AS a JOIN CARGOS_DESCONTOS AS b ON a.CARGO_DESCONTO = b.CARGO_DESCONTO WHERE a.VENDEDOR = ?", (matricula,))
    #resultado = cursor.fetchone()
    #cargo_desconto = resultado[0]

    cursor.execute("""
                   SELECT OPERADOR, NOME, ABERTURA_CAIXA, FECHAMENTO_CAIXA, CANCELAMENTO_CUPOM, SANGRIA_CAIXA, SUPERVISOR
                    FROM OPERADORES WHERE OPERADOR = ?
                   """, (matricula,))

    linha = cursor.fetchone()

    if linha:
        (numero_matricula, nome, abertura_caixa, 
         fechamento_caixa, cancelamento_cupom, sangria_caixa, supervisor) = linha  # Desempacotamento
        
        return f"Matrícula: {numero_matricula} foi atualizada!\n{nome} \n\nAbertura de Caixa: {'Sim' if abertura_caixa == 'S' else 'Não'} \nFechamento de Caixa: {'Sim' if fechamento_caixa == 'S' else 'Não'} \nCancelamento de Cupom: {'Sim' if cancelamento_cupom == 'S' else 'Não'} \nSangria de Caixa: {'Sim' if sangria_caixa == 'S' else 'Não'} \nSupervisor: {'Sim' if supervisor == 'S' else 'Não'}"
    else:
        return f"Nenhum colaborador encontrado com a matrícula {matricula}"

    cursor.close()

# --------------------------------------------------------------------------------

def integrar_nota(conn, NF):

    dir_atual = Path(__file__).parent  
    caminho_script_integrar = 'ScriptsSQL\\scrip_integrar_nf.sql'

    with open(caminho_script_integrar, 'r', encoding='utf-8') as file:
        script = file.read()

    cursor = conn.cursor()

    cursor.execute("EXEC('SELECT PEDIDO_COMPRA, NF_COMPRA FROM NF_COMPRA WHERE CHAVE_NFE = ?') AT RETAGUARDA", (NF,))
    
    select_pedido_nf = cursor.fetchone()

    if select_pedido_nf:
        (pedido_compra, nf_compra) = select_pedido_nf

    print(nf_compra)
    print(pedido_compra)

    cursor.execute(script, (nf_compra, pedido_compra))

    resultado_formatado = cursor.fetchone()
    resultado_nao_formatado = cursor.fetchall()

    if resultado_formatado:
        (nf_de_compra, empresa, entidade, movimento, nf_serie, 
         nf_numero, pedido_de_compra, produto, descricao, quantidade,) = resultado_formatado

        return f"NF DE COMPRA: {nf_de_compra}\nPEDIDO DE COMPRA: {pedido_de_compra}\nSERIE NF: {nf_serie}\nNÚMERO NF: {nf_numero}\nFILIAL: {entidade}"
    else:
        return f"RESULTADO NÃO FORMATADO: {resultado_nao_formatado}"

    cursor.close()    
#--------------------------------------------------------------------------------
def consultar_versao(conn):

    cursor = conn.cursor()
    
    status_versao = cursor.execute("SELECT VERSAO FROM PARAMETROS").fetchone()
    if status_versao:
        resultado_select = status_versao[0]
        return resultado_select

    cursor.close()

def atualizar_versao(conn, versao):

    cursor = conn.cursor()
    
    cursor.execute("UPDATE PARAMETROS SET VERSAO = ?", (versao,))

    cursor.close()
#--------------------------------------------------------------------------------

def atualizar_estoque(conn):

    cursor = conn.cursor()

    try:
        dir_atual = Path(__file__).parent
        caminho_script_estoque = 'ScriptsSQL\\script_atualizar_estoque.sql'
        with open(caminho_script_estoque, 'r', encoding='utf-8') as file:
            script_estoque = file.read()

        cursor.execute(script_estoque)
        
        return f"Estoque da filial atualizado com sucesso!"
    except:
        return f"!ERRO: Não foi possível atualizar o estoque!\n Acessar Banco e verificar."
    
    cursor.close()

#--------------------------------------------------------------------------------

def limpar_temp_ps1(ip_maquina_remota):
    # Caminho do PsExec
    psexec_path = r"C:\caminho\para\PSTools\PsExec.exe" #adicionar caminho correto
    

    comando = [
        psexec_path,
        f"\\\\{ip_maquina_remota}",
        "-u", usuario_proc, 
        "-p", senha_proc,
        "powershell.exe", 
        "-ExecutionPolicy", "Bypass",  # Ignorar a política de execução
        "-Command",
        (
            "ipconfig"
        )
    ]
    
    try:
       
        resultado = subprocess.run(comando, capture_output=True, text=True)

        # Verificando a saída e erros do comando
        if resultado.returncode == 0:
            return f"Script executado com sucesso.\n\nSaída do PowerShell: {resultado.stdout}"
        else:
            return f"Erro ao executar o script:\n{resultado.stderr}"

    except Exception as e:
        print(f"Erro ao executar o PsExec: {e}")

#--------------------------------------------------------------------------------
