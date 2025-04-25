import pyodbc

def conectar_banco(filial):

        filial = int(filial)

        if 0 <= filial <= 199 or filial == 241:
            return f"10.16.{filial}.24"

        elif 200 <= filial <= 240:
            ultimos_digitos = filial % 100
            return f"10.17.{ultimos_digitos}.24"
        elif 242 <= filial <= 299:
            ultimos_digitos = filial % 100
            return f"10.17.{ultimos_digitos}.24"

        elif 300 <= filial <= 399:
            ultimos_digitos = filial % 100
            return f"10.17.1{ultimos_digitos}.24"

        elif 400 <= filial <= 499:
            ultimos_digitos = filial % 100
            return f"10.18.{ultimos_digitos}.24"

        else:
            return None

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

def primary_cheio(conn):

        cursor = conn.cursor()

        select_erpm_upload = cursor.execute("SELECT ENVIADO FROM ERPM_UPLOAD WITH (NOLOCK) WHERE ENVIADO = 'S'").fetchone()
        if select_erpm_upload:
            #curso.execute com DELETE ERPM_UPLOAD FROM ERPM_UPLOAD WITH (NOLOCK) WHERE ENVIADO = 'S'
            return "Feita a limpeza de Log's\n\nCorreção de Primary cheio!"
        else:
                return "Não há arquivos para limpar."

        cursor.close()

# --------------------------------------------------------------------------------

def atualizar_biometria(conn, matricula):


    cursor = conn.cursor()

    cursor.execute("""
                   SELECT OPERADOR, NOME, ABERTURA_CAIXA, FECHAMENTO_CAIXA, CANCELAMENTO_CUPOM, SANGRIA_CAIXA, SUPERVISOR
                    FROM OPERADORES WHERE OPERADOR = ?
                   """, (matricula,))
    
    linha = cursor.fetchone()

    if linha:
        (numero_matricula, nome, abertura_caixa, 
         fechamento_caixa, cancelamento_cupom, sangria_caixa, supervisor) = linha  # Desempacotamento
        
        return f"Matrícula: {numero_matricula} foi atualizada! \n{nome}\n \nAbertura de Caixa: {'Sim' if abertura_caixa == 'S' else 'Não'} \nFechamento de Caixa: {'Sim' if fechamento_caixa == 'S' else 'Não'} \nCancelamento de Cupom: {'Sim' if cancelamento_cupom == 'S' else 'Não'} \nSangria de Caixa: {'Sim' if sangria_caixa == 'S' else 'Não'} \nSupervisor: {'Sim' if supervisor == 'S' else 'Não'}"
    else:
        return f"Nenhum colaborador encontrado com a matrícula {matricula}"

    cursor.close()
# --------------------------------------------------------------------------------

     

#--------------------------------------------------------------------------------

# primary_cheio()

# conn.close()