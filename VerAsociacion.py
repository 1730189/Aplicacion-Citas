import sys
import os
import string
import collections
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from pybtex.database.input import bibtex
from PyQt5.QtCore import Qt

class VerGrafica(QDialog):
    def __init__(self,parent):
        super(VerGrafica,self).__init__(parent)
        loadUi("asociacion.ui", self)

        self.repositorioGeneral = ""
        self.direccionGeneral = ""

        self.btn_buscar.clicked.connect(self.BuscarAsociacion)

        #Deshabilitamos la Posible Modificacion desde la Tabla
        self.tw_asociaciones.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #Deshabilitamos el Movimiento de la tabla
        self.tw_asociaciones.setDragDropOverwriteMode(False)
        #Seleccionamos toda una fila
        self.tw_asociaciones.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Seleccionamos solo 1 fila
        self.tw_asociaciones.setSelectionMode(QAbstractItemView.SingleSelection)
        #Indicamos la aparicion de "..." si el texto es mas grande que la columna
        self.tw_asociaciones.setTextElideMode(Qt.ElideRight)
        #Deshabilitamos el ajuste de texto
        self.tw_asociaciones.setWordWrap(False)
        #Deshabilitamos clasificacion de datos
        self.tw_asociaciones.setSortingEnabled(False)
        #Establecemos las columnas
        self.tw_asociaciones.setColumnCount(2)
        #Centramos el texto en la columna
        self.tw_asociaciones.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        #Hacmos que la visualizacion de la ultima columna rellene el espacio faltante
        self.tw_asociaciones.horizontalHeader().setStretchLastSection(True)
        #Modificamos los colores de fondo salteados
        self.tw_asociaciones.setAlternatingRowColors(True)
        #Establecemos los encabezados
        nombreColumnas = ("Llave", "Title")
        self.tw_asociaciones.setHorizontalHeaderLabels(nombreColumnas)

    def BuscarAsociacion(self):
        autor = ""
        autor = self.le_autor.text()
        autor = " " + autor
        match = ""
        Llave = ""
        nombreTitulo = ""
        numero = 0
        row = 0
        print(autor)
        print("Buscar")

        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()

        archivo = parser.parse_file(open(self.repositorioGeneral + "/" + self.direccionGeneral, 'r'))

        for i in archivo.entries.values():
            nombreLlaveAsociacion = i.key
            b = i.fields
            #nombreTituloAsociacion = b["title"]
            authors = ""
            for author in i.persons["author"]:
                nombreAutor = str(author.first()) + " " + str(author.last())
                #print(nombreAutor + " Primero")
                nombreAutor = nombreAutor.translate(translator)
                #print(nombreAutor + " Segundo")
                #print(autor + "Espacio")
                #print(autor == nombreAutor)

                if len(authors) == 0:
                    authors = '' + nombreAutor
                    #print(nombreAutor + " Tercero")
                else:
                    authors = authors + ", " + nombreAutor
                    #print(nombreAutor + " Cuarto")

                if autor == nombreAutor:
                    #print("Coinciden")
                    nombreTitulo = b["title"]
                    Llave = nombreLlaveAsociacion
                    numero = numero + 1
                    print(nombreTitulo)
                    print(Llave)
                    self.tw_asociaciones.setRowCount(numero)
                    self.tw_asociaciones.setItem(row, 0, QTableWidgetItem(Llave))
                    self.tw_asociaciones.setItem(row, 1, QTableWidgetItem(nombreTitulo))
                    row += 1
                else:
                    print("No")
        #print(nombreTituloAsociacion)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VerGrafica()
    GUI.show()
    sys.exit(app.exec_())