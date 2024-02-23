from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conexionDB

class VentanaClientesDesdeFact(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vClientesDesdeFact.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vClientesDesdeFact.ui', self)

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
        self.btn_buscar_cliente.clicked.connect(lambda: self.buscar())
        self.btn_mostrar_cliente.clicked.connect(lambda: self.mostrarTodo())
        self.btn_aceptar_cliente.clicked.connect(self.close)
        
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

    # Metodo que llama Facturacion para obtener el DNI y el Apellido y Nombre del cliente seleccionado
    def enviarInformacionCliente(self):
        dni=self.cDni.text()
        apeNom=self.cApeNom.text()
        return (dni, apeNom)
        
    def buscar(self):
        buscarApeNom=self.cBuscar.text().upper()
        self.mostrarBusquedaClientes(buscarApeNom)

    def mostrarTodo(self):
        self.mostrarClientes()
        self.cBuscar.setText("")
        
    def vaciarCeldasDatosCliente(self):
        self.cDni.setText("")
        self.cApeNom.setText("")
        self.cTelefono.setText("")

