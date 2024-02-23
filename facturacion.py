from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import conexionDB
from datetime import date
import clientesDesdeFact
import serviciosDesdeFact

class VentanaFacturacion(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vFacturacion.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vFacturacion.ui', self)

        # Configuracion de la Tabla
        # -- alterar nombres de columnas --
        self.fTabla.setHorizontalHeaderLabels(['N° Factura', 'Apellido y Nombre', 'DNI', 'Servicio', 'Fecha', 'Monto', 'Metodo de pago', 'Entrada/Salida', 'Mes/es Pago/s', 'Descripcion'])
        # -- No permite editar la tabla --
        self.fTabla.setEditTriggers(QTableWidget.NoEditTriggers)
        # -- Permite seleccionar toda la fila --
        self.fTabla.setSelectionBehavior(QTableWidget.SelectRows)
        # -- Permite seleccionar una fila a la vez --
        self.fTabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # -- Colocar punto susppensivo(...) cuando el texto es largo --
        self.fTabla.setTextElideMode(Qt.ElideRight)
        # -- Desabilitar el ajuste de texto --
        self.fTabla.setWordWrap(False)
        # -- Desabilitar el resaltado del encabezado al seleccionar fila --
        self.fTabla.horizontalHeader().setHighlightSections(False)
        # -- Ocultar el enzabezado vertical --
        self.fTabla.verticalHeader().setVisible(False)
        # -- Fondo alernado entre fila de por medio --
        self.fTabla.setAlternatingRowColors(True)
        # -- Altura de la fila --
        self.fTabla.verticalHeader().setDefaultSectionSize(20)
        # -- Ancho de columna --
        for indice, ancho in enumerate((70, 180, 80, 140, 80, 90, 120, 95, 100, 160), start=0):
            self.fTabla.setColumnWidth(indice, ancho)

        # Colocar fecha del dia por defecto
        self.fFecha.setDate(date.today())

        # Muestra los registro de la tabla al abrir la ventana
        self.mostrarFacturacion()

        # Acciones de botones
        self.btn_agregar_factura.clicked.connect(lambda: self.agregar())
        self.btn_modificar_factura.clicked.connect(lambda: self.modificar())
        self.btn_eliminar_factura.clicked.connect(lambda: self.eliminar())
        self.btn_cancelar_factura.clicked.connect(lambda: self.cancelar())

        # Boton buscar DNI y Objeto (instancia) de VentanaCliente
        self.btn_buscar_dni_factura.clicked.connect(self.obtenerBusquedaCliente)
        self.vtnClientesDesdeFact = clientesDesdeFact.VentanaClientesDesdeFact()

        # Boton buscar SERVICIO y Objeto (instancia) de VentanaCliente
        self.btn_buscar_serv_factura.clicked.connect(self.obtenerBusquedaServicio)
        self.vtnServicioDesdeFact = serviciosDesdeFact.VentanaServiciosDesdeFact()
        
        # Recuperar informacion
            # Ver si una fila esta seleccionada
        self.fTabla.cellClicked.connect(lambda: self.seleccionFila())


    # METODOS
    def mostrarFacturacion(self):
        # Iniciamos la fila en 0
        self.fTabla.setRowCount(0)
        # Indice(recorrido) de control
        indiceControl=0
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        listFacturas=conex.consultarFacturacion(self.mostrarFechaDmA(str(self.fFecha.date().toPyDate())))
        #listFacturas=conex.consultarFacturacion()
        for factura in listFacturas:
            self.fTabla.setRowCount(indiceControl+1)
            # Mosrar valores en columna 1, 2  y 3
            self.fTabla.setItem(indiceControl, 0, QTableWidgetItem(str(factura[0])))
            self.fTabla.setItem(indiceControl, 1, QTableWidgetItem(str(factura[1])))
            self.fTabla.setItem(indiceControl, 2, QTableWidgetItem(str(factura[2])))
            self.fTabla.setItem(indiceControl, 3, QTableWidgetItem(str(factura[3])))
            self.fTabla.setItem(indiceControl, 4, QTableWidgetItem(str(factura[4])))
            self.fTabla.setItem(indiceControl, 5, QTableWidgetItem(str(factura[5])))
            self.fTabla.setItem(indiceControl, 6, QTableWidgetItem(str(factura[6])))
            self.fTabla.setItem(indiceControl, 7, QTableWidgetItem(str(factura[7])))
            self.fTabla.setItem(indiceControl, 8, QTableWidgetItem(str(factura[8])))
            self.fTabla.setItem(indiceControl, 9, QTableWidgetItem(str(factura[9])))
            indiceControl+=1
        # Permite actiar y desactivar botones
        self.btn_agregar_factura.setEnabled(True)
        self.btn_modificar_factura.setEnabled(False)
        self.btn_eliminar_factura.setEnabled(False)
        self.btn_cancelar_factura.setEnabled(True)

    # Recuperar datos de la fila seleccionada
    def seleccionFila(self):
        self.vaciarCeldasDatosFactura()
        # Selecciona los valores de todas las columnas
        numFact=self.fTabla.selectedIndexes()[0].data()
        nomApe=self.fTabla.selectedIndexes()[1].data()
        dni=self.fTabla.selectedIndexes()[2].data()
        serv=self.fTabla.selectedIndexes()[3].data()
        fecha=self.fTabla.selectedIndexes()[4].data()
        monto=self.fTabla.selectedIndexes()[5].data()
        metPago=self.fTabla.selectedIndexes()[6].data()
        entSal=self.fTabla.selectedIndexes()[7].data()
        mesPago=self.fTabla.selectedIndexes()[8].data()
        descrip=self.fTabla.selectedIndexes()[9].data()
        # Asignar a los QLineEdit
        self.fNumFact.setText(numFact)
        self.fnomApe.setText(nomApe)
        self.fDNI.setText(dni)
        self.fServicio.setText(serv)
        #self.fFecha.setText(fecha)
        self.fMonto.setText(monto)
        self.cargarMetPago(metPago)
        self.checkEntradaSalida(entSal)
        self.checkMesPagado(mesPago)
        self.fDescripcion.setText(descrip)
        # Permite actiar y desactivar botones
        self.btn_agregar_factura.setEnabled(False)
        self.btn_modificar_factura.setEnabled(True)
        self.btn_eliminar_factura.setEnabled(True)
        self.btn_cancelar_factura.setEnabled(True)

    # Cargar valor a QComboBox desde BBDD
    def cargarMetPago(self, metPago):
        if metPago =='EFECTIVO':
            self.fMetodoPago.setCurrentText('EFECTIVO')
        if metPago =='TARJETA DE DEBITO':
            self.fMetodoPago.setCurrentText('TARJETA DE DEBITO')
        if metPago =='TARJETA DE CREDITO':
            self.fMetodoPago.setCurrentText('TARJETA DE CREDITO')
        if metPago =='CHEQUE':
            self.fMetodoPago.setCurrentText('CHEQUE')
        if metPago =='DEBITO AUTOMATICO':
            self.fMetodoPago.setCurrentText('DEBITO AUTOMATICO')
        if metPago =='OTRO':
            self.fMetodoPago.setCurrentText('OTRO')

    # Metodo para colocar check Entrada/Salida al seleccionar
    def checkEntradaSalida(self, entSal):
        if entSal=='INGRESO':
            self.fIngreso.setChecked(True)
        else:
            self.fEgreso.setChecked(True)

    # Metodo para colocar check Mes/es pagado/s al seleccionar
    def checkMesPagado(self, mesPago):
        listMeses=mesPago.split('-')
        for mes in listMeses:
            if mes=='ENERO':
                self.fPago_Enero.setChecked(True)
            if mes=='FEBRERO':
                self.fPago_Febrero.setChecked(True)
            if mes=='MARZO':
                self.fPago_Marzo.setChecked(True)
            if mes=='ABRIL':
                self.fPago_Abril.setChecked(True)
            if mes=='MAYO':
                self.fPago_Mayo.setChecked(True)
            if mes=='JUNIO':
                self.fPago_Junio.setChecked(True)
            if mes=='JULIO':
                self.fPago_Julio.setChecked(True)
            if mes=='AGOSTO':
                self.fPago_Agosto.setChecked(True)
            if mes=='SEPTIEMBRE':
                self.fPago_Septiembre.setChecked(True)
            if mes=='OCTUBRE':
                self.fPago_Octubre.setChecked(True)
            if mes=='NOVIEMBRE':
                self.fPago_Noviembre.setChecked(True)
            if mes=='DICIEMBRE':
                self.fPago_Diciembre.setChecked(True)

    # Si el check esta seleccionado, se agrega a la BBDD
    def setCheckEntradaSalida(self):
        if self.fIngreso.isChecked()==True:
            return 'INGRESO'
        if self.fEgreso.isChecked()==True:
            return 'EGRESO'

    # Si el check esta seleccionado, se agrega a la BBDD
    def setCheckMesPagado(self):
        listMesesPagado=[]
        if self.fPago_Enero.isChecked()==True:
            listMesesPagado.append('ENERO')
        if self.fPago_Febrero.isChecked()==True:
            listMesesPagado.append('FEBRERO')
        if self.fPago_Marzo.isChecked()==True:
            listMesesPagado.append('MARZO')
        if self.fPago_Abril.isChecked()==True:
            listMesesPagado.append('ABRIL')
        if self.fPago_Mayo.isChecked()==True:
            listMesesPagado.append('MAYO')
        if self.fPago_Junio.isChecked()==True:
            listMesesPagado.append('JUNIO')
        if self.fPago_Julio.isChecked()==True:
            listMesesPagado.append('JULIO')
        if self.fPago_Agosto.isChecked()==True:
            listMesesPagado.append('AGOSTO')
        if self.fPago_Septiembre.isChecked()==True:
            listMesesPagado.append('SEPTIEMBRE')
        if self.fPago_Octubre.isChecked()==True:
            listMesesPagado.append('OCTUBRE')
        if self.fPago_Noviembre.isChecked()==True:
            listMesesPagado.append('NOVIEMBRE')
        if self.fPago_Diciembre.isChecked()==True:
            listMesesPagado.append('DICIEMBRE')
        stringMesesPagado= '-'.join(listMesesPagado)
        return stringMesesPagado

    # BOTONES 
    def agregar(self):
        # Validar campos
        if self.validarCampos():
            return False
        # Recuperar los valores
        dni=self.fDNI.text()
        serv=self.fServicio.text().upper()
        fecha=self.mostrarFechaDmA(str(self.fFecha.date().toPyDate()))
        if self.alertaSoloNumeroMonto():
            return False
        else:
            monto=self.fMonto.text()
        metPago=self.fMetodoPago.itemText(self.fMetodoPago.currentIndex()).upper()
        entSal=self.setCheckEntradaSalida()
        mesPago=self.setCheckMesPagado()
        descrip=self.fDescripcion.toPlainText().upper()
        datosFactura=(dni, serv, fecha, monto, metPago, entSal, mesPago, descrip)
        conex=conexionDB.conexion()
        # Inicia conexion e insertar en la BBDD
        conex.agregarFactura(datosFactura)
        self.mostrarFacturacion()
        self.vaciarCeldasDatosFactura() 

    def modificar(self):
        # Validar campos
        if self.validarCampos():
            return False
        numFact=self.fNumFact.text().upper()
        dni=self.fDNI.text().upper()
        serv=self.fServicio.text().upper()
        monto=self.fMonto.text().upper()
        metPago=self.fMetodoPago.currentText()
        entSal=self.setCheckEntradaSalida()
        mesPago=self.setCheckMesPagado()
        descrip=self.fDescripcion.toPlainText().upper()
        datosFactura=(dni, serv, monto, metPago, entSal, mesPago, descrip, numFact)
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Inicia conexion e insertar en la BBDD
        conex.modificarFactura(datosFactura)
        self.mostrarFacturacion()
        self.vaciarCeldasDatosFactura()

    def eliminar(self):
        numFact=self.fNumFact.text()
        # Instancia(objeto) de conexionDB
        conex=conexionDB.conexion()
        # Consultar clientes
        conex.borrarFactura(numFact)
        self.mostrarFacturacion()
        self.vaciarCeldasDatosFactura()

    def cancelar(self):
        self.mostrarFacturacion()
        self.vaciarCeldasDatosFactura()
        
    def vaciarCeldasDatosFactura(self):
        self.fNumFact.setText("")
        self.fnomApe.setText("")
        self.fDNI.setText("")
        self.fServicio.setText("")
        self.fMonto.setText("")
        self.fMetodoPago.setCurrentText('')
        self.vaciarIngresoEgreso()
        self.fDescripcion.setText("")
        self.fPago_Enero.setChecked(False)
        self.fPago_Febrero.setChecked(False)
        self.fPago_Marzo.setChecked(False)
        self.fPago_Abril.setChecked(False)
        self.fPago_Mayo.setChecked(False)
        self.fPago_Junio.setChecked(False)
        self.fPago_Julio.setChecked(False)
        self.fPago_Agosto.setChecked(False)
        self.fPago_Septiembre.setChecked(False)
        self.fPago_Octubre.setChecked(False)
        self.fPago_Noviembre.setChecked(False)
        self.fPago_Diciembre.setChecked(False)

    def vaciarIngresoEgreso(self):
        if self.fIngreso.isChecked() == True:
            self.fIngreso.setChecked(False)
        if self.fEgreso.isChecked() == True:
            self.fEgreso.setChecked(False)

    def mostrarFechaDmA(self, fecha):
        fecha=fecha.split('-')
        anio=fecha[0]
        mes=fecha[1]
        dia=fecha[2]
        fechaMod= dia+'/'+mes+'/'+anio
        return fechaMod

    def validarCampos(self):
        if self.fDNI.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'DNI' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if self.fServicio.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'SERVICIO' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if self.fMetodoPago.currentText()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'METODO DE PAGO' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if not self.validarMesPago():
            alerta=QMessageBox()
            alerta.setText("Debes seleccionar al menos un MES en 'PAGO DEL MES DE:'")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True 
        if self.fMonto.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'MONTO' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if self.validarIngEgr():
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Debes seleccionar un valor: 'INGRESO' o 'EGRESO'")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True   

    # Error, si ambos se encuentran sin seleccion. 
    def validarIngEgr(self):
        if self.fIngreso.isChecked()==False and self.fEgreso.isChecked()==False:
            return True
        if self.fIngreso.isChecked()==True and self.fEgreso.isChecked()==True:
            return True
        
    def validarMesPago(self):
        if self.fPago_Enero.isChecked()==True:
            return True
        if self.fPago_Febrero.isChecked()==True:
            return True
        if self.fPago_Marzo.isChecked()==True:
            return True
        if self.fPago_Abril.isChecked()==True:
            return True
        if self.fPago_Mayo.isChecked()==True:
            return True
        if self.fPago_Junio.isChecked()==True:
            return True
        if self.fPago_Julio.isChecked()==True:
            return True
        if self.fPago_Agosto.isChecked()==True:
            return True
        if self.fPago_Septiembre.isChecked()==True:
            return True
        if self.fPago_Octubre.isChecked()==True:
            return True
        if self.fPago_Noviembre.isChecked()==True:
            return True
        if self.fPago_Diciembre.isChecked()==True:
            return True
        return False

    # Metodo para verificar que el valor del monto sea numerico
    def alertaSoloNumeroMonto(self):
        if not self.fMonto.text().isdigit():
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("Error en el campo MONTO, solo se puede ingresar un valor numerico")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True 
            
    # Abrir ventana para buscar cliente
    def obtenerBusquedaCliente(self):
        # Ejecutar ventana
        self.vtnClientesDesdeFact.exec_()
        # Retornar informacion
        datos=self.vtnClientesDesdeFact.enviarInformacionCliente()
        self.fDNI.setText(datos[0])
        self.fnomApe.setText(datos[1])

    def obtenerBusquedaServicio(self):
        # Ejecutar ventana
        self.vtnServicioDesdeFact.exec_()
        # Retornar informacion
        datos=self.vtnServicioDesdeFact.enviarInformacionServicio()
        self.fServicio.setText(datos)