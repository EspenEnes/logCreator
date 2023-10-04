import os

cwd = os.getcwd()
os.system(f'cmd /c "pyinstaller --noconfirm --onefile --windowed --icon "{cwd}/QtDesign/icon.ico" --add-data "{cwd}/QtDesign;QtDesign/"  "{cwd}/main.py"')


#pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/enese/PycharmProjects/logCreator/QtDesign/icon.ico" --add-data "C:/Users/enese/PycharmProjects/logCreator/QtDesign;QtDesign/"  "C:/Users/enese/PycharmProjects/logCreator/main.py"