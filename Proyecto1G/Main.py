import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi


#-----------------------------------------LOGIN-------------------------------------------------#
#carga la ventana de inicio y llama a las otras funciones la mostrar la ventana correspondiente
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
            ventana_inquilinos = VentanaInicioInquilinos(self)
            ventana_inquilinos.show()
        elif self.rbPropietario.isChecked():
            ventana_propietarios = VentanaInicioPropietarios(self)
            ventana_propietarios.show()
        else:
            QMessageBox.critical(self, "Error", "Debe seleccionar si es Inquilino o Propietario")


# class VentanaInicio(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         loadUi('InterfazGrafica/ventanaLogin.ui', self)
#         self.btnIngresar.clicked.connect(self.validar_ingreso)
#         self.btnRegistrar.clicked.connect(self.abrir_ventana_Registro)
#         self.txtCedula.textChanged.connect(self.validar_cedula)  # Conectar la señal textChanged a la función validar_cedula

#     def abrir_ventana_Registro(self):
#         ventana_registro = VentanaRegistro(self)
#         ventana_registro.show()

#     def validar_cedula(self):
#         # Obtener el texto actual del campo txtCedula
#         texto = self.txtCedula.text()
#         # Verificar si el texto está vacío
#         if not texto:
#             # Mostrar un mensaje de error
#             QMessageBox.critical(self, "Error", "El campo Cédula no puede estar vacío")
#             return
#         # Verificar si el texto contiene algún carácter que no sea un número
#         if not texto.isnumeric():
#             # Eliminar el último carácter ingresado si no es un número
#             self.txtCedula.setText(texto[:-1])

#     def validar_ingreso(self):
#         # Obtener el texto actual del campo txtCedula
#         cedula = self.txtCedula.text()
#         # Verificar si el campo está vacío
#         if not cedula:
#             # Mostrar un mensaje de error
#             QMessageBox.critical(self, "Error", "El campo Cédula no puede estar vacío")
#             return
#         # Realizar otras validaciones y acciones necesarias para el ingreso
#         rol = "Propietario" if self.rbPropietario.isChecked() else "Inquilino"
#         if ingresarSistema(rol, cedula):
#             # Si la función ingresarSistema devuelve True, el ingreso fue exitoso
#             QMessageBox.information(self, "Ingreso exitoso", "¡Bienvenido!")
#         else:
#             QMessageBox.critical(self, "Error", "No se pudo ingresar al sistema. Verifique sus credenciales.")

# cedulaUsuario = ''
# rolUsuario = ''

# def ingresarSistema(rol,cedula):
#     global cedulaUsuario, rolUsuario

#     if(existeUsuario(cedula) == True) : 
#         if(rol == "Propietario"):
#             if(existePropietario(cedula) == True):
#                 rolUsuario = rol
#                 cedulaUsuario = cedula
#                 return True
#             else: 
#                 return False
#         else:
#             if(existeInquilinoBD(cedula) == True):
#                 rolUsuario = rol
#                 cedulaUsuario = cedula
#                 return True
#             else: 
#                 return False 
#     else: 
#         return False

#---------------------------------------TERMINA VALIDACIÓN LOGIN------------------------------------#

#-------------------------------------REGISTRAR PROPIETARIO NUEVO-------------------------------------#
#llama la ventanaRegistrarUsuari (cuando el propietario no esta registrado para acceder)
class VentanaRegistro(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarUsuario.ui', self)
        self.txtCedula.textChanged.connect(self.validar_queSeaNum)
        self.txtTelefono.textChanged.connect(self.validar_queSeaNum)  # esto es para validar campo de texto
        self.btnRegistrar.clicked.connect(self.validar_ingreso)       # BOTON
    def validar_queSeaNum(self):
        # Obtener el texto actual del campo txtCedula y txtTelefono
        cedula = self.txtCedula.text()
        telefono = self.txtTelefono.text()

        # Verificar si el texto contiene algún carácter que no sea un número
        if not cedula.isnumeric() and cedula:
            # Eliminar el último carácter ingresado si no es un número
            self.txtCedula.setText(cedula[:-1])

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

        # Verificar que todos los campos requeridos no estén vacíos
        if not nombre or not apellido1 or not apellido2 or not correo or not cedula or not telefono:
            QMessageBox.critical(self, "Error", "Complete todos los campos solicitados")
        else:
            QMessageBox.information(self, "Éxito", "El registro se realizó correctamente")

          




        

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
        loadUi('InterfazGrafica/ventanaEnviarMjs.ui',self.parent)
        self.parent.show()

class VentanaRecibidos(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaMjsRecibidos.ui',self.parent)
        self.parent.show()

class VentanaEnviados(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaMjsEnviados.ui',self.parent)
        self.parent.show()

class VentanaMantenimientoInq(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarManteInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnVizualizarSolicitud.clicked.connect(self.abrir_ventana_visualizar_mante)
        self.btnRegisSolicitud.clicked.connect(self.abrir_ventana_visualizar_mante)
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
   
class VentanaVisualizarMante(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarManteInquilino.ui',self.parent)
        self.parent.show()

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

#-- VENTANA PROPIEDADES
class VentanaRegistrarPropiedades(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarPropiedades.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnRegistrar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnVisualizar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnEditar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnEliminar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnVolver.clicked.connect(self.abrir_ventana_Registrar)

    def abrir_ventana_Registrar(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnRegistrar:
            ventana_visualizar = VentanaRegistrar(self)
        elif sender_button == self.btnVisualizar:
            ventana_visualizar = VentanaVisualizar(self)
        elif sender_button == self.btnEditar:
            ventana_visualizar = VentanaEditar(self)
            ventana_visualizar.show()
        elif sender_button == self.btnEliminar:
            ventana_visualizar = VentanaEliminar(self)
            ventana_visualizar.show()
        elif sender_button == self.btnVolver:
            ventana_inicio_propietarios = VentanaInicioPropietarios()
            ventana_inicio_propietarios.show()
            self.close()

class VentanaRegistrar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaRegistrarPropiedades.ui',self.parent)
        self.parent.show()

class VentanaVisualizar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaVisualizarPropiedades.ui',self.parent)
        self.parent.show()
        
class VentanaEditar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEditarPropiedades.ui',self.parent)
        self.parent.show()

class VentanaEliminar(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        loadUi('InterfazGrafica/ventanaEliminarPropiedades.ui',self.parent)
        self.parent.show()

#--

# VENTANA INQUILINOS - PROPIETARIOS
class VentanaRegistrarInquilino(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('InterfazGrafica/ventanaRegistrarInquilino.ui', self)

        # Conectar los botones a los métodos correspondientes
        self.btnRegistrar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnVisualizar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnEditar.clicked.connect(self.abrir_ventana_Registrar)
        self.btnVolver.clicked.connect(self.abrir_ventana_Registrar)

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

    def abrir_ventana_Registrar(self):
        sender_button = self.sender()  # Obtener el botón que envió la señal
        if sender_button == self.btnVolver:
            self.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_inicio.show()
    sys.exit(app.exec_())




