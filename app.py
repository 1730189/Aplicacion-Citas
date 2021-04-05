import sys
import os
import string
import collections
import matplotlib.pyplot as plt
import pdflatex
import subprocess

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from pybtex.database.input import bibtex
from PyQt5.QtCore import Qt
from pdflatex import PDFLaTeX


from CrearArticulo import *
from VerAsociacion import *

global repositorio
global archivos
global direccion


class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("gui_app.ui", self)

        self.row=0
        self.dialogCrear = AbrirVista(self)
        self.dialogAsociar = VerGrafica(self)

        self.btn_asociar.setEnabled(False)
        self.btn_vista.setEnabled(False)
        self.btn_grafica.setEnabled(False)
        self.btn_crearbib.setEnabled(False)
        self.btn_individual.setEnabled(False)

        self.btn_asociar.clicked.connect(self.ConectarAsociar)
        self.btn_vista.clicked.connect(self.ConectarCrear)
        self.btn_abrir.clicked.connect(self.AbrirRepositorio)
        self.btn_grafica.clicked.connect(self.Grafica)
        self.btn_crearbib.clicked.connect(self.CrearBib)
        self.btn_pdf.clicked.connect(self.CrearPdfIndividual)
        self.btn_individual.clicked.connect(self.Individual)
        self.btn_pdfgeneral.clicked.connect(self.CrearPdfGeneral)
        self.tableWidget.clicked.connect(self.actual)

        #Deshabilitamos la Posible Modificacion desde la Tabla
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #Deshabilitamos el Movimiento de la tabla
        self.tableWidget.setDragDropOverwriteMode(False)
        #Seleccionamos toda una fila
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Seleccionamos solo 1 fila
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        #Indicamos la aparicion de "..." si el texto es mas grande que la columna
        self.tableWidget.setTextElideMode(Qt.ElideRight)
        #Deshabilitamos el ajuste de texto
        self.tableWidget.setWordWrap(False)
        #Deshabilitamos clasificacion de datos
        self.tableWidget.setSortingEnabled(False)
        #Establecemos las columnas
        self.tableWidget.setColumnCount(5)
        #Centramos el texto en la columna
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        #Hacmos que la visualizacion de la ultima columna rellene el espacio faltante
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #Modificamos los colores de fondo salteados
        self.tableWidget.setAlternatingRowColors(True)
        #Establecemos los encabezados
        nombreColumnas = ("Llave","Author/Editor", "Year", "Journal", "Title")
        self.tableWidget.setHorizontalHeaderLabels(nombreColumnas)

        #self.ventana = AbrirVista()


    #####################################################################
    def AbrirRepositorio(self):
        self.cb_contenido.clear()
        global repositorio
        repositorio = str(QFileDialog.getExistingDirectory(self, "Seleccione Repositorio"))
        self.dialogCrear.repositorioGeneral = repositorio
        self.dialogAsociar.repositorioGeneral = repositorio
        global archivos
        archivos = os.listdir(repositorio)

        for i in archivos:
            if i.endswith(".bib"):
                self.cb_contenido.addItem(str(i))

        self.cb_contenido.activated[str].connect(self.onChanged)

    #####################################################################
    def onChanged(self):
        global direccion
        self.btn_grafica.setEnabled(True)
        #self.lw_contenido.clear()
        #Prueba de ver en que esta posicionado el combobox
        direccion = self.cb_contenido.currentText()
        self.dialogCrear.direccionGeneral = direccion
        self.dialogAsociar.direccionGeneral = direccion
        #print(direccion)

        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()

        archivo = parser.parse_file(open(repositorio + "/" + direccion, 'r'))
        #print(archivo)
        self.dialogCrear.archivoGeneral = archivo
        self.row = 0
        self.tableWidget.setRowCount(len(archivo.entries))
        #print("Aqui: ")
        #print(len(archivo.entries))

        for i in archivo.entries:
            #print(i)
            b = archivo.entries[i].fields
            #self.lw_contenido.addItem(i)
            nombreArticulo = b["title"]
            nombreJournal = b["journal"]
            nombreYear = b["year"]
            authors = ""
            for author in archivo.entries[i].persons["author"]:
                nombreAutor = str(author.first()) + " " + str(author.last())
                nombreAutor = nombreAutor.translate(translator)
                if len(authors) == 0:
                    authors = '' + nombreAutor
                else:
                    authors = authors + ", " + nombreAutor
            #print(authors)
            #print("\n")

            #print(row)
            self.tableWidget.setItem(self.row, 0, QTableWidgetItem(i))
            self.tableWidget.setItem(self.row, 1, QTableWidgetItem(authors))
            self.tableWidget.setItem(self.row, 2, QTableWidgetItem(nombreYear))
            self.tableWidget.setItem(self.row, 3, QTableWidgetItem(nombreJournal))
            self.tableWidget.setItem(self.row, 4, QTableWidgetItem(nombreArticulo))
            self.row += 1

            #print(nombreArticulo)
        self.btn_asociar.setEnabled(True)
        self.btn_vista.setEnabled(True)
        #archivo.close()
    #####################################################################
    def actual(self):
        self.btn_crearbib.setEnabled(True)
        self.btn_individual.setEnabled(True)
        #Limpiamos los labels
        self.le_ano.clear()
        self.le_autor.clear()
        self.le_journal.clear()
        self.le_nombre.clear()
        self.le_titulo.clear()

        #Se toma el item de la fila seleccionada
        row = self.tableWidget.currentRow()
        llave = self.tableWidget.item(row,0)
        autor = self.tableWidget.item(row,1)
        year = self.tableWidget.item(row,2)
        journal = self.tableWidget.item(row,3)
        titulo = self.tableWidget.item(row,4)

        #Agregamos los items a los labels
        self.le_autor.setText(autor.text())
        self.le_nombre.setText(llave.text())
        self.le_journal.setText(journal.text())
        self.le_ano.setText(year.text())
        self.le_titulo.setText(titulo.text())

        #print(llave.text())
        #print(autor.text())
        #print(year.text())
        #print(journal.text())
        #print(titulo.text())
    #####################################################################
    def CrearArticulo(self):
        global repositorio
        global direccion
        #nombre = self.le_nombre.text()
        autor = self.le_autor.text()
        titulo = self.le_titulo.text()
        journalO = self.le_journal.text()
        ano = self.le_ano.text()

        #Union de nombres de autores con &
        autores = autor.split('and')
        print(autores)
        apellidos = ""
        for i in autores:
            vector = i.lstrip().rstrip().split(' ')
            print(vector)
            apellido = vector[-1]
            print(apellido)
            apellidos += apellido + "&"
        apellidos = apellidos[:-1]
        print(apellidos)

        #Creacion del texto sin espacios del journal
        journal = journalO.replace(" ", "")
        print(journal)

        #Creacion de la llave
        llave = apellidos + "_" + journal + "_" + ano
        print(llave)

        #Visualizacion de la salida del articulo
        print("@articule{" + llave + ",\n" +
              "author = {" + autor + "},\n" +
              "title = {" + titulo + "},\n" +
              "journal = {" + journal + "},\n" +
              "year = " + ano + ",\n" +
              "}")

        #Creacion del .bib en el repositorio
        #print(repositorio)
        '''file = open(repositorio + "/" + direccion, "a")
        file.write("\n@articule{" + llave + ",\n" +
                   "\ttitle = {" + titulo + "},\n" +
                   "\tjournal = {" + journalO + "},\n" +
                   "\tyear = {" + ano + "},\n" +
                   "\tauthor = {" + autor + "},\n" +
                   "}")
        file.close()'''
    #####################################################################
    def ConectarCrear(self):
        self.dialogCrear.setModal(True)
        self.dialogCrear.show()
    #####################################################################
    def ConectarAsociar(self):
        self.dialogAsociar.setModal(True)
        self.dialogAsociar.show()
    #####################################################################
    def Grafica(self):
        nombreYear = []
        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()
        archivo = parser.parse_file(open(repositorio + "/" + direccion, 'r'))
        row = 0
        for i in archivo.entries.values():
            nombreLlave = i.key

            b = i.fields

            nombreYear.append(b["year"])
        repetidos = collections.Counter(nombreYear)
        print("Fechas y Cuantas Veces se Repiten " + str(repetidos))
        fechas = []
        for x in nombreYear:
            if x not in fechas:
                fechas.append(x)
        print(fechas.sort())
        #print(nombreYear)
        otravariablerepetida = []
        for x in fechas:
            otravariablerepetida.append(int(format(repetidos[x])))
        print(otravariablerepetida)

        fig, ax = plt.subplots()
        
        ax.set_title('Citado por Año')
        
        plt.bar(fechas, otravariablerepetida)
        
        direccionSola = direccion.split('.')
        
        
        plt.savefig(repositorio + "/" + direccionSola[0] + '.png')
        
        plt.show()

    #####################################################################
    def CrearBib(self):
        row = self.tableWidget.currentRow()
        llave = self.tableWidget.item(row,0)
        llavebib = llave.text()
        print(llavebib)
        file = open(repositorio + "/" + llavebib + ".bib", "w")
        file.close()

    #####################################################################
    def Individual(self):
        row = self.tableWidget.currentRow()
        llave = self.tableWidget.item(row,0)
        llavebib = llave.text()
        print(llavebib)
        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()
        archivo = parser.parse_file(open(repositorio + "/" + direccion, 'r'))
        for i in archivo.entries.values():
            print(i.key)
            nombreLlave = i.key
            b = i.fields
            if(llavebib == nombreLlave):
                #print("Es igual")
                nombreTitulo = b["title"]
                nombreJournal = b["journal"]
                nombreYear = b["year"]
                authors = ""
                for author in i.persons["author"]:
                    nombreAutor = str(author.first()) + " " + str(author.last())
                    nombreAutor = nombreAutor.translate(translator)
                    if len(authors) == 0:
                        authors = '' + nombreAutor
                    else:
                        authors = authors + ", " + nombreAutor

                file = open(repositorio + "/" + llavebib + "_IND.bib", "w")
                file.write("\n@article{" + llavebib + ",\n" +
                           "\ttitle = {" + nombreTitulo + "},\n" +
                           "\tauthor = {" + authors + "},\n" +
                           "\tjournal = {" + nombreJournal + "},\n" +
                           "\tyear = {" + nombreYear + "},\n" +
                           "}")
                file.close()
            else:
                print("Es diferente")

    #####################################################################
    def CrearPdfIndividual(self):
        print("Hola pdf")
        cwd = os.getcwd()
        variableNew = "\ "
        variableNewNew = variableNew.split(' ')
        f = open('seccionCInd.tex', 'r')
        seccionC = f.read()
        #print(seccionC)
        f.close()
        
        row = self.tableWidget.currentRow()
        llave = self.tableWidget.item(row,0)
        llavebib = llave.text()
        print(llavebib)

        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()
        archivo = parser.parse_file(open(repositorio + "/" + direccion, 'r'))
        
        for i in archivo.entries.values():
            print(i.key)
            nombreLlave = i.key
            if(llavebib == nombreLlave):
                #print("Encontrado")
                a = open(repositorio + "/" + llavebib + ".tex", "w")
                a.write("\documentclass{article}\n" + 
                        variableNewNew[0] + "newcommand{\Cita}{" + llavebib + "}\n" +
                        seccionC)
                a.close()
                os.chdir(str(repositorio))
                os.system("pdflatex " + llavebib + ".tex")
                os.system("biber " + llavebib)
                os.system("pdflatex " + llavebib + ".tex")
                os.system("pdflatex " + llavebib + ".tex")
                os.system("del *.aux *.bbl *.blg *.bcf *.out *.xml *.log")
                os.chdir(str(cwd))
        

    #####################################################################
    def CrearPdfGeneral(self):
        variableNew = "\ "
        variableNewNew = variableNew.split(' ')
        numero = 0
        cwd = os.getcwd()
        f = open('seccionAGene.tex', 'r')
        seccionAGene = f.read()
        print(seccionAGene)
        f.close()

        f = open('seccionBGene.tex', 'r')
        seccionBGene = f.read()
        f.close()

        f = open('seccionCGene.tex', 'r')
        seccionCGene = f.read()
        print(seccionCGene)
        f.close()
        nombresSolosA = []
        archivos = os.listdir(repositorio)

        for i in archivos:
            if i.endswith(".tex"):
                nombres = i
                nombresSolos = nombres.split('.')
                nombresSolosA.append(nombresSolos[0])
                print(nombresSolosA)
        
        #\includegraphics[width=0.8\linewidth]{ListadodeArticulos_y_Citas.png}
        direccionCor = direccion.split(".")

        f = open(repositorio + "/" + direccionCor[0] +".tex", "w")
        f.write(seccionAGene + "\n")

        f.write(variableNewNew[0] + "addbibresource{" + direccionCor[0] + ".bib}\n")

        f.write(seccionBGene + "\n")

        print(direccionCor[0])
        f.write("\includegraphics[width=0.8\linewidth]{" + direccionCor[0] + ".png}\n")

        f.write(seccionCGene + "\n")
        for a in nombresSolosA:
            numero = numero + 1
            numerostr = str(numero)
            print(numerostr)
            f.write(variableNewNew[0] + "addtocounter{ContadorArticulos}{1}" + variableNewNew[0] +"arabic{ContadorArticulos}.&\AtNextCite{\defcounter{maxnames}{99}}" + variableNewNew[0] +"fullcite{" + a + "}\hyperref[XlabelX" + numerostr + "]{--Listado detallado sin auto-citas incluidas} " + variableNewNew[0] +"\ \hline" + "\n")
        
        f.write("\hline \hline\n" +
                "\end{longtable}\n" +
                "\setboolean{@twoside}{false}\n")
        
        translator = str.maketrans('', '', string.punctuation)
        parser = bibtex.Parser()
        archivo = parser.parse_file(open(repositorio + "/" + direccion, 'r'))
        contador = 0

        for b in archivos:
            #print("Dentro primer For")
            if b.endswith(".tex"):
                #print("Dentro primer If")
                nombresTex = b
                nombresTexSep = nombresTex.split(".")
                #print(nombresTexSep)
                for c in archivo.entries.values():
                    #print("Dentro segundo For")
                    nombreDLlave = c.key
                    #print(nombreDLlave)
                    d = c.fields
                    if nombresTexSep[0] == nombreDLlave:
                        contador = contador + 1
                        contadorstr = str(contador)
                        #print("Dentro segundo If")
                        nombreDTitulo = d["title"]
                        #print(nombreDTitulo)

                        f.write("\clearpage\n" +
                                "\phantomsection\n" +
                                "\label{XlabelX" + contadorstr +"}\n" +
                                "\includepdf[pages=-,pagecommand={}]{" + nombresTexSep[0] + ".pdf}\n" +
                                "" + variableNewNew[0] +"addcontentsline{toc}{section}{[" + contadorstr +"]. " + nombreDTitulo + "}\n")

        f.write("\clearpage\n" +
                "\phantomsection\n" +
                "Pagina Vacia\n" +
                "\clearpage\n" +
                "\end{document}\n")
        
        f.close()

        os.chdir(str(repositorio))
        os.system("pdflatex " + direccionCor[0] + ".tex")
        os.system("biber " + direccionCor[0])
        os.system("pdflatex " + direccionCor[0] + ".tex")
        os.system("pdflatex " + direccionCor[0] + ".tex")
        os.system("del *.aux *.bbl *.blg *.bcf *.out *.xml *.log")
        os.chdir(str(cwd))

    #####################################################################
    def closeEvent(self, event):
        pregunta = QMessageBox.question(self, "Salir", "¿Esta Seguro Que Quiere Salir?",
                                        QMessageBox.Yes | QMessageBox.No)
        if pregunta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
GUI = Principal()
GUI.show()
sys.exit(app.exec_())
