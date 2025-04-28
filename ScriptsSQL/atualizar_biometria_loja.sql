---ATUALIZAR BIOMETRIA (SERVIDOR)


use LOJA

DECLARE @MATRICULA VARCHAR(MAX) = ? --- Insira a matrícula do colaborador.
	   ,@COMANDO   NVARCHAR(MAX)
	   ,@LOJA	   VARCHAR(3)			

IF LEN(@MATRICULA) <> 5
BEGIN
	RAISERROR('O valor da variável ''@matricula'' não pode ser diferente de cinco caracteres. Insira um número válido.', 16, 1) WITH NOWAIT
END
ELSE BEGIN
	IF ISNUMERIC(@MATRICULA) = 1 AND
				 @MATRICULA <> ''
	BEGIN
		SET @MATRICULA = CONVERT(NUMERIC, @MATRICULA)
	END
	ELSE BEGIN
		RAISERROR('O valor da variável ''@matricula'' não pode ser uma string. Insira um número válido.', 16, 1) 
	END
END

BEGIN TRY
	IF EXISTS (SELECT * FROM OPERADORES WHERE OPERADOR = @MATRICULA)
	   DELETE FROM OPERADORES WHERE OPERADOR = @MATRICULA

	IF EXISTS (SELECT * FROM BIOMETRIAS WHERE VENDEDOR = @MATRICULA)
	   DELETE FROM BIOMETRIAS WHERE VENDEDOR = @MATRICULA

	SELECT @LOJA = EMPRESA FROM PARAMETROS

	SET @COMANDO = 'SELECT A.VENDEDOR																				 AS OPERADOR               
						  ,A.NOME																					 AS NOME      
						  ,IIF(A.EXIGIR_BIOMETRIA = ''N'', DBO.adm_Base64Encode(HASHBYTES(''SHA1'', B.SENHA)), NULL) AS SENHA               
						  ,A.DESCONTO_MAXIMO_PMC																     AS DESCONTO_MAXIMO               
						  ,B.VENDA																				     AS VENDA                
						  ,B.ABERTURA_CAIXA																		     AS ABERTURA_CAIXA                 
						  ,B.FECHAMENTO_CAIXA																	     AS FECHAMENTO_CAIXA                
						  ,B.CANCELAMENTO_ITEM																	     AS CANCELAMENTO_ITEM                 
						  ,B.CANCELAMENTO_CUPOM																	     AS CANCELAMENTO_CUPOM                
						  ,B.LEITURA_X																			     AS LEITURA_X                 
						  ,B.REDUCAO_Z																			     AS REDUCAO_Z                 
						  ,B.FUNCOES																			     AS FUNCOES                
						  ,B.SANGRIA_CAIXA																		     AS SANGRIA_CAIXA                 
						  ,B.SUPRIMENTO_CAIXA																	     AS SUPRIMENTO_CAIXA                 
						  ,A.SUPERVISOR																			     AS SUPERVISOR                 
						  ,0																					     AS DESCONTO_TOTAL_BALCAO               
						  ,0																					     AS DESCONTO_PDV                 
						  ,GETDATE()																			     AS DATA_HORA                 
						  ,B.USUARIO_FP																			     AS USUARIO_FP                
						  ,B.SENHA_FP																			     AS SENHA_FP                
						  ,A.CARGO_DESCONTO																		     AS CARGO_DESCONTO                
						  ,NULL																					     AS CANCELAMENTO_CUPOM_ANDAMENTO      
						  ,A.REIMPRESSAO_RELATORIO_GERENCIAL													     AS REIMPRESSAO_RELATORIO_GERENCIAL  
						  ,B.MAX_ABERTURA_CAIXA																	     AS MAX_ABERTURA_CAIXA  
						  ,B.MAX_MULTIPLICADOR_PRODUTO															     AS MAX_MULTIPLICADOR_PRODUTO   
					  FROM VENDEDORES AS A WITH (NOLOCK)                
					  JOIN OPERADORES AS B WITH (NOLOCK) ON B.VENDEDOR = A.VENDEDOR                
					 WHERE A.CADASTRO_ATIVO = ''S''     
					   AND A.PERFIL = ''N''  
					   AND B.VENDEDOR NOT IN (9, 21)
					-- AND A.EMPRESA_USUARIA = ''' + @LOJA + '''
					   AND A.VENDEDOR = ''' + CONVERT(VARCHAR, @MATRICULA) + ''''

	INSERT INTO  OPERADORES(OPERADOR          
						   ,NOME      
						   ,SENHA     
						   ,DESCONTO_MAXIMO                 
						   ,VENDA         
						   ,ABERTURA_CAIXA            
						   ,FECHAMENTO_CAIXA          
						   ,CANCELAMENTO_ITEM           
						   ,CANCELAMENTO_CUPOM                     
						   ,LEITURA_X           
						   ,REDUCAO_Z           
						   ,FUNCOES         
						   ,SANGRIA_CAIXA           
						   ,SUPRIMENTO_CAIXA      
						   ,SUPERVISOR      
						   ,DESCONTO_TOTAL_BALCAO                      
						   ,DESCONTO_PDV       
						   ,DATA_HORA        
						   ,USUARIO_FP         
						   ,SENHA_FP         
						   ,CARGO_DESCONTO     
						   ,CANCELAMENTO_CUPOM_ANDAMENTO  
						   ,REIMPRESSAO_RELATORIO_GERENCIAL
						   ,MAX_ABERTURA_CAIXA
						   ,MAX_MULTIPLICADOR_PRODUTO) 

	EXEC(@COMANDO) AT RETAGUARDA 

	USE [PBS_LOCAL_DADOS]

	IF EXISTS (SELECT * FROM sys.all_views WHERE name = 'BIOMETRIAS_EXPORTACAO_LOJAS_LOCAL'    AND type = 'V') AND
	   EXISTS (SELECT * FROM sys.all_views WHERE name = 'VW_BIOMETRIAS_EXPORTACAO_LOJAS_LOCAL' AND type = 'V')
	BEGIN
		USE [LOJA]

		SET @COMANDO = 'SELECT BIOMETRIA    
							  ,TIPO    
							  ,CODIGO    
							  ,STATUS    
							  ,NITGEN_ISDB    
							  ,VENDEDOR    
						  FROM [PBS_LOCAL].PBS_LOCAL_DADOS.DBO.BIOMETRIAS_EXPORTACAO_LOJAS_LOCAL WITH (NOLOCK)
						 WHERE VENDEDOR = ''' + CONVERT(VARCHAR, @MATRICULA) + ''''

		INSERT INTO  BIOMETRIAS(BIOMETRIA    
							   ,TIPO    
							   ,CODIGO    
							   ,STATUS    
							   ,NITGEN_ISDB    
							   ,VENDEDOR) 

		EXEC(@COMANDO) AT PBS_LOCAL
	END
	ELSE BEGIN
		RAISERROR('Não foi possível encontrar o servidor vinculado BIOMETRIAS_EXPORTACAO_LOJAS_LOCAL, crie o recurso de comunicação.', 15, 1)
	END

	SELECT OPERADOR
		  ,NOME
		  ,VENDA
		  ,ABERTURA_CAIXA
		  ,FECHAMENTO_CAIXA
		  ,CANCELAMENTO_ITEM
		  ,CANCELAMENTO_CUPOM
		  ,LEITURA_X
		  ,REDUCAO_Z
		  ,FUNCOES
		  ,SANGRIA_CAIXA
		  ,SUPRIMENTO_CAIXA
		  ,SUPERVISOR
	  FROM OPERADORES 
	 WHERE OPERADOR = @MATRICULA

	SELECT BIOMETRIA
		  ,TIPO
		  ,CODIGO
		  ,STATUS
		  ,VENDEDOR
	  FROM BIOMETRIAS
	 WHERE VENDEDOR = @MATRICULA
END TRY
BEGIN CATCH
	IF NOT EXISTS (SELECT * FROM RETAGUARDA.PBS_NISSEI_DADOS.DBO.VENDEDORES WHERE VENDEDOR = @MATRICULA)
	BEGIN
		RAISERROR('Nenhum registro foi encontrado pelo formulário de VENDEDORES. A filial deve contatar o setor do Departamento Pessoal.', 15, 1)
	END
	ELSE BEGIN 
		DECLARE @ENTIDADE NUMERIC = (SELECT ENTIDADE FROM RETAGUARDA.PBS_NISSEI_DADOS.DBO.VENDEDORES WHERE VENDEDOR = @MATRICULA)

		IF NOT EXISTS (SELECT * FROM PBS_LOCAL.PBS_LOCAL_DADOS.DBO.BIOMETRIAS WHERE CODIGO = @entidade)
		BEGIN
			RAISERROR('Não existe dado de biometria pelo banco PBS_LOCAL_DADOS. Execute a rotina de ''syncLocal''.', 15, 1)
		END
		ELSE BEGIN
			IF NOT EXISTS (SELECT * FROM RETAGUARDA.PBS_NISSEI_DADOS.DBO.BIOMETRIAS WHERE CODIGO = @ENTIDADE)
			BEGIN
				RAISERROR('Biometria não cadastrada! Realize o registro.', 15, 1)
			END
			ELSE BEGIN
				RAISERROR('Erro de atualização requer análise adicional para determinar a causa raiz.', 15, 1)
			END 
		END
	END
END CATCH