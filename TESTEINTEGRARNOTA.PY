import pyodbc

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

    cursor = conn.cursor()

    print(f"Valor de NF sendo usado: {NF}")

    cursor.execute("""
        EXEC('SELECT PEDIDO_COMPRA, NF_COMPRA 
            FROM NF_COMPRA 
            WHERE CHAVE_NFE = ?') AT RETAGUARDA
            """, (NF,))

    select_pedido_nf = cursor.fetchone()

    if select_pedido_nf:
        (pedido_compra, nf_compra) = select_pedido_nf

    print(pedido_compra)
    print(nf_compra)

    sql = """DECLARE @NF_COMPRA     VARCHAR(15) = ?
             DECLARE @PEDIDO_COMPRA VARCHAR(15) = ?
             
             SET NOCOUNT ON;
             
             -- Exclui os dados no banco local
             IF EXISTS (SELECT TOP 1 1 FROM NF_COMPRA WHERE NF_COMPRA = @NF_COMPRA)
                BEGIN DELETE FROM NF_COMPRA WHERE NF_COMPRA = @NF_COMPRA END;
             
             IF EXISTS (SELECT TOP 1 1 FROM PEDIDOS_COMPRAS WHERE PEDIDO_COMPRA = @PEDIDO_COMPRA)
                BEGIN DELETE FROM PEDIDOS_COMPRAS WHERE PEDIDO_COMPRA = @PEDIDO_COMPRA END;
             
             IF EXISTS (SELECT TOP 1 1 FROM PEDIDOS_COMPRAS_PRODUTOS WHERE PEDIDO_COMPRA = @PEDIDO_COMPRA)
                BEGIN DELETE FROM PEDIDOS_COMPRAS_PRODUTOS WHERE PEDIDO_COMPRA = @PEDIDO_COMPRA END;
             
             -- Insere os dados na tabela NF_COMPRA
             INSERT INTO [NF_COMPRA] 
                        ([NF_COMPRA]
                        ,[FORMULARIO_ORIGEM]
                        ,[TAB_MASTER_ORIGEM]
                        ,[REG_MASTER_ORIGEM]
                        ,[REG_LOG_INCLUSAO]
                        ,[ROWVERSION]
                        ,[EMPRESA]
                        ,[ENTIDADE]
                        ,[MOVIMENTO]
                        ,[NF_ESPECIE]
                        ,[NF_SERIE]
                        ,[NF_NUMERO]
                        ,[CHAVE_NFE]
                        ,[PEDIDO_COMPRA]
                        ,[RECEBIMENTO]
                        ,[TOTAL_GERAL]
                        ,[PROCESSAR]
                        ,[STATUS_VALIDACAO_COMERCIAL])
             EXEC ('SELECT [NF_COMPRA]
                          ,[FORMULARIO_ORIGEM]
                          ,[TAB_MASTER_ORIGEM]
                          ,[REG_MASTER_ORIGEM]
                          ,111 AS [REG_LOG_INCLUSAO]
                          ,[ROWVERSION]
                          ,[EMPRESA]
                          ,[ENTIDADE]
                          ,[MOVIMENTO]
                          ,[NF_ESPECIE]
                          ,[NF_SERIE]
                          ,[NF_NUMERO]
                          ,[CHAVE_NFE]
                          ,[PEDIDO_COMPRA]
                          ,[RECEBIMENTO]
                          ,[TOTAL_GERAL]
                          ,[PROCESSAR]
                          ,[STATUS_VALIDACAO_COMERCIAL]
                    FROM NF_COMPRA
                   WHERE NF_COMPRA = ''' + @NF_COMPRA + '''') AT [RETAGUARDA];
             
             -- Insere os dados na tabela PEDIDOS_COMPRAS
             INSERT INTO [PEDIDOS_COMPRAS] 
                        ([PEDIDO_COMPRA]
                        ,[FORMULARIO_ORIGEM]
                        ,[TAB_MASTER_ORIGEM]
                        ,[REG_MASTER_ORIGEM]
                        ,[REG_LOG_INCLUSAO]
                        ,[ROWVERSION]
                        ,[ENTIDADE]
                        ,[EMPRESA]
                        ,[DATA_HORA]
                        ,[SUGESTAO_COMPRA]
                        ,[CICLO_ELETRONICO])
             EXEC ('SELECT [PEDIDO_COMPRA]
                          ,[FORMULARIO_ORIGEM]
                          ,[TAB_MASTER_ORIGEM]
                          ,[REG_MASTER_ORIGEM]
                          ,111 AS [REG_LOG_INCLUSAO]
                          ,[ROWVERSION]
                          ,[ENTIDADE]
                          ,[EMPRESA]
                          ,[DATA_HORA]
                          ,[SUGESTAO_COMPRA]
                          ,[CICLO_ELETRONICO]
                    FROM PEDIDOS_COMPRAS
                   WHERE PEDIDO_COMPRA = ''' + @PEDIDO_COMPRA + '''') AT [RETAGUARDA];
             
             -- Insere os dados na tabela PEDIDOS_COMPRAS_PRODUTOS
             SET IDENTITY_INSERT PEDIDOS_COMPRAS_PRODUTOS ON;
             
             INSERT INTO [PEDIDOS_COMPRAS_PRODUTOS] 
                        ([PEDIDO_COMPRA_PRODUTO]
                        ,[FORMULARIO_ORIGEM]
                        ,[TAB_MASTER_ORIGEM]
                        ,[REG_MASTER_ORIGEM]
                        ,[REG_LOG_INCLUSAO]
                        ,[ROWVERSION]
                        ,[PEDIDO_COMPRA]
                        ,[REFERENCIA]
                        ,[PRODUTO]
                        ,[QUANTIDADE]
                        ,[QUANTIDADE_EMBALAGEM]
                        ,[QUANTIDADE_ESTOQUE])
             EXEC ('SELECT [PEDIDO_COMPRA_PRODUTO]
                          ,[FORMULARIO_ORIGEM]
                          ,[TAB_MASTER_ORIGEM]
                          ,[REG_MASTER_ORIGEM]
                          ,111 AS [REG_LOG_INCLUSAO]
                          ,[ROWVERSION]
                          ,[PEDIDO_COMPRA]
                          ,[REFERENCIA]
                          ,[PRODUTO]
                          ,[QUANTIDADE]
                          ,[QUANTIDADE_EMBALAGEM]
                          ,[QUANTIDADE_ESTOQUE]
                    FROM PEDIDOS_COMPRAS_PRODUTOS
                   WHERE PEDIDO_COMPRA = ''' + @PEDIDO_COMPRA + '''') AT [RETAGUARDA];
             
             SET IDENTITY_INSERT PEDIDOS_COMPRAS_PRODUTOS OFF;
             
             -- Consulta final
             SELECT A.NF_COMPRA
                   ,A.EMPRESA
                   ,A.ENTIDADE                          AS FORNECEDOR
                   ,CONVERT(VARCHAR, A.MOVIMENTO, 103) AS MOVIMENTO
                   ,A.NF_SERIE
                   ,A.NF_NUMERO
                   ,B.PEDIDO_COMPRA
                   ,C.PRODUTO
                   ,D.DESCRICAO
                   ,C.QUANTIDADE
               FROM NF_COMPRA                AS A
               JOIN PEDIDOS_COMPRAS         AS B ON A.PEDIDO_COMPRA = B.PEDIDO_COMPRA
               JOIN PEDIDOS_COMPRAS_PRODUTOS AS C ON B.PEDIDO_COMPRA = C.PEDIDO_COMPRA
               JOIN PRODUTOS                AS D ON C.PRODUTO = D.PRODUTO
              WHERE A.NF_COMPRA     = @NF_COMPRA
                AND B.PEDIDO_COMPRA = @PEDIDO_COMPRA;
             
             SET NOCOUNT OFF;
             """

    cursor.execute(sql, (nf_compra, pedido_compra))
    resultado_integracao = cursor.fetchall()

    print(resultado_integracao)

    cursor.close()
    return resultado_integracao
    