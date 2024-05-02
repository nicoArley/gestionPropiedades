import pyodbc
from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

cedulaUsuario = ''
rolUsuario = ''
periodo = ''

#-----------------------------------------BACKEND-------------------------------------------------#

def conectarBD():
    SERVER = 'localhost'
    DATABASE = 'Proyecto1'
    USERNAME = 'NewSA'
    PASSWORD = 'mypassword'

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'
    cnxn = pyodbc.connect(connectionString) 
    return cnxn

def desconectarBD(cnxn, cursor):
    cnxn.commit()
    cursor.close()

def ingresarSistema(rol, cedula):
    global cedulaUsuario, rolUsuario

    if(existeUsuario(cedula) == True) : 
        if(rol == "Propietario"):
            if(existePropietario(cedula) == True):
                rolUsuario = rol
                cedulaUsuario = cedula
                return True
            else: 
                return False
        else:
            if(existeInquilinoBD(cedula) == True):
                rolUsuario = rol
                cedulaUsuario = cedula
                return True
            else: 
                return False  
    else: 
        return False

#Esta es la funcion que llama la base de datos luego de atrapar los datos de la interfaz (en el login al crear un usurio para ingresar )
#y se los pasa con esas variables

def crearPropietario(cedula, nombre, apellido1, apellido2, telefono,correo): 
    if(existeUsuario(cedula) == False):
        nuevoUsuario = (cedula, nombre, apellido1, apellido2, telefono,correo)
        try: 
            insertarUsuario(nuevoUsuario)
            insertarPropietario(cedula)
            return True
        except: 
            return False
    elif(existePropietario(cedula) == False):
        try: 
            nuevoPropietario = (cedula)
            insertarPropietario(nuevoPropietario)
            return True
        except: 
            return False
    else: 
        return False
    
def existeUsuario(cedula):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Usuario WHERE cedula=?', (cedula))
    checkUsername = cursor.fetchone()
    if (checkUsername == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#valida que los datos tengan las caracteristicas necesarias
def existePropietario(cedula):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Propietario WHERE cedula=?', (cedula))
    checkUsername = cursor.fetchone()
    if (checkUsername == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

# usa el statement de insercion y execute para guardar el cambio en la base de datos
def insertarPropietario(cedulaPropietario):
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement_insertar_usuario = 'INSERT INTO Propietario (cedula) VALUES (?);'
        cursor.execute(statement_insertar_usuario, cedulaPropietario) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

#usa el statement de insercion y execute para guardar el cambio en la base de datos

def insertarUsuario(nuevoUsuario): 
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement_insertar_usuario = 'INSERT INTO Usuario (cedula, nombre, apellido1, apellido2, telefono, correo) VALUES (?, ?, ?, ?, ?, ?);'
        cursor.execute(statement_insertar_usuario, nuevoUsuario) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

def existeInquilinoBD(cedulaInquilino):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Inquilino WHERE cedula=?', (cedulaInquilino))
    checkInquilino = cursor.fetchone()
    if (checkInquilino == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True
    
#CREAR MODULO PROPIEDAD (Propietario)

#Esta es la funcion que llama la base de datos luego de atrapar los datos de la interfaz (Al darle la opcion de crear propiedad)
#y se los pasa con esas variables

def crearPropiedad(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastosAdicionales):
    if(existePropiedad(idPropiedad) == False) :
        nuevaPropiedad = (idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, cedulaUsuario, descripcion, estadoActual, precioAlquiler, gastosAdicionales)
        try: 
            insertarPropiedad(nuevaPropiedad)
            return True
        except: 
            return False
    else: 
        return False

#valida que los datos tengan las caracteristicas necesarias
def existePropiedad(idPropiedad):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Propiedad WHERE idPropiedad=?', (idPropiedad))
    checkPropiedad = cursor.fetchone()
    if (checkPropiedad == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True
    
def existePropiedadPropietario(idPropiedad):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Propiedad WHERE idPropiedad=? AND cedulaPropietario=?', idPropiedad, cedulaUsuario)
    checkPropiedad = cursor.fetchone()
    if (checkPropiedad == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

# usa el statement de insercion y execute para guardar el cambio en la base de datos
def insertarPropiedad(nuevaPropiedad):
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO Propiedad (idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, cedulaPropietario, descripcion, estadoActual, precioAlquiler, gastosAdicionales) VALUES (?,?,?,?,?,?,?,?,?,?)'
        cursor.execute(statement, nuevaPropiedad) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False


#VISUALIZAR MODULO PROPIEDAD (Propietario)

# Esta funcion es la que se llama luego de presionar el boton de visualizar

# PENDIENTE ver si existe en la base de datos 
def visualizarPropiedades():
    global cedulaUsuario
    try:
        tablaPropiedades = obtenerPropiedades()
        return tablaPropiedades
    except: 
        return []

#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
# cuando hay que pasarle al sistema las propiedades disponibles para ese propietario
def obtenerPropiedades():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT idPropiedad, tipoPropiedad, tamanoMetros, descripcion, precioAlquiler, direccion, numeroHabitaciones, estado, gastosAdicionales FROM Propiedad JOIN EstadosPermitidos ON estadoActual = idEstado WHERE cedulaPropietario = ?;'
    cursor.execute(statement, cedulaUsuario) 
    listaPropiedades = []
    listaPropiedades = cursor.fetchall()
    desconectarBD(cnxn, cursor)
    return listaPropiedades

#EDITAR MODULO PROPIEDAD(revisar si es asi) (Propietario)

def obtenerPropiedad(idPropiedad): 
    if(existePropiedad(idPropiedad)):
        try:
            cnxn = conectarBD()
            cursor = cnxn.cursor()
            statement = 'SELECT idPropiedad, tipoPropiedad, tamanoMetros, descripcion, precioAlquiler, direccion, numeroHabitaciones, estadoActual, gastosAdicionales FROM Propiedad WHERE idPropiedad = ?;'
            cursor.execute(statement, idPropiedad) 
            listaPropiedades = []
            listaPropiedades = cursor.fetchall()
            desconectarBD(cnxn, cursor)
            return listaPropiedades
        except: 
            return []
    else:
        return []

def editarPropiedad(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler,gastosAdicionales):
    try: 
        cambiarPropiedadBD(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastosAdicionales)
        return True
    except: 
        return False      

#Acá se hace la accion en la BD con el execute, hace el update   
def cambiarPropiedadBD(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros,descripcion, estadoActual, precioAlquiler,gastosAdicionales):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'UPDATE Propiedad SET direccion = ?, tipoPropiedad= ?, numeroHabitaciones = ?, tamanoMetros = ?, descripcion = ?, estadoActual = ?, precioAlquiler = ?, gastosAdicionales = ? WHERE cedulaPropietario = ? AND idPropiedad = ? ;'
        cursor.execute(statement, direccion,tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastosAdicionales, cedulaUsuario, idPropiedad) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False


#MODULO INQUILINOS (Propietario)
#CREAR MODULO INQUILINOS (Propietario)

#Esta es la funcion que llama la base de datos luego de atrapar los datos de la interfaz (Al darle la opcion de crear inquilino)
#y se los pasa con esas variables
#El idPropiedad debe ser mostrado los disponibles, preguntar como hacerlo si es necesario una tabla intermedia

def crearInquilino(nombre, primerApellido, segundoApellido, cedula, telefono, correo,idPropiedad, fechaInicio, fechaFinal): 
    if(existePropiedadPropietario(idPropiedad) == True and propiedadDisponible(idPropiedad, fechaInicio, fechaFinal) == True):
        if(existeUsuario(cedula) == False):
            if (existeInquilinoBD(cedula) == False) :
                nuevoUsuario = (cedula, nombre, primerApellido, segundoApellido, telefono,correo)
                try: 
                    insertarUsuario(nuevoUsuario)
                    insertarInquilino(cedula)
                    nuevoAlquiler = (cedula,idPropiedad,fechaInicio, fechaFinal)
                    insertarAlquiler(nuevoAlquiler)
                    actualizarPropiedadAlquiler(idPropiedad)
                    return True
                except: 
                    return False
            else: 
                return False
        elif(existeInquilinoBD(cedula) == False):
            try: 
                insertarInquilino(cedula)
                nuevoAlquiler = (cedula,idPropiedad,fechaInicio, fechaFinal)
                insertarAlquiler(nuevoAlquiler)
                actualizarPropiedadAlquiler(idPropiedad)
                return True
            except: 
                return False
        elif(existeUsuario(cedula) == True and existeInquilinoBD(cedula) == True):
            try: 
                nuevoAlquiler = (cedula,idPropiedad,fechaInicio, fechaFinal)
                insertarAlquiler(nuevoAlquiler)
                actualizarPropiedadAlquiler(idPropiedad)
                return True
            except: 
                return False
        else: 
            return False
    else: 
        False

#Ver que no exista ningun otro inquilino con esa cédula
def existeInquilinoBD(cedulaInquilino):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Inquilino WHERE cedula=?', (cedulaInquilino))
    checkInquilino = cursor.fetchone()
    if (checkInquilino == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

# usa el statement de insercion y execute para guardar el cambio en la base de datos
def insertarInquilino(cedulaInquilino):
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO Inquilino (cedula) VALUES (?)'
        cursor.execute(statement, cedulaInquilino) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

def propiedadDisponible(idPropiedad, fechaInicio, fechaFinal): 
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'SELECT * FROM Alquiler WHERE (idPropiedad = ?) AND ((? BETWEEN fechaInicio AND fechaFin) OR (? BETWEEN fechaInicio AND fechaFin))'
        cursor.execute(statement, idPropiedad, fechaInicio, fechaFinal ) 
        checkInquilino = cursor.fetchone()
        if (checkInquilino == None):
            desconectarBD(cnxn, cursor)
            return True
        else:
            desconectarBD(cnxn, cursor)
            return False
    except: 
        desconectarBD(cnxn, cursor)
        return False

def insertarAlquiler(nuevoAlquiler):
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO Alquiler (cedulaInquilino,idPropiedad,fechaInicio,fechaFin) VALUES (?,?,?,?)'
        cursor.execute(statement, nuevoAlquiler) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

def actualizarPropiedadAlquiler(idPropiedad):
    global cursor
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'UPDATE Propiedad SET estadoActual = 2 WHERE idPropiedad = ?;'
        cursor.execute(statement, idPropiedad) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

#VISUALIZAR MODULO INQUILINOS (Propietario)

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarInquilinos():
    if(existeInquilinosPropietario()):
        try:
            tablaInquilinos = obtenerInquilinos()
            #enviar datos a la interfaz
            return tablaInquilinos
        except: 
            return []
    else:
        return []


#Valida que existan inquilinos en sus propiedades con la cedula del propietario 
#cambiar el statement
def existeInquilinosPropietario():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT Inquilino.cedula, Usuario.nombre, Usuario.apellido1, Usuario.apellido2, Usuario.telefono, Usuario.correo, Propiedad.idPropiedad, Alquiler.fechaInicio, Alquiler.fechaFin FROM Inquilino  JOIN Usuario ON Inquilino.cedula = Usuario.cedula JOIN Alquiler ON Alquiler.cedulaInquilino = Inquilino.cedula JOIN Propiedad ON Alquiler.idPropiedad = Propiedad.idPropiedad WHERE Propiedad.cedulaPropietario = ?'
    cursor.execute(statement, (cedulaUsuario))
    checkInquilinoP = cursor.fetchone()
    if (checkInquilinoP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True


#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
# cuando hay que pasarle al sistema las propiedades disponibles para ese propietario
def obtenerInquilinos():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT Inquilino.cedula, Usuario.nombre, Usuario.apellido1, Usuario.apellido2, Usuario.telefono, Usuario.correo, Propiedad.idPropiedad, Alquiler.fechaInicio, Alquiler.fechaFin FROM Inquilino  JOIN Usuario ON Inquilino.cedula = Usuario.cedula JOIN Alquiler ON Alquiler.cedulaInquilino = Inquilino.cedula JOIN Propiedad ON Alquiler.idPropiedad = Propiedad.idPropiedad WHERE Propiedad.cedulaPropietario = ?'
    cursor.execute(statement, cedulaUsuario) 
    listaInquilinos = []
    listaInquilinos = cursor.fetchall()
    for inquilino in listaInquilinos:
        inquilino[7] = inquilino[7].strftime("%Y/%m/%d")
        inquilino[8] = inquilino[8].strftime("%Y/%m/%d")
    desconectarBD(cnxn, cursor)
    return listaInquilinos

#EDITAR MODULO PROPIEDAD(revisar si es asi) (Propietario)

def obtenerInquilino(cedulaInquilino): 
    if(existeInquilinoBD(cedulaInquilino)):
        try:
            cnxn = conectarBD()
            cursor = cnxn.cursor()
            statement = 'SELECT nombre, apellido1, apellido2, telefono, correo FROM Usuario WHERE cedula = ?'
            cursor.execute(statement, cedulaInquilino) 
            listaPropiedades = []
            listaPropiedades = cursor.fetchall()
            desconectarBD(cnxn, cursor)
            return listaPropiedades
        except: 
            return []
    else:
        return []

def editarInquilino(cedulaInquilino,nombre, apellido1, apellido2, telefono, correo):
    try: 
        cambiarInquilino(cedulaInquilino,nombre, apellido1, apellido2, telefono, correo)
        return True
    except: 
        return False      

#Acá se hace la accion en la BD con el execute, hace el update   
def cambiarInquilino(cedulaInquilino,nombre, apellido1, apellido2, telefono, correo):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'UPDATE Usuario SET nombre = ?, apellido1= ?, apellido2 = ?, telefono = ?, correo = ? WHERE cedula = ?;'
        cursor.execute(statement,nombre, apellido1, apellido2, telefono, correo, cedulaInquilino) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

#MODULO MANTENIMIENTO (Propietario)

#MODULO MANTENIMIENTO VISUALIZAR SOLICITUDES (Propietario)

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarSolicitudesP():
    if(existeInquilinosPropietario()):
        if(existeSolicitudesPropietario()):
            try:
                tablaSolicitudes = obtenerSolicitudesP()
                
                #enviar datos a la interfaz
                return tablaSolicitudes
            except: 
                return []
        else: 
            return[]
    else: 
        return[]

#Valida que existan solicitudes en sus propiedades con la cedula del propietario 
def existeSolicitudesPropietario():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    
    statement = 'SELECT * FROM SolicitudMantenimiento JOIN Propiedad ON Propiedad.idPropiedad = SolicitudMantenimiento.idPropiedad WHERE cedulaPropietario = ?;'
    cursor.execute(statement, cedulaUsuario)
    checkSolicitudesP = cursor.fetchone()
    if (checkSolicitudesP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
def obtenerSolicitudesP():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT idSolicitud, Propiedad.idPropiedad, descripcionProblema, fechaSolicitud, estado, prioridad, nombre, primerApellido, segundoApellido, especialidad, telefono FROM SolicitudMantenimiento JOIN Propiedad ON SolicitudMantenimiento.idPropiedad = Propiedad.idPropiedad JOIN PrioridadesPermitidas ON SolicitudMantenimiento.idPrioridad = PrioridadesPermitidas.idPrioridad JOIN Proveedores ON SolicitudMantenimiento.idProveedor = Proveedores.idProveedor WHERE Propiedad.cedulaPropietario = ?'
    cursor.execute(statement, cedulaUsuario) 
    listaSolicitudes = []
    listaSolicitudes = cursor.fetchall()
    for solicitud in listaSolicitudes:
        solicitud[3] = solicitud[3].strftime("%Y/%m/%d")
    desconectarBD(cnxn, cursor)
    return listaSolicitudes


#MODULO MANTENIMIENTO ACTUALIZAR ESTADO SOLICITUD (Propietario)

def actualizarSolicitud(idSolicitud, estado):
    global cedulaUsuario
    if(existeSolicitudesPropietario()):
        if(existeSolicitud(idSolicitud)):
            try:
                #solicitud = obtenerSolicitud(idSolicitud)
                cambiarEstadoSolicitud(idSolicitud,estado)
                return True
            except: 
                return False 
        else: return False     
    else: return False 


#comprueba que el id si exista en la base de datos y que pertenezca a una propiedad del propietario
def existeSolicitud(idSolicitud):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM SolicitudMantenimiento WHERE idSolicitud=?', (idSolicitud))
    checkSolicitudesP = cursor.fetchone()
    if (checkSolicitudesP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#aqui
#Acá se hace la accion en la BD con el execute  
def cambiarEstadoSolicitud(idSolicitud, estado):

    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'UPDATE SolicitudMantenimiento SET estado = ? WHERE idSolicitud = ?'
        cursor.execute(statement, estado, idSolicitud) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False


#MODULO DE REPORTES (Propietario, inquilino (es el mismo))

def mostrarReporte(periodo):
    global cedulaUsuario, rolUsuario
    if(rolUsuario == "Propietario"):
        try:
            reportes = obtenerReportesPropietario(periodo)
            return reportes
        except:
            return []
    else: 
        try: 
            reportes = obtenerReportesInquilino(periodo)
            return reportes
        except: 
            return []

# Revisa en la base de datos  que la tabla de pagos existan inquilinos relacionados con las propiedades del propietario (esta consulta es anidada y feita) en el periodo especifico
def existenReportesPropietario(periodo):
    global cedulaUsuario 
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    fechaFinal = datetime.now()
    fechaInicial = definirFechaInicial(periodo)
    statement = 'SELECT * FROM Pagos JOIN Alquiler ON Pagos.cedulaInquilino = Alquiler.cedulaInquilino JOIN Propiedad ON Alquiler.idPropiedad = Propiedad.idPropiedad WHERE (Propiedad.cedulaPropietario = ?) AND (Pagos.fechaPago BETWEEN ? AND ?);'
    cursor.execute(statement, cedulaUsuario, fechaInicial, fechaFinal )

    checkReportesP = cursor.fetchone()
    if (checkReportesP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#obtiene solo los las cedulas de todos los inquilinos relacionados con una propiedad del propietario en login
def obtenerIdsInquilinos(cedulaPropietario):
    pass

# compara los inquilinos  tomados del metodo obtenerIdsInquilinos(cedulaPropietario) con los reportes existentes para mostrar solo los que cumplen,
# puede ser un select con un Where cedula IN (SELECT cedula ....)
# luego obtiene por medio de uan consulta a la en la base de datos las tuplas

def obtenerReportesPropietario(periodo):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()

    fechaFinal = datetime.now()
    fechaInicial = definirFechaInicial(periodo)
    statement = 'SELECT idPago, Alquiler.cedulaInquilino, Pagos.fechaPago, Pagos.monto, TiposPagoPermitidos.tipoPago, EstadosPagoPermitidos.estadoPago, Pagos.metodoPago FROM Pagos JOIN TiposPagoPermitidos ON Pagos.tipoPago = TiposPagoPermitidos.idTipoPago JOIN EstadosPagoPermitidos ON EstadosPagoPermitidos.idEstadoPago  = Pagos.estadoPago JOIN Alquiler ON Pagos.cedulaInquilino = Alquiler.cedulaInquilino JOIN Propiedad ON Alquiler.idPropiedad = Propiedad.idPropiedad  WHERE (Propiedad.cedulaPropietario = ?) AND (Pagos.fechaPago BETWEEN ? AND ?);'
    cursor.execute(statement, cedulaUsuario, fechaInicial, fechaFinal ) 
    listaReportes = []
    listaReportes = cursor.fetchall()
    for reporte in listaReportes:
        reporte[2] = reporte[2].strftime("%Y/%m/%d")
    desconectarBD(cnxn, cursor)
    return listaReportes


def definirFechaInicial(periodo):
    fechaActual = datetime.now()
    if (periodo == 'Trimestral'):
        # Suma 3 meses a la fecha actual para obtener la fecha final del trimestre
        fechaInicial = fechaActual - timedelta(days=90)
        return fechaInicial
    elif (periodo == 'Mensual'):
        # Suma 1 mes a la fecha actual para obtener la fecha final del mes siguiente
        fechaInicial = fechaActual - timedelta(days=30)
        return fechaInicial
    else:
        # Resta 1 año a la fecha actual para obtener la fecha final del año siguiente
        fechaInicial = fechaActual - timedelta(days=365)
        return fechaInicial

# Cuando es un inquilino revisa en la base de datos que el inquilino haya registrado reportes en el periodo solicitado
def existeReportesInquilino(cedulaUsuario,periodo):
    #global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    fechaFinal = datetime.now()
    fechaInicial = definirFechaInicial(periodo)
    statement = 'SELECT * FROM Pagos WHERE (Pagos.cedulaInquilino = ?) AND (Pagos.fechaPago BETWEEN ? AND ?);'
    cursor.execute(statement, cedulaUsuario, fechaInicial, fechaFinal )
    checkReportesI = cursor.fetchone()
    if (checkReportesI == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#Pendiente
# Obtiene los reportes del inquilino en el perido usa la cedula usuario
def obtenerReportesInquilino(periodo):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT idPago, Alquiler.cedulaInquilino, Pagos.fechaPago, Pagos.monto, TiposPagoPermitidos.tipoPago, EstadosPagoPermitidos.estadoPago, Pagos.metodoPago FROM Pagos JOIN TiposPagoPermitidos ON Pagos.tipoPago = TiposPagoPermitidos.idTipoPago JOIN EstadosPagoPermitidos ON EstadosPagoPermitidos.idEstadoPago  = Pagos.estadoPago JOIN Alquiler ON Pagos.cedulaInquilino = Alquiler.cedulaInquilino JOIN Propiedad ON Alquiler.idPropiedad = Propiedad.idPropiedad  WHERE (Pagos.cedulaInquilino = ?) AND (Pagos.fechaPago BETWEEN ? AND ?);'
    fechaFinal = datetime.now()
    fechaInicial = definirFechaInicial(periodo)
    cursor.execute(statement, cedulaUsuario, fechaInicial, fechaFinal ) 
    listaReportes = []
    listaReportes = cursor.fetchall()
    for reporte in listaReportes:
        reporte[2] = reporte[2].strftime("%Y/%m/%d")
    desconectarBD(cnxn, cursor)
    return listaReportes

#MODULO COMUNICACION (Propietario, inquilino (es el mismo))

#ENVIAR MODULO COMUNICACION (Propietario, inquilino (es el mismo))
#Esta es la funcion que la interfaz llama luego de validar los datos atrapados y asignarlos a variables 
def enviarMensaje(cedulaReceptor,contenido):
    global cedulaUsuario
    if(existeUsuario(cedulaReceptor)): 
        try:
            estado = 'No Leido'
            fechaMensaje = datetime.now().date()
            horaMensaje = datetime.now().time()
            valores = (cedulaUsuario,cedulaReceptor,fechaMensaje,horaMensaje,contenido, estado)
            agregarComunicacion(valores)
            return True
        except:
            return False
    else: 
        return False

#Esta funcion utiliza el stament y manda el insert a la base de datos
def agregarComunicacion(valores): 
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO Comunicacion (cedulaEmisor, cedulaReceptor, fechaMensaje, horaMensaje, contenido, estado) VALUES (?,?,?,?,?,?)'
        cursor.execute(statement, valores) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False
    
def marcarMsjLeidos(): 
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'UPDATE Comunicacion SET estado = \'Leido\' WHERE cedulaReceptor = ?'
        cursor.execute(statement, cedulaUsuario) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

#RECIBIDOS MODULO COMUNICACION (Propietario, inquilino (es el mismo))

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarMsjRecibidos():
    global cedulaUsuario
    try:
        tablaMsjRecibidos = obtenerMsjRecibidos()   
        marcarMsjLeidos()
        #enviar datos a la interfaz
        return tablaMsjRecibidos
    except: 
        return []

#Esta funcion utiliza el stament y manda el select con execute a la base de datos
def obtenerMsjRecibidos(): 
    global cedulaUsuario
    try:
        cnxn = conectarBD()
        cursor = cnxn.cursor()
        statement = 'SELECT cedulaEmisor, fechaMensaje, horaMensaje, contenido FROM Comunicacion WHERE cedulaReceptor = ?'
        cursor.execute(statement, cedulaUsuario) 
        listaMensajes = []
        listaMensajes = cursor.fetchall()
        for mensaje in listaMensajes:
            mensaje[1] = mensaje[1].strftime("%Y/%m/%d")
        desconectarBD(cnxn, cursor)
        return listaMensajes
    except: 
        return []


#ENVIADOs MODULO COMUNICACION (Propietario, inquilino (es el mismo))

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarMsjEnviados():
    global cedulaUsuario
    try:
        tablaMsjEnviados = obtenerMsjEnviados()   
        #enviar datos a la interfaz
        return tablaMsjEnviados
    except: 
        return []

#Esta funcion utiliza el stament y manda el select con execute a la base de datos
def obtenerMsjEnviados():
    global cedulaUsuario
    try:
        cnxn = conectarBD()
        cursor = cnxn.cursor()
        statement = 'SELECT cedulaReceptor, fechaMensaje, horaMensaje, contenido, estado FROM Comunicacion WHERE cedulaEmisor = ?'
        cursor.execute(statement, cedulaUsuario) 
        listaMensajes = []
        listaMensajes = cursor.fetchall()
        for mensaje in listaMensajes:
            mensaje[1] = mensaje[1].strftime("%Y/%m/%d")
        desconectarBD(cnxn, cursor)
        return listaMensajes
    except: 
        return []

#INQUILINOS MODULO PAGOS
 
#INQUILINOS MODULO PAGOS REGISTRAR PAGOS 

def registrarPago(idPago, monto, tipoPago, estadoPago, metodoPago): 
    global cedulaUsuario
    if(existePagoId(idPago) == False):
        fechaPago = datetime.now()
        nuevoPago = (idPago,cedulaUsuario, fechaPago, monto, tipoPago, estadoPago, metodoPago)
        try: 
            insertarPago(nuevoPago)
            return True
        except: 
            return False
    else: 
        return False

#--Terminada
#valida que no exista ya un pago con ese id
def existePagoId(idPago):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Pagos WHERE idPago=?', (idPago))
    checkPago = cursor.fetchone()
    if (checkPago == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

# usa el statement de insercion y execute para guardar el cambio en la base de datos
def insertarPago(nuevoPago):
    global cursor,cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO Pagos (idPago,cedulaInquilino,fechaPago,monto,tipoPago,estadoPago, metodoPago) VALUES (?,?,?,?,?,?,?)'
        cursor.execute(statement, nuevoPago,) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False



# INQUILINOS MODULO MANTENIMIENTO REGISTRAR

def registrarMantenimiento(idSolicitud,idPropiedad,descripcionProblema,idProveedor,idPrioridad):
    if(existeSolicitud(idSolicitud) == False):
        if(existeAlquiler(idPropiedad)):
            try: 
                fechaSolicitud = datetime.now()
                estado = 1
                mantenimiento = (idSolicitud, idPropiedad, descripcionProblema, idProveedor, fechaSolicitud, estado, idPrioridad)
                return insertarMantenimiento(mantenimiento)
            except: 
                return False
        else: 
            return False
    else: 
        return False

#comprueba que el id si exista en la base de datos y que pertenezca a una propiedad del propietario
def existeSolicitud(idSolicitud):
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM SolicitudMantenimiento WHERE idSolicitud=?', (idSolicitud))
    checkSolicitudesP = cursor.fetchone()
    if (checkSolicitudesP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#Comprueba que el usuario se refiera a una propiedad que alquila, no puede solicitar mantenimiento para una propiedad que no alquile
def existeAlquiler(idPropiedad):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Alquiler WHERE idPropiedad=? AND cedulaInquilino = ?', idPropiedad, cedulaUsuario)
    checkAlquiler = cursor.fetchone()
    if (checkAlquiler == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True


#usa el statement de insercion y execute para guardar el cambio en la base de datos
def insertarMantenimiento(mantenimiento):
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    try:
        statement = 'INSERT INTO SolicitudMantenimiento (idSolicitud, idPropiedad, descripcionProblema, idProveedor, fechaSolicitud, estado, idPrioridad) VALUES (?,?,?,?,?,?,?)'
        cursor.execute(statement, mantenimiento)
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

#-----------------------------------------FRONTEND-------------------------------------------------#

#-----------------------------------------LOGIN-------------------------------------------------#
#carga la ventana de inicio y llama a las otras funciones la mostrar la ventana correspondiente

#-----Esta funcion es pruba para validar los campos, despues se debe cambiar por la de abajo
class VentanaInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('InterfazGrafica/ventanaLogin.ui', self)
        self.btnIngresar.clicked.connect(self.validar_ingreso)
        self.btnRegistrar.clicked.connect(self.abrir_ventana_Registro)
        self.txtCedula.textChanged.connect(self.validar_cedula)  # Conectar la señal textChanged a la función validar_cedula

    def abrir_ventana_Registro(self):
        ventana_registro = VentanaRegistro(self)
        ventana_registro.show()

    def validar_cedula(self):
        # Obtener el texto actual del campo txtCedula
        texto = self.txtCedula.text()
        # Verificar si el texto está vacío
        if not texto:
            # Mostrar un mensaje de error
            QMessageBox.critical(self, "Error", "El campo Cédula no puede estar vacío")
            return
        # Verificar si el texto contiene algún carácter que no sea un número
        if not texto.isnumeric():
            # Eliminar el último carácter ingresado si no es un número
            self.txtCedula.setText(texto[:-1])

    def validar_ingreso(self):
        # Obtener el texto actual del campo txtCedula
        texto = self.txtCedula.text()
        # Verificar si el campo está vacío
        if not texto:
            # Mostrar un mensaje de error
            QMessageBox.critical(self, "Error", "El campo Cédula no puede estar vacío")
            return
        # Realizar otras validaciones y acciones necesarias para el ingreso
        if self.rbInquilino.isChecked():
            if ingresarSistema("Inquilino", texto):
                ventana_inquilinos = VentanaInicioInquilinos(self)
                ventana_inquilinos.show()
            else:
                QMessageBox.critical(self, "Error", "El inquilino no existe")
        elif self.rbPropietario.isChecked():
            if ingresarSistema("Propietario", texto):
                ventana_propietarios = VentanaInicioPropietarios(self)
                ventana_propietarios.show()
            else:
                QMessageBox.critical(self, "Error", "El propietario no existe")
        else:
            QMessageBox.critical(self, "Error", "Debe seleccionar si es Inquilino o Propietario")

#-------------------------------------REGISTRAR PROPIETARIO NUEVO-------------------------------------#
#llama la ventanaRegistrarUsuari (cuando el propietario no esta registrado para acceder)
class VentanaRegistro(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarUsuario.ui', self)
        self.txtCedula.textChanged.connect(self.validar_queSeaNum)
        self.txtTelefono.textChanged.connect(self.validar_queSeaNum)
        self.btnRegistrar.clicked.connect(self.validar_ingreso)

    def validar_queSeaNum(self):
        # Verificar si el texto contiene algún carácter que no sea un número
        cedula = self.txtCedula.text()
        if not cedula.isnumeric() and cedula:
            # Eliminar el último carácter ingresado si no es un número
            self.txtCedula.setText(cedula[:-1])

        telefono = self.txtTelefono.text()
        if not telefono.isnumeric() and telefono:
            # Eliminar el último carácter ingresado si no es un número
            self.txtTelefono.setText(telefono[:-1])

    def validar_ingreso(self):
        nombre = self.txtNombre.text()
        apellido1 = self.txtApellido1.text()
        apellido2 = self.txtApellido2.text()
        correo = self.txtCorreo.text()
        cedula = self.txtCedula.text()
        telefono = self.txtTelefono.text()

        # Verifica que todos los campos requeridos no estén vacíos
        if not nombre or not apellido1 or not apellido2 or not correo or not cedula or not telefono:
            QMessageBox.critical(self, "Error", "Complete todos los campos solicitados")
        else:
            # Llama a la función crearPropietario con los datos ingresados
            if crearPropietario(cedula, nombre, apellido1, apellido2, telefono, correo): #Pasa las variables a la funcion
                QMessageBox.information(self, "Éxito", "El registro se realizó correctamente")
            else:
                QMessageBox.critical(self, "Error", "No se pudo realizar el registro")
  

# ---------------------------------------- INQUILINOS --------------------------------------- #

#llama la ventanaInicioInquilinos
class VentanaInicioInquilinos(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaInicioInquilinos.ui', self)
        print("Interfaz cargada correctamente")
        # Verificar el nombre correcto del botón en el archivo .ui
        self.btnPagos.clicked.connect(self.abrir_ventana_Pagos)
        self.btnManteInquilinos.clicked.connect(self.abrir_ventana_mantenimiento)
        self.btnComunicacion.clicked.connect(self.abrir_ventana_comunicacion_enviar)
        self.btnReporte.clicked.connect(self.abrir_ventana_reporte)

    def abrir_ventana_comunicacion_enviar(self):
        ventana_comunicacion = VentanaComunicacionInq(self)
        ventana_comunicacion.show()

    def abrir_ventana_Pagos(self):
        ventana_registrar_propiedades = VentanaRegistrarPago(self)
        ventana_registrar_propiedades.show()

    def abrir_ventana_mantenimiento(self):
        ventana_mantenimiento = VentanaMantenimientoInq(self)
        ventana_mantenimiento.show()

    def abrir_ventana_reporte(self):
        ventana_reporte = VentanaReportePagos(self)
        ventana_reporte.show()

class VentanaComunicacionInq(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaEnviarMjs.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnENVIAR.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnRecibidos.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnEnviados.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnVolver.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnEnviar.clicked.connect(self.enviar_mensaje)

    def abrir_ventana_comunicacion(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnENVIAR:
            ventana_enviar = VentanaEnviar(self)
            ventana_enviar.show()
        elif sender_button == self.btnRecibidos:
            ventana_recibidos = VentanaRecibidos(self)
            ventana_recibidos.show()
        elif sender_button == self.btnEnviados:
            ventana_enviados = VentanaEnviados(self)
            ventana_enviados.show()
        elif sender_button == self.btnVolver:
             self.close()

    def enviar_mensaje(self):
        cedulaReceptor = self.txtReceptor.text()
        contenido = self.txtContenido.text()

        # Valida que los campos sean numéricos y no estén vacíos
        if not cedulaReceptor.isnumeric() or not contenido:
            QMessageBox.critical(self, "Error", "Los campos ID Mensaje, Receptor y Contenido son obligatorios y deben ser numéricos")
            return

        # Llama a la función enviarMensaje con los datos de los campos
        if enviarMensaje(cedulaReceptor, contenido):
            QMessageBox.information(self, "Éxito", "Mensaje enviado correctamente")
        else:
            QMessageBox.critical(self, "Error", "Error al enviar el mensaje")
   
class VentanaEnviar(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaEnviarMjs.ui', self)

        self.btnEnviar.clicked.connect(self.enviar_mensaje)
        self.btnRecibidos.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnEnviados.clicked.connect(self.abrir_ventana_comunicacion)
        self.btnVolver.clicked.connect(self.abrir_ventana_comunicacion)
    
    def abrir_ventana_comunicacion(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnENVIAR:
            ventana_enviar = VentanaEnviar(self)
            ventana_enviar.show()
        elif sender_button == self.btnRecibidos:
            ventana_recibidos = VentanaRecibidos(self)
            ventana_recibidos.show()
        elif sender_button == self.btnEnviados:
            ventana_enviados = VentanaEnviados(self)
            ventana_enviados.show()
        elif sender_button == self.btnVolver:
             self.close()

    def enviar_mensaje(self):
        cedulaReceptor = self.txtReceptor.text()
        contenido = self.txtContenido.text()

        # Valida que los campos sean numéricos y no estén vacíos
        if not cedulaReceptor.isnumeric() or not contenido:
            QMessageBox.critical(self, "Error", "Los campos ID Mensaje, Receptor y Contenido son obligatorios y deben ser numéricos")
            return

        # Llama a la función enviarMensaje con los datos de los campos
        if enviarMensaje(cedulaReceptor, contenido):
            QMessageBox.information(self, "Éxito", "Mensaje enviado correctamente")
        else:
            QMessageBox.critical(self, "Error", "Error al enviar el mensaje")

class VentanaRecibidos(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaMjsRecibidos.ui', self)
        # Datos a insertar en la tabla
        self.btnConsultar.clicked.connect(self.consultar)

    def consultar(self):
        # Obtener datos de visualizarMsjRecibidos
     #   data = visualizarMsjRecibidos() prueba

        # Agregar filas a la tablaMjsRecibidos con los datos obtenidos
     #   agregar_filas_a_tabla(self.tableMjsRecibidos, data)  prueba
        # Insertar filas en la tabla CON LA FUNCIÓN DE BRI
        agregar_filas_a_tabla(self.tableMjsRecibidos, visualizarMsjRecibidos())  

#PARA AGREGAR INFORMACIÓN A TODAS LAS TABLAS HECHAS DE DUPLAS
def agregar_filas_a_tabla(table_widget, data):
    for row_data in data:
        current_row = table_widget.rowCount()
        table_widget.insertRow(current_row)
            
        # Insertar datos en cada celda de la fila
        for column, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            table_widget.setItem(current_row, column, item)        


class VentanaEnviados(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaMjsEnviados.ui', self)
        # Datos a insertar en la tabla
        self.btnConsultarEnviados.clicked.connect(self.consultar)

    def consultar(self):
        # Obtener datos de visualizarMsjRecibidos
     #   data = visualizarMsjRecibidos() prueba

        # Agregar filas a la tablaMjsRecibidos con los datos obtenidos
     #   agregar_filas_a_tabla(self.tableMjsRecibidos, data)  prueba
        # Insertar filas en la tabla CON LA FUNCIÓN DE BRI
        agregar_filas_a_tabla(self.tableEnviados, visualizarMsjEnviados())
               
class VentanaMantenimientoInq(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarManteInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnVolver.clicked.connect(self.abrir_ventana_visualizar_mante)

    def abrir_ventana_visualizar_mante(self):
        # Aquí se abre la ventana 'ventanaVisualizarPago' dependiendo del botón que se haya presionado
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnVolver:
            self.close()

    def validar_registro_solicitud(self):
        idSolicitud = self.txtIDSolicitudMante.text()
        idPropiedad = self.txtIDPropMante.text()
        prioridad = self.txtPrioridad.text()
        descripcionProblema = self.txtDesProblema.text()
        comentarios = self.txtComentariosMante.text()
        idProveedor = self.txtProveedor.text()  

        # Verificar que ningún campo esté vacío
        if not idSolicitud or not idPropiedad or not prioridad or not descripcionProblema or not comentarios or not idProveedor:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        if not idSolicitud.isnumeric() or not idPropiedad.isnumeric() or not prioridad.isnumeric() or not idProveedor.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos ID Solicitud, ID Propiedad, Prioridad y Estado deben ser numéricos")
            return
        
        if int(idProveedor) > 5 and int(idProveedor) < 1:
            QMessageBox.critical(self, "Error", "El proveedor no existe")
            return
            
        # Llama a la función para registrar el mantenimiento
        if registrarMantenimiento(idSolicitud, idPropiedad, descripcionProblema, idProveedor, prioridad):
            QMessageBox.information(self, "Éxito", "Mantenimiento registrado correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el mantenimiento")

class VentanaRegistrarPago(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarPago.ui', self)

        self.btnRegistrar.clicked.connect(self.enviar_datos)

    def enviar_datos(self):
        idPago = self.txtIDpago.text()
        monto = self.txtMonto.text()
        tipoPago = self.txtTipoPago.text()
        estadoPago = self.txtEstadoPago.text()
        metodoPago = self.txtMetodoPago.text()

        # Valida que los campos sean numéricos y no estén vacíos
        if not idPago.isnumeric() or not monto.isnumeric()  or not tipoPago.isnumeric() or not estadoPago.isnumeric()  or not metodoPago:
            QMessageBox.critical(self, "Error", "Verifique que todos los campos se encuentren completos")
            return

        # Llama a la función enviarMensaje con los datos de los campos
        if registrarPago(idPago, monto, tipoPago, estadoPago, metodoPago):
            QMessageBox.information(self, "Éxito", "Registro exitoso")
        else:
            QMessageBox.critical(self, "Error", "Verifique sus datos")

class VentanaReportePagos(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaReportePagos.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnMensual.clicked.connect(self.abrir_ventana_visualizar_pago)
        self.btnTrimestral.clicked.connect(self.abrir_ventana_visualizar_pago)
        self.btnAnual.clicked.connect(self.abrir_ventana_visualizar_pago)
        self.btnVOLVER.clicked.connect(self.abrir_ventana_visualizar_pago)

    def abrir_ventana_visualizar_pago(self):
        # Aquí se abre la ventana 'ventanaVisualizarPago' dependiendo del botón que se haya presionado
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnMensual:
            # Abre ventana para mostrar pagos mensuales
            ventana_visualizar_pago = VentanaVisualizarPago(self)
        elif sender_button == self.btnTrimestral:
            # Abre ventana para mostrar pagos trimestrales
            ventana_visualizar_pago = VentanaVisualizarPago(self)
        elif sender_button == self.btnAnual:
            # Abre ventana para mostrar pagos anuales
            ventana_visualizar_pago = VentanaVisualizarPago(self)
            ventana_visualizar_pago.show()
        elif sender_button == self.btnVOLVER:
             self.close()

class VentanaVisualizarPago(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaVisualizarPago.ui', self)
        # Datos a insertar en la tabla
        self.btnConsultar.clicked.connect(self.consultar)

    def consultar(self):
        global periodo
        agregar_filas_a_tabla(self.tablePagos, mostrarReporte(periodo))  

# ---------------------------------------------- PROPIETARIOS --------------------------------------- #

class VentanaInicioPropietarios(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaInicioPropietarios.ui', self)
        print("Interfaz cargada correctamente")
        # Verificar el nombre correcto del botón en el archivo .ui
        self.btnPropiedades.clicked.connect(self.abrir_ventana_registrar_propiedades)
        self.btnINQUILINOS.clicked.connect(self.abrir_ventana_registrar_inquilinos)
        self.btnMANTENIMIENTO.clicked.connect(self.abrir_ventana_mantenimiento)
        self.btnCOMUNICACION.clicked.connect(self.abrir_ventana_enviar)
        self.btnREPORTE.clicked.connect(self.abrir_ventana_reporte)

    def abrir_ventana_registrar_propiedades(self):
        ventana_registrar_propiedades = VentanaRegistrarPropiedades(self)
        ventana_registrar_propiedades.show()

    def abrir_ventana_registrar_inquilinos(self):
        ventana_registrar_inquilino = VentanaRegistrarInquilino(self)
        ventana_registrar_inquilino.show()

    def abrir_ventana_mantenimiento(self):
        ventana_consultar_mantenimiento = VentanaMantenimiento(self)
        ventana_consultar_mantenimiento.show()
        
    def abrir_ventana_enviar(self):
        ventana_consultar_mantenimiento = VentanaEnviar(self)
        ventana_consultar_mantenimiento.show()

    def abrir_ventana_reporte(self):
        ventana_consultar_mantenimiento = VentanaReporte(self)
        ventana_consultar_mantenimiento.show()

# VENTANA REPORTE - PAGOS  
class VentanaReporte(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaReportePagosProp.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnMensual.clicked.connect(self.abrir_ventana_Reporte)
        self.btnTrimestral.clicked.connect(self.abrir_ventana_Reporte)
        self.btnAnual.clicked.connect(self.abrir_ventana_Reporte)
        self.btnVolver.clicked.connect(self.abrir_ventana_Reporte)

    def abrir_ventana_Reporte(self):
        global periodo
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnMensual:
            periodo = 'Mensual'
            # Abre ventana para mostrar pagos mensuales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
            ventana_visualizar_pago.show()
        elif sender_button == self.btnTrimestral:
            periodo = 'Trimestral'
            # Abre ventana para mostrar pagos trimestrales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
            ventana_visualizar_pago.show()
        elif sender_button == self.btnAnual:
            periodo = 'anual'
            # Abre ventana para mostrar pagos anuales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
            ventana_visualizar_pago.show()
        elif sender_button == self.btnVolver:
             self.close()


class VentanaVisualizarReporte(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaVisualizarPago.ui', self)
        # Datos a insertar en la tabla
        self.btnConsultar.clicked.connect(self.consultar)

    def consultar(self):
        global periodo
        agregar_filas_a_tabla(self.tablePagos, mostrarReporte(periodo))  

#-- VENTANA PROPIEDADES
class VentanaRegistrarPropiedades(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarPropiedades.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnREGISTRAR.clicked.connect(self.validar_registro)
        self.btnVisualizar.clicked.connect(self.abrir_ventana_)
        self.btnEditar.clicked.connect(self.abrir_ventana_)
        self.btnVolver.clicked.connect(self.abrir_ventana_)

    def abrir_ventana_(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnVisualizar:
            ventana_visualizar = VentanaVisualizarPropiedades(self)
            ventana_visualizar.show()
        elif sender_button == self.btnEditar:
            ventana_visualizar = VentanaEditarPropiedades(self)
            ventana_visualizar.show()
        elif sender_button == self.btnVolver:
             self.close()

    def validar_registro(self):
        # Obtener los valores de los campos
        idPropiedad = self.txtIDpropiedad.text()
        precioAlquiler = self.txtPrecioAlquiler.text()
        numeroHabitaciones = self.txtNumHabitaciones.text()
        tamanoMetros = self.txtTamPropiedad.text()
        gastosAdicionales = self.txtGastos.text()
        estadoActual = self.txtEstado.text()
        direccion = self.txtDireccion.text()
        tipoPropiedad = self.txtTipoPropiedad.text()
        descripcion = self.txtDesPropiedad.text()

        # Verifica que ningún campo esté vacío
        if not idPropiedad or not precioAlquiler or not numeroHabitaciones or not tamanoMetros or not gastosAdicionales or not estadoActual or not direccion or not tipoPropiedad or not descripcion:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Verifica que los campos numéricos solo contengan números
        if not idPropiedad.isnumeric() or not precioAlquiler.isnumeric() or not numeroHabitaciones.isnumeric() or not tamanoMetros.isnumeric() or not gastosAdicionales.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos numéricos solo pueden contener números")
            return

        # Llama a la función crearPropiedad con los datos ingresados
        if crearPropiedad(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastosAdicionales):
            QMessageBox.information(self, "Éxito", "La propiedad se registró correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la propiedad")

#---------------VENTANA VISUALIZAR PROPIEDADES
class VentanaVisualizarPropiedades(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaVisualizarPropiedades.ui',self)

        # Conectar el botón btnConsultar a la función mostrar_datos
        self.btnConsultar.clicked.connect(self.mostrar_datos)

    def mostrar_datos(self):
        global cedulaUsuario

        # Llamar a la función visualizarPropiedades para obtener los datos
        datosPropiedades = visualizarPropiedades()
        # Limpia la tabla antes de agregar nuevos datos
        self.tableVisualizar.setRowCount(0)

        # Llena la tabla con los datos obtenidos
        for row_num, row_data in enumerate(datosPropiedades):
            self.tableVisualizar.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableVisualizar.setItem(row_num, col_num, QTableWidgetItem(str(data)))

#--------------- EDITAR PROPIEDAD--------------       
class VentanaEditarPropiedades(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaEditarPropiedades.ui', self)

        # Conectar los botones a las funciones correspondientes
        self.btnbuscar.clicked.connect(self.cargar_datos)
        self.btnAceptar.clicked.connect(self.guardar_cambios)

    def cargar_datos(self):
        # Buscar la propiedad y cargar los datos 
        idPropiedad = self.txtIDpropiedad.text()  # Obtener el ID de la propiedad a editar
        datos_propiedad = obtenerPropiedad(idPropiedad)  # Implementa esta función para obtener los datos de la propiedad

        if len(datos_propiedad) == 1:
            
            # Si se encontraron datos, cargarlos en los campos correspondientes
            #idPropiedad, tipoPropiedad, tamanoMetros, descripcion, precioAlquiler, direccion, numeroHabitaciones, estado, gastosAdicionales
            self.txtTipo.setText(str(datos_propiedad[0][1]))
            self.txtTam.setText(str(datos_propiedad[0][2]))
            self.txtDescripcion.setText(str(datos_propiedad[0][3]))
            self.Txtprecio.setText(str(datos_propiedad[0][4]))
            self.txtDireccion.setText(str(datos_propiedad[0][5]))
            self.txtNumH.setText(str(datos_propiedad[0][6]))
            self.txtEstado.setText(str(datos_propiedad[0][7]))
            self.txtGastosA.setText(str(datos_propiedad[0][8]))
        else:
            QMessageBox.critical(self, "Error", "La propiedad no se encontró")

    def guardar_cambios(self):
        # Obtener los datos de los campos
        direccion = self.txtDireccion.text()
        tipoPropiedad = self.txtTipo.text()
        numeroHabitaciones = self.txtNumH.text()
        tamanoMetros = self.txtTam.text()
        descripcion = self.txtDescripcion.text()
        estadoActual = self.txtEstado.text()
        precioAlquiler = self.Txtprecio.text()
        gastosAdicionales = self.txtGastosA.text()
        idPropiedad = self.txtIDpropiedad.text()

        # Verificar que ningún campo esté vacío
        if not direccion or not tipoPropiedad or not numeroHabitaciones or not tamanoMetros or not descripcion or not estadoActual or not precioAlquiler or not gastosAdicionales:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Llamar a la función editarPropiedad para guardar los cambios
        if editarPropiedad(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastosAdicionales):
            QMessageBox.information(self, "Éxito", "Los cambios se guardaron correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar los cambios")

# -----------------------VENTANA INQUILINOS - PROPIETARIOS

#--------VENTANA REGISTRAR INQUILINOS-------------------------
class VentanaRegistrarInquilino(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnREGISTRAR.clicked.connect(self.validar_registro)
        self.btnVisualizar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnRegistrar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnEditar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnVolver.clicked.connect(self.abrir_ventana_Registrar)

    def validar_registro(self):
        # Obtener los valores de los campos
        idInquilino = self.txtIDpropiedad.text()
        nombre = self.txtNombre.text()
        primerApellido = self.txtApellido1.text()
        segundoApellido = self.txtApellido2.text()
        cedula = self.txtCedInquilino.text()
        telefono = self.txtTelefono.text()
        correo = self.txtCorreo.text()
        idPropiedad = self.txtIDpropiedad.text()
        fechaInicio = self.txtFechaInicio.text()
        fechaFinal = self.txtFechaFin.text()

        # Valida que los campos no estén vacíos y que cumplan con los requisitos
        if not idInquilino or not nombre or not primerApellido or not segundoApellido or not cedula or not telefono or not correo or not idPropiedad or not fechaInicio or not fechaFinal:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Valida que los campos que deben contener solo números contengan solo números
        if not cedula.isnumeric() or not telefono.isnumeric() or not idPropiedad.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos de cédula y teléfono deben contener solo números")
            return

        # Llama a la función para crear el inquilino
        if crearInquilino(nombre, primerApellido, segundoApellido, cedula, telefono, correo, idPropiedad, fechaInicio, fechaFinal):
            QMessageBox.information(self, "Éxito", "El inquilino se registró correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el inquilino")

    def abrir_ventana_Registrar(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnRegistrar:
            ventana_visualizar = VentanaRegistrar(self)
        elif sender_button == self.btnVisualizar:
            ventana_visualizar = VentanaVisualizar(self)
            ventana_visualizar.show()
        elif sender_button == self.btnEditar:
            ventana_visualizar = VentanaEditar(self)
            ventana_visualizar.show()
        elif sender_button == self.btnVolver:
            ventana_inicio_propietarios = VentanaInicioPropietarios()
            ventana_inicio_propietarios.show()
            self.close()


class VentanaRegistrar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaRegistrarInquilino.ui',self.parent)
        self.parent.show()

#En esta ventana tambien esta eliminar
class VentanaVisualizar(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaVisualizarInquilino.ui',self)
        
        self.btnConsultarInq.clicked.connect(self.consultar)

    def consultar(self):
        # Insertar filas en la tabla CON LA FUNCIÓN DE BRI
        agregar_filas_a_tabla(self.tableVizualizarInquilinos, visualizarInquilinos())  
       

class VentanaEditar(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaEditarInquilino.ui', self)
        
        # Conectar los botones a las funciones correspondientes
        self.btnBuscar.clicked.connect(self.cargar_datos)
        self.btnAceptar.clicked.connect(self.guardar_cambios)

    def cargar_datos(self):
        # Buscar la propiedad y cargar los datos 
        cedulaInquilino = self.txtIDinquilino.text()  # Obtener el ID de la propiedad a editar
        datos_inquilino = obtenerInquilino(cedulaInquilino)  # Implementa esta función para obtener los datos de la propiedad

        if len(datos_inquilino) == 1:
            # Si se encontraron datos, cargarlos en los campos correspondientes
            #nombre, apellido1, apellido2, telefono, correo
            self.txtNombre.setText(str(datos_inquilino[0][0]))
            self.txtApellido1.setText(str(datos_inquilino[0][1]))
            self.txtApellido2.setText(str(datos_inquilino[0][2]))
            self.txtTelefono.setText(str(datos_inquilino[0][3]))
            self.txtCorreo.setText(str(datos_inquilino[0][4]))
        else:
            QMessageBox.critical(self, "Error", "La propiedad no se encontró")

    def guardar_cambios(self):
        # Obtener los datos de los campos
        cedulaInquilino = self.txtIDinquilino.text()
        nombre = self.txtNombre.text()
        apellido1 = self.txtApellido1.text()
        apellido2 = self.txtApellido2.text()
        telefono = self.txtTelefono.text()
        correo = self.txtCorreo.text()

        # Verificar que ningún campo esté vacío
        if not nombre or not apellido1 or not apellido2 or not telefono or not correo or not cedulaInquilino:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Llamar a la función editarPropiedad para guardar los cambios
        if editarInquilino(cedulaInquilino, nombre, apellido1, apellido2, telefono, correo):
            QMessageBox.information(self, "Éxito", "Los cambios se guardaron correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar los cambios")



#////

# VENTANA MANTENIMIENTO PROPIETARIO
class VentanaMantenimiento(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaMantenimientoPropietarios.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnVolver.clicked.connect(self.abrir_ventana_Registrar)
        self.btnActualizar.clicked.connect(self.validar_actualizacion)
        self.btnConsultar.clicked.connect(self.consultar_solicitudes)

    def abrir_ventana_Registrar(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnVolver:
            self.close()

    def validar_actualizacion(self):
       idsolicitud = self.txtIDsolicitud.text()
       estado = self.txtEstado.text()


       if not idsolicitud.isnumeric() or not estado.isnumeric():
             QMessageBox.critical(self, "Error", "Los campos ID Solicitud y Estado deben ser numéricos")
             return

       if not idsolicitud or not estado:
              QMessageBox.critical(self, "Error", "Complete todos los campos")
              return

       cedula_propietario = '...'  # Aquí deberías obtener la cédula del propietario
       if actualizarSolicitud(idsolicitud, estado):
           QMessageBox.information(self, "Éxito", "La solicitud se actualizó correctamente")
       else:
           QMessageBox.critical(self, "Error", "No se pudo actualizar la solicitud")

    def consultar_solicitudes(self):
        tabla_solicitudes = visualizarSolicitudesP()

        if tabla_solicitudes:

            agregar_filas_a_tabla(self.tableSolicitudes, tabla_solicitudes)  

        else:
            QMessageBox.information(self, "Información", "No hay solicitudes para mostrar")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())
