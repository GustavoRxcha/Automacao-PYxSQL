import pyodbc
from pathlib import *

ip = r'localhost\SQLEXPRESS'
database='LOJA'

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={ip};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'  #autenticação Windows
    )
    print("Conexão bem-sucedida!\n")
except pyodbc.Error as ex:
    print(f"Erro detalhado: {ex}")


def integrar_nota(NF):

    dir_atual = Path(__file__).parent  
    caminho_script_integrar = dir_atual / "ScriptsSQL" / "scrip_integrar_nf.sql"

    with open(caminho_script_integrar, 'r', encoding='utf-8') as file:
        script = file.read()

    cursor = conn.cursor()

    cursor.execute("""
        EXEC('SELECT PEDIDO_COMPRA, NF_COMPRA 
            FROM NF_COMPRA 
            WHERE CHAVE_NFE = ?') AT RETAGUARDA
            """, (NF,))
    
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
         nf_numero, pedido_de_compra, produto, descricao, quantidade,) = resultado_formatado  # Desempacotamento

        print(f"NF DE COMPRA: {nf_de_compra}, PEDIDO DE COMPRA: {pedido_de_compra}, SERIE NF: {nf_serie}, NÚMERO NF: {nf_numero}, FILIAL: {entidade},")        
    else:
        return print(resultado_nao_formatado)

    cursor.close()
