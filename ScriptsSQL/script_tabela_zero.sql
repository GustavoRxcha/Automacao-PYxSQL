BEGIN
 
DECLARE @SQL   NVARCHAR(MAX) = NULL;
DECLARE @INDEX_WHILE INT     = 1; 
DECLARE @TABLE_NAME NVARCHAR(255)  = NULL  
  
SELECT TOP 1 @INDEX_WHILE = MIN(ID)   
   FROM TABELA_SYNC_BALCAO  
  
  
WHILE @INDEX_WHILE IS NOT NULL   
BEGIN   
    
  SELECT TOP 1 @TABLE_NAME = TABELA   
    FROM TABELA_SYNC_BALCAO  
   WHERE ID = @INDEX_WHILE  
  
  
  BEGIN TRY   
  
   EXEC ('  
     
    TRUNCATE TABLE ' + @TABLE_NAME + '  
      INSERT INTO  ' + @TABLE_NAME + '   
      SELECT TOP 1   
       *   
     FROM [BALCAO].[LOJA].[dbo].[' + @TABLE_NAME + ']  
  
   ')  
  
  END TRY   
  BEGIN CATCH   
  
   EXEC ('  
  
   DECLARE @SQL NVARCHAR(MAX)  
  
  
   DROP TABLE IF EXISTS #' + @TABLE_NAME + ';  
   
   SELECT TOP 1   
       *   
     INTO #' + @TABLE_NAME + '      
     FROM [BALCAO].[LOJA].[dbo].[' + @TABLE_NAME + ']  
    WHERE 1 = 2  
  
     
   IF EXISTS ( SELECT TOP 1 1 FROM sys.objects WHERE object_id = OBJECT_ID(N''[dbo].[' + @TABLE_NAME + ']'') AND type IN (N''U'') )  
    DROP TABLE [dbo].[' + @TABLE_NAME + '];  
  
  
   SELECT @SQL = dbo.FN_TABLE_STRUCTURE(''SELECT * FROM #' + @TABLE_NAME + ''', ''' +  @TABLE_NAME + ''')  
   EXEC ( @SQL )   
  
    ')  
  
  END CATCH   
  
  
  SET @INDEX_WHILE = ( SELECT MIN(ID) FROM TABELA_SYNC_BALCAO WHERE ID > @INDEX_WHILE )  
  
END  
  
END