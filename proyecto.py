import pyodbc
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

cedulaUsuario = ''
rolUsuario = ''

#-----------------------------------------BACKEND-------------------------------------------------#

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

    def abrir_ventana_comunicacion_enviar(self):
        ventana_comunicacion = VentanaComunicacionInq(self)
        ventana_comunicacion.show()

    def abrir_ventana_Pagos(self):
        ventana_registrar_propiedades = VentanaReportePagos(self)
        ventana_registrar_propiedades.show()

    def abrir_ventana_mantenimiento(self):
        ventana_mantenimiento = VentanaMantenimientoInq(self)
        ventana_mantenimiento.show()

class VentanaComunicacionInq(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaEnviarMjs.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnENVIAR.clicked.connect(self.abrir_ventana_comunicacion)
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
   
class VentanaEnviar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEnviarMjs.ui', self.parent)
        self.parent.show()

        self.btnEnviar.clicked.connect(self.enviar_mensaje)

    def enviar_mensaje(self):
        idMensaje = self.txtIDmjs.text()
        cedulaReceptor = self.txtReceptor.text()
        contenido = self.txtContenido.text()
        fecha = self.dtFecha.text()
        hora = self.tmHora.text()

        # Valida que los campos sean numéricos y no estén vacíos
        if not idMensaje.isnumeric() or not cedulaReceptor.isnumeric() or not contenido:
            QMessageBox.critical(self, "Error", "Los campos ID Mensaje, Receptor y Contenido son obligatorios y deben ser numéricos")
            return

        # Llama a la función enviarMensaje con los datos de los campos
        if enviarMensaje(idMensaje, cedulaReceptor, fecha, contenido, hora):
            QMessageBox.information(self, "Éxito", "Mensaje enviado correctamente")
        else:
            QMessageBox.critical(self, "Error", "Error al enviar el mensaje")

class VentanaRecibidos(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaMjsRecibidos.ui', self.parent)
        self.parent.show()

        self.btnConsultar.clicked.connect(self.visualizarMsjRecibidos)
               #Aca nose como mostrar los datos en la tabla :(

class VentanaEnviados(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaMjsRecibidos.ui', self.parent)
        self.parent.show()

        self.btnConsultarEnviados.clicked.connect(self.existeMsjEnviados)
               #Aca nose como mostrar los datos en la tabla :(
               
class VentanaMantenimientoInq(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarManteInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnVizualizarSolicitud.clicked.connect(self.abrir_ventana_visualizar_mante)
        self.btnRegisSolicitud.clicked.connect(self.validar_registro_solicitud)
        self.btnVolver.clicked.connect(self.abrir_ventana_visualizar_mante)

    def abrir_ventana_visualizar_mante(self):
        # Aquí se abre la ventana 'ventanaVisualizarPago' dependiendo del botón que se haya presionado
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnVizualizarSolicitud:
            ventana_mante = VentanaVisualizarMante(self)
            ventana_mante.show()
        elif sender_button == self.btnRegisSolicitud:
            ventana_registrar = VentanaRegistrarMante(self)
            ventana_registrar.show()
        elif sender_button == self.btnVolver:
            self.close()

    def validar_registro_solicitud(self):
        idsolicitud = self.txtIDSolicitudMante.text()
        idpropiedad = self.txtIDPropMante.text()
        prioridad = self.txtPrioridad.text()
        estado = self.txtEstado.text()
        fechaSolicitud = self.date.get()
        descripcionProblema = self.txtDesProblema.toPlainText()
        comentarios = self.txtComentariosMante.toPlainText()

        if not idsolicitud.isnumeric() or not idpropiedad.isnumeric() or not prioridad.isnumeric() or not estado.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos ID Solicitud, ID Propiedad, Prioridad y Estado deben ser numéricos")
            return
        # Verificar que ningún campo esté vacío
        if not idsolicitud or not idpropiedad or not prioridad or not estado or not descripcionProblema or not comentarios:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        if not self.validar_radio_buttons():
            return
        # Llama a la función para registrar el mantenimiento
        if self.registrar_mantenimiento(idsolicitud, idpropiedad, descripcionProblema, fechaSolicitud):
            QMessageBox.information(self, "Éxito", "Mantenimiento registrado correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el mantenimiento")

    def validar_radio_buttons(self):
        if not self.rbElectricista.isChecked() and not self.rbJardinero.isChecked() and not self.rbPintor.isChecked() and not self.rbPlomero.isChecked() and not self.rbCarpintero.isChecked():
            QMessageBox.critical(self, "Error", "Seleccione al menos un tipo de proveedor")
            return False
        return True

class VentanaRegistrarMante(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaRegistrarManteInquilino.ui',self.parent)
        self.parent.show()

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
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarPago.ui',self.parent)
        self.parent.show()

    #     self.btnVOLVER.clicked.connect(self.cerrar)
    # def cerrar(self):
    #     sender_button = self.sender()  # Obtener el botón que envió la señal
    #     if sender_button == self.btnVOLVER:
    #        self.close()


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

# class VentanaReporte(QMainWindow):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         loadUi('InterfazGrafica/ventanaReportePagosProp.ui',self.parent)
#         self.parent.show()

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
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnMensual:
            # Abre ventana para mostrar pagos mensuales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
        elif sender_button == self.btnTrimestral:
            # Abre ventana para mostrar pagos trimestrales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
        elif sender_button == self.btnAnual:
            # Abre ventana para mostrar pagos anuales
            ventana_visualizar_pago = VentanaVisualizarReporte(self)
            ventana_visualizar_pago.show()
        elif sender_button == self.btnVolver:
             self.close()


class VentanaVisualizarReporte(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarPago.ui',self.parent)
        self.parent.show() 
        
        self.btnConsultar.clicked.connect(self.mostrar_reporte)

    def mostrar_reporte(self):
        # Llama a la función mostrarReporte 
        per = periodo 
        reportes = mostrarReporte(periodo)
        if reportes:
            # Mostrar los reportes en la interfaz gráfica
            pass
        else:
            QMessageBox.information(self, "Información", "No hay reportes para mostrar")

#-- VENTANA PROPIEDADES
class VentanaRegistrarPropiedades(QMainWindow):
   def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarPropiedades.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnRegistrar.clicked.connect(self.validar_registro)

   def validar_registro(self):
        # Obtener los valores de los campos
        idpropiedad = self.txtIDpropiedad.text()
        precioAlquiler = self.txtPrecioAlquiler.text()
        numeroHabitaciones = self.txtNumHabitaciones.text()
        tamanoMetros = self.txtTamPropiedad.text()
        gastosAdicionales = self.txtGastos.text()
        estadoActual = self.txtEstado.text()
        direccion = self.txtDireccion.text()
        tipoPropiedad = self.txtTipoPropiedad.text()
        descripcion = self.txtDesPropiedad.text()

        # Verifica que ningún campo esté vacío
        if not idpropiedad or not precioAlquiler or not numeroHabitaciones or not tamanoMetros or not gastosAdicionales or not estadoActual or not direccion or not tipoPropiedad or not descripcion:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Verifica que los campos numéricos solo contengan números
        if not idpropiedad.isnumeric() or not precioAlquiler.isnumeric() or not numeroHabitaciones.isnumeric() or not tamanoMetros.isnumeric() or not gastos.isnumeric() or not gastosAdicionales.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos numéricos solo pueden contener números")
            return

        # Llama a la función crearPropiedad con los datos ingresados
        if crearPropiedad(idpropiedad, direccion, tipoPropiedad, numeroHabitaciones, tamanoMetros, descripcion, estadoActual, precioAlquiler, gastos):
            QMessageBox.information(self, "Éxito", "La propiedad se registró correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la propiedad")

# class VentanaRegistrar(QMainWindow):
#     def __init__(self, parent):
#         super().__init__()
#         self.parent = parent
#         loadUi('InterfazGrafica/ventanaRegistrarPropiedades.ui',self.parent)
#         self.parent.show()

#---------------VENTANA VISUALIZAR PROPIEDADES
class VentanaVisualizar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarPropiedades.ui',self.parent)
        self.parent.show()   

        # Conectar el botón btnConsultar a la función mostrar_datos
        self.btnConsultar.clicked.connect(self.mostrar_datos)

    def mostrar_datos(self):
        # Obtener la cédula del propietario
        cedulaPropietario = self.parent.cedula_propietario   # Asegúrate de tener esta variable disponible en tu ventana principal

        # Llamar a la función visualizarPropiedades para obtener los datos
        datosPropiedades = visualizarPropiedades(cedulaPropietario)

        # Limpia la tabla antes de agregar nuevos datos
        self.tableVisualizar.setRowCount(0)

        # Llena la tabla con los datos obtenidos
        for row_num, row_data in enumerate(datosPropiedades):
            self.tableVisualizar.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableVisualizar.setItem(row_num, col_num, QTableWidgetItem(str(data)))

#--------------- EDITAR PROPIEDAD--------------       
class VentanaEditar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEditarPropiedades.ui', self.parent)
        self.parent.show()

        # Conectar los botones a las funciones correspondientes
        self.btnbuscar.clicked.connect(self.cargar_datos)
        self.btnAceptar.clicked.connect(self.guardar_cambios)

    def cargar_datos(self):
        # Obtener la cédula del propietario
        idPropiedad = self.parent.cedula_propietario   

        # Buscar la propiedad y cargar los datos 
        id_propiedad = self.txtIDpropiedad.text()  # Obtener el ID de la propiedad a editar
        datos_propiedad = obtenerDatosPropiedad(id_propiedad, idPropiedad)  # Implementa esta función para obtener los datos de la propiedad

        if datos_propiedad:
            # Si se encontraron datos, cargarlos en los campos correspondientes
            self.txtTipo.setText(datos_propiedad['tipo'])
            self.txtTam.setText(datos_propiedad['tamano'])
            self.txtDescripcion.setText(datos_propiedad['descripcion'])
            self.Txtprecio.setText(datos_propiedad['precio'])
            self.txtDireccion.setText(datos_propiedad['direccion'])
            self.txtNumH.setText(datos_propiedad['num_habitaciones'])
            self.txtEstado.setText(datos_propiedad['estado'])
            self.txtGastosA.setText(datos_propiedad['gastos_adicionales'])
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

class VentanaEliminar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEliminarPropiedades.ui',self.parent)
        self.parent.show()

#----------------

# -----------------------VENTANA INQUILINOS - PROPIETARIOS

#--------VENTANA REGISTRAR INQUILINOS-------------------------
class VentanaRegistrarInquilino(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnRegistrar.clicked.connect(self.validar_registro)
        self.btnVisualizar.clicked.connect(self.abrir_ventana_Registrar)
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

        # Valida que los campos no estén vacíos y que cumplan con los requisitos
        if not idInquilino or not nombre or not primerApellido or not segundoApellido or not cedula or not telefono or not correo:
            QMessageBox.critical(self, "Error", "Complete todos los campos")
            return

        # Valida que los campos que deben contener solo números contengan solo números
        if not cedula.isnumeric() or not telefono.isnumeric():
            QMessageBox.critical(self, "Error", "Los campos de cédula y teléfono deben contener solo números")
            return

        # Llama a la función para crear el inquilino
        if crearInquilino(idInquilino, nombre, primerApellido, segundoApellido, cedula, telefono, correo):
            QMessageBox.information(self, "Éxito", "El inquilino se registró correctamente")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el inquilino")

    def abrir_ventana_Registrar(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnRegistrar:
            ventana_visualizar = VentanaRegistrar(self)
        elif sender_button == self.btnVisualizar:
            ventana_visualizar = VentanaVisualizar(self)
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
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarInquilino.ui',self.parent)
        self.parent.show()
       

class VentanaEditar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEditarInquilino.ui',self.parent)
        self.parent.show()

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
       comentario = self.txtAgregarComentario.text()

       if not idsolicitud.isnumeric() or not estado.isnumeric():
             QMessageBox.critical(self, "Error", "Los campos ID Solicitud y Estado deben ser numéricos")
             return

       if not idsolicitud or not estado or not comentario:
              QMessageBox.critical(self, "Error", "Complete todos los campos")
              return

       cedula_propietario = '...'  # Aquí deberías obtener la cédula del propietario
       if actualizarSolicitud(idsolicitud, estado, comentario, cedula_propietario):
           QMessageBox.information(self, "Éxito", "La solicitud se actualizó correctamente")
       else:
           QMessageBox.critical(self, "Error", "No se pudo actualizar la solicitud")

    def consultar_solicitudes(self):
        cedula_propietario = '...'  # aquí obtener la cédula del propietario
        tabla_solicitudes = visualizarSolicitudesP(cedula_propietario)

        if tabla_solicitudes:
            # Mostrar los datos en la tabla visualizarSolicitudes
            pass
        else:
            QMessageBox.information(self, "Información", "No hay solicitudes para mostrar")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())