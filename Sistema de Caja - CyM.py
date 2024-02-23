from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
import conexionDB
import clientes
import servicios
import facturacion
import reportes
import caja
import cambiarConexion

# Constructor de la ventana (hereda de QMainWindows)
class Principal(QMainWindow):
    def __init__(self):
        # Inicializar el objeto
        QMainWindow.__init__(self)
        # Cargar la configuracion del archivo
        uic.loadUi(r'C:\Users\Usuario\Documents\AppCrudPython\appOficina\ventanaPrinc.ui', self)
        
        # Maximizar ventana
        self.showMaximized()
        # -- ARCHIVO --
        self.archivo_copia_seguridad.triggered.connect(self.copiaSeguridad)
        self.vtnConexionBD = conexionDB.conexion()
        self.archivo_conectar.triggered.connect(self.abrirConexion)
        self.vtnCambiarConexion = cambiarConexion.VentanaCambiarConexion() 
        # -- CLIENTE --
        # Boton para llamar a la ventana clientes
        self.btn_clientes.clicked.connect(self.abrirClientes)
        # Objeto (instancia) de VentanaCliente
        self.vtnClientes = clientes.VentanaClientes()
        # -- SERVICIO --
        # Boton para llamar a la ventana servicios
        self.btn_servicios.clicked.connect(self.abrirServicios)
        # Objeto (instancia) de VentanaCliente
        self.vtnServicios = servicios.VentanaServicios()
        # -- FACTURACION --
        # Boton para llamar a la ventana facturacion
        self.btn_facturacion.clicked.connect(self.abrirFacturacion)
        # Objeto (instancia) de VentanaCliente
        self.vtnFacturacion = facturacion.VentanaFacturacion()

        # Boton para llamar a la ventana reportes
        self.btn_reportes.clicked.connect(self.abrirReportes)
        # Objeto (instancia) de VentanaReporte
        self.vtnReportes = reportes.VentanaReportes()
        # Boton para llamar a la ventana caja
        self.btn_caja.clicked.connect(self.abrirCaja)
        # Objeto (instancia) de VentanaCaja
        self.vtnCaja = caja.VentanaCaja()

    # Metodo para abrir ventana conexionBD
    def copiaSeguridad(self):
        # Ejecutar ventana
        self.vtnConexionBD.crearCopiaSeguridad()

    # Metodo para abrir ventana cliente
    def abrirConexion(self):
        # Ejecutar ventana
        self.vtnCambiarConexion.exec_()

    # Metodo para abrir ventana cliente
    def abrirClientes(self):
        # Posicionar ventana
        x = (self.width() - self.vtnClientes.width()) / 2
        y = (self.height() - self.vtnClientes.height()) / 2
        self.vtnClientes.move(int(x), int(y))
        # Ejecutar ventana
        self.vtnClientes.exec_()

    # Metodo para abrir ventana servicio
    def abrirServicios(self):
        # Posicionar ventana
        x = (self.width() - self.vtnServicios.width()) / 2
        y = (self.height() - self.vtnServicios.height()) / 2
        self.vtnServicios.move(int(x), int(y))
        # Ejecutar ventana
        self.vtnServicios.exec_()

    # Metodo para abrir ventana facturacion
    def abrirFacturacion(self):
        # Posicionar ventana
        x = (self.width() - self.vtnFacturacion.width()) / 2
        y = (self.height() - self.vtnFacturacion.height()) / 2
        self.vtnFacturacion.move(int(x), int(y-3))
        # Ejecutar ventana
        self.vtnFacturacion.exec_()
    
    # Metodo para abrir ventana reportes
    def abrirReportes(self):
        # Ejecutar ventana
        self.vtnReportes.showMaximized()
        self.vtnReportes.exec_()

    # Metodo para abrir ventana caja
    def abrirCaja(self):
        # Posicionar ventana
        x = (self.width() - self.vtnCaja.width()) / 2
        y = (self.height() - self.vtnCaja.height()) / 2
        self.vtnCaja.move(int(x), int(y))
        # Ejecutar ventana
        self.vtnCaja.exec_()

#              APP
# ============================== 

# Instancia para INICIAR APP (Variable del programa)
aplicacion=QApplication(sys.argv)

# Cargar objeto ventana
ventanaPrinc=Principal()
# Mostrar ventana
ventanaPrinc.show()

# == CERRAR APP ==
sys.exit(aplicacion.exec())