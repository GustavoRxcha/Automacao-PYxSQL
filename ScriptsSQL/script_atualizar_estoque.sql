
INSERT INTO SINCRONIZACAO_ESTOQUE_LOJA_LOG ( LOJA ) SELECT EMPRESA FROM PARAMETROS

DECLARE @TESTE VARCHAR(10)
DECLARE @srvproduct NVARCHAR(256)
DECLARE @datasrc NVARCHAR(1000)
DECLARE @rmtpassword SYSNAME
DECLARE @rmtuser SYSNAME
DECLARE @catalog SYSNAME

SELECT TOP 1
 @srvproduct = A.CENTRAL_SERVIDOR,
 @datasrc = A.CENTRAL_SERVIDOR,
 @rmtpassword = A.CENTRAL_SENHA,
 @rmtuser = A.CENTRAL_USUARIO,
 @catalog = A.CENTRAL_BANCO
FROM
 PARAMETROS A WITH(NOLOCK)


IF  EXISTS (SELECT srv.name FROM sys.servers srv WHERE srv.server_id != 0 AND srv.name = N'RETAGUARDA')EXEC master.dbo.sp_dropserver @server=N'RETAGUARDA', @droplogins='droplogins'

EXEC master.dbo.sp_addlinkedserver @server = N'RETAGUARDA', @srvproduct=@srvproduct, @provider=N'SQLNCLI', @datasrc=@datasrc, @catalog = @catalog
EXEC master.dbo.sp_addlinkedsrvlogin @rmtsrvname=N'RETAGUARDA',@useself=N'False',@locallogin=NULL,@rmtuser=@rmtuser,@rmtpassword=@rmtpassword
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'collation compatible', @optvalue=N'false'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'data access', @optvalue=N'true'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'dist', @optvalue=N'false'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'pub', @optvalue=N'false'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'rpc', @optvalue=N'true'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'rpc out', @optvalue=N'true'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'sub', @optvalue=N'false'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'connect timeout', @optvalue=N'0'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'collation name', @optvalue=null
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'lazy schema validation', @optvalue=N'false'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'query timeout', @optvalue=N'0'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'use remote collation', @optvalue=N'true'
EXEC master.dbo.sp_serveroption @server=N'RETAGUARDA', @optname=N'remote proc transaction promotion', @optvalue=N'false'


 SET DEADLOCK_PRIORITY 0

 SET XACT_ABORT ON

    DECLARE @SQL             NVARCHAR(MAX)
 DECLARE @EMPRESA         NUMERIC(15)
 DECLARE @EMPRESA_VARCHAR VARCHAR(15)
    DECLARE @LISTA_PRODUTOS  NVARCHAR(MAX)

 SELECT TOP 1 @EMPRESA         = A.EMPRESA
               , @EMPRESA_VARCHAR = CONVERT(VARCHAR(15), A.EMPRESA)

            FROM PARAMETROS A


 IF OBJECT_ID('tempdb..#TEMP_PRODUTOS_PENDENTES') IS NOT NULL DROP TABLE #TEMP_PRODUTOS_PENDENTES

    CREATE TABLE #TEMP_PRODUTOS_PENDENTES (PRODUTO NVARCHAR(MAX))


 INSERT INTO #TEMP_PRODUTOS_PENDENTES /* 1. Há dados de venda pendentes para envio ao Retaguarda..*/
 SELECT DISTINCT
     A.CONTEUDO.value('(//PRODUTO)[1]', 'nvarchar(50)')
   FROM ERPM_UPLOAD A (NOLOCK)
  WHERE A.ENVIADO = 'N'
    AND A.DESTINO = 'PDV_ITENS'


 SET @SQL = 'SELECT B.PRODUTO
      FROM PDV_ITENS_INTEGRACOES A (NOLOCK)
                  JOIN PDV_ITENS             B (NOLOCK) ON A.VENDA     = B.VENDA
                                                       AND A.MOVIMENTO = B.MOVIMENTO
                                                       AND B.LOJA      = A.LOJA
                                                       AND B.CAIXA     = A.CAIXA
                                                       AND A.ITEM      = B.ITEM
     WHERE A.LOJA = ' + @EMPRESA_VARCHAR + '
       AND A.INTEGRADO = ''N'''

 INSERT INTO #TEMP_PRODUTOS_PENDENTES /* 2. Há dados de venda pendentes para integração de estoque na Retaguarda..*/
     EXEC (@SQL) AT [RETAGUARDA]


 SET @SQL = 'SELECT A.CONTEUDO.value(''(//PRODUTO)[1]'', ''nvarchar(50)'')
      FROM ERPM_DOWNLOAD A WITH(NOLOCK)
     WHERE A.EMPRESA = ' + @EMPRESA_VARCHAR + '
       AND A.DESTINO = ''ESTOQUE_MOVIMENTOS''
       AND A.ENVIADO = ''N'''

 INSERT INTO #TEMP_PRODUTOS_PENDENTES /* 3. Há uma entrada de estoque pendente na Retaguarda.. */
      EXEC (@SQL) AT [RETAGUARDA]


 SET @SQL = 'SELECT A.CONTEUDO.value(''(//PRODUTO)[1]'', ''nvarchar(50)'')
      FROM ERPM_UPLOAD A WITH(NOLOCK)
     WHERE A.EMPRESA = ' + @EMPRESA_VARCHAR + '
       AND A.IMPORTADO = ''N''
       AND A.CONTEUDO.value(''(//Transacao/@Tabela)[1]'', ''SYSNAME'') = ''PDV_ITENS'''

 INSERT INTO #TEMP_PRODUTOS_PENDENTES /* 4. Dados pendentes para processamento de estoque na retaguarda..*/
     EXEC (@SQL) AT [RETAGUARDA]


 IF (SELECT COUNT(*) AS TOTAL FROM #TEMP_PRODUTOS_PENDENTES) > 100
 BEGIN
  RAISERROR('Existe atualmente um total de produtos em processamento superior a 100. Por favor, verifique a replicação de dados da loja para garantir a atualização correta do estoque.', 15, -1)
  RETURN
 END

    SELECT @LISTA_PRODUTOS = ( SELECT DISTINCT ', ' + CAST ( PRODUTO AS VARCHAR(15) ) FROM #TEMP_PRODUTOS_PENDENTES FOR XML PATH(''), TYPE ).value('.', 'nvarchar(max)')
       SET @LISTA_PRODUTOS = RIGHT ( @LISTA_PRODUTOS, LEN ( @LISTA_PRODUTOS ) - 2 )
    SET @LISTA_PRODUTOS = ISNULL(@LISTA_PRODUTOS, 1)


    SET @SQL = 'UPDATE ERPM_DOWNLOAD
                   SET ENVIADO = ''P''
        WHERE EMPRESA = ' + @EMPRESA_VARCHAR + '
          AND DESTINO = ''ESTOQUE_MOVIMENTOS''
          AND ENVIADO = ''N''
          AND CONTEUDO.value(''(//PRODUTO)[1]'', ''nvarchar(50)'') NOT IN (' + @LISTA_PRODUTOS + ')'

 EXEC (@SQL) AT [RETAGUARDA]


    SET @SQL = 'DELETE
                  FROM PDV_ESTOQUE_MOVIMENTOS
                 WHERE LOJA = ' + @EMPRESA_VARCHAR + '
                   AND PRODUTO NOT IN (' + @LISTA_PRODUTOS + ')'

 EXEC (@SQL) AT [RETAGUARDA]

 BEGIN TRY
  BEGIN TRANSACTION


  IF OBJECT_ID('tempdb..#TEMP_ESTOQUE_MOVIMENTOS') IS NOT NULL DROP TABLE #TEMP_ESTOQUE_MOVIMENTOS

  SELECT A.REGISTRO
    , A.PRODUTO
    , A.ENTRADA
    , A.SAIDA
    , A.FORMULARIO_ORIGEM
    , A.TAB_MASTER_ORIGEM
    , A.REG_MASTER_ORIGEM
    , A.DATA
    , A.LOCAL_MOVIMENTACAO
    , A.ID_ORIGEM

   INTO #TEMP_ESTOQUE_MOVIMENTOS

   FROM ESTOQUE_MOVIMENTOS         A (NOLOCK)
   WHERE EXISTS ( SELECT TOP 1 1
        FROM #TEMP_PRODUTOS_PENDENTES  B (NOLOCK)
       WHERE B.PRODUTO = A.PRODUTO )


  TRUNCATE TABLE ESTOQUE_MOVIMENTOS


  INSERT INTO ESTOQUE_MOVIMENTOS
  (
   REGISTRO
   , PRODUTO
   , ENTRADA
   , SAIDA
   , DATA
   , LOCAL_MOVIMENTACAO
  )
  SELECT REGISTRO
    , PRODUTO
    , ENTRADA
    , SAIDA
    , DATA
    , LOCAL_MOVIMENTACAO

   FROM #TEMP_ESTOQUE_MOVIMENTOS


  SET @SQL =  'SELECT ROW_NUMBER() OVER ( ORDER BY A.PRODUTO ) AS REGISTRO
       , A.PRODUTO
       , CASE WHEN A.ESTOQUE_SALDO > 0 THEN A.ESTOQUE_SALDO ELSE 0 END AS ENTRADA
       , CASE WHEN A.ESTOQUE_SALDO < 0 THEN -(A.ESTOQUE_SALDO) ELSE 0 END AS SAIDA
       , GETDATE() AS DATE
       , 0 AS LOCAL_MOVIMENTACAO -- Saldo Inicial

      FROM ESTOQUE_ATUAL      A
      JOIN EMPRESAS_ESTOQUES  B ON B.OBJETO_CONTROLE = A.CENTRO_ESTOQUE
            AND B.TIPO_ESTOQUE = 2

      WHERE B.EMPRESA_USUARIA = ' + @EMPRESA_VARCHAR + '
      AND A.ESTOQUE_SALDO <> 0
      AND A.PRODUTO NOT IN (' + @LISTA_PRODUTOS + ')'

  INSERT INTO ESTOQUE_MOVIMENTOS
  (
   REGISTRO
   , PRODUTO
   , ENTRADA
   , SAIDA
   , DATA
   , LOCAL_MOVIMENTACAO
  )
  EXEC (@SQL) AT [RETAGUARDA]

  COMMIT TRANSACTION
 END TRY
 BEGIN CATCH
  IF @@TRANCOUNT > 0
   ROLLBACK TRANSACTION

  RAISERROR('A execução não pôde ser concluída. A atualização do estoque não foi realizada. Por favor, tente novamente.', 16, 1)
  RETURN
 END CATCH