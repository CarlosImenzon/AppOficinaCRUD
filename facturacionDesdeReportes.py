from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date
import clientesDesdeFact
import serviciosDesdeFact

class VentanaFactDesdeReportes(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vFactDesdeReportes.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vFactDesdeReportes.ui', self)

        # Acciones de botones
        self.btn_verificar.clicked.connect(self.validarCampos)
        self.btn_aceptar.clicked.connect(self.close)

        # Boton buscar DNI y Objeto (instancia) de VentanaCliente
        self.btn_buscar_dni_factura.clicked.connect(self.obtenerBusquedaCliente)
        self.vtnClientesDesdeFact = clientesDesdeFact.VentanaClientesDesdeFact()

        # Boton buscar SERVICIO y Objeto (instancia) de VentanaCliente
        self.btn_buscar_serv_factura.clicked.connect(self.obtenerBusquedaServicio)
        self.vtnServicioDesdeFact = serviciosDesdeFact.VentanaServiciosDesdeFact()

    # METODOS
    def enviarInformacionFactura(self):
        # Asignar a los QLineEdit
        nomApe=self.fnomApe.text()
        dni=self.fDNI.text()
        serv=self.fServicio.text().upper()
        monto=self.fMonto.text()
        metPago=self.fMetodoPago.itemText(self.fMetodoPago.currentIndex()).upper()
        entSal=self.setCheckEntradaSalida()
        mesPago=self.setCheckMesPagado()
        descrip=self.fDescripcion.toPlainText().upper()
        datosFactura=(nomApe, dni, serv, monto, metPago, entSal, mesPago, descrip)
        return datosFactura

    def obtenerSel(self, datos):
        self.fNumFact.setText(datos[0])
        self.fnomApe.setText(datos[1])
        self.fDNI.setText(datos[2])
        self.fServicio.setText(datos[3])
        self.fMonto.setText(datos[4])
        self.cargarMetPago(datos[5])
        self.checkEntradaSalida(datos[6])
        self.checkMesPagado(datos[7])
        self.fDescripcion.setText(datos[8])

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

    def validarCampos(self):
        if self.fServicio.text()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'SERVICIO' se encuentra vacio")
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
        if self.fMetodoPago.currentText()=='':
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("El campo 'METODO DE PAGO' se encuentra vacio")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            return True
        if not self.validarMesPago():
            alerta=QMessageBox()
            alerta.setText("Debes seleccionar al menos un 'MES'")
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
        if not self.fServicio.text()=='' and not self.fMonto.text()=='' and not self.fMetodoPago.currentText()=='' and self.validarMesPago() and not self.validarIngEgr():
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText("No hay campos vacio, precione ACEPTAR")
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()

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