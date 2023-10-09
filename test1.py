# importing libraries 
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys 
import os
cxfel_root = os.environ['CXFEL_ROOT']
startup_file = cxfel_root+'/misc_tools/startup.py'
exec(open(startup_file).read())
from misc_tools import read_h5

class Window(QMainWindow): 
    
    def __init__(self): 
        super().__init__() 

        # setting title 
        self.setWindowTitle("Diffusion Map") 

        # setting geometry 
        self.setGeometry(200, 200, 900, 400) 

        self.file_path = None
        # calling method 
        self.LoadFile()
        self.parameter_box("Variable Name:",10,50,110,30)
        self.parameter_box("h5",10,90,40,30)
        self.parameter_box("Transpose",10,130,100,30)
        self.parameter_box("Nearest Neighbour:",10,170,140,30)
        self.parameter_box("Sigma Factor:",10,210,110,30)
        self.parameter_box("nEigs:",10,250,60,30)
        self.line1 = QLineEdit("",self)
        self.line1.setGeometry(150,50,60,30)
        self.line2 = QLineEdit("",self)
        self.line2.setGeometry(150,90,60,30)
        self.line3 = QLineEdit("",self)
        self.line3.setGeometry(150,130,60,30)
        self.line4 = QLineEdit("",self)
        self.line4.setGeometry(150,170,60,30)
        self.line5 = QLineEdit("",self)
        self.line5.setGeometry(150,210,60,30)
        self.line6 = QLineEdit("",self)
        self.line6.setGeometry(150,250,60,30)
       


        self.v_name,self.nN,self.sigfac = None,None,None
        self.save_variable()

        # showing all the widgets 
        self.show() 

    def open_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print('Data file ' + fileName + ' is selected')
            self.popup_text(fileName,120,10,200,30)
            self.file_path = fileName

    def LoadFile(self):
        button_load= QPushButton("Open Data File", self)
        button_load.setGeometry(10,10,100,30)
        button_load.clicked.connect(self.open_dialog)
#       
    def popup_text(self,a,x,y,w,h):
        line_file = QLineEdit(a,self)
        line_file.setGeometry(x,y,w,h)
        line_file.show()

    def parameter_box(self,a,x,y,w,h):
        label = QLabel(a, self)
        label.setGeometry(x,y,w,h)
        label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        label.setLineWidth(2)
        label.setMidLineWidth(2)
        label.show()

    def save_variable(self):
        button = QPushButton("OK",self)
        button.setGeometry(810,350,50,30) 
        button.clicked.connect(self.click_save)
        
    def click_save(self):
##            global v_name,nN,sigfac
        self.v_name = str(self.line1.text())
        self.h5 = bool(self.line2.text())
        self.transpose = bool(self.line3.text())
        self.nN = int(self.line4.text())
#        print(self.v_name,self.nN,self.sigfac,self.file_path)




    # method for components 
    def UiComponents(self): 

        # creating a QLineEdit object 
        line_edit = QLineEdit("Variable Name: ", self) 

        # setting geometry 
        line_edit.setGeometry(180, 80, 150, 40) 

        # creating a label 
    #    label = QLabel("GfG", self) 

        # setting geometry to the label 
    #    label.setGeometry(80, 150, 120, 60) 

        # setting word wrap property of label 
    #    label.setWordWrap(True) 

        # adding action to the line edit when enter key is pressed 
    #    line_edit.returnPressed.connect(lambda: do_action()) 

        # method to do action 
    #    def do_action(): 

            # getting text from the line edit 
     #       value = line_edit.text() 

            # setting text to the label 
      #      label.setText(value) 




# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
window = Window() 
# start the app 
sys.exit(App.exec()) 
