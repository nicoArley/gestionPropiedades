# import pyodbc



# SERVER = 'localhost'
# DATABASE = 'Proyecto1' #aqui va el nombre
# USERNAME = 'NewSA'
# PASSWORD = 'mypassword'

# connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'

# # import pyodbc
# cnxn = pyodbc.connect(connectionString) 


# #Para insertar
# statement1 = "INSERT INTO Usuario (cedula, nombre, primerApellido, segundoApellido, telefono, correo) VALUES (38282821, 'kiki', 'Arley', 'Cedeno', 11111, 'kiki@gmail.com')"
# cursor = cnxn.cursor()
# cursor.execute(statement1) 

# #Para obtener
# cursor = cnxn.cursor()	
# statement2 = "SELECT * FROM Usuario"
# cursor.execute(statement2) 

# # aqui lo atrapa en una variable 
# row = cursor.fetchone() 

# while row:
#     print (row) 
#     row = cursor.fetchone()

# cnxn.commit()
# cursor.close()

def login():
    printer = "Enter username: "
    print(printer)
#   username = input()
#   cursor = cnxn.cursor()
#   checkUsername = cursor.execute('SELECT username FROM users WHERE username = %(username)s', { 'username' : username })
#   if checkUsername != 0:
#     print('Username is not exist')
#   else:
#     print('Logged In!')



