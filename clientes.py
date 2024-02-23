from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conexionDB


class VentanaClientes(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vClientes.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vClientes.ui', self)

        # Configuracion de la Tabla
        # -- alterar nombres de columnas --
        self.cTabla.setHorizontalHeaderLabels(['DNI', 'Apellido y Nombres', 'Télefono'])
        # -- No permite editar la tabla --
        self.cTabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # -- Permite seleccionar toda la fila --
        self.cTabla.setSelectionBehavior(QTableWidget.SelectRows)
        # -- Permite seleccionar una fila a la vez --
        self.cTabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # -- Colocar punto susppensivo(...) cuando el texto es largo --
        self.cTabla.setTextElideMode(Qt.ElideRight)
        # -- Desabilitar el ajuste de texto --
        self.cTabla.setWordWrap(False)
        # -- Desabilitar el resaltado del encabezado al seleccionar fila --
        self.cTabla.horizontalHeader().setHighlightSections(False)
        # -- Ocultar el enzabezado vertical --
        self.cTabla.verticalHeader().setVisible(False)
        # -- Fondo alernado entre fila de por medio --
        self.cTabla.setAlternatingRowColors(True)
        # -- Altura de la fila --
        self.cTabla.verticalHeader().setDefaultSectionSize(20)
        # -- Ancho de columna --
        for indice, ancho in enumerate((100, 424, 125), start=0):
            self.cTabla.setColumnWidth(indice, ancho)

        # Muestra los registro de la tabla al abrir la ventana
        self.mostrarClientes()

        # Acciones de botones
        self.btn_agregar_cliente.clicked.connect(lambda: self.agregar())
        self.btn_modificar_cliente.clicked.connect(lambda: self.modificar())
        self.btn_eliminar_cliente.clicked.connect(lambda: self.eliminar())
        self.btn_cancelar_cliente.clicked.connect(lambda: self.calcelar())
        self.btn_buscar_cliente.clicked.connect(lambda: self.buscar())
        self.btn_mostrar_cliente.clicked.connect(lambda: self.mostrarTodo())
        
        # Recuperar informacion
            # Ver si una fila esta seleccionada
        self.cTabla.cellClicked.connect(lambda: self.seleccionFila())

    # METODOS
    def mostrarClientes(self):
        # Iniciamos la fila en 0
        self.cTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        listClientes=conex.consultarClientes()
        for cliente in listClientes:
            self.cTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.cTabla.setItem(indiceControl, 0, QTableWidgetItem(str(cliente[0])))
            self.cTabla.setItem(indiceControl, 1, QTableWidgetItem(str(cliente[1])))
            self.cTabla.setItem(indiceControl, 2, QTableWidgetItem(str(cliente[2])))
            indiceControl+=1
        # Permite actiar y desactivar botones
        self.btn_agregar_cliente.setEnabled(True)
        self.btn_modificar_cliente.setEnabled(False)
        self.btn_eliminar_cliente.setEnabled(False)
        self.btn_cancelar_cliente.setEnabled(True)

    def mostrarBusquedaClientes(self, buscarApeNom):
        # Iniciamos la fila en 0
        self.cTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        listClientes=conex.buscarCliente(buscarApeNom)
        for cliente in listClientes:
            self.cTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.cTabla.setItem(indiceControl, 0, QTableWidgetItem(str(cliente[0])))
            self.cTabla.setItem(indiceControl, 1, QTableWidgetItem(str(cliente[1])))
            self.cTabla.setItem(indiceControl, 2, QTableWidgetItem(str(cliente[2])))
            indiceControl+=1

    # Recuperar datos de la fila seleccionada
    def seleccionFila(self):
        # Selecciona los valores en columna 1, 2 y 3
        dni=self.cTabla.selectedIndexes()[0].data()
        apeNom=self.cTabla.selectedIndexes()[1].data()
        tel=self.cTabla.selectedIndexes()[2].data()
        # Asignar a los QLineEdit
        self.cDni.setText(dni)
        self.cApeNom.setText(apeNom)
        self.cTelefono.setText(tel)
        # Permite actiar y desactivar botones
        self.btn_agregar_cliente.setEnabled(False)
        self.btn_modificar_cliente.setEnabled(True)
        self.btn_eliminar_cliente.setEnabled(True)
        self.btn_cancelar_cliente.setEnabled(True)

    # BOTONES 
    def agregar(self):
        try: 
            # Validar campos
            if self.validarCampos():
                return False
            # Recuperar los valores
            dni=self.cDni.text()
            tel=self.cTelefono.text()
            apeNom=self.cApeNom.text().upper()
            datosCliente=(dni, apeNom, tel)
            # Instancia(objeto) de conexionDB
            conex=conexionDB.conexion()
            # Inicia conexion e insertar en la BBDD
            conex.agregarCliente(datosCliente)
            self.mostrarClientes()
            self.vaciarCeldasDatosCliente()
        except:
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Error, el DNI existe")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()

    def modificar(self):
        # Validar campos
        if self.validarCampos():
            return False
        # Recuperar los valores
        dni=self.cDni.text()
        tel=self.cTelefono.text()
        apeNom=self.cApeNom.text().upper()
        datosCliente=(apeNom, tel, dni)
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Inicia conexion e insertar en la BBDD
        conex.modificarCliente(datosCliente)
        self.mostrarClientes()
        self.vaciarCeldasDatosCliente()

    def eliminar(self):
        dni=self.cDni.text()
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        conex.borrarCliente(dni)
        self.mostrarClientes()
        self.vaciarCeldasDatosCliente()

    def calcelar(self):
        self.mostrarClientes()
        self.vaciarCeldasDatosCliente()

    def buscar(self):
        if self.cBuscar.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Campo BUSCAR vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:    
            buscarApeNom=self.cBuscar.text().upper()
            self.mostrarBusquedaClientes(buscarApeNom)

    def mostrarTodo(self):
        self.mostrarClientes()
        self.cBuscar.setText("")
        
    def vaciarCeldasDatosCliente(self):
        self.cDni.setText("")
        self.cApeNom.setText("")
        self.cTelefono.setText("")

    def validarCampos(self):
        if self.cDni.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Campo DNI vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if not self.cDni.text().isdigit():
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Error en el campo DNI, solo se puede ingresar un valor numerico.")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if len(self.cDni.text())!=8:
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El DNI debe contener 8 digitos (En caso de tener 7 digitos, agregar un cero al comienzo)")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if self.cApeNom.text()=='':
                alerta=QMessageBox()
                alerta.setText("Campo APELLIDO Y NOMBRE vacio")
                alerta.setIcon(QMessageBox.Information)
                alerta.exec()
                return True
        separarNombre=self.cApeNom.text().split(' ')
        for nombre in separarNombre:
            if not nombre.isalpha():
                alerta=QMessageBox()
                alerta.setWindowTitle('Mensaje')
                alerta.setText("Error en el campo APELLIDO Y NOMBRE, solo puede contener letras")
                alerta.setIcon(QMessageBox.Information)
                alerta.exec()
                return True
        if not self.cTelefono.text()=='' and not self.cTelefono.text().isdigit():
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Error en el campo TELEFONO, solo se puede ingresar un valor numerico.")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True