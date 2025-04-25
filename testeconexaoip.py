import pyodbc

def conectar_banco(filial):

        filial = int(filial)

        if 0 <= filial <= 199 or filial == 241:
            ip = f"10.16.{filial}.24"

        elif 200 <= filial <= 240:
            ultimos_digitos = filial % 100
            ip = f"10.17.{ultimos_digitos}.24"
        elif 242 <= filial <= 299:
            ultimos_digitos = filial % 100
            ip = f"10.17.{ultimos_digitos}.24"

        elif 300 <= filial <= 399:
            ultimos_digitos = filial % 100
            ip = f"10.17.1{ultimos_digitos}.24"

        elif 400 <= filial <= 499:
            ultimos_digitos = filial % 100
            ip = f"10.18.{ultimos_digitos}.24"

        else:
            return "Número de filial inválido."
        
        return ip

filial = input("Digite o número da filial: ")
ip = conectar_banco(filial)
print(f"\n {ip} \n")

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


