##############################################################################
## Created by Emmanuel Flores for use on development of the game ToTheTop   ##
## by Team Fire                                                             ##
##############################################################################

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os


class ExtendedQLabel(QLabel):
 
	def __init__(self, parent, id):
		QLabel.__init__(self, parent)
		
		self.parent = parent
		self.id = id
		
		self.pixIdx = 0
		self.pixmaps = []

		self.pixmaps.append(QPixmap(self.parent.cwd + "/images/dotted_frame.png"))
		self.pixmaps.append(QPixmap(self.parent.cwd + "/images/emptyTrunk.png"))
		self.pixmaps.append(QPixmap(self.parent.cwd + "/images/beehiveTrunk.png"))
		self.pixmaps.append(QPixmap(self.parent.cwd + "/images/snakeTrunk.png"))
		self.pixmaps.append(QPixmap(self.parent.cwd + "/images/bushTrunk.png"))
		
	def getIdx(self):
		return self.pixIdx;
		
	def getPic(self):
		return self.pixmaps[self.pixIdx]
 
	def altSetPic(self,new_idx):
		self.pixIdx = new_idx
		self.setPixmap(self.pixmaps[self.pixIdx].scaled(self.size()))
 
	def setPic(self,new_idx):
		if (new_idx == 0 and self.pixIdx == 4) or new_idx == 4:
			if self.id % 3 == 0:
				self.parent.images[self.id+1].altSetPic(new_idx)
				self.parent.images[self.id+2].altSetPic(new_idx)
			elif self.id % 3 == 1:
				self.parent.images[self.id-1].altSetPic(new_idx)
				self.parent.images[self.id+1].altSetPic(new_idx)
			else:
				self.parent.images[self.id-2].altSetPic(new_idx)
				self.parent.images[self.id-1].altSetPic(new_idx)	
		elif self.pixIdx == 4 or new_idx == 5:
			if self.id % 3 == 0:
				self.parent.images[self.id+1].altSetPic(1)
				self.parent.images[self.id+2].altSetPic(1)
			elif self.id % 3 == 1:
				self.parent.images[self.id-1].altSetPic(1)
				self.parent.images[self.id+1].altSetPic(1)
			else:
				self.parent.images[self.id-2].altSetPic(1)
				self.parent.images[self.id-1].altSetPic(1)
				
		if new_idx == 5:
			new_idx = 1
			
		self.pixIdx = new_idx
		self.setPixmap(self.pixmaps[self.pixIdx].scaled(self.size()))
 
	def mousePressEvent(self, event):
		if event.type() == QEvent.MouseButtonPress and ( event.button() == Qt.LeftButton and not self.parent.shiftKeyPressed and not self.parent.ctrlKeyPressed ):
			self.setPic(self.parent.itemSelected)
			self.parent.istranslating = False
			self.parent.setWindowTitle("*%s"%(self.parent.windowTitle))
		elif event.type() == QEvent.MouseButtonPress and ( event.button() == Qt.MidButton or ( event.button() == Qt.LeftButton and self.parent.shiftKeyPressed ) ):
			self.parent.istranslating = True
			self.parent.iszooming = False
			self.parent.clicked = event.globalPos()
			self.parent.pos = self.parent.images[0].geometry().topLeft()
		elif event.type() == QEvent.MouseButtonPress and self.parent.ctrlKeyPressed and event.button() == Qt.LeftButton:
			self.parent.istranslating = False
			self.parent.iszooming = True
			self.parent.clicked = event.globalPos()
		else:
			self.parent.istranslating = False
			self.parent.iszooming = False
			
	def mouseMoveEvent(self,event):
		if self.parent.istranslating:
			dx = event.globalX() - self.parent.clicked.x()
			dy = event.globalY() - self.parent.clicked.y()
			if self.parent.pos.x()+dx >= self.parent.leftBorder and self.parent.pos.x()+self.parent.images[0].geometry().width()*3+dx <= self.parent.rightBorder:
				hOffset = self.parent.images[0].geometry().height()
				wOffset = self.parent.images[0].geometry().width()
				for i in range(len(self.parent.images)):
					if i % 3 == 0:
						if i == 0:
							self.parent.images[i].move(self.parent.pos.x()+dx,self.parent.pos.y()+dy)
						else:
							self.parent.images[i].move(self.parent.pos.x()+dx,self.parent.pos.y()+dy+hOffset*int(i/3))
					elif i % 3 == 1:
						if i == 1:
							self.parent.images[i].move(self.parent.pos.x()+dx+wOffset,self.parent.pos.y()+dy)
						else:
							self.parent.images[i].move(self.parent.pos.x()+dx+wOffset,self.parent.pos.y()+dy+hOffset*int(i/3))
					else:
						if i == 2:
							self.parent.images[i].move(self.parent.pos.x()+dx+wOffset*2,self.parent.pos.y()+dy)
						else:
							self.parent.images[i].move(self.parent.pos.x()+dx+wOffset*2,self.parent.pos.y()+dy+hOffset*int(i/3))
		elif self.parent.iszooming:
			if event.globalY() > self.parent.clicked.y()+10:
				self.parent.zoom(-120)
				self.parent.clicked = event.globalPos()
			elif event.globalY() < self.parent.clicked.y()-10:
				self.parent.zoom(120)
				self.parent.clicked = event.globalPos()


#############Define MyWindow Class Here ############
class MyWindow(QMainWindow):
##-----------------------------------------
	def __init__(self, altGridHeight=25, readLevel=False, readFile=""):
		QMainWindow.__init__(self)
		
		self.x = 0
		self.prev_x = 0
		self.zoom_step = 10
		
		self.max_zoom = 10
		self.min_zoom = -5
		
		self.leftBorder = 400
		self.rightBorder = 400
		
		self.istranslating = False
		self.iszooming = False
		
		self.gridHeight = altGridHeight #number of tree trunk sections
		
		self.readLevel = readLevel	#determines whether the designer should load a new scene or read in a level from file
		self.readFile = readFile
		
		self.itemSelected = 0
		
		self.btns = []
		
		self.windowTitle = "Level Designer"

		self.cwd = os.getcwd()
			
		self.shiftKeyPressed = False
		self.ctrlKeyPressed = False
		
		self.initUI()

##-----------------------------------------		
	def initUI(self):
		i = 0
		self.images = []
		
		if not self.readLevel:
			for i in range(self.gridHeight):
				for j in range(3):
					self.images.append(ExtendedQLabel(self,i*3+j))
					self.images[-1].setGeometry(800+100*j,900-100*(self.gridHeight-i),100,100)
					self.images[-1].setPixmap(self.images[-1].getPic().scaled(self.images[-1].size()))
		else:
			self.readInFile()
		
		#Create control buttons
		emptyTreeIcon = QIcon(QPixmap(self.cwd + "/images/emptyTrunk.png"))
		emptyTreeBtn = QPushButton("",self)
		emptyTreeBtn.setGeometry(100,50,120,120)
		emptyTreeBtn.setToolTip("Add empty tree trunk to one slot")
		emptyTreeBtn.setIcon(emptyTreeIcon)
		emptyTreeBtn.setIconSize(emptyTreeBtn.geometry().size()-QSize(20,20))
		emptyTreeBtn.clicked.connect(lambda : self.btnClick("emptyTrunk"))
		
		emptyTreesIcon = QIcon(QPixmap(self.cwd + "/images/tripleEmptyTrunk.png"))
		emptyTreesBtn = QPushButton("",self)
		emptyTreesBtn.setGeometry(100,200,120,120)
		emptyTreesBtn.setToolTip("Add empty tree trunk to all 3 trees")
		emptyTreesBtn.setIcon(emptyTreesIcon)
		emptyTreesBtn.setIconSize(emptyTreesBtn.geometry().size()-QSize(20,20))
		emptyTreesBtn.clicked.connect(lambda : self.btnClick("tripleEmptyTrunk"))
		
		beehiveTreeIcon = QIcon(QPixmap(self.cwd + "/images/beehiveTrunk.png"))
		beehiveTreeBtn = QPushButton("",self)
		beehiveTreeBtn.setGeometry(100,350,120,120)
		beehiveTreeBtn.setToolTip("Add beehive tree trunk to one slot")
		beehiveTreeBtn.setIcon(beehiveTreeIcon)
		beehiveTreeBtn.setIconSize(beehiveTreeBtn.geometry().size()-QSize(20,20))
		beehiveTreeBtn.clicked.connect(lambda : self.btnClick("beehiveTrunk"))
		
		snakeTreeIcon = QIcon(QPixmap(self.cwd + "/images/snakeTrunk.png"))
		snakeTreeBtn = QPushButton("",self)
		snakeTreeBtn.setGeometry(100,500,120,120)
		snakeTreeBtn.setToolTip("Add snake tree trunk to one slot")
		snakeTreeBtn.setIcon(snakeTreeIcon)
		snakeTreeBtn.setIconSize(snakeTreeBtn.geometry().size()-QSize(20,20))
		snakeTreeBtn.clicked.connect(lambda : self.btnClick("snakeTrunk"))
		
		bushTreeIcon = QIcon(QPixmap(self.cwd + "/images/bushTrunks.png"))
		bushTreeBtn = QPushButton("",self)
		bushTreeBtn.setGeometry(100,650,120,120)
		bushTreeBtn.setToolTip("Add bush tree trunk to all 3 trees")
		bushTreeBtn.setIcon(bushTreeIcon)
		bushTreeBtn.setIconSize(bushTreeBtn.geometry().size()-QSize(20,20))
		bushTreeBtn.clicked.connect(lambda : self.btnClick("bushTrunk"))
		
		eraseTreeIcon = QIcon(QPixmap(self.cwd + "/images/eraser.png"))
		eraseTreeBtn = QPushButton("",self)
		eraseTreeBtn.setGeometry(100,800,120,120)
		eraseTreeBtn.setToolTip("Erase one slot")
		eraseTreeBtn.setIcon(eraseTreeIcon)
		eraseTreeBtn.setIconSize(eraseTreeBtn.geometry().size()-QSize(20,20))
		eraseTreeBtn.clicked.connect(lambda : self.btnClick("eraseTrunk"))
		
		self.btns.append(emptyTreeBtn)
		self.btns.append(beehiveTreeBtn)
		self.btns.append(snakeTreeBtn)
		self.btns.append(bushTreeBtn)
		self.btns.append(emptyTreesBtn)
		self.btns.append(eraseTreeBtn)
		
		
		extendBtn = QPushButton("Extend",self)
		extendBtn.setToolTip("Extend the level height")
		extendBtn.clicked.connect(self.extendLevel)
		
		extendLabel = QLabel(self)
		extendLabel.setText("Extension:")
		
		self.extensionValue = QLineEdit(self)
		self.extensionValue.setText("10")
		self.extensionValue.setToolTip("Positive = Extend, Negative = Reduce")
		
		newBtn = QPushButton("New",self)
		newBtn.setToolTip("Start a new level design with the following height")
		newBtn.clicked.connect(self.newLevel)
		
		newheightLabel = QLabel(self)
		newheightLabel.setText("New height:")
		
		self.newHeight = QLineEdit(self)
		self.newHeight.setText("25")
		
		importBtn = QPushButton("Import",self)
		importBtn.setToolTip("Import level design")
		importBtn.clicked.connect(self.importLevel)
		
		filenameLabel1 = QLabel(self)
		filenameLabel1.setText("Filename:")
		
		self.importFilename = QLineEdit(self)
		self.importFilename.setText("")
		
		extensionLabel1 = QLabel(self)
		extensionLabel1.setText(".level")
		
		exportBtn = QPushButton("Export",self)
		exportBtn.setToolTip("Export the level design")
		exportBtn.clicked.connect(self.exportLevel)
		
		filenameLabel2 = QLabel(self)
		filenameLabel2.setText("Save as:")
		
		self.exportFilename = QLineEdit(self)
		self.exportFilename.setText("")
		
		extensionLabel2 = QLabel(self)
		extensionLabel2.setText(".level")
		
		
		lline = QFrame(self);
		lline.setFrameShape(QFrame.VLine);
		lline.setFrameShadow(QFrame.Sunken);

		rline = QFrame(self);
		rline.setFrameShape(QFrame.VLine);
		rline.setFrameShadow(QFrame.Sunken);
		
		
		linedivider1 = QFrame(self);
		linedivider1.setFrameShape(QFrame.HLine);
		linedivider1.setFrameShadow(QFrame.Sunken);
		
		linedivider2 = QFrame(self);
		linedivider2.setFrameShape(QFrame.HLine);
		linedivider2.setFrameShadow(QFrame.Sunken);
		
		linedivider3 = QFrame(self);
		linedivider3.setFrameShape(QFrame.HLine);
		linedivider3.setFrameShadow(QFrame.Sunken);
		
		self.levelNameLabel = QLabel(self)
		if self.readLevel:
			self.levelNameLabel.setText("Level Name: "+self.readFile+".level")
			self.exportFilename.setText(self.readFile)
			self.windowTitle += " [" + self.cwd + "\\levels\\" + str(self.readFile) + ".level]"
			self.setWindowTitle(self.windowTitle)
		else:
			self.levelNameLabel.setText("Level Name: [untitled]")
			self.windowTitle += " [untitled]"
			self.setWindowTitle(self.windowTitle)
		
		levelHeightLabel = QLabel(self)
		levelHeightLabel.setText("Level Height: "+str(self.gridHeight))
		
		
		self.showMaximized()
		
		self.levelNameLabel.setGeometry(self.leftBorder+20,self.geometry().height()-75,self.levelNameLabel.geometry().width()+100,self.levelNameLabel.geometry().height())
		levelHeightLabel.setGeometry(self.leftBorder+20,self.geometry().height()-50,levelHeightLabel.geometry().width()+100,levelHeightLabel.geometry().height())
		
		self.rightBorder = self.geometry().width() - self.rightBorder;
		
		lline.setGeometry(self.leftBorder,0,5,self.geometry().height())
		rline.setGeometry(self.rightBorder,0,5,self.geometry().height())
		
		linedivider1.setGeometry(self.rightBorder+30,self.geometry().height()/4,self.geometry().width()-self.rightBorder-60,5)
		linedivider2.setGeometry(self.rightBorder+30,2*self.geometry().height()/4,self.geometry().width()-self.rightBorder-60,5)
		linedivider3.setGeometry(self.rightBorder+30,3*self.geometry().height()/4,self.geometry().width()-self.rightBorder-60,5)
		
		newBtn.setGeometry((self.geometry().width()-self.rightBorder)/2+self.rightBorder-80,linedivider1.geometry().topLeft().y()-200,160,80)
		newheightLabel.move(newBtn.geometry().topLeft().x(),newBtn.geometry().topLeft().y()+100)
		self.newHeight.setGeometry(newBtn.geometry().topLeft().x(),newBtn.geometry().topLeft().y()+130,160,20)
		
		importBtn.setGeometry((self.geometry().width()-self.rightBorder)/2+self.rightBorder-80,linedivider2.geometry().topLeft().y()-200,160,80)
		filenameLabel1.move(importBtn.geometry().topLeft().x(),importBtn.geometry().topLeft().y()+100)
		self.importFilename.setGeometry(importBtn.geometry().topLeft().x(),importBtn.geometry().topLeft().y()+130,120,20)
		extensionLabel1.move(importBtn.geometry().topLeft().x()+125,importBtn.geometry().topLeft().y()+125)
		
		exportBtn.setGeometry((self.geometry().width()-self.rightBorder)/2+self.rightBorder-80,linedivider3.geometry().topLeft().y()-200,160,80)
		filenameLabel2.move(exportBtn.geometry().topLeft().x(),exportBtn.geometry().topLeft().y()+100)
		self.exportFilename.setGeometry(exportBtn.geometry().topLeft().x(),exportBtn.geometry().topLeft().y()+130,120,20)
		extensionLabel2.move(exportBtn.geometry().topLeft().x()+125,exportBtn.geometry().topLeft().y()+125)
		
		extendBtn.setGeometry((self.geometry().width()-self.rightBorder)/2+self.rightBorder-80,self.geometry().height()-200,160,80)
		extendLabel.move(extendBtn.geometry().topLeft().x(),extendBtn.geometry().topLeft().y()+100)
		self.extensionValue.setGeometry(extendBtn.geometry().topLeft().x(),extendBtn.geometry().topLeft().y()+130,160,20)
		
		
##-----------------------------------------		
	def newLevel(self):
		window = MyWindow(int(self.newHeight.text()))
		window.show()
		self.close()
		
##-----------------------------------------
	def importLevel(self):
		if self.importFilename.text() == "":
			QMessageBox.about(self, "File Not Specified", "Please specify the name of a level to import")
			return
		
		if not os.path.exists(self.cwd + "/levels/" + self.importFilename.text() + ".level"):
			QMessageBox.about(self, "File Not Found", "%s.level was not found in the levels/ directory" % (self.importFilename.text()))
			return
			
		window = MyWindow(0,True,self.importFilename.text())
		window.show()
		self.close()
	
##-----------------------------------------
	def exportLevel(self):
		if self.exportFilename.text() == "":
			QMessageBox.about(self, "File Not Specified", "Please specify a name for the level before exporting")
			return
	
		if not os.path.isdir(self.cwd + "/levels"):
			os.makedirs(self.cwd + "/levels")
			
		f = open(self.cwd + "/levels/" + self.exportFilename.text() + ".level","w+")
		
		for i in range(self.gridHeight-1,-1,-1):
			n1 = self.images[i*3].getIdx() if self.images[i*3].getIdx() > 0 else 1
			n2 = self.images[i*3+1].getIdx() if self.images[i*3+1].getIdx() > 0 else 1
			n3 = self.images[i*3+2].getIdx() if self.images[i*3+2].getIdx() > 0 else 1
			f.write( str(n1) + " " + str(n2) + " " + str(n3) + "\n" )
		
		f.close()
		
		QMessageBox.about(self, "File Saved Successfully", "%s.level has been saved in the levels/ directory" % (self.exportFilename.text()))

		self.levelNameLabel.setText("Level Name: "+self.exportFilename.text()+".level")
		self.windowTitle = "Level Designer [" + self.cwd + "\\levels\\" + self.exportFilename.text() + ".level]"
		self.setWindowTitle(self.windowTitle)

##-----------------------------------------
	def readInFile(self):
		f = open(self.cwd + "/levels/" + self.readFile + ".level", "r")
					
		lines = f.readlines()
		idx = 0
		row = 0
		
		self.gridHeight = len(lines)
		
		for line in reversed(lines):
			self.images.append(ExtendedQLabel(self,idx))
			self.images[-1].setGeometry(800,900-100*(self.gridHeight-row),100,100)
			self.images[-1].altSetPic(int(line[0]))
			idx = idx + 1
			self.images.append(ExtendedQLabel(self,idx))
			self.images[-1].setGeometry(900,900-100*(self.gridHeight-row),100,100)
			self.images[-1].altSetPic(int(line[2]))
			idx = idx + 1
			self.images.append(ExtendedQLabel(self,idx))
			self.images[-1].setGeometry(1000,900-100*(self.gridHeight-row),100,100)
			self.images[-1].altSetPic(int(line[4]))
			idx = idx + 1
			row = row + 1
		
		f.close()
	
##-----------------------------------------
	def extendLevel(self):
		if self.exportFilename.text() == "":
			QMessageBox.about(self, "File Not Specified", "Please specify a name to save the level before extending")
			return
	
		if not os.path.isdir(self.cwd + "/levels"):
			os.makedirs(self.cwd + "/levels")
			
		f = open(self.cwd + "/levels/" + self.exportFilename.text() + ".level","w+")
		
		extVal = int(self.extensionValue.text())
		
		for i in range(self.gridHeight-1,-1,-1):
			if extVal < 0 and i < -extVal :
				break
			n1 = self.images[i*3].getIdx() if self.images[i*3].getIdx() > 0 else 1
			n2 = self.images[i*3+1].getIdx() if self.images[i*3+1].getIdx() > 0 else 1
			n3 = self.images[i*3+2].getIdx() if self.images[i*3+2].getIdx() > 0 else 1
			f.write( str(n1) + " " + str(n2) + " " + str(n3) + "\n" )
			
		if extVal > 0:
			for i in range(extVal):
				f.write( "1 1 1\n" )
		
		f.close()
		
		QMessageBox.about(self, "File Saved Successfully", "%s.level has been saved in the levels/ directory" % (self.exportFilename.text()))

		window = MyWindow(0,True,self.exportFilename.text())
		window.show()
		self.close()
	
##-----------------------------------------	
	def btnClick(self,buttonId):
		for btn in self.btns:
			btn.setStyleSheet("background-color: none")
	
		if buttonId == "emptyTrunk":
			self.itemSelected = 1
			self.btns[0].setStyleSheet("background-color: green")
		elif buttonId == "beehiveTrunk":
			self.itemSelected = 2
			self.btns[1].setStyleSheet("background-color: green")
		elif buttonId == "snakeTrunk":
			self.itemSelected = 3
			self.btns[2].setStyleSheet("background-color: green")
		elif buttonId == "bushTrunk":
			self.itemSelected = 4
			self.btns[3].setStyleSheet("background-color: green")
		elif buttonId == "tripleEmptyTrunk":
			self.itemSelected = 5
			self.btns[4].setStyleSheet("background-color: green")
		else:
			self.itemSelected = 0
			self.btns[5].setStyleSheet("background-color: green")
			
##-----------------------------------------
	def zoom(self,zoomAmt):
		tempx = self.x + zoomAmt/120
		
		if tempx < self.prev_x and tempx >= self.min_zoom:
			for image in self.images:
				image.resize(image.geometry().width()-self.zoom_step,image.geometry().height()-self.zoom_step)
				image.setPixmap(image.getPic().scaled(image.size()))
				
			for i in range(len(self.images)):
				oldPos = self.images[i].geometry().topLeft()
				if i % 3 == 0:
					if i == 0:
						self.images[i].move(oldPos.x()+self.zoom_step,oldPos.y())
					else:
						self.images[i].move(oldPos.x()+self.zoom_step,oldPos.y()-self.zoom_step*int(i/3))
				elif i % 3 == 1:
					if i != 2:
						self.images[i].move(oldPos.x(),oldPos.y()-self.zoom_step*int(i/3))
				else:
					if i == 3:
						self.images[i].move(oldPos.x()-self.zoom_step,oldPos.y())
					else:
						self.images[i].move(oldPos.x()-self.zoom_step,oldPos.y()-self.zoom_step*int(i/3))
						
			self.x = tempx
			self.prev_x = self.x
			
		elif tempx > self.prev_x and tempx <= self.max_zoom and self.images[0].geometry().topLeft().x()-self.zoom_step >= self.leftBorder and self.images[2].geometry().topLeft().x()+self.images[2].geometry().width()+self.zoom_step*2 <= self.rightBorder:
			for image in self.images:
				image.resize(image.geometry().width()+self.zoom_step,image.geometry().height()+self.zoom_step)
				image.setPixmap(image.getPic().scaled(image.size()))
			
			for i in range(len(self.images)):
				oldPos = self.images[i].geometry().topLeft()
				if i % 3 == 0:
					if i == 0:
						self.images[i].move(oldPos.x()-self.zoom_step,oldPos.y())
					else:
						self.images[i].move(oldPos.x()-self.zoom_step,oldPos.y()+self.zoom_step*int(i/3))
				elif i % 3 == 1:
					if i != 1:
						self.images[i].move(oldPos.x(),oldPos.y()+self.zoom_step*int(i/3))
				else:
					if i == 2:
						self.images[i].move(oldPos.x()+self.zoom_step,oldPos.y())
					else:
						self.images[i].move(oldPos.x()+self.zoom_step,oldPos.y()+self.zoom_step*int(i/3))
						
			self.x = tempx
			self.prev_x = self.x
			
##-----------------------------------------
	def wheelEvent(self,event):
		self.zoom(event.delta())

##-----------------------------------------			
	def mousePressEvent(self,event):
		if event.type() == QEvent.MouseButtonPress and ( event.button() == Qt.MidButton or ( self.shiftKeyPressed and event.button() == Qt.LeftButton) ):
			self.istranslating = True
			self.iszooming = False
			self.clicked = event.globalPos()
			self.pos = self.images[0].geometry().topLeft()
		elif event.type() == QEvent.MouseButtonPress and self.ctrlKeyPressed and event.button() == Qt.LeftButton:
			self.istranslating = False
			self.iszooming = True
			self.clicked = event.globalPos()
		else:
			self.istranslating = False
			self.iszooming = False

##-----------------------------------------			
	def mouseMoveEvent(self,event):
		if self.istranslating:
			dx = event.globalX() - self.clicked.x()
			dy = event.globalY() - self.clicked.y()
			if self.pos.x()+dx >= self.leftBorder and self.pos.x()+self.images[0].geometry().width()*3+dx <= self.rightBorder:
				hOffset = self.images[0].geometry().height()
				wOffset = self.images[0].geometry().width()
				for i in range(len(self.images)):
					if i % 3 == 0:
						if i == 0:
							self.images[i].move(self.pos.x()+dx,self.pos.y()+dy)
						else:
							self.images[i].move(self.pos.x()+dx,self.pos.y()+dy+hOffset*int(i/3))
					elif i % 3 == 1:
						if i == 1:
							self.images[i].move(self.pos.x()+dx+wOffset,self.pos.y()+dy)
						else:
							self.images[i].move(self.pos.x()+dx+wOffset,self.pos.y()+dy+hOffset*int(i/3))
					else:
						if i == 2:
							self.images[i].move(self.pos.x()+dx+wOffset*2,self.pos.y()+dy)
						else:
							self.images[i].move(self.pos.x()+dx+wOffset*2,self.pos.y()+dy+hOffset*int(i/3))
		elif self.iszooming:
			if event.globalY() > self.clicked.y()+10:
				self.zoom(-120)
				self.clicked = event.globalPos()
			elif event.globalY() < self.clicked.y()-10:
				self.zoom(120)
				self.clicked = event.globalPos()
	
##-----------------------------------------
	def keyPressEvent(self, event):
		if type(event) == QKeyEvent and event.key() == Qt.Key_Shift:
			self.shiftKeyPressed = True
		elif type(event) == QKeyEvent and event.key() == Qt.Key_Control:
			self.ctrlKeyPressed = True
			
##-----------------------------------------
	def keyReleaseEvent(self, event):
		if type(event) == QKeyEvent and event.key() == Qt.Key_Shift:
			self.shiftKeyPressed = False
		elif type(event) == QKeyEvent and event.key() == Qt.Key_Control:
			self.ctrlKeyPressed = False
	
##-----------------------------------------
##########End of Class Definition ################## 


def main():
	app = QApplication(sys.argv)
	
	if len(sys.argv) > 1:
		window = MyWindow(int(sys.argv[1]))
		window.show()
	else:
		window = MyWindow()
		window.show() 
	
	sys.exit(app.exec_())
 
if __name__ == "__main__": 
	main() 