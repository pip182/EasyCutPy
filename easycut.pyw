#!/usr/bin/python

#0.1 = proof of concept / simple square -Done!!
#0.2 = cut out rectangle and 3/4 dadoes
#0.3 = mostly functioning lines
#0.4 = all line functions/tool change/options/save @ load
#0.5 = resizeable and reusable parts
#0.6 = preview window
#0.7 = Line Bore
#......
#1.0 = Able to cut out any part accuratly


import sys, pickle
from PyQt4 import QtGui, QtCore

#Tool Information you can and should change this...
#       Tool Name      |    Tool size
tool = [["1/2 Downcut",  0.498],    #1
        ["V-Groove Bit",  0.0],     #2   
        ["Slot Cutter",  1.942],    #3
        ["Nothing",  0.0],          #4
        ["1/2 Downcut",  0.498],    #5
        ["1/4 Bit",  0.225],        #6
        ["3/8 Bit",  0.370],        #7
        ["Surfacing Bit",  3.75]]   #8

#Global Variables DO NOT CHANGE!!!!!!
xCut = 0 
yCut = 1
xCutPos = 2
xCutNeg = 3
yCutPos = 4
yCutNeg = 5
topCut = 6
bottomCut = 7
leftCut = 8
rightCut = 9
yes = 1
no = 0 
vLine = 6
hLine = 7
version = "0.5 Beta 2.1  "

mainRect= 1
rabbet = 2
absLine= 3
dado34 = 4
toolChange = 5
relLine = 6


fileOutHeader = ["(BRAD RULES)", 
    "(SIMPLE CUTOUT)", 
    "G20", # Set's input to inch. 
    "G91 G28 Z0 M15", 
    "G90 G40 G49 M22", 
    "M25",
    "M06",
    "G08 P1"]


fileOutFooter =  ["G0 Z1.2500 M59", 
    "G40", 
    "G91 G28 Z0 M15", 
    "G90 G49 H0 M22", 
    "M25", 
    "M88 B0", 
    "M89 B0", 
    "G08 P0", 
    "G0 X60.0 Y120.0"]



class commandClass:
    type = 0
    z = 0.7
    cutEdge = no
    twoPass = no
    cutType = 0.0
    cutLength = 0.0
    x = 0.0
    y = 0.0
    xx = 0.0
    yy = 0.0
    text = "blank"
    toolNumber = 7
    negPoint = 0
    posPoint = 0 
    negFrom = no
    posFrom = no
    offset = 0.0
    
class variableClass:
    testDepth = 0.73
    finalDepth = -0.0051
    edgeOffset = 0.1875
    tightness34 = 0.753
    mainRectNum = 0
    rectCreated = no
    defaultTool = 7
    defaultToolSize = 0.370
    listRectNum = 0




class cutClass:
    def __init__(self,  output_file):
        global var
        self.outFile = open(output_file, "w")
        self.bitOffset = 0.29
        self.lineNum = 0 
        self.pushOff = 0
        self.toolNum = 0
      
        #Initial Header
        for x in range(0, len(fileOutHeader)):
            print >> self.outFile,  fileOutHeader[x]
          
        
    def line(self,  x,  y):
        print >> self.outFile,  "G1 X"+ str(x) + " Y" + str(y)
    
        
    def raiseBitGo(self, x, y):
        print >> self.outFile,  "G0 Z1.24 M59"
        print >> self.outFile,  "G0 X" +str(x)+ " Y"+ str(y)
        
        
    def setDepth(self,  z):
        #Final Cut depth should be -0.0051!!!!!
        if mainWin.testCheckBox.isChecked():
            z = var.testDepth
        if z < var.finalDepth:
            z = var.finalDepth
        print >> self.outFile,  "G0 Z" + str(z) + " F160.0000"
       
        
    def changeBit(self, bitNum,  bitSize):
        print >> self.outFile,  "(BIT CHANGE TO NUMBER " + str(bitNum) +")"
        #print >> self.outFile,  "G0 Z1.2700 M59" # Maybee..... turn off router
        print >> self.outFile,  "M59"
        print >> self.outFile,  "G91 G28 Z0 M15"
        print >> self.outFile,  "G90 G49 H0 M22"
        print >> self.outFile,  "M25"
        print >> self.outFile,  "M88 B0"
        print >> self.outFile,  "M89 B0"
        print >> self.outFile,  "T1" + str(bitNum)
        print >> self.outFile,  "M13 S24000"
        print >> self.outFile,  "(END BIT CHANGE)"
        self.bitOffset = bitSize/2
        self.toolNum = bitNum
    
    def beginCut(self, x, y, z,  type):
        # type 0 = cut into x. pos
        # type 1 = cut into y pos
        if mainWin.testCheckBox.isChecked():
            z = var.testDepth
        if z < var.finalDepth:
            z = var.finalDepth
        print >> self.outFile,  "(CUT IN SEQUENCE)"
        print >> self.outFile,  "G0 X" + str(x) + " Y" + str(y)
        print >> self.outFile,  "G43 H1" +str(self.toolNum) +" Z1.25 M58"  #Start router
        print >> self.outFile,  "Z0.99"
        if type == xCut :
            print >> self.outFile,  "G1 X" + str(x+2) + " Y" + str(y) +" Z0.7500 F300.0000"
        if type == yCut:
            print >> self.outFile,  "G1 X" + str(x) + " Y" + str(y+2) +" Z0.7500 F300.0000"
        print >> self.outFile,  "G1 X" + str(x) +" Y" + str(y) + " Z"+ str(z) + " F575.0000"
        print >> self.outFile,  "(END CUT IN SEQUENCE)"
       
    def doLineX(self, x, y,  xx,  z,  type, cutIn):
       
       
        if type == xCutPos:
            if cutIn == yes:
                
                self.beginCut(x+var.edgeOffset, (y-self.bitOffset) + var.edgeOffset, z, xCut)
            self.line(x+var.edgeOffset-self.bitOffset, (y-self.bitOffset)+var.edgeOffset)
            self.line(xx+var.edgeOffset+self.bitOffset, (y-self.bitOffset)+var.edgeOffset)
            
        if type == xCutNeg:
            if cutIn == yes:
                
                self.beginCut(x+var.edgeOffset, (y+self.bitOffset)+var.edgeOffset, z, xCut)
            self.line(x+var.edgeOffset+self.bitOffset, (y+self.bitOffset)+var.edgeOffset)
            self.line(xx+var.edgeOffset-self.bitOffset, (y+self.bitOffset)+var.edgeOffset)
        
    def doLineY(self, x, y, yy, z, type,  cutIn):
        #cutPoint = ((yy - y) /2) + y 
        
        if type == yCutPos:
            if cutIn == yes:
                #self.raiseBitGo(x, yy/2)
                self.beginCut((x- self.bitOffset)+var.edgeOffset, y + var.edgeOffset, z, yCut)
            self.line((x-self.bitOffset)+var.edgeOffset, y + var.edgeOffset+self.bitOffset)
            self.line((x-self.bitOffset)+var.edgeOffset, yy +var.edgeOffset-self.bitOffset)
            
        if type == yCutNeg:
            if cutIn == yes:
                #self.raiseBitGo(x, yy/2)
                self.beginCut((x+self.bitOffset)+var.edgeOffset, y+var.edgeOffset, z, yCut)
            self.line((x+self.bitOffset) + var.edgeOffset, y+var.edgeOffset-self.bitOffset)
            self.line((x+self.bitOffset) + var.edgeOffset, yy+var.edgeOffset+self.bitOffset)
    
    def doRect(self, x, y, xx, yy, z):
        self.doLineX(x, y, xx, z, xCutPos, yes)
        self.doLineY(xx,y, yy, z, yCutNeg, no)
        self.doLineX(xx, yy, x, z, xCutNeg, no)
        self.doLineY(x, yy, y, z, yCutPos, no)
        self.raiseBitGo(x, y)
        
    def doDado34(self, x, y, length,z,  type):
        if type == xCut:
            self.doLineX(x, y, (length + x), z, xCutNeg, yes)
            self.doLineX((length+x), y + (var.tightness34/2), x, z, xCutPos, no)
            self.doLineX(x, y +var.tightness34,  (length + x), z, xCutPos, no)
            self.raiseBitGo((length + x), y+var.tightness34)
            
        if type == yCut:  
            self.doLineY(x, y, (length + y), z, yCutNeg, yes)
            self.doLineY(x + (var.tightness34/2), (length +y), y, z, yCutPos, no)
            self.doLineY(x +var.tightness34, y,  (length + y), z, yCutPos, no)
            self.raiseBitGo(x+var.tightness34, (length+y))
        

    def finalize(self):
         #Attach footer/End program
        print >> self.outFile,  "(FINALIZE)"
        for x in range(0, len(fileOutFooter)):
            print >> self.outFile,  fileOutFooter[x]
        if self.pushOff == 1:
            print >> self.outFile,  "M105"
        print >> self.outFile,  "M30" 
        self.outFile.close()  
        
class dado34Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Cut 3/4 Dado")
        self.resize(150, 150)
        self.center()
        self.doneButt = QtGui.QPushButton("Done")
        self.xLabel = QtGui.QLabel('Start X:')
        self.yLabel = QtGui.QLabel('Start Y:')
        self.lengthLabel = QtGui.QLabel('Length:')
        self.depthLabel = QtGui.QLabel('Depth:')
        
        self.depthEdit = QtGui.QLineEdit()
        self.xEdit = QtGui.QLineEdit()
        self.yEdit = QtGui.QLineEdit()
        self.lengthEdit = QtGui.QLineEdit()
        
        self.depthEdit.setText(str(0.50))
        self.xEdit.setText(str(0.0))
        self.yEdit.setText(str(0.0))
        self.lengthEdit.setText(str(0.0))
        
        self.depthEdit.setValidator(QtGui.QDoubleValidator(-2, 1.25, 4, self.depthEdit))
        self.xEdit.setValidator(QtGui.QDoubleValidator(0.0, 60, 4, self.xEdit))
        self.yEdit.setValidator(QtGui.QDoubleValidator(0.0, 120, 4, self.yEdit))
        self.lengthEdit.setValidator(QtGui.QDoubleValidator(-120, 120, 4, self.lengthEdit))
                
        self.radioX = QtGui.QRadioButton(self.tr("Cut On X"))
        self.radioX.setToolTip('Will always use negative as the edge')
        self.radioY = QtGui.QRadioButton(self.tr("Cut On Y"))
        self.radioY.setToolTip('Will always use negative as the edge')
        self.radioX.setChecked(True)
       
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.xLabel, 1, 0)
        grid.addWidget(self.xEdit, 1, 1)
        grid.addWidget(self.yLabel, 2, 0)
        grid.addWidget(self.yEdit, 2, 1)
        grid.addWidget(self.lengthLabel, 3, 0)
        grid.addWidget(self.lengthEdit, 3, 1)
        grid.addWidget(self.depthLabel, 4, 0)
        grid.addWidget(self.depthEdit, 4, 1)
        grid.addWidget(self.radioY, 5, 0)
        grid.addWidget(self.radioX, 5, 1)
        grid.addWidget(self.doneButt, 6, 1)
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)
        
        self.setLayout(grid)
        
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
   
    def allDone(self):
      
        cutOut.append(commandClass())
        cutOut[len(cutOut)-1].type = dado34
        cutOut[len(cutOut)-1].x = float(self.xEdit.text())
        cutOut[len(cutOut)-1].y = float(self.yEdit.text())
        cutOut[len(cutOut)-1].z = float(self.depthEdit.text())
        cutOut[len(cutOut)-1].cutLength = float(self.lengthEdit.text())
        
        print self.radioY.isChecked()
        if self.radioY.isChecked():
            cutOut[len(cutOut)-1].cutType = yCut 
            self.txt = "Y"
        if self.radioX.isChecked():
            cutOut[len(cutOut)-1].cutType = xCut
            self.txt = "X"
   
        
        cutOut[len(cutOut)-1].text = "3/4 Dado - X = " + str(cutOut[len(cutOut)-1].x) + " Y = " + str(cutOut[len(cutOut)-1].y) + " | Cut " + str(cutOut[len(cutOut)-1].cutLength) + " on " + self.txt + " | Depth = " + str(cutOut[len(cutOut)-1].z) 
        
        mainWin.listBox.addItem(cutOut[len(cutOut)-1].text)     
  
        self.close()
        

class rectangleWidget(QtGui.QWidget):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Cutout Rectangle")
        self.resize(150, 150)
        self.center() 
      
        self.doneButt = QtGui.QPushButton("Done")
        self.width = QtGui.QLabel('Width:')
       
        self.height = QtGui.QLabel('Height:')
        
        self.depth = QtGui.QLabel('Depth:')
        
        self.passCheckBox = QtGui.QCheckBox("Double Pass")
        self.connect(self.passCheckBox,  QtCore.SIGNAL("stateChanged(int)"),  self.checkPass)
        
        self.widthEdit = QtGui.QLineEdit()
        self.heightEdit = QtGui.QLineEdit()
        self.depthEdit = QtGui.QLineEdit()
        self.widthEdit.setToolTip('Subtract 0.03125 for edgebanding')
        self.heightEdit.setToolTip('Subtract 0.03125 for edgebanding')
        self.widthEdit.setText (str(0.0))
        self.heightEdit.setText (str(0.0))
        self.depthEdit.setText (str(0.0))
        
        self.widthEdit.setValidator(QtGui.QDoubleValidator(-1, 60.0, 4, self.widthEdit))
        self.heightEdit.setValidator(QtGui.QDoubleValidator(-1, 120.0, 4, self.heightEdit))
        self.depthEdit.setValidator(QtGui.QDoubleValidator(-1, 1.25, 4, self.depthEdit))
        
        
  
        self.depthEdit.setReadOnly(no)
        
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.width, 1, 0)
        grid.addWidget(self.widthEdit, 1, 1)
        
        grid.addWidget(self.passCheckBox, 4, 0)

        grid.addWidget(self.height, 2, 0)
        grid.addWidget(self.heightEdit, 2, 1)
        
        grid.addWidget(self.depth, 3, 0)
        grid.addWidget(self.depthEdit, 3, 1)

        grid.addWidget(self.doneButt, 4,1)
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)  #If button is clicked generate code (genCode)
        
        self.setLayout(grid)
     
    def checkPass(self):
    
       if  self.passCheckBox.checkState()  == 2:
            self.depthEdit.setReadOnly(yes)
            self.depthEdit.setText (str(0.125))
            
       if self.passCheckBox.checkState() == 0:
            self.depthEdit.setReadOnly(no)
            self.depthEdit.setText (str(0.75))
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
    def allDone(self):

        
        cutOut.append(commandClass())
        cutOut[len(cutOut)-1].type = mainRect
        cutOut[len(cutOut)-1].xx = float(self.widthEdit.text())
        cutOut[len(cutOut)-1].yy = float(self.heightEdit.text())
        cutOut[len(cutOut)-1].z = float(self.depthEdit.text())
        if  self.passCheckBox.checkState()  == 2:
            cutOut[len(cutOut)-1].twoPass = yes
            passText = "yes"
        else:
            cutOut[len(cutOut)-1].twoPass = no
            passText = "No"
        cutOut[len(cutOut)-1].text = "Rectangle - " + str(cutOut[len(cutOut)-1].xx) + " X " + str(cutOut[len(cutOut)-1].yy) + " | Doublepass = " + passText + " | Depth = " + str(cutOut[len(cutOut)-1].z)
  
        mainWin.listBox.addItem(cutOut[len(cutOut)-1].text)     
        var.listRectNum =  mainWin.listBox.count()-1
        var.rectCreated = yes
        var.mainRectNum = len(cutOut)-1
        self.close()
        

class absLineWidget(QtGui.QWidget):
    
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Cutout Absolute Line")
        self.resize(150, 150)
        self.center() 
        
        self.doneButt = QtGui.QPushButton("Done")
        self.xLabel = QtGui.QLabel('Start X:')
        self.yLabel = QtGui.QLabel('Start Y:')
        self.lengthLabel = QtGui.QLabel('End Point:')
        self.depthLabel = QtGui.QLabel('Tool Depth:')
        
        self.depthEdit = QtGui.QLineEdit()
        self.xEdit = QtGui.QLineEdit()
        self.yEdit = QtGui.QLineEdit()
        self.lengthEdit = QtGui.QLineEdit()
        
        self.depthEdit.setText(str(0.50))
        self.depthEdit.setToolTip("-0.005 = Full Cut Depth\n0.2450 = Rabbet depth")
        self.xEdit.setText(str(0.0))
        self.yEdit.setText(str(0.0))
        self.lengthEdit.setText(str(0.0))
        
        self.radioX = QtGui.QRadioButton(self.tr("Cut On X"))
        self.radioX.setToolTip('Cut along X axis.')
        self.radioY = QtGui.QRadioButton(self.tr("Cut On Y"))
        self.radioY.setToolTip('Cut along Y axis.')
        self.radioX.setChecked(True)
        
        self.depthEdit.setValidator(QtGui.QDoubleValidator(-2, 1.25, 4, self.depthEdit))
        self.xEdit.setValidator(QtGui.QDoubleValidator(-0.5, 60, 4, self.xEdit))
        self.yEdit.setValidator(QtGui.QDoubleValidator(-0.5, 120, 4, self.yEdit))
        self.lengthEdit.setValidator(QtGui.QDoubleValidator(-120, 120, 4, self.lengthEdit))
        
        self.positiveCheckBox = QtGui.QCheckBox("Cut Positive?")
        self.positiveCheckBox.setChecked(False)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.xLabel, 1, 0)
        grid.addWidget(self.xEdit, 1, 1)
        grid.addWidget(self.yLabel, 2, 0)
        grid.addWidget(self.yEdit, 2, 1)
        grid.addWidget(self.lengthLabel, 3, 0)
        grid.addWidget(self.lengthEdit, 3, 1)
        grid.addWidget(self.depthLabel, 4, 0)
        grid.addWidget(self.depthEdit, 4, 1)
        grid.addWidget(self.doneButt, 6, 1)
        grid.addWidget(self.radioY, 5, 0)
        grid.addWidget(self.radioX, 5, 1)
        grid.addWidget(self.positiveCheckBox, 6, 0)
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)
        
        self.setLayout(grid)
        
    def allDone(self):
     
        cutOut.append(commandClass())
        cutOut[len(cutOut)-1].type = absLine
        cutOut[len(cutOut)-1].x = float(self.xEdit.text())
        cutOut[len(cutOut)-1].y = float(self.yEdit.text())
        cutOut[len(cutOut)-1].z = float(self.depthEdit.text())
        cutOut[len(cutOut)-1].cutLength = float(self.lengthEdit.text())
        
        
        if self.radioY.isChecked():
            cutOut[len(cutOut)-1].cutType = yCut 
            self.txt = "Y"
            if self.positiveCheckBox.isChecked():
                cutOut[len(cutOut)-1].cutEdge = yCutPos
                self.pos = "positive"
            else:
                cutOut[len(cutOut)-1].cutEdge = yCutNeg
                self.pos = "negative"
        if self.radioX.isChecked():
            cutOut[len(cutOut)-1].cutType = xCut
            self.txt = "X"
            if self.positiveCheckBox.isChecked():
                cutOut[len(cutOut)-1].cutEdge = xCutPos
                self.pos = "positive"
            else:
                cutOut[len(cutOut)-1].cutEdge = xCutNeg
                self.pos = "negative"
            
        cutOut[len(cutOut)-1].text = "Absolute Line - X = " + str(cutOut[len(cutOut)-1].x) + " Y = " + str(cutOut[len(cutOut)-1].y) + " | To " + str(cutOut[len(cutOut)-1].cutLength) + " on " + self.txt + " | Edge is " +self.pos + " | Depth = " + str(cutOut[len(cutOut)-1].z) 
        
        mainWin.listBox.addItem(cutOut[len(cutOut)-1].text)     
        self.close()
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    


class relLineWidget(QtGui.QWidget):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Cutout Relative Line")
        self.resize(350, 200)
        
        edgeGroup = QtGui.QButtonGroup
       
        self.doneButt = QtGui.QPushButton("Done")
        self.negLabel = QtGui.QLabel('Negative Point:')
        self.posLabel = QtGui.QLabel('Positive Point:')
        self.offsetLabel = QtGui.QLabel('Offset:')
        self.depthLabel = QtGui.QLabel('Tool Depth:')
        
        self.depthEdit = QtGui.QLineEdit()
        self.negEdit = QtGui.QLineEdit()
        self.posEdit = QtGui.QLineEdit()
        self.offsetEdit = QtGui.QLineEdit()
        
        self.depthEdit.setText(str(0.2450))
        self.depthEdit.setToolTip("-0.005 = Full Cut Depth\n0.2450 = Rabbet depth")
        self.negEdit.setText(str(0.0))
        self.posEdit.setText(str(0.0))
        self.offsetEdit.setText(str(0.0))
        
        self.negCheckBox = QtGui.QCheckBox("Cut From")
        self.negCheckBox.setChecked(False)
        self.connect(self.negCheckBox,  QtCore.SIGNAL("stateChanged(int)"),  self.cutCheck)
        self.posCheckBox = QtGui.QCheckBox("Cut From")
        self.posCheckBox.setChecked(False)
        self.connect(self.posCheckBox,  QtCore.SIGNAL("stateChanged(int)"),  self.cutCheck)
        
        
        
        self.radioTop = QtGui.QRadioButton(self.tr("Top"))
     
        self.radioBottom = QtGui.QRadioButton(self.tr("Bottom"))

        self.radioLeft = QtGui.QRadioButton(self.tr("Left"))

        self.radioRight = QtGui.QRadioButton(self.tr("Right"))

        self.radioLeft.setChecked(True)
        
        self.groupBox = QtGui.QGroupBox(self.tr("Relative to Edge"))
        buttGrid = QtGui.QGridLayout()
        buttGrid.addWidget(self.radioTop, 0, 0)
        buttGrid.addWidget(self.radioBottom, 0, 1)
        buttGrid.addWidget(self.radioLeft, 1,  0)
        buttGrid.addWidget(self.radioRight, 1, 1)
        self.groupBox.setLayout(buttGrid)

        
        self.depthEdit.setValidator(QtGui.QDoubleValidator(-2, 1.25, 4, self.depthEdit))
        self.negEdit.setValidator(QtGui.QDoubleValidator(-0.5, 60, 4, self.negEdit))
        self.posEdit.setValidator(QtGui.QDoubleValidator(-0.5, 120, 4, self.posEdit))
        self.offsetEdit.setValidator(QtGui.QDoubleValidator(-120, 120, 4, self.offsetEdit))
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.negLabel, 1, 0)
        grid.addWidget(self.negEdit, 1, 1)
        grid.addWidget(self.negCheckBox, 1, 2)
        grid.addWidget(self.posLabel, 2, 0)
        grid.addWidget(self.posEdit, 2, 1)
        grid.addWidget(self.posCheckBox, 2, 2)
        grid.addWidget(self.offsetLabel, 3, 0)
        grid.addWidget(self.offsetEdit, 3, 1)
        grid.addWidget(self.depthLabel, 4, 0)
        grid.addWidget(self.depthEdit, 4, 1)
        grid.addWidget(self.doneButt, 7, 1)
        grid.addWidget(self.groupBox, 5, 0, 5, 1)
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)
        
        self.setLayout(grid)
        self.center() 
        
    
    def allDone(self):
        cutOut.append(commandClass())
        cutOut[len(cutOut)-1].type = relLine
        cutOut[len(cutOut)-1].z = float(self.depthEdit.text())
        self.txt = "Line - Relative to "
        if self.posEdit.text() == "---":
            self.posEdit.setText ("0.0")
        if self.negEdit.text() == "---":
            self.negEdit.setText ("0.0")
        
        cutOut[len(cutOut)-1].negPoint = float(self.negEdit.text())
        cutOut[len(cutOut)-1].posPoint = float(self.posEdit.text())
      
        
        if self.radioLeft.isChecked():
            self.txt = self.txt + "Left "
            if  self.negCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = no
                cutOut[len(cutOut)-1].negFrom = yes
                
            if self.posCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = yes
                cutOut[len(cutOut)-1].negFrom = no
                
            cutOut[len(cutOut)-1].cutType = yCut
            cutOut[len(cutOut)-1].offset = float(self.offsetEdit.text())
            cutOut[len(cutOut)-1].cutEdge = yCutPos
        
        if self.radioRight.isChecked():
            self.txt = self.txt + "Right "
            if  self.negCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = no
                cutOut[len(cutOut)-1].negFrom = yes
            if self.posCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = yes
                cutOut[len(cutOut)-1].negFrom = no
                
            cutOut[len(cutOut)-1].cutType = yCut
            cutOut[len(cutOut)-1].offset = float(self.offsetEdit.text())
            cutOut[len(cutOut)-1].cutEdge = yCutNeg
        
            
        if self.radioTop.isChecked():
            self.txt = self.txt + "Top"
            if  self.negCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = no
                cutOut[len(cutOut)-1].negFrom = yes
            if self.posCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = yes
                cutOut[len(cutOut)-1].negFrom = no
                
            cutOut[len(cutOut)-1].cutType = xCut
            cutOut[len(cutOut)-1].offset = float(self.offsetEdit.text())
            cutOut[len(cutOut)-1].cutEdge = xCutNeg
        
        
        if self.radioBottom.isChecked():
            self.txt = self.txt + "Bottom"
            if  self.negCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = no
                cutOut[len(cutOut)-1].negFrom = yes
            if self.posCheckBox.checkState()  == 2:
                cutOut[len(cutOut)-1].posFrom = yes
                cutOut[len(cutOut)-1].negFrom = no
                
            cutOut[len(cutOut)-1].cutType = xCut
            cutOut[len(cutOut)-1].offset = float(self.offsetEdit.text())
            cutOut[len(cutOut)-1].cutEdge = xCutPos
        
        self.txt = self.txt + " | Negative " + self.negEdit.text()
        self.txt = self.txt + " | Positive " + self.posEdit.text()
        self.txt = self.txt + " | Offset " + self.offsetEdit.text()
        self.txt = self.txt + " | Depth " + self.depthEdit.text()
        
        cutOut[len(cutOut)-1].text = self.txt
        mainWin.listBox.addItem(cutOut[len(cutOut)-1].text)     
            
        self.close()
        
    def cutCheck(self):
        if  self.negCheckBox.checkState()  == 2:
            self.posEdit.setReadOnly(yes)
            self.posEdit.setText ("---")
            
        if self.negCheckBox.checkState() == 0:
            self.posEdit.setReadOnly(no)
            if self.posEdit.text() == "---":
                 self.posEdit.setText ("0.0")
           
        if  self.posCheckBox.checkState()  == 2:
            self.negEdit.setReadOnly(yes)
            self.negEdit.setText ("---")
            
        if self.posCheckBox.checkState() == 0:
            self.negEdit.setReadOnly(no)
            if self.negEdit.text() == "---":
                 self.negEdit.setText ("0.0")

        
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    

class optionsWidget(QtGui.QWidget):

    def __init__(self,  parent=None):
        global var
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Program Settings")
        self.resize(150, 150)
        self.center() 
        self.doneButt = QtGui.QPushButton("Done")
        self.dadoLabel = QtGui.QLabel('3/4 Dado Tighness:')
        self.edgeLabel = QtGui.QLabel('Edge Offset:')
        self.finalDepthLabel = QtGui.QLabel("Final Depth:")
        
        self.dadoEdit = QtGui.QLineEdit()
        self.edgeEdit = QtGui.QLineEdit()
        self.finalDepthEdit = QtGui.QLineEdit()
        self.dadoEdit.setText(str(var.tightness34))
        self.edgeEdit.setText(str(var.edgeOffset))
        self.edgeEdit.setToolTip("-0.03125 if you want no edge.")
        self.finalDepthEdit.setText(str(var.finalDepth))
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.dadoLabel, 1, 0)
        grid.addWidget(self.dadoEdit, 1, 1)
        grid.addWidget(self.edgeLabel, 2, 0)
        grid.addWidget(self.edgeEdit, 2, 1)
        grid.addWidget(self.finalDepthLabel, 3, 0)
        grid.addWidget(self.finalDepthEdit, 3, 1)
        
        grid.addWidget(self.doneButt, 4, 1)
        
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)
        
        self.setLayout(grid)
       
    def allDone(self):
        var.tightness34 = float(self.dadoEdit.text())
        var.edgeOffset = float(self.edgeEdit.text())
        var.finalDepth = float(self.finalDepthEdit.text())
        self.close()

      
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

class toolChangeWidget(QtGui.QWidget):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Tool Change")
        self.resize(150, 200)
        self.center() 
        self.doneButt = QtGui.QPushButton("Done")
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)
        self.toolList = QtGui.QListWidget()
        self.toolList.addItem("1: " + tool[0][0] + "  -  " + str(tool[0][1]))     
        self.toolList.addItem("2: " + tool[1][0] + "  -  " + str(tool[1][1]))     
        self.toolList.addItem("3: " + tool[2][0] + "  -  " + str(tool[2][1]))     
        self.toolList.addItem("4: " + tool[3][0] + "  -  " + str(tool[3][1]))     
        self.toolList.addItem("5: " + tool[4][0] + "  -  " + str(tool[4][1]))     
        self.toolList.addItem("6: " + tool[5][0] + "  -  " + str(tool[5][1]))     
        self.toolList.addItem("7: " + tool[6][0] + "  -  " + str(tool[6][1]))     
        self.toolList.addItem("8: " + tool[7][0] + "  -  " + str(tool[7][1]))     
        grid = QtGui.QGridLayout() 
        grid.addWidget(self.toolList, 1, 0)
        grid.addWidget(self.doneButt, 6, 0)
        self.setLayout(grid)
        
    def allDone(self):
        num = self.toolList.currentRow()
        cutOut.append(commandClass())

        print num
        if self.toolList.currentRow() >= 0:
            num = num+1
            if  num == 3:
                QtGui.QMessageBox.warning(self, self.tr("Oops "),
                self.tr("Sorry but as of this time there is no way for you to \nuse the slot cutter bit without screwing things up!\nWill use 3/8 bit instead..."))
                cutOut[len(cutOut)-1].toolNumber = 7
                num = 7
        
            cutOut[len(cutOut)-1].text = "Change to " + tool[num-1][0] + " | Tool number "+ str(num) 
            mainWin.listBox.addItem(cutOut[len(cutOut)-1].text)     
            cutOut[len(cutOut)-1].type = toolChange
            cutOut[len(cutOut)-1].toolNumber = num
            self.close()
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    

class resizePartWidget(QtGui.QDialog):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setWindowFlags(self, QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Resize Part")
        self.resize(150, 200)
        self.center() 
        self.doneButt = QtGui.QPushButton("Done")
        self.width = QtGui.QLabel('Width:')
        self.height = QtGui.QLabel('Height:')
        self.widthEdit = QtGui.QLineEdit()
        self.heightEdit = QtGui.QLineEdit()
       
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.width, 1, 0)
        grid.addWidget(self.widthEdit, 1, 1)
        grid.addWidget(self.height, 2, 0)
        grid.addWidget(self.heightEdit, 2, 1)
        
        self.checkTop = QtGui.QCheckBox("Top")
        self.checkBottom = QtGui.QCheckBox("Bottom")
        self.checkLeft = QtGui.QCheckBox("Left")
        self.checkRight = QtGui.QCheckBox("Right")
        
        self.groupBox = QtGui.QGroupBox(self.tr("Edgebanding on"))
        buttGrid = QtGui.QGridLayout()
        buttGrid.addWidget(self.checkTop, 0, 0)
        buttGrid.addWidget(self.checkBottom, 0, 1)
        buttGrid.addWidget(self.checkLeft, 1,  0)
        buttGrid.addWidget(self.checkRight, 1, 1)
        self.groupBox.setLayout(buttGrid)
        grid.addWidget(self.groupBox, 3,0, 1, 3)
        
        
        
        grid.addWidget(self.doneButt, 4,0, 1, 4)
        self.connect(self.doneButt, QtCore.SIGNAL("clicked()"), self.allDone)  #If button is clicked generate code (genCode)
        
        self.setLayout(grid)
    
    def allDone(self):
        cutOut[var.mainRectNum].xx = float(self.widthEdit.text())
        cutOut[var.mainRectNum].yy = float(self.heightEdit.text())
        if self.checkTop.checkState() == 2:
            cutOut[var.mainRectNum].yy = cutOut[var.mainRectNum].yy - 0.03125
        if self.checkBottom.checkState() == 2: 
            cutOut[var.mainRectNum].yy = cutOut[var.mainRectNum].yy - 0.03125
        if self.checkRight.checkState() == 2:
            cutOut[var.mainRectNum].xx = cutOut[var.mainRectNum].xx - 0.03125
        if self.checkLeft.checkState() == 2:
            cutOut[var.mainRectNum].xx = cutOut[var.mainRectNum].xx - 0.03125
        
        if cutOut[var.mainRectNum].twoPass == yes:
            passText = "yes"
        else:
            passText = "no"
        cutOut[var.mainRectNum].text = "Rectangle - " + str(cutOut[var.mainRectNum].xx) + " X " + str(cutOut[var.mainRectNum].yy) + " | Doublepass = " + passText + " | Depth = " + str(cutOut[var.mainRectNum].z)
        mainWin.listBox.item(var.listRectNum).setText(cutOut[var.mainRectNum].text)
        self.close()
    
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
    
class mainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #GUI Setup
        QtGui.QMainWindow.__init__(self, parent)
        self.rectWindow = rectangleWidget(self)
        self.dado34Window = dado34Widget(self)
        self.absLineWindow = absLineWidget(self)
        self.settingsWindow = optionsWidget(self)
        self.relLineWindow = relLineWidget(self)
        self.resizeWindow = resizePartWidget(self)
        self.toolChangeWindow = toolChangeWidget(self)
        self.setWindowTitle("Easy ANDI Cutout")
        self.resize(550, 250)
        self.center()
        
        w = QtGui.QWidget()
        self.setCentralWidget(w)
       
        self.newAct = QtGui.QAction(self.tr("&New"), self)
        self.newAct.setShortcut(self.tr("Ctrl+N"))
        self.connect(self.newAct, QtCore.SIGNAL("triggered()"), self.newFile)

        self.openAct = QtGui.QAction(self.tr("&Load Part"), self)
        self.openAct.setShortcut(self.tr("Ctrl+O"))
        self.connect(self.openAct, QtCore.SIGNAL("triggered()"), self.loadPart)

        self.saveAct = QtGui.QAction(self.tr("&Save Part"), self)
        self.saveAct.setShortcut(self.tr("Ctrl+S"))
        self.connect(self.saveAct, QtCore.SIGNAL("triggered()"), self.savePart)
        
        self.exitAct = QtGui.QAction(self.tr("E&xit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.connect(self.exitAct, QtCore.SIGNAL("triggered()"), self.close)
        
        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.deleteAct = QtGui.QAction("&Delete", self)
        self.connect(self.deleteAct, QtCore.SIGNAL("triggered()"), self.delItem)
        
        self.resizeAct = QtGui.QAction("&Resize Part", self)
        self.connect(self.resizeAct, QtCore.SIGNAL("triggered()"), self.resizePart)
        
        
        self.optionsAct = QtGui.QAction("&Settings", self)
        self.connect(self.optionsAct, QtCore.SIGNAL("triggered()"), self.optionsMenu)
       
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.resizeAct)
        self.editMenu.addAction(self.deleteAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.optionsAct)
        
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        
        self.genButt = QtGui.QPushButton("Generate")
        self.connect(self.genButt, QtCore.SIGNAL("clicked()"), self.generateCode)  #If button is clicked generate code (genCode)

        self.rectButt = QtGui.QPushButton("Main Rectangle")
        self.rectButt.setToolTip('Create a main rectangle for your part.')
        self.connect(self.rectButt, QtCore.SIGNAL("clicked()"), self.showRect) 
        
        self.dadoAct34 = QtGui.QAction("3/4 Dado", self)
        self.connect(self.dadoAct34, QtCore.SIGNAL("triggered()"), self.showDado34)
        
        self.absLineAct = QtGui.QAction("Absolute Line", self)
        self.connect(self.absLineAct,  QtCore.SIGNAL("triggered()"), self.showAbsLine)
        
        self.relLineAct = QtGui.QAction("Relative Line", self)
        self.relLineAct.setToolTip('Creates a line relative to edges of the main rectangle.')
        self.connect(self.relLineAct,  QtCore.SIGNAL("triggered()"), self.showRelLine)
    
        self.lineButt = QtGui.QPushButton("Lines")
        self.lineButt.setToolTip('Performs various line functions.') #why no work?
        self.lineMenu = QtGui.QMenu(self)
        self.lineMenu.addAction(self.dadoAct34)
        self.lineMenu.addAction(self.absLineAct)
        self.lineMenu.addAction(self.relLineAct)
       
        self.lineButt.setMenu(self.lineMenu)
        

        self.changeToolButt = QtGui.QPushButton("Change Tool")
        self.connect(self.changeToolButt,  QtCore.SIGNAL("clicked()"), self.showToolChange)
        
        self.testCheckBox = QtGui.QCheckBox("Test Run")
        self.testCheckBox.setToolTip("Will only cut very shallow in case \nsomething isn't right.")
        self.testCheckBox.setChecked(False)
        
        self.pushOffCheckBox = QtGui.QCheckBox("Push Off")
        self.pushOffCheckBox.setToolTip("Sets the program to push off \nthe part when it is done.")
        self.pushOffCheckBox.setChecked(False)
       
        self.listBox = QtGui.QListWidget()
                      
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        #grid.addWidget(self.width, 1, 0)
        grid.addWidget(self.rectButt, 1, 0)
    
        grid.addWidget(self.lineButt, 2, 0)
 
        grid.addWidget(self.changeToolButt, 3, 0)
        
        grid.addWidget(self.listBox, 1, 1,4,1)
        
        grid.addWidget(self.genButt, 5,1)
        grid.addWidget(self.testCheckBox, 5, 0)
        grid.addWidget(self.pushOffCheckBox, 6, 0)
        
        w.setLayout(grid)
        
    def generateCode(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                         self.tr("Generate File"),
                                         self.tr("default.anc"),
                                         self.tr("ANDI Files (*.anc);;All Files (*)"))
        if not fileName.isEmpty():
            self.myCut = cutClass(fileName)
            self.myCut.changeBit(var.defaultTool,  var.defaultToolSize)
            self.finalPass = 0
            self.finalNum = 0
            self.currentTool = var.defaultTool
            for x in range(len(cutOut)):
                if cutOut[x].type == mainRect:
                    if cutOut[x].twoPass == yes:
                        self.myCut.doRect(cutOut[x].x, cutOut[x].y, cutOut[x].xx, cutOut[x].yy, cutOut[x].z)
                        self.finalPass = 1
                    else:
                        self.myCut.doRect(cutOut[x].x, cutOut[x].y, cutOut[x].xx, cutOut[x].yy, cutOut[x].z)
    
                if cutOut[x].type == dado34:
                    self.myCut.doDado34(cutOut[x].x,  cutOut[x].y,  cutOut[x].cutLength, cutOut[x].z, cutOut[x].cutType)
                    
                if cutOut[x].type == absLine:
                    if cutOut[x].cutType ==  yCut:
                        self.myCut.doLineY(cutOut[x].x,(cutOut[x].y+self.myCut.bitOffset),(cutOut[x].cutLength-self.myCut.bitOffset), cutOut[x].z, cutOut[x].cutEdge, yes)
                        self.myCut.raiseBitGo(cutOut[x].x,cutOut[x].cutLength)
                    if cutOut[x].cutType == xCut:
                        self.myCut.doLineX((cutOut[x].x+self.myCut.bitOffset),cutOut[x].y,(cutOut[x].cutLength-self.myCut.bitOffset), cutOut[x].z, cutOut[x].cutEdge, yes)
                        self.myCut.raiseBitGo(cutOut[x].cutLength,cutOut[x].y)

                if cutOut[x].type == relLine:
                    if cutOut[x].cutType ==  yCut:
                        if cutOut[x].cutEdge == yCutPos:
                            
                            if ((cutOut[x].negFrom == yes) and (cutOut[x].posFrom == no)):
                                self.myCut.doLineY(cutOut[var.mainRectNum].x + cutOut[x].offset,cutOut[var.mainRectNum].y,cutOut[x].negPoint, cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].x,cutOut[var.mainRectNum].y)
                            elif ((cutOut[x].posFrom == yes) and (cutOut[x].negFrom == no)):
                                self.myCut.doLineY(cutOut[var.mainRectNum].x + cutOut[x].offset,cutOut[var.mainRectNum].yy, (cutOut[var.mainRectNum].yy - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].x,cutOut[var.mainRectNum].yy)
                            elif ((cutOut[x].posFrom == no) and (cutOut[x].negFrom == no)):
                               self.myCut.doLineY(cutOut[var.mainRectNum].x + cutOut[x].offset,(cutOut[var.mainRectNum].y + cutOut[x].negPoint), (cutOut[var.mainRectNum].yy - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes) 
                               self.myCut.raiseBitGo(cutOut[var.mainRectNum].x,cutOut[var.mainRectNum].yy)
                        
                        if cutOut[x].cutEdge == yCutNeg:
                            if ((cutOut[x].negFrom == yes) and (cutOut[x].posFrom == no)):
                                self.myCut.doLineY(cutOut[var.mainRectNum].xx - cutOut[x].offset,cutOut[var.mainRectNum].y,cutOut[x].negPoint, cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].y)
                            elif ((cutOut[x].posFrom == yes) and (cutOut[x].negFrom == no)):
                                self.myCut.doLineY(cutOut[var.mainRectNum].xx - cutOut[x].offset,cutOut[var.mainRectNum].yy, (cutOut[var.mainRectNum].yy - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].yy)
                            elif ((cutOut[x].posFrom == no) and (cutOut[x].negFrom == no)):
                               self.myCut.doLineY(cutOut[var.mainRectNum].xx - cutOut[x].offset,(cutOut[var.mainRectNum].y + cutOut[x].negPoint), (cutOut[var.mainRectNum].yy - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes) 
                               self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].yy)

                    if cutOut[x].cutType == xCut:
                        if cutOut[x].cutEdge == xCutPos:
                            
                            if ((cutOut[x].negFrom == yes) and (cutOut[x].posFrom == no)):
                                self.myCut.doLineX(cutOut[var.mainRectNum].x, cutOut[var.mainRectNum].y  + cutOut[x].offset,cutOut[x].negPoint, cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].x,cutOut[var.mainRectNum].y)
                            elif ((cutOut[x].posFrom == yes) and (cutOut[x].negFrom == no)):
                                self.myCut.doLineX(cutOut[var.mainRectNum].xx, cutOut[var.mainRectNum].y  + cutOut[x].offset, (cutOut[var.mainRectNum].xx - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].y)
                            elif ((cutOut[x].posFrom == no) and (cutOut[x].negFrom == no)):
                               self.myCut.doLineX(cutOut[var.mainRectNum].x  + cutOut[x].negPoint, (cutOut[var.mainRectNum].y+ cutOut[x].offset), (cutOut[var.mainRectNum].xx - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes) 
                               self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].y)
                       
                        if cutOut[x].cutEdge == xCutNeg:
                            if ((cutOut[x].negFrom == yes) and (cutOut[x].posFrom == no)):
                                self.myCut.doLineX(cutOut[var.mainRectNum].x, cutOut[var.mainRectNum].yy  - cutOut[x].offset,cutOut[x].negPoint, cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].x,cutOut[var.mainRectNum].yy)
                            elif ((cutOut[x].posFrom == yes) and (cutOut[x].negFrom == no)):
                                self.myCut.doLineX(cutOut[var.mainRectNum].xx, cutOut[var.mainRectNum].yy  - cutOut[x].offset, (cutOut[var.mainRectNum].xx - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes)
                                self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].yy)
                            elif ((cutOut[x].posFrom == no) and (cutOut[x].negFrom == no)):
                               self.myCut.doLineX(cutOut[var.mainRectNum].x  + cutOut[x].negPoint, (cutOut[var.mainRectNum].yy - cutOut[x].offset), (cutOut[var.mainRectNum].xx - cutOut[x].posPoint), cutOut[x].z, cutOut[x].cutEdge, yes) 
                               self.myCut.raiseBitGo(cutOut[var.mainRectNum].xx,cutOut[var.mainRectNum].yy)
                        
            
                if cutOut[x].type == toolChange:
                    self.myCut.changeBit(cutOut[x].toolNumber,  tool[cutOut[x].toolNumber-1][1])
                    self.currentTool = cutOut[x].toolNumber
            if self.finalPass == 1:
                if self.currentTool != var.defaultTool:
                    self.myCut.changeBit(var.defaultTool,  var.defaultToolSize)
                self.myCut.doRect(cutOut[var.mainRectNum].x, cutOut[var.mainRectNum].y, cutOut[var.mainRectNum].xx, cutOut[var.mainRectNum].yy, var.finalDepth)
                
            if self.pushOffCheckBox.isChecked():
                self.myCut.pushOff =1
            self.myCut.finalize()
           
            fart = QtGui.QMessageBox.information(self, 'All done!',
                "Your program has been created. \nNow you can run your file." )
            

    def showRect(self):
        
        if var.rectCreated == no:
            self.rectWindow.show()
        else:
            fart = QtGui.QMessageBox.information(self, 'Doh!',
            "You are only allowed 1 main rectangle." )
        
            
    def resizePart(self):
        if var.rectCreated == yes:
            self.resizeWindow.widthEdit.setText (str(cutOut[var.mainRectNum].xx))
            self.resizeWindow.heightEdit.setText (str(cutOut[var.mainRectNum].yy))
      
            self.resizeWindow.show()
        else:
            fart = QtGui.QMessageBox.information(self, 'Doh!',
            "You can only resize a part if it has a main rectangle." )
        
    def showAbsLine(self):

        self.absLineWindow.show()
        
    def showRelLine(self):
        if var.rectCreated == no:
            fart = QtGui.QMessageBox.information(self, 'Doh!',
            "Relative lines require a main rectangle." )
        else :
            self.relLineWindow.show()

    
    def showDado34(self):
      
        self.dado34Window.show()
    
    def showToolChange(self):
        self.toolChangeWindow.show()
    
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("Version "+ version),
                self.tr("Brad's ANDI cutout program! Developed for Homestead Cabinets. This program is open source, written by me and is not considered fit for any purpose other than education. \n\nThere is no error checking implemented at this time so be careful with your values!"))
            
    def delItem(self):
        if self.listBox.currentRow() >= 0:
            if cutOut[self.listBox.currentRow()].type == mainRect:
                var.rectCreated = no
            print  cutOut[self.listBox.currentRow()].type
            del cutOut[self.listBox.currentRow()]
            self.listBox.takeItem(self.listBox.currentRow())
        
        print len(cutOut)
            
    def newFile(self):
        global cutOut
        reply = QtGui.QMessageBox.question(self, self.tr("New file..."),
                    "Are you sure you want to create a new file?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply ==QtGui.QMessageBox.Yes:
            if len(cutOut) != 0:   
                for x in range(0, len(cutOut)-1):
                    del cutOut[x]
                del cutOut[len(cutOut)-1]
                self.listBox.clear()
            
        var.rectCreated = no
        var.edgeOffset = 0.1875
        var.tightness34 = 0.753
        self.settingsWindow.dadoEdit.setText(str(var.tightness34))
        self.settingsWindow.edgeEdit.setText(str(var.edgeOffset))
                                          
    def optionsMenu(self):
        print "options menu"
        self.settingsWindow.show()
    def savePart(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                                 self.tr("Save Parts File"),
                                 self.tr("default.part"),
                                 self.tr("Part Files (*.part);;All Files (*)"))
        if not fileName.isEmpty():
            pfile = file(fileName, 'wb')
            pickle.dump(cutOut, pfile) 
            pickle.dump(var.testDepth, pfile)
            pickle.dump(var.finalDepth, pfile)
            pickle.dump(var.edgeOffset, pfile)
            pickle.dump(var.tightness34, pfile)
            pickle.dump(var.mainRectNum, pfile)
            pickle.dump(var.rectCreated, pfile)
            pickle.dump(var.defaultTool, pfile)
            pickle.dump(var.defaultToolSize, pfile)
            pickle.dump(var.listRectNum, pfile)
            pfile.close()
            QtGui.QMessageBox.information(self, self.tr("All Done! "),
                    self.tr("Your part has been saved successfully. "))
        
    
   
    def loadPart(self):
        global cutOut
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                 self.tr("Load Parts File"),
                                 self.tr("default.part"),
                                 self.tr("Part Files (*.part);;All Files (*)"))
        if not fileName.isEmpty():
       
            self.listBox.clear()    
            if len(cutOut) != 0:   
                for x in range(0, len(cutOut)-1):
                    del cutOut[x]
                del cutOut[len(cutOut)-1]     

            pfile = file(fileName, 'rb')
            cutOut = pickle.load(pfile) 
            var.testDepth = pickle.load(pfile)
            var.finalDepth= pickle.load(pfile)
            var.edgeOffset= pickle.load(pfile)
            var.tightness34= pickle.load(pfile)
            var.mainRectNum= pickle.load(pfile)
            var.rectCreated= pickle.load(pfile)
            var.defaultTool= pickle.load(pfile)
            var.defaultToolSize= pickle.load(pfile)
            var.listRectNum= pickle.load(pfile)
            pfile.close()
            print var.mainRectNum
            for x in range(0, len(cutOut)):
                 self.listBox.addItem(cutOut[x].text)    
            

        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    




cutOut = []
var = variableClass
app = QtGui.QApplication(sys.argv)
mainWin = mainWindow()
mainWin.show()
sys.exit(app.exec_())
