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


# The Overall Window
class Window(QMainWindow): 
	
	def __init__(self): 
		super().__init__() 

		# setting title 
		self.setWindowTitle("Diffusion Map") 

		# setting geometry 
		self.setGeometry(200, 200, 900, 450) 
		self.tab_widget = MyTabWidget(self) 
		self.setCentralWidget(self.tab_widget) 

		self.show()

# Tabs 
class MyTabWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget() 

		# First tab : main 
		self.tab1 = QWidget()
#		self.resize(900,400)
	#	self.tab1.layout = QVBoxLayout(self.tab1) 
		self.file_path = None

		# Load File
		self.LoadFile()
		
		# Put parameter box
		self.parameter_box("Transpose",10,130,100,30)
		self.parameter_box("Nearest Neighbour:",10,170,140,30)
		self.parameter_box("Sigma Factor:",10,210,110,30)
		self.parameter_box("nEigs:",10,250,60,30)
		self.checkbox_transpose = QCheckBox(self.tab1)
		self.checkbox_transpose.setGeometry(160,130,60,30)
		self.line4 = QLineEdit("",self.tab1)
		self.line4.setGeometry(160,170,60,30)
		self.line5 = QLineEdit("",self.tab1)
		self.line5.setGeometry(160,210,60,30)
		self.line6 = QLineEdit("",self.tab1)
		self.line6.setGeometry(160,250,60,30)
	   
		# Claiming parameters
		self.v_name,self.nN,self.sigfac,self.h5,self.nEigs,self.transpose = None,None,None,None,None,None
		self.save_variable()
		self.run_button()

	#	self.tab1.layout.addWidget(p1)
	#	self.tab1.layout.addWidget(p2)
	#	self.tab1.layout.addWidget(p3)
	#	self.tab1.layout.addWidget(p4)
	#	self.tab1.setLayout(self.tab1.layout) 

		self.tabs.addTab(self.tab1, "Main")
		self.layout.addWidget(self.tabs) 
		self.setLayout(self.layout) 

	# Open File Function
	def open_dialog(self):
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(self.tab1,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print('Data file ' + fileName + ' is selected')
			self.popup_text(fileName,170,10,300,30)
			self.file_path = fileName
			self.parameter_box("h5",10,50,40,30)
			button_variable=QPushButton("Variable Name:",self.tab1)
			button_variable.setGeometry(10,90,110,30)
			button_variable.clicked.connect(self.pulldown_v)
			button_variable.show()
			self.checkbox_h5 = QCheckBox(self.tab1)
			self.checkbox_h5.setGeometry(160,50,60,30)
			self.checkbox_h5.show()
	
	def pulldown_v(self):
		if self.checkbox_h5.isChecked():
			import h5py
			import numpy as np
			f = h5py.File(self.file_path,'r')
			self.v_list = list(f.keys())
		else:
			from scipy.io import loadmat
			f = loadmat(str(self.file_path))
			self.v_list = list(f.keys()) 
		self.line1 = QComboBox(self.tab1)
		self.line1.setGeometry(160,90,120,30)
		self.line1.addItems(self.v_list[::-1])
		self.line1.show()             


	def LoadFile(self):
		button_load= QPushButton("Open Data File", self.tab1)
		button_load.setGeometry(10,10,150,30)
		button_load.clicked.connect(self.open_dialog)
	   
	def get_variable_names(self):
		if self.h5:
			import h5py
			import numpy as np
			f = h5py.File(self.file_path,'r')
			self.v_list = list(f.keys())
		else:
			from scipy.io import loadmat
			f = loadmat(str(self.file_path))
			self.v_list = list(f.keys()) 


	def popup_text(self,a,x,y,w,h):
		line_file = QLineEdit(a,self.tab1)
		line_file.setGeometry(x,y,w,h)
		line_file.show()

	def parameter_box(self,a,x,y,w,h):
		label = QLabel(a, self.tab1)
		label.setGeometry(x,y,w,h)
		label.setFrameStyle(QFrame.Panel | QFrame.Raised)
		label.setLineWidth(2)
		label.setMidLineWidth(2)
		label.show()

	def save_variable(self):
		button = QPushButton("Save Parameter",self.tab1)
		button.setGeometry(700,280,150,30) 
		button.clicked.connect(self.click_save)
		button.clicked.connect(self.print_log)

	def print_log(self):
		text = " Data = {} \n Variable Name = {} \n h5 = {} \n Transpose = {} \n nN = {} \n Sigma Factor = {} \n nEigs = {}".format(self.file_path,self.v_name,self.h5,self.transpose,self.nN,self.sigfac,self.nEigs)
		label = QLabel(text,self.tab1)
		label.setGeometry(500,20,300,120)
		label.show()
		
	def click_save(self):
##            global v_name,nN,sigfac
#        self.v_name = str(self.line1.text())
		self.h5 = self.checkbox_h5.isChecked()
		self.transpose = self.checkbox_transpose.isChecked()
		self.nN = int(self.line4.text())
		self.sigfac = float(self.line5.text())
		self.nEigs = int(self.line6.text()) 
		self.v_name = self.line1.currentText()  
#        print(self.v_name,self.nN,self.sigfac,self.file_path)

#    def check_h5(self,checked):
#        if checked:
#            self.h5 = True
#        else: 
#            self.h5 = False

	def run_button(self):
		button = QPushButton("Run",self.tab1)
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

		label = QLabel("sqDist Done",self.tab1)
		label.setGeometry(500,140,100,30)
		label.show()

		from ferguson import analyze as fer_ana

		sigma_opt,_ = fer_ana(yRow_yCol_yVal_file)
		label = QLabel("Ferguson Analysis Done",self.tab1)
		label.setGeometry(500,180,200,30)
		label.show()

		from diffmap import analyze as diff_ana
		from diffmap import plot2D
		sigma = sigma_factor*sigma_opt
		self.h5_eigVec_eigVal = diff_ana(yRow_yCol_yVal_file,sigma,nEigs,alpha)
		
	 
		label = QLabel("Diffuion map analysis Done",self.tab1)
		label.setGeometry(500,220,200,30)
		label.show() 

		self.line_eigv1 = QLineEdit("",self.tab1)
		self.line_eigv1.setGeometry(500,325,40,25)
		self.line_eigv1.show()
		self.parameter_box("Eigen Vector Index: ",360,320,130,30)
		self.line_eigv2 = QLineEdit("",self.tab1)
		self.line_eigv2.setGeometry(500,365,40,25)
		self.line_eigv2.show()
		self.parameter_box("Eigen Vector Index: ",360,360,130,30)

#        for j in [1]:
  # colored based on \psi_j
#            write_h5('colorcode.h5',eigVec[:,j]/eigVec[:,0],'colorcode')
#            figure_name = plot2D(h5_eigVec_eigVal,[1,2],s=20)
#            os.rename(figure_name,'diffmap_2D_psi_1_2_psi_{}_colored.jpg'.format(j))

		plot_button = QPushButton("Display",self.tab1)
		plot_button.setGeometry(700,360,150,30)
		plot_button.clicked.connect(self.plot)
		plot_button.show()
	
	def plot(self):
		eigVec = read_h5(self.h5_eigVec_eigVal,'eigVec')
		ev1 = int(self.line_eigv1.text())
		ev2 = int(self.line_eigv2.text())
		x = eigVec[:,ev1]/eigVec[:,0]
		y = eigVec[:,ev2]/eigVec[:,0]
		import matplotlib.pyplot as plt
		fig,ax1 = plt.subplots(1,1)
		fig.set_size_inches(8,6)
		sc1 = ax1.scatter(x,y,c='k',s=5)
		my_xlabel = '$\Psi_'+str(ev1)+'$'
		my_ylabel = '$\Psi_'+str(ev2)+'$'
		ax1.set_xlabel(my_xlabel,fontsize=15)
		ax1.set_ylabel(my_ylabel,fontsize=15)
		ax1.set_aspect('equal','box')
		figure_name = 'diffmap_2D.jpg'
		plt.savefig(figure_name,bbox_inches='tight')

		self.tab2 = QWidget()
		label = QLabel(self.tab2)
		layout = QVBoxLayout()
		pixmap = QPixmap('diffmap_2D.jpg')
		label.setPixmap(pixmap)

		layout.addWidget(label)
		self.tab2.setLayout(layout)

		self.tabs.addTab(self.tab2, "Manifold")


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
		pixmap = QPixmap('diffmap_2D.jpg')
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