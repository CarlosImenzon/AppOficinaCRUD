import sqlite3
from sqlite3.dbapi2 import connect
from datetime import date
from PyQt5.QtWidgets import *
import os
import shutil

class conexion():
    
    def iniciarConexion(self):
        # Iniciar conexion
        try: 
            miConexion=sqlite3.connect("sistemaOficinaDB.s3db")
            miConexion.text_factory = lambda b: b.decode(errors = 'ignore')
            return miConexion
        except sqlite3.Error as error:
            alerta=QMessageBox()
            alerta.setWindowTitle('Mensaje')
            alerta.setText('Se ha producido un error: ', error)
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()
            
    # METODOS PARA -- COPIA DE SEGURIDAD --
    def crearCopiaSeguridad(self):
        if not os.path.exists('backup'):
            os.mkdir('backup')
        else:
            nombreBackupFecha='sistemaOficinaDB_'+str(date.today())
            shutil.copy("sistemaOficinaDB.s3db", "./backup/"+nombreBackupFecha+".s3db")
            alerta=QMessageBox()
            alerta.setWindowTitle('Copia de seguridad')
            alerta.setText('La copia de seguridad se ha creado con exito.')
            alerta.setIcon(QMessageBox.Information)
            alerta.exec()

    # METODOS PARA -- CLIENTES --
    def consultarClientes(self):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="SELECT * FROM Cliente ORDER BY ApellidoNombre"
        miCursor.execute(sentenciaSLQ)
        return miCursor.fetchall()

    def agregarCliente(self, datosCliente):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="INSERT INTO Cliente (DNI, ApellidoNombre, Telefono) VALUES (?,?,?)"
        miCursor.execute(sentenciaSLQ, datosCliente)
        miConexion.commit()
        miConexion.close()

    def borrarCliente(self, dni):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="DELETE FROM Cliente WHERE DNI=(?)"
        miCursor.execute(sentenciaSLQ,[dni])
        miConexion.commit()
        miConexion.close()
        
    def modificarCliente(self, datosCliente): 
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="UPDATE Cliente SET ApellidoNombre=?, Telefono=? WHERE DNI=?"
        miCursor.execute(sentenciaSLQ, datosCliente)
        miConexion.commit()
        miConexion.close()

    def buscarCliente(self, apeNom): 
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="SELECT * FROM Cliente WHERE ApellidoNombre LIKE  ?"
        miCursor.execute(sentenciaSLQ,['%'+apeNom+'%',])
        return miCursor.fetchall()

    # METODOS DE -- SERVICIOS --
    def consultarServicios(self):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="SELECT * FROM Servicio ORDER BY NombreServicio"
        miCursor.execute(sentenciaSLQ)
        return miCursor.fetchall()

    def agregarServicio(self, nom):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="INSERT INTO Servicio (NombreServicio) VALUES (?)"
        miCursor.execute(sentenciaSLQ, [nom])
        miConexion.commit()
        miConexion.close()

    def borrarServicio(self, nom):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="DELETE FROM Servicio WHERE NombreServicio=(?)"
        miCursor.execute(sentenciaSLQ,[nom])
        miConexion.commit()
        miConexion.close()

    def buscarServicio(self, buscarNom): 
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="SELECT * FROM Servicio WHERE NombreServicio LIKE  ?"
        miCursor.execute(sentenciaSLQ,['%'+buscarNom+'%',])
        return miCursor.fetchall()

    # METODOS DE -- FACTURACION --
    def consultarFacturacion(self, fecha):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        #sentenciaSLQ="SELECT * FROM Facturacion ORDER BY Fecha"
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE Fecha=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, [fecha])
        return miCursor.fetchall()

    def agregarFactura(self, datosFactura):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="INSERT INTO Facturacion VALUES (NULL,?,?,?,?,?,?,?,?)"
        miCursor.execute(sentenciaSLQ, datosFactura)
        miConexion.commit()
        miConexion.close()

    def borrarFactura(self, numFact):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="DELETE FROM Facturacion WHERE IdFactura=(?)"
        miCursor.execute(sentenciaSLQ,[numFact])
        miConexion.commit()
        miConexion.close()

    def modificarFactura(self, datosCliente): 
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="UPDATE Facturacion SET DNI=?, NombreServ=?, Monto=?, MetodoDePago=?, IngresoEgreso=?, MesPago=?, Descripcion=? WHERE IdFactura=?"
        miCursor.execute(sentenciaSLQ, datosCliente)
        miConexion.commit()
        miConexion.close()

    # METODOS DE -- REPORTES --
    def consultarReportes(self):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        #sentenciaSLQ="SELECT * FROM Facturacion ORDER BY Fecha"
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ)
        return miCursor.fetchall()
    
    def consultarReportesCliente(self, dni):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE f.DNI=?
                        ORDER BY Fecha DESC'''
        miCursor.execute(sentenciaSLQ, [dni])
        return miCursor.fetchall()

    def consultarReportesUnaFecha(self, fecha):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, [fecha])
        return miCursor.fetchall()

    def consultarReportesFechas(self, fechas):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha BETWEEN ? AND ?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, fechas)
        return miCursor.fetchall()
    
    def consultarReportesServicio(self, nom):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE f.NombreServ=?
                        ORDER BY Fecha DESC'''
        miCursor.execute(sentenciaSLQ, [nom])
        return miCursor.fetchall()

    def modificarFacturaReporte(self, datosFacturaRep): 
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ="UPDATE Facturacion SET DNI=?, NombreServ=?, Monto=?, MetodoDePago=?, IngresoEgreso=?, MesPago=?, Descripcion=? WHERE IdFactura=?"
        miCursor.execute(sentenciaSLQ, datosFacturaRep)
        miConexion.commit()
        miConexion.close()

    def consultarReportesUnaFechaServicio(self, fechaServ):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha=? AND f.NombreServ=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, fechaServ)
        return miCursor.fetchall()
   
    def consultarReportesFechasServicio(self, fechasServ):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha BETWEEN ? AND ? AND f.NombreServ=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, fechasServ)
        return miCursor.fetchall()

    # METODOS DE -- CAJA --
    def consultarFactCajaIngEgre(self, fecha):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha=? AND IngresoEgreso=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, fecha)
        return miCursor.fetchall()
    
    def consultarFactCajaIngEgreFechas(self, fechas):
        miConexion=self.iniciarConexion()
        miCursor=miConexion.cursor()    # Cursor de la conexion
        sentenciaSLQ='''SELECT IdFactura, c.ApellidoNombre, f.DNI, f.NombreServ, Fecha, Monto, MetodoDePago, IngresoEgreso, MesPago, Descripcion 
                        FROM Facturacion AS f
                        INNER JOIN Cliente AS c
                        ON f.DNI = c.DNI
                        WHERE fecha BETWEEN ? AND ? AND IngresoEgreso=?
                        ORDER BY Fecha'''
        miCursor.execute(sentenciaSLQ, fechas)
        return miCursor.fetchall()