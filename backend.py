
import pyodbc
from datetime import datetime, timedelta




def conectarBD():
    SERVER = 'localhost'
    DATABASE = 'Proyecto1' #aqui va el nombre
    USERNAME = 'NewSA'
    PASSWORD = 'mypassword'

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'
    cnxn = pyodbc.connect(connectionString) 
    return cnxn

def desconectarBD(cnxn, cursor):
    cnxn.commit()
    cursor.close()

#LOGIN
cedulaUsuario = ''
rolUsuario = ''


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
def visualizarPropiedades(cedulaPropietario):
    try:
        tablaPropiedades = obtenerPropiedades(cedulaPropietario)
        return tablaPropiedades
    except: 
        return []

#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
# cuando hay que pasarle al sistema las propiedades disponibles para ese propietario
def obtenerPropiedades(cedulaPropietario):
    #debe retornar una []
    pass


#EDITAR MODULO PROPIEDAD(revisar si es asi) (Propietario)

def obtenerPropiedad(idPropiedad): 
    if(existePropiedad(idPropiedad)):
        try:
            #informacion = execute.... 
            return #informacion
        except: 
            return []
    else:
        return []


def editarPropiedad(idPropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros,cedulaPropietario,descripcion, estadoActual, precioAlquiler,gastosAdicionales):

    try:
        nuevosDatos = (direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros,cedulaPropietario,descripcion, estadoActual, precioAlquiler,gastosAdicionales)
        cambiarPropiedadBD(nuevosDatos)
        return True
    except: 
        return False      


#Acá se hace la accion en la BD con el execute, hace el update   
def cambiarPropiedadBD(nuevosDatos):
    pass


# ELIMINAR MODULO PROPIEDAD (Propietario)

# Esta funcion es la que se llama luego de atrapar el id del sistema 
def eliminarPropiedad(idPropiedad):
    if(existePropiedad(idPropiedad)):
        try:
            #execute delete
            return True
        except: 
            return False 
    else:
        return False

 

#MODULO INQUILINOS (Propietario)
#CREAR MODULO INQUILINOS (Propietario)

#Esta es la funcion que llama la base de datos luego de atrapar los datos de la interfaz (Al darle la opcion de crear inquilino)
#y se los pasa con esas variables
#El idPropiedad debe ser mostrado los disponibles, preguntar como hacerlo si es necesario una tabla intermedia

def crearInquilino(nombre, primerApellido, segundoApellido, cedula, telefono, correo, idPropiedad, fechaInicio, fechaFinal): 
    if(existePropiedad(idPropiedad) == True and propiedadDisponible(idPropiedad) == True):
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
def visualizarInquilinos(cedulaPropietario):
    if(existeInquilinosPropietario()):
        try:
            tablaInquilinos = obtenerInquilinos()
            
            #enviar datos a la interfaz
            return tablaInquilinos
        except: 
            return []
    return[]


#Valida que existan inquilinos en sus propiedades con la cedula del propietario 
#cambiar el statement
def existeInquilinosPropietario():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    #---------------------
    statement = 'SELECT COUNT(*) FROM Propiedad p JOIN Inquilino i ON p.cedulaPropietario = ?'
    cursor.execute(statement, (cedulaUsuario))
    checkInquilinoP = cursor.fetchone()[0]
    if (checkInquilinoP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True


#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
# cuando hay que pasarle al sistema las propiedades disponibles para ese propietario
def obtenerInquilinos(cedulaPropietario):
    pass

#ELIMINAR MODULO INQUILINOS (Propietario)

def eliminarInquilino(cedulaInquilino):
    if(existeInquilinoBD(cedulaInquilino)):
        try:
            #execute 
            return True
        except: 
            return False 
    else:
        return False

 
#MODULO MANTENIMIENTO (Propietario)

#MODULO MANTENIMIENTO VISUALIZAR SOLICITUDES (Propietario)

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarSolicitudesP(cedulaPropietario):
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
def existeSolicitudesPropietario(cedulaUsuario):
    # global cedulaUsuario
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
    pass

#MODULO MANTENIMIENTO ACTUALIZAR ESTADO SOLICITUD (Propietario e Inquilino)

def actualizarSolicitud(idSolicitud, estado, comentario,cedulaPropietario):
    if(existeSolicitudesPropietario(cedulaPropietario)):
        if(existeSolicitud(idSolicitud)):
            try:
                solicitud = obtenerSolicitud(idSolicitud)
                cambiarEstadoSolicitud(solicitud,idSolicitud,estado,comentario)
                return True
            except: 
                return False 
        else: return False     
    else: return False 

#obtiene los datos de la solicitud especifica
def obtenerSolicitud(idSolicitud):
    pass


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


#Acá se hace la accion en la BD con el execute  
def cambiarEstadoSolicitud(solicitud, idSolicitud, estado, comentario):
    pass

#MODULO DE REPORTES (Propietario, inquilino (es el mismo))

def mostrarReporte(periodo):
    global cedulaUsuario, rolUsuario
    if(rolUsuario == "Propietario"):
        if(existeInquilinosPropietario() == True and existenReportesPropietario(periodo) == True):
                try:
                    reportes = obtenerReportesPropietario(periodo)
                    return reportes
                except:
                    return []
        else: 
            return[]
    elif(existeReportesInquilino(periodo)):
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
    if (periodo == 'trimestral'):
        # Suma 3 meses a la fecha actual para obtener la fecha final del trimestre
        fechaFinal = fechaActual - timedelta(days=90)
        return fechaFinal
    elif (periodo == 'mensual'):
        # Suma 1 mes a la fecha actual para obtener la fecha final del mes siguiente
        fechaFinal = fechaActual - timedelta(days=30)
        return fechaFinal
    else:
        # Suma 1 año a la fecha actual para obtener la fecha final del año siguiente
        fechaFinal = fechaActual - timedelta(days=365)
        return fechaFinal

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
    pass




# INQUILINOS

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
    global cursor
    #cedulaUsuario
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

#RECIBIDOS MODULO COMUNICACION (Propietario, inquilino (es el mismo))

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarMsjRecibidos():
    global cedulaUsuario
    if(existeMsjRecibidos()):
        try:
            tablaMsjRecibidos = obtenerMsjRecibidos()   
            #enviar datos a la interfaz
            return tablaMsjRecibidos
        except: 
            return []
    else: 
        return[]

#Revisa en la tabla de comunicacion si existen mensajes recibidos es decir en el where cedula receptor = cedula usuario (de la persona que esta usando el sistema)
def existeMsjRecibidos(): 
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT * FROM Comunicacion WHERE cedulaReceptor = ?'
    cursor.execute(statement, cedulaUsuario)
    checkReportesP = cursor.fetchone()
    if (checkReportesP == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True
    
#Esta funcion utiliza el stament y manda el select con execute a la base de datos
def obtenerMsjRecibidos(): 
    global cedulaUsuario, rolUsuario
    pass

#ENVIADOs MODULO COMUNICACION (Propietario, inquilino (es el mismo))

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarMsjEnviados():
    global cedulaUsuario
    if(existeMsjEnviados()):
        try:
            tablaMsjEnviados = obtenerMsjEnviados()   
            #enviar datos a la interfaz
            return tablaMsjEnviados
        except: 
            return []
    else: 
        return[]

#Revisa en la tabla de comunicacion si existen mensajes enviados es decir en el where cedula emisor = cedula usuario (de la persona que esta usando el sistema)
def existeMsjEnviados(): 
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    #---------------------
    statement = 'SELECT * FROM Comunicacion WHERE cedulaEmisor = ?'
    cursor.execute(statement, (cedulaUsuario))
    #---------------------
    checkMsjE = cursor.fetchone()
    if (checkMsjE == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True

#Esta funcion utiliza el stament y manda el select con execute a la base de datos
def obtenerMsjEnviados():
    global cedulaUsuario
    pass

#INQUILINOS 

#INQUILINOS MODULO PAGOS
 
#INQUILINOS MODULO PAGOS REGISTRAR PAGOS 

def registrarPago (idPago, monto, tipoPago, estadoPago, metodoPago): 
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
                mantenimiento = (idSolicitud,idPropiedad,descripcionProblema,idProveedor,fechaSolicitud, estado, idPrioridad)
                insertarMantenimiento(mantenimiento)
                return True
            except: 
                return False
        else: 
            return False
    else: 
        return False

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
    global cursor,cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    
    try:
        statement = 'INSERT INTO SolicitudMantenimiento (idSolicitud, idPropiedad, descripcionProblema, idProveedor, fechaSolicitud, estado, idPrioridad) VALUES (?,?,?,?,?,?,?)'
        cursor.execute(statement, mantenimiento,) 
        desconectarBD(cnxn, cursor)
        return True
    except: 
        desconectarBD(cnxn, cursor)
        return False

# INQUILINOS MODULO MANTENIMIENTO VISUALIZAR

# Esta funcion es la que se llama luego de presionar el boton de visualizar 
def visualizarSolicitudesI(cedulaInquilino):
    if(existeSolicitudesInquilino(cedulaInquilino)):
        try:
            tablaSolicitudes = obtenerSolicitudesI(cedulaInquilino)

                #enviar datos a la interfaz
            return tablaSolicitudes
        except: 
            return []
    else: 
        return[]

#Valida que existan solicitudes en sus propiedades con la cedula del propietario (el metodo debe ser diferente para propietario e inquilino)
def existeSolicitudesInquilino():
    global cedulaUsuario
    cnxn = conectarBD()
    cursor = cnxn.cursor()
    statement = 'SELECT * FROM SolicitudMantenimiento JOIN Alquiler ON Alquiler.idPropiedad = SolicitudMantenimiento.idPropiedad WHERE Alquiler.cedulaInquilino = ?; '
    cursor.execute(statement, cedulaUsuario)
    checkSolicitudI = cursor.fetchone()
    if (checkSolicitudI == None):
        desconectarBD(cnxn, cursor)
        return False
    else:
        desconectarBD(cnxn, cursor)
        return True 

#usa Execute y llama a la base de datos usando el statement, lo guarda en una lista, esta misma funcion se puede usar
def obtenerSolicitudesI(cedulaPropietario):
    pass



