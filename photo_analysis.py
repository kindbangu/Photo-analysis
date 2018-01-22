# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import exifread 

tags = []
normal = []
faketime = []
fakesize = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1105, 851)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 20, 531, 801))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(10, 50, 511, 511))
        self.graphicsView.setObjectName("graphicsView")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(10, 600, 511, 31))
        self.comboBox.setMouseTracking(False)
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 60, 491, 491))
        self.label.setText("")
        self.label.setObjectName("label")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 640, 511, 161))
        self.textEdit_2.setObjectName("textEdit_2")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(559, 19, 531, 801))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textEdit = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 521, 791))
        self.textEdit.setObjectName("textEdit")
        self.frame.raise_()
        self.frame_2.raise_()
        self.frame_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.pushButtonEvt)
    #    print("faketime: "+str(faketime))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.comboBox.addItem('<분 류>')
        self.comboBox.addItem('크기 위조된 파일')
        self.comboBox.addItem('시간 위조된 파일')
        self.comboBox.addItem('정상 파일')

        self.comboBox.activated[str].connect(self.onActivated)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Viewer"))
        self.pushButton.setText(_translate("MainWindow", "분석"))

    def pushButtonEvt(self, MainWindow):
        global tags, normal, faketime, fakesize
        self.textEdit.clear()
        filepath = self.lineEdit.text()
        pixmap = QtGui.QPixmap(filepath)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        img_file = open(filepath, 'rb')
        img_file2 = Image.open(filepath)
        tags = exifread.process_file(img_file)
        widths, heights = img_file2.size

        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print("Key: %s, value: %s" % (tag, tags[tag]))
                exifValue = str(tags[tag])
                self.textEdit.append(tag+":  "+ exifValue)
        if (str(tags['EXIF ExifImageWidth']) != str(widths)) or (str(tags['EXIF ExifImageLength']) != str(heights)):
            fakesize.append(self.lineEdit.text())
            print("tags['EXIF ExifImageWidth']: "+str(tags['EXIF ExifImageWidth']))
            print("widths: "+str(widths))
            print("tags['EXIF ExifImageLength']: "+str(tags['EXIF ExifImageLength']))
            print("heights: "+str(heights))
            print("fakesize : "+str(fakesize))
        elif ((str(tags['Image DateTime']) != str(tags['EXIF DateTimeOriginal'])) or (str(tags['Image DateTime']) != str(tags['EXIF DateTimeDigitized'])) or (str(tags['EXIF DateTimeOriginal']) != str(tags['EXIF DateTimeDigitized']))):
            faketime.append(self.lineEdit.text())
            print("faketime : "+str(faketime))
        else:
            normal.append(self.lineEdit.text())
            print("normal : "+str(normal))

    
    def onActivated(self, index):
    #    global normal, faketime, fakesize
        self.textEdit_2.clear()
        print("fakesize : "+str(fakesize))
        print("faketime : "+str(faketime))
        print("normal : "+str(normal))
#        if index == "<분 류>:

        if index == "크기 위조된 파일":
            if fakesize:
                for row in fakesize:
                    self.textEdit_2.insertPlainText(row+'\n')
            else:
                self.textEdit_2.clear()
        if index == "시간 위조된 파일":
            if faketime:
                for row in faketime:
                    self.textEdit_2.insertPlainText(row+'\n')
            else:
                self.textEdit_2.clear()
        if index == "정상 파일":
            if normal:
                for row in normal:
                    self.textEdit_2.insertPlainText(row+'\n')
            else:
                self.textEdit_2.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

