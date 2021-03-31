import os
#
os.system("del *.pdf") # Termine sin error
os.system("del *.aux *.bbl *.blg *.bcf *.out *.xml *.log")

os.system("pdflatex 23.tex")
os.system("biber 23")
os.system("pdflatex 23.tex")
os.system("pdflatex 23.tex")
# Compilar segundo listado
os.system("pdflatex 21.tex")
os.system("biber 21")
os.system("pdflatex 21.tex")
os.system("pdflatex 21.tex")
# Compilar las "N" items del respositorio, cada una genera su propior documento PDF

# Compilar el documento "Principal"

os.system("pdflatex ListadodeArticulos_y_Citas.tex")
os.system("biber Pequeno")
os.system("pdflatex ListadodeArticulos_y_Citas.tex")
os.system("pdflatex ListadodeArticulos_y_Citas.tex")


