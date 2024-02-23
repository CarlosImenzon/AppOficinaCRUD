from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conexionDB

class VentanaServicios(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vServicios.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vServicios.ui', self)

        # Configuracion de la Tabla
        # -- alterar nombres de columnas --
        self.sTabla.setHorizontalHeaderLabels(['Nombre'])
        # -- No permite editar la tabla --
        self.sTabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # -- Permite seleccionar toda la fila --
        self.sTabla.setSelectionBehavior(QTableWidget.SelectRows)
        # -- Permite seleccionar una fila a la vez --
        self.sTabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # -- Colocar punto susppensivo(...) cuando el texto es largo --
        self.sTabla.setTextElideMode(Qt.ElideRight)
        # -- Desabilitar el ajuste de texto --
        self.sTabla.setWordWrap(False)
        # -- Desabilitar el resaltado del encabezado al seleccionar fila --
        self.sTabla.horizontalHeader().setHighlightSections(False)
        # -- Ocultar el enzabezado vertical --
        self.sTabla.verticalHeader().setVisible(False)
        # -- Fondo alernado entre fila de por medio --
        self.sTabla.setAlternatingRowColors(True)
        # -- Altura de la fila --
        self.sTabla.verticalHeader().setDefaultSectionSize(20)
        # -- Ancho de columna --
        self.sTabla.setColumnWidth(0, 639)

        # Muestra los registro de la tabla al abrir la ventana
        self.mostrarServicios()

        # Acciones de botones
        self.btn_agregar_servicio.clicked.connect(lambda: self.agregar())
        self.btn_eliminar_servicio.clicked.connect(lambda: self.eliminar())
        self.btn_cancelar_servicio.clicked.connect(lambda: self.calcelar())
        self.btn_buscar_servicio.clicked.connect(lambda: self.buscar())
        self.btn_mostrar_servicio.clicked.connect(lambda: self.mostrarTodo())
        
        # Recuperar informacion
            # Ver si una fila esta seleccionada
        self.sTabla.cellClicked.connect(lambda: self.seleccionFila())

    # METODOS
    def mostrarServicios(self):
        # Iniciamos la fila en 0
        self.sTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar servicios
        listServicios=conex.consultarServicios()
        for servicio in listServicios:
            self.sTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1
            self.sTabla.setItem(indiceControl, 0, QTableWidgetItem(str(servicio[0])))
            indiceControl+=1
        # Permite actiar y desactivar botones
        self.btn_agregar_servicio.setEnabled(True)
        self.btn_eliminar_servicio.setEnabled(False)
        self.btn_cancelar_servicio.setEnabled(False)

    def mostrarBusquedaServicios(self, buscarNom):
        # Iniciamos la fila en 0
        self.sTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar servicios
        listServicios=conex.buscarServicio(buscarNom)
        for servicio in listServicios:
            self.sTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1
            self.sTabla.setItem(indiceControl, 0, QTableWidgetItem(str(servicio[0])))
            indiceControl+=1

    # Recuperar datos de la fila seleccionada
    def seleccionFila(self):
        # Selecciona los valores en columna 1, 2 y 3
        nom=self.sTabla.selectedIndexes()[0].data()
        # Asignar a los QLineEdit
        self.sNom.setText(nom)
        # Permite actiar y desactivar botones
        self.btn_agregar_servicio.setEnabled(False)
        self.btn_eliminar_servicio.setEnabled(True)
        self.btn_cancelar_servicio.setEnabled(True)

    # BOTONES 
    def agregar(self):
        try:
            if self.sNom.text()=='':
                alerta=QMessageBox()
                alerta.setWindowTitle('Mensaje')
                alerta.setText("El campo 'NOMBRE DEL SERVICIO' se encuentra vacio")
                alerta.setIcon(QMessageBox.Information)
                alerta.exec()
                return True
            # Recuperar los valores
            nom=self.sNom.text().upper()
            #datosServicio=(nom)
            # Instancia(objeto) de conexionDB
            conex=conexionDB.conexion()
            # Inicia conexion e insertar en la BBDD
            conex.agregarServicio(nom)
            self.mostrarServicios()
            self.vaciarCeldasDatosServicio()
        except:
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Error, el NOMBRE DEL SERVICIO existe")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()

    def eliminar(self):
        nom=self.sNom.text()
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar servicios
        conex.borrarServicio(nom)
        self.mostrarServicios()
        self.vaciarCeldasDatosServicio()

    def calcelar(self):
        self.mostrarServicios()
        self.vaciarCeldasDatosServicio()

    def buscar(self):
        if self.sBuscar.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'BUSCAR' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:
            buscarNomServicio=self.sBuscar.text().upper()
            self.mostrarBusquedaServicios(buscarNomServicio)

    def mostrarTodo(self):
        self.mostrarServicios()
        self.sBuscar.setText("")
        
    def vaciarCeldasDatosServicio(self):
        self.sNom.setText("")
        
