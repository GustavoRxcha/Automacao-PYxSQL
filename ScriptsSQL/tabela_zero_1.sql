  
CREATE FUNCTION fn_table_structure_pdv   
(  
 @input_sql  AS NVARCHAR(4000)  
  , @table_name AS NVARCHAR(128) = NULL  
)  
RETURNS NVARCHAR(4000)  
AS  
BEGIN  
  
 DECLARE @sql     NVARCHAR(4000)  
 DECLARE @name     NVARCHAR(128)  
 DECLARE @is_nullable   BIT   
 DECLARE @system_type_name NVARCHAR(128)  
 DECLARE @collation_name   NVARCHAR(128)  
 DECLARE @new_line    NVARCHAR(2) = CHAR(13) + CHAR(10) -- # CRLF  
  
  
 DECLARE cur_table CURSOR LOCAL FAST_FORWARD  
 FOR  
     
  SELECT name   
    , is_nullable   
    , system_type_name   
    , collation_name  
    FROM sys.dm_exec_describe_first_result_set(@input_sql, NULL, NULL)  
   WHERE is_hidden = 0  
   ORDER   
      BY column_ordinal ASC   
  
 OPEN cur_table  
  
 FETCH NEXT FROM cur_table INTO @name, @is_nullable, @system_type_name, @collation_name  
  
  
 SET @sql = 'CREATE TABLE [' + ISNULL(@table_name, 'TABLE_NAME') + '] (' + @new_line  
  
  
 WHILE @@FETCH_STATUS = 0  
 BEGIN   
  
  SET @sql += @new_line + '[' + @name + ']' + ' ' + @system_type_name  
            + CASE WHEN @collation_name IS NOT NULL THEN '  COLLATE ' + @collation_name + ' '  
                   ELSE '' END  
               + CASE WHEN @is_nullable   = 0    THEN ' NOT NULL '  
                   ELSE '' END   
         + ','  
  
  
  FETCH NEXT FROM cur_table INTO @name, @is_nullable, @system_type_name, @collation_name  
  
 END   
  
  
 SET @sql = LEFT(@sql, LEN(@sql) - 1) + @new_line + ')'  
  
  
 CLOSE    cur_table  
 DEALLOCATE cur_table  
  
  
 RETURN @sql  
  
END