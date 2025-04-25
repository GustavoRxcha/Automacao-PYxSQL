import pyodbc

def limpeza_log_caixa(conn):

    cursor = conn.cursor()
    select_nfg_log = cursor.execute("SELECT ENVIADO FROM ERPM_UPLOAD WITH (NOLOCK) WHERE ENVIADO = 'S'").fetchone() #SELECT * FROM NFCE_LOG WITH WHERE MOVIMENTO <= '01-01-2025'
    if select_nfg_log:
        #curso.execute com DELETE NFCE_LOG FROM NFCE_LOG WITH (NOLOCK) WHERE MOVIMENTO <= '01-01-2025' 
        return "Feita a limpeza de Log's"
    else:
            return "Não há arquivos para limpar."
    cursor.close()

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
        cursor.execute("SELECT OPERADOR, NOME, ABERTURA_CAIXA, FECHAMENTO_CAIXA, CANCELAMENTO_CUPOM, SANGRIA_CAIXA, SUPERVISOR FROM OPERADORES WHERE OPERADOR = '36051'")
        # cursor.execute("TRUNCATE TABLE OPERADORES; INSERT INTO OPERADORES SELECT * FROM [BALCAO].LOJA.DBO.OPERADORES; TRUNCATE TABLE BIOMETRIAS; INSERT INTO BIOMETRIAS(BIOMETRIA, DATA_HORA, TIPO, CODIGO, STATUS, NITGEN_ISDB, VENDEDOR) SELECT BIOMETRIA, DATA_HORA, TIPO, CODIGO, STATUS, NITGEN_ISDB, VENDEDOR FROM [BALCAO].LOJA.DBO.BIOMETRIAS;")
        conn.commit()
        
        return f"Feito atualização de Biometrias no caixa selecionado!\nTRUNCATE - Ctrl + T"
    except:
        return f"!ERRO: Não foi possível atualizar Biometrias!\n Acessar Banco e verificar."

    cursor.close()

# --------------------------------------------------------------------------------

# conn.close()