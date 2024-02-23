from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VentanaFechaDesdeFact(QDialog):
    def __init__(self):
        # Inicializar el objeto
        QWidget.__init__(self)
        # Cargar la configuracion del archivo
        #uic.loadUi("vFechaDesdeFact.ui", self)
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\vFechaDesdeFact.ui', self)

        # Acciones de botones
        #self.btn_aceptar_fecha.clicked.connect(lambda: )
        self.btn_aceptar_fecha.clicked.connect(lambda: self.close())
        
    # METODOS
    def enviarInformacionFechaUno(self):
        fecha = self.mostrarFechaDmA(str(self.fecha_calendario.selectedDate().toPyDate()))
        return fecha
    
    def enviarInformacionFechaDos(self):
        fecha = self.mostrarFechaDmA(str(self.fecha_calendario.selectedDate().toPyDate()))
        return fecha

    def mostrarFechaDmA(self, fecha):
        fecha=fecha.split('-')
        anio=fecha[0]
        mes=fecha[1]
        dia=fecha[2]
        fechaMod= dia+'/'+mes+'/'+anio
        return fechaMod
