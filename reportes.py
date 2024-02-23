from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conexionDB
import clientesDesdeFact
import fechaDesdeReporte
import facturacionDesdeReportes
import servDesdeReportes

class VentanaReportes(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vReportes.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vReportes.ui', self)

        # Configuracion de la Tabla
        # -- alterar nombres de columnas --
        self.rTabla.setHorizontalHeaderLabels(['N° Factura', 'Apellido y Nombre', 'DNI', 'Servicio', 'Fecha', 'Monto', 'Metodo de pago', 'Entrada/Salida', 'Mes/es Pago/s', 'Descripcion'])
        # -- No permite editar la tabla --
        self.rTabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # -- Permite seleccionar toda la fila --
        self.rTabla.setSelectionBehavior(QTableWidget.SelectRows)
        # -- Permite seleccionar una fila a la vez --
        self.rTabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # -- Colocar punto susppensivo(...) cuando el texto es largo --
        self.rTabla.setTextElideMode(Qt.ElideRight)
        # -- Desabilitar el ajuste de texto --
        self.rTabla.setWordWrap(False)
        # -- Desabilitar el resaltado del encabezado al seleccionar fila --
        self.rTabla.horizontalHeader().setHighlightSections(False)
        # -- Ocultar el enzabezado vertical --
        self.rTabla.verticalHeader().setVisible(False)
        # -- Fondo alernado entre fila de por medio --
        self.rTabla.setAlternatingRowColors(True)
        # -- Altura de la fila --
        self.rTabla.verticalHeader().setDefaultSectionSize(20)
        # -- Ancho de columna --
        for indice, ancho in enumerate((70, 180, 80, 140, 80, 90, 120, 95, 100, 160), start=0):
            self.rTabla.setColumnWidth(indice, ancho)

        # Muestra los registro de la tabla al abrir la ventana
        self.mostrarFacturacion()

        # Acciones de botones
        self.btn_buscar_apeNom.clicked.connect(lambda: self.mostrarFactDeCliente())
        self.btn_mostrar.clicked.connect(lambda: self.mostrarFacturacion())
        self.btn_cancelar.clicked.connect(lambda: self.vaciarCeldasDatosReportes())
        self.btn_buscar_fecha.clicked.connect(lambda: self.mostrarFacturacionPorFecha())
        self.btn_buscar_servicio.clicked.connect(lambda: self.mostrarFacturacionPorServicio())
        self.btn_buscar_fecha_serv.clicked.connect(lambda: self.mostrarFacturacionPorFechaServicio())

        # Boton para buscar CLIENTE y Objeto (instancia) de VentanaCliente
        self.btn_buscar_cliente.clicked.connect(self.obtenerBusquedaCliente)
        self.vtnClientesDesdeReportes = clientesDesdeFact.VentanaClientesDesdeFact()
        
        # Botones para obtener FECHAS y Objeto (instancia) de Fecha
        self.btn_buscar_fecha_desde.clicked.connect(self.obtenerBusquedaFechaUno)
        self.btn_buscar_fecha_hasta.clicked.connect(self.obtenerBusquedaFechaDos)
        self.vtnFechaDesdeReportes = fechaDesdeReporte.VentanaFechaDesdeFact()

        # Botones para obtener las modificaciones de FACTURAS y Objeto (instancia) de Reportes
        self.btn_guardarCambios.clicked.connect(self.modificarDatosReportes)
        self.btn_modificar.clicked.connect(self.obtenerDatosClienteModificados)
        self.btn_actualizar.clicked.connect(self.cargarFilasModificadas)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.vtnFactDesdeReportes = facturacionDesdeReportes.VentanaFactDesdeReportes()

        # Boton para buscar SERVICIO Objeto (instancia) de Servicios
        self.btn_buscar_servicio_servicio.clicked.connect(self.obtenerBusquedaServicio)
        self.vtnServDesdeReportes = servDesdeReportes.VentanaServDesdeReportes()

        # Recuperar informacion
            # Ver si una fila esta seleccionada
        self.rTabla.cellClicked.connect(lambda: self.seleccionFila())

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
    
    def mostrarFacturacionPorFechaServicio(self):
        if self.r_fecha_desde.text()=='' or self.r_nom_serv.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Los campo se encuentran vacios")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:
        # Accion
            if self.r_fecha_hasta.text()=='':
                self.mostrarFacturacionUnaFechaServicio()
            else:
                self.mostrarFacturacionDosFechaServicio()

    def enviarInformacionServicio(self):
        nomServ=self.sNom.text()
        return nomServ
    
    def mostrarFacturacion(self):
        # Iniciamos la fila en 0
        self.rTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        listFacturas=conex.consultarReportes()
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.rTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1
        self.vaciarCeldasDatosReportes()

    def mostrarFactDeCliente(self):
        if self.r_dni.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Los campo se encuentran vacios")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:
            # Iniciamos la fila en 0
            self.rTabla.setRowCount(0)
            # Indice(recorrido) de control
            indiceControl=0
            # Instancia(objeto) de conexionDB
            conex=conexionDB.conexion()
            # Consultar clientes
            listFacturas=conex.consultarReportesCliente(self.r_dni.text())
            #listFacturas=conex.consultarFacturacion()
            for factura in listFacturas:
                self.rTabla.setRowCount(indiceControl+1)
                # Mosrar valores en columna 1, 2  y 3
                self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
                self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
                self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
                self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
                self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
                self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
                self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
                self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
                self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
                self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
                indiceControl+=1
    
    def mostrarFacturacionUnaFecha(self):
        # Iniciamos la fila en 0
        self.rTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fecha=self.r_fecha_desde.text()
        listFacturas=conex.consultarReportesUnaFecha(fecha)
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.rTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1

    def mostrarFacturacionDosFecha(self):
        # Iniciamos la fila en 0
        self.rTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fechaDesde=self.r_fecha_desde.text()
        fechaHasta=self.r_fecha_hasta.text()
        fechas=(fechaDesde,fechaHasta)
        listFacturas=conex.consultarReportesFechas(fechas)
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.rTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1
    
    def mostrarFacturacionUnaFechaServicio(self):
        # Iniciamos la fila en 0
        self.rTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fecha=self.r_fecha_desde.text()
        servicio=self.r_nom_serv.text()
        fechaServ=(fecha, servicio)
        listFacturas=conex.consultarReportesUnaFechaServicio(fechaServ)
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.rTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1

    def mostrarFacturacionDosFechaServicio(self):
        # Iniciamos la fila en 0
        self.rTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        fechaDesde=self.r_fecha_desde.text()
        fechaHasta=self.r_fecha_hasta.text()
        servicio=self.r_nom_serv.text()
        fechasServ=(fechaDesde,fechaHasta,servicio)
        listFacturas=conex.consultarReportesFechasServicio(fechasServ)
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.rTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1

    def mostrarFacturacionPorServicio(self):
        # Validar campos
        if self.r_nom_serv.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
        else:
        # Accion
            # Iniciamos la fila en 0
            self.rTabla.setRowCount(0)
            # Indice(recorrido) de control
            indiceControl=0
            # Instancia(objeto) de conexionDB
            conex=conexionDB.conexion()
            # Consultar clientes
            listFacturas=conex.consultarReportesServicio(self.r_nom_serv.text())
            #listFacturas=conex.consultarFacturacion()
            for factura in listFacturas:
                self.rTabla.setRowCount(indiceControl+1)
                # Mosrar valores en columna 1, 2  y 3
                self.rTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
                self.rTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
                self.rTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
                self.rTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
                self.rTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
                self.rTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
                self.rTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
                self.rTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
                self.rTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
                self.rTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
                indiceControl+=1

    # Recuperar datos de la fila seleccionada
    def seleccionFila(self):
        #self.vaciarCeldasDatosFactura()
        # Selecciona los valores de todas las columnas
        numFact=self.rTabla.selectedIndexes()[0].data()
        nomApe=self.rTabla.selectedIndexes()[1].data()
        dni=self.rTabla.selectedIndexes()[2].data()
        serv=self.rTabla.selectedIndexes()[3].data()
        fecha=self.rTabla.selectedIndexes()[4].data()
        monto=self.rTabla.selectedIndexes()[5].data()
        metPago=self.rTabla.selectedIndexes()[6].data()
        entSal=self.rTabla.selectedIndexes()[7].data()
        mesPago=self.rTabla.selectedIndexes()[8].data()
        descrip=self.rTabla.selectedIndexes()[9].data()
        # Asignar a los QLineEdit
        self.rNumFact.setText(numFact)
        self.rNomApe.setText(nomApe)
        self.rDNI.setText(dni)
        self.rServicio.setText(serv)
        self.rFecha.setText(fecha)
        self.rMonto.setText(monto)
        self.rMetPago.setText(metPago)
        self.rEntSal.setText(entSal)
        self.rMesPago.setText(mesPago)
        self.rDescripcion.setText(descrip)
        # return sirve para enviar informacion a facturacionDesdeReporte para modificar
        return (numFact, nomApe, dni, serv, monto, metPago, entSal, mesPago, descrip)

    # Abrir ventana para buscar cliente
    def obtenerBusquedaCliente(self):
        # Ejecutar ventana
        self.vtnClientesDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnClientesDesdeReportes.enviarInformacionCliente()
        self.r_dni.setText(datos[0])
        self.r_ape_nom.setText(datos[1])

    # Abrir ventana para buscar cliente
    def obtenerBusquedaFechaUno(self):
        # Ejecutar ventana
        self.vtnFechaDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnFechaDesdeReportes.enviarInformacionFechaUno()
        self.r_fecha_desde.setText(str(datos))
        #self.vaciarCeldasDatosReportes()

    def obtenerBusquedaFechaDos(self):
        # Ejecutar ventana
        self.vtnFechaDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnFechaDesdeReportes.enviarInformacionFechaDos()
        self.r_fecha_hasta.setText(str(datos))
        #self.vaciarCeldasDatosReportes()

    def vaciarCeldasDatosReportes(self):
        self.r_fecha_desde.setText("")
        self.r_fecha_hasta.setText("")
        self.r_ape_nom.setText("")
        self.r_dni.setText("")
        self.r_nom_serv.setText("")

    def vaciarCeldasDatosFactura(self):
        self.rNumFact.setText("")
        self.rNomApe.setText("")
        self.rDNI.setText("")
        self.rServicio.setText("")
        self.rFecha.setText("")
        self.rMonto.setText("")
        self.rMetPago.setText("")
        self.rEntSal.setText("")
        self.rMesPago.setText("")
        self.rDescripcion.setText("")

    # Abrir ventana para modificar factura
    def obtenerDatosClienteModificados(self):
        # Ejecutar ventana
        self.vtnFactDesdeReportes.vaciarCeldasDatosFactura()
        self.vtnFactDesdeReportes.obtenerSel(self.seleccionFila())
        self.vtnFactDesdeReportes.exec_()

    def cargarFilasModificadas(self):
        #self.vaciarCeldasDatosFactura()
        datos=self.vtnFactDesdeReportes.enviarInformacionFactura()
        self.rNomApe.setText(datos[0])
        self.rDNI.setText(datos[1])
        self.rServicio.setText(datos[2])
        self.rMonto.setText(datos[3])
        self.rMetPago.setText(datos[4])
        self.rEntSal.setText(datos[5])
        self.rMesPago.setText(datos[6])
        self.rDescripcion.setText(datos[7])

    def modificarDatosReportes(self):
        # Validar campos
        #if self.validarCampos():
        #    return False
        numFact=self.rNumFact.text().upper()
        #nomApe=self.rNomApe.text().upper()
        dni=self.rDNI.text().upper()
        serv=self.rServicio.text().upper()
        monto=self.rMonto.text().upper()
        metPago=self.rMetPago.text().upper()
        entSal=self.rEntSal.text().upper()
        mesPago=self.rMesPago.text().upper()
        descrip=self.rDescripcion.toPlainText().upper()
        datosFacturaRep=(dni, serv, monto, metPago, entSal, mesPago, descrip, numFact)
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Inicia conexion e insertar en la BBDD
        conex.modificarFacturaReporte(datosFacturaRep)
        self.mostrarFacturacion()
        self.vaciarCeldasDatosFactura()
        self.groupBoxDatosSelec.setChecked(False)
    
    def eliminar(self):
        numFact=self.rNumFact.text()
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        conex.borrarFactura(numFact)
        self.mostrarFacturacion()
        self.groupBoxDatosSelec.setChecked(False)
        self.vaciarCeldasDatosFactura()

    def obtenerBusquedaServicio(self):
        # Ejecutar ventana
        self.vtnServDesdeReportes.exec_()
        # Retornar informacion
        datos=self.vtnServDesdeReportes.enviarInformacionServicio()
        self.r_nom_serv.setText(datos)