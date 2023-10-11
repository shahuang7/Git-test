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
        self.line1.setGeometry(160,50,60,30)
        self.line2 = QLineEdit("",self)
        self.line2.setGeometry(160,90,60,30)
        self.line3 = QLineEdit("",self)
        self.line3.setGeometry(160,130,60,30)
        self.line4 = QLineEdit("",self)
        self.line4.setGeometry(160,170,60,30)
        self.line5 = QLineEdit("",self)
        self.line5.setGeometry(160,210,60,30)
        self.line6 = QLineEdit("",self)
        self.line6.setGeometry(160,250,60,30)
       


        self.v_name,self.nN,self.sigfac,self.h5,self.nEigs,self.transpose = None,None,None,None,None,None
        self.save_variable()
        self.run_button()

        # showing all the widgets 
        self.show() 

    def open_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print('Data file ' + fileName + ' is selected')
            self.popup_text(fileName,170,10,300,30)
            self.file_path = fileName

    def LoadFile(self):
        button_load= QPushButton("Open Data File", self)
        button_load.setGeometry(10,10,150,30)
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
        button = QPushButton("Save Parameter",self)
        button.setGeometry(700,280,150,30) 
        button.clicked.connect(self.click_save)
        button.clicked.connect(self.print_log)

    def print_log(self):
        text = " Data = {} \n Variable Name = {} \n h5 = {} \n Transpose = {} \n nN = {} \n Sigma Factor = {} \n nEigs = {}".format(self.file_path,self.v_name,self.h5,self.transpose,self.nN,self.sigfac,self.nEigs)
        label = QLabel(text,self)
        label.setGeometry(500,20,300,120)
        label.show()
        
    def click_save(self):
##            global v_name,nN,sigfac
        self.v_name = str(self.line1.text())
        self.h5 = bool(self.line2.text())
        self.transpose = bool(self.line3.text())
        self.nN = int(self.line4.text())
        self.sigfac = float(self.line5.text())
        self.nEigs = int(self.line6.text()) 
#        print(self.v_name,self.nN,self.sigfac,self.file_path)

    def run_button(self):
        button = QPushButton("Run",self)
        button.setGeometry(700,320,150,30) 
        button.clicked.connect(self.click_run)

    def click_run(self):
        xyz = read_h5(self.file_path,self.v_name,self.h5,self.transpose)
        yRow_yCol_yVal_file = 'sqDist.h5'
        nN = self.nN
        sigma_factor = self.sigfac
        nEigs = self.nEigs
        alpha = 1.0

        from scipy.spatial.distance import cdist
        sqDist = cdist(xyz,xyz,'sqeuclidean')
        from sparsify import smallest_items_in_each_row_of_table,symmetrize
        from misc_tools import write_h5
        yRow,yCol,yVal = smallest_items_in_each_row_of_table(sqDist,nN)
        yRow_symm,yCol_symm,yVal_symm = symmetrize(yRow,yCol,yVal)
        write_h5(yRow_yCol_yVal_file,yRow_symm,'yRow')
        write_h5(yRow_yCol_yVal_file,yCol_symm,'yCol')
        write_h5(yRow_yCol_yVal_file,yVal_symm,'yVal')

        label = QLabel("sqDist Done",self)
        label.setGeometry(500,140,100,30)
        label.show()

        from ferguson import analyze as fer_ana

        sigma_opt,_ = fer_ana(yRow_yCol_yVal_file)
        label = QLabel("Ferguson Analysis Done",self)
        label.setGeometry(500,180,200,30)
        label.show()

        from diffmap import analyze as diff_ana
        from diffmap import plot2D
        sigma = sigma_factor*sigma_opt
        h5_eigVec_eigVal = diff_ana(yRow_yCol_yVal_file,sigma,nEigs,alpha)
        eigVec = read_h5(h5_eigVec_eigVal,'eigVec')
     
        label = QLabel("Diffuion map analysis Done",self)
        label.setGeometry(500,220,200,30)
        label.show() 

        for j in [1]:
  # colored based on \psi_j
            write_h5('colorcode.h5',eigVec[:,j]/eigVec[:,0],'colorcode')
            figure_name = plot2D(h5_eigVec_eigVal,[1,2],s=20)
            os.rename(figure_name,'diffmap_2D_psi_1_2_psi_{}_colored.jpg'.format(j))

        plot_button = QPushButton("Display",self)
        plot_button.setGeometry(700,360,150,30)
        plot_button.clicked.connect(self.plot)
        plot_button.show()
    
    def plot(self):
        self.w = AnotherWindow()
        self.w.show()
#            w.label = QLabel(self)
#            pixmap = QPixmap('diffmap_2D_psi_1_2_psi_1_colored.jpg')
#            w.label.setPixmap(pixmap)

            
class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        layout = QVBoxLayout()
        pixmap = QPixmap('diffmap_2D_psi_1_2_psi_1_colored.jpg')
        self.label.setPixmap(pixmap)

        layout.addWidget(self.label)
        self.setLayout(layout)



# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
window = Window() 
# start the app 
sys.exit(App.exec()) 
#App.exec()