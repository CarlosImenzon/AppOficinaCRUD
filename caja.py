from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import conexionDB
from datetime import date
import fechaDesdeReporte

class VentanaCaja(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vCaja.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vCaja.ui', self)

        # Configuracion de la Tabla
        # -- alterar nombres de columnas --
        self.cjTabla.setHorizontalHeaderLabels(['N° Factura', 'Apellido y Nombre', 'DNI', 'Servicio', 'Fecha', 'Monto', 'Metodo de pago', 'Entrada/Salida', 'Mes/es Pago/s', 'Descripcion'])
        # -- No permite editar la tabla --
        self.cjTabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # -- Permite seleccionar toda la fila --
        self.cjTabla.setSelectionBehavior(QTableWidget.SelectRows)
        # -- Permite seleccionar una fila a la vez --
        self.cjTabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # -- Colocar punto susppensivo(...) cuando el texto es largo --
        self.cjTabla.setTextElideMode(Qt.ElideRight)
        # -- Desabilitar el ajuste de texto --
        self.cjTabla.setWordWrap(False)
        # -- Desabilitar el resaltado del encabezado al seleccionar fila --
        self.cjTabla.horizontalHeader().setHighlightSections(False)
        # -- Ocultar el enzabezado vertical --
        self.cjTabla.verticalHeader().setVisible(False)
        # -- Fondo alernado entre fila de por medio --
        self.cjTabla.setAlternatingRowColors(True)
        # -- Altura de la fila --
        self.cjTabla.verticalHeader().setDefaultSectionSize(20)
        # -- Ancho de columna --
        for indice, ancho in enumerate((70, 180, 80, 140, 80, 90, 120, 95, 100, 160), start=0):
            self.cjTabla.setColumnWidth(indice, ancho)

        # Acciones de botones
        self.btn_buscar_fecha.clicked.connect(lambda: self.mostrarFacturacionPorFecha())
        self.btn_cancelar.clicked.connect(lambda: self.vaciarCeldasDatosCaja())
    
        # Botones obtener fecha y Objeto (instancia) de Fecha
        self.btn_buscar_fecha_desde.clicked.connect(self.obtenerBusquedaFechaUno)
        self.btn_buscar_fecha_hasta.clicked.connect(self.obtenerBusquedaFechaDos)
        self.vtnFechaDesdeReportes = fechaDesdeReporte.VentanaFechaDesdeFact()

    # METODOS

    def mostrarFacturacionPorFecha(self):
        # Validar datos
        if self.r_fecha_desde.text()=='' and self.r_fecha_hasta.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Los campo se encuentran vacios")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:
            # Acciones
            if self.r_fecha_hasta.text()=='':
                self.mostrarFacturacionUnaFecha()
            else:
                self.mostrarFacturacionDosFecha()
    
    def mostrarFacturacionUnaFecha(self):
        # Iniciamos la fila en 0
        self.cjTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fecha=self.r_fecha_desde.text()
        fechaIngreso=(fecha, 'INGRESO')
        fechaEgreso=(fecha, 'EGRESO')
        listFacturas=conex.consultarReportesUnaFecha(fecha)
        self.listFacturasIngresos=conex.consultarFactCajaIngEgre(fechaIngreso)
        self.listFacturasEgresos=conex.consultarFactCajaIngEgre(fechaEgreso)
        self.obtenerIngresos()
        self.obtenerEgresos()
        self.obtenerTotal()
        for factura in listFacturas:
            self.cjTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.cjTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.cjTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.cjTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.cjTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.cjTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.cjTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.cjTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.cjTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.cjTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.cjTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1

    def mostrarFacturacionDosFecha(self):
        # Iniciamos la fila en 0
        self.cjTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fechaDesde=self.r_fecha_desde.text()
        fechaHasta=self.r_fecha_hasta.text()
        fechas=(fechaDesde, fechaHasta)
        fechasIngreso=(fechaDesde,fechaHasta, 'INGRESO')
        fechasEgreso=(fechaDesde,fechaHasta, 'EGRESO')
        listFacturas=conex.consultarReportesFechas(fechas)
        self.listFacturasIngresosFechas=conex.consultarFactCajaIngEgreFechas(fechasIngreso)
        self.listFacturasEgresosFechas=conex.consultarFactCajaIngEgreFechas(fechasEgreso)
        self.obtenerIngresosFechas()
        self.obtenerEgresosFechas()
        self.obtenerTotal()
        for factura in listFacturas:
            self.cjTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.cjTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.cjTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.cjTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.cjTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.cjTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.cjTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.cjTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.cjTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.cjTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.cjTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1

    # Metodos de mostrarFacturacionUnaFecha
    def obtenerIngresos(self):
        self.sumaIngreso=0
        for factura in self.listFacturasIngresos:
            self.sumaIngreso+=factura[-5]
        self.ingreso.setText(str(self.sumaIngreso))
    
    def obtenerEgresos(self):
        self.sumaEgreso=0
        for factura in self.listFacturasEgresos:
            self.sumaEgreso+=factura[-5]
        self.egreso.setText(str(self.sumaEgreso))
    
    # Metodos de mostrarFacturacionDosFecha
    def obtenerIngresosFechas(self):
        self.sumaIngreso=0
        for factura in self.listFacturasIngresosFechas:
            self.sumaIngreso+=factura[-5]
        self.ingreso.setText(str(self.sumaIngreso))
    
    def obtenerEgresosFechas(self):
        self.sumaEgreso=0
        for factura in self.listFacturasEgresosFechas:
            self.sumaEgreso+=factura[-5]
        self.egreso.setText(str(self.sumaEgreso))
    
    def obtenerTotal(self):
        sumaTotal=self.sumaIngreso-self.sumaEgreso
        self.total.setText(str(sumaTotal))

    # Obtener Fecha (Se usa la misma ventana que la de reportes)
    def obtenerBusquedaFechaUno(self):
        # Ejecutar ventana
        self.vtnFechaDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnFechaDesdeReportes.enviarInformacionFechaUno()
        self.r_fecha_desde.setText(str(datos))

    # Obtener Fechas (Se usa la misma ventana que la de reportes)
    def obtenerBusquedaFechaDos(self):
        # Ejecutar ventana
        self.vtnFechaDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnFechaDesdeReportes.enviarInformacionFechaDos()
        self.r_fecha_hasta.setText(str(datos))

    # Limpiar datos
    def vaciarCeldasDatosCaja(self):
        self.r_fecha_desde.setText("")
        self.r_fecha_hasta.setText("")
        self.cjTabla.clearContents()
        self.ingreso.setText("")
        self.egreso.setText("")
        self.total.setText("")