import sys
import os
import string
import re

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pybtex.database.input import bibtex
from PyQt5.QtCore import Qt
from functools import partial

class AbrirVista(QDialog):
    def __init__(self,parent):
        super(AbrirVista,self).__init__(parent)
        loadUi("ventana.ui", self)

        self.repositorioGeneral = ""
        self.direccionGeneral = ""

        # Pestaña Numero 1
        self.Btn_Crear1.clicked.connect(partial(self.GenerarArticuloManual,parent))
        # /Pestaña Numero 1
        
        #Pestaña Numero 2
        self.Btn_Crear2.clicked.connect(partial(self.GenerarArticuloDescarga,parent))
        self.btn_seleccionar.clicked.connect(self.AbrirRepositorio2)
        self.repositorio2 = ""
        self.direccion2 = ""
        self.archivos2 = ""
        self.archivo2 = ""
        #/Pestaña Numero 2
        
        #Pestaña Numero 3
        self.Btn_Crear3.clicked.connect(partial(self.GenerarArticuloPlano,parent))
        #/Pestaña Numero 3

    #Pestaña Numero 1
    def GenerarArticuloManual(self,parent):
        # nombre = self.le_nombre.text()
        autor = self.Tab1_Autor.text()
        journalO = self.Tab1_Journal.text()
        ano = self.Tab1_Year.text()
        titulo = self.Tab1_Titulo.text()

        au = False
        j = False
        a = False
        t = False

        if autor == "":
            print("Escriba algo")
            self.l_autor.setText("Campo Obligatorio")
        else:
            self.l_autor.setText("")
            au = True

        if journalO == "":
            self.l_journal.setText("Campo Obligatorio")
        else:
            self.l_journal.setText("")
            j = True

        if ano == "":
            self.l_year.setText("Campo Obligatorio")
        else:
            self.l_year.setText("")
            a = True

        if titulo == "":
            self.l_titulo.setText("Campo Obligatorio")
        else:
            self.l_titulo.setText("")
            t = True


        # Union de nombres de autores con &
        autores = autor.split('and')
        print(autores)
        apellidos = ""
        for i in autores:
            vector = i.lstrip().rstrip().split(' ')
            print(vector)
            apellido = vector[-1]
            print(apellido)
            apellidos += apellido + "-"
        apellidos = apellidos[:-1]
        print(apellidos)

        # Creacion del texto sin espacios del journal
        journal = journalO.replace(" ", "")
        print(journal)

        # Creacion de la llave
        llave = apellidos + "_" + journal + "_" + ano
        print(llave)
        
        # Visualizacion de la salida del articulo
        print("\n@articule{" + llave + ",\n" +
              "\ttitle = {" + titulo + "},\n" +
              "\tjournal = {" + journalO + "},\n" +
              "\tyear = {" + ano + "},\n" +
              "\tauthor = {" + autor + "},\n" +
              "}")
        # Creacion del .bib en el repositorio
        if (au == True) and (j == True) and (a == True) and (t == True):
        # print(repositorio)
            file = open(self.repositorioGeneral + "/" + self.direccionGeneral, "a")
            file.write("\n@articule{" + llave + ",\n" +
                       "\ttitle = {" + titulo + "},\n" +
                       "\tauthor = {" + autor + "},\n" +
                       "\tjournal = {" + journalO + "},\n" +
                       "\tyear = {" + ano + "},\n" +
                       "}")
            file.close()
            parent.onChanged()
            self.Tab1_Autor.clear()
            self.Tab1_Journal.clear()
            self.Tab1_Year.clear()
            self.Tab1_Titulo.clear()
            self.close()
        else:
            print("No entro")
        
    #/Pestaña Numero 1

    #Pestaña Numero 2
    def AbrirRepositorio2(self):
        self.repositorio2 = str(QFileDialog.getExistingDirectory(self, "Seleccione el Archivo Bibtext"))
        self.archivos2 = os.listdir(self.repositorio2)
        for i in self.archivos2:
            self.cb_archivos.addItem(str(i))

    def GenerarArticuloDescarga(self):
        self.direccion2 = self.cb_archivos.currentText()
        translator = str.maketrans('', '', string.punctuation)
        parse = bibtex.Parser()
        self.archivo2 = parse.parse_file(open(self.repositorio2 + "/" + self.direccion2, 'r'))

        for i in self.archivo2.entries.values():
            print(i.key)
            nombreLlave = i.key
            b = i.fields
            #nombreArticulo = b["booktitle"]
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

        print(nombreLlave)
        print(nombreTitulo)
        print(nombreJournal)
        print(nombreYear)
        print(authors)
        print(self.repositorioGeneral)
        print(self.direccionGeneral)
        file = open(self.repositorioGeneral + "/" + self.direccionGeneral, "a")
        file.write("\n@articule{" + llave + ",\n" +
                   "\ttitle = {" + titulo + "},\n" +
                   "\tauthor = {" + authors + "},\n" +
                   "\tjournal = {" + journalO + "},\n" +
                   "\tyear = {" + ano + "},\n" +
                   "}")
        file.close()
        parent.onChanged()
        self.close()

    #/Pestaña Numero 2
    
    #Pestaña Numero 3
    def GenerarArticuloPlano(self):
        texto = self.te_source.toPlainText()
        print(texto)
        #Titulo
        patternTitulo = "((title:?={[\s*\w{0,}(\-)]{0,}})|(title\s:?=\s{[\s*\w{0,}(\-)]{0,}}))"
        xTitulo = re.search(patternTitulo, texto)
        #print(xTitulo)

        pstTitulo = int(xTitulo.span()[0])
        pst2Titulo = int(xTitulo.span()[1])
        #print(pstTitulo)
        #print(pst2Titulo)

        if(texto[pst2Titulo] == '}'):
            print("Llave Final")

        if(texto[pstTitulo+6] == '{'):
            titulo = texto[pstTitulo+7:pst2Titulo-1]
        else:
            titulo = texto[pstTitulo+9:pst2Titulo-1]
        print("El titulo es: " + titulo)
        #/titulo
        
        #author
        patternAuthor = "((author:?={[\s*\w{0,}(\-)]{0,}})|(author\s:?=\s{[\s*\w{0,}(\-)]{0,}}))"
        xAuthor = re.search(patternAuthor, texto)

        pstAuthor = int(xAuthor.span()[0])
        pst2Author = int(xAuthor.span()[1])

        if(texto[pstAuthor+7] == '{'):
            author = texto[pstAuthor+8:pst2Author-1]
        else:
            author = texto[pstAuthor+10:pst2Author-1]
        print("El autor es: " + author)
        #/author
        #Journal
        patternJournal = "((journal:?={[\s*\w{0,}(\-)]{0,}})|(journal\s:?=\s{[\s*\w{0,}(\-)]{0,}}))"
        xJournal = re.search(patternJournal, texto)

        pstJournal = int(xJournal.span()[0])
        pst2Journal = int(xJournal.span()[1])

        if(texto[pstJournal+8] == '{'):
            journal = texto[pstJournal+9:pst2Journal-1]
        else:
            journal = texto[pstJournal+11:pst2Journal-1]
        print("El journal es: " + journal)
        #/Journal
        #Year
        patternYear = "((year:?={[\s*\w{0,}(\-)]{0,}})|(year\s:?=\s{[\s*\w{0,}(\-)]{0,}}))"
        xYear = re.search(patternYear, texto)

        pstYear = int(xYear.span()[0])
        pst2Year = int(xYear.span()[1])
        #print(pstYear)
        #print(pst2Year)

        if(texto[pstYear+5] == '{'):
            year = texto[pstYear+6:pst2Year-1]
        else:
            year = texto[pstYear+8:pst2Year-1]
        print("El año es: " + year)
        #/Year
        #Tipo
        patternTipo = "@(\w{0,})"
        xTipo = re.search(patternTipo, texto)

        pstTipo = int(xTipo.span()[0])
        pst2Tipo = int(xTipo.span()[1])

        tipo = texto[pstTipo+1:pst2Tipo]
        print("El tipo es: " + tipo)
        #/Tipo
        #Llave
        patternLlave = "{(\w{0,}),"
        xLlave = re.search(patternLlave, texto)

        pstLlave = int(xLlave.span()[0])
        pst2Llave = int(xLlave.span()[1])

        llave = texto[pstLlave+1:pst2Llave-1]
        print("La llave es: " + llave)
        #/Llave
        file = open(self.repositorioGeneral + "/" + self.direccionGeneral, "a")
        file.write("\n@" + tipo + "{" + llave + ",\n" +
                   "\ttitle = {" + titulo + "},\n" +
                   "\tauthor = {" + author + "},\n" +
                   "\tjournal = {" + journal + "},\n" +
                   "\tyear = {" + year + "},\n" +
                   "}")
        file.close()
        parent.onChanged()
        self.close()
    #/Pestaña Numero 3

    '''def closeEvent(self, event):
        pregunta = QMessageBox.question(self, "Salir", "¿Desea Cancelar el Proceso?", QMessageBox.Yes | QMessageBox.No)
        if pregunta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = AbrirVista()
    GUI.show()
    sys.exit(app.exec_())