from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 500)
        Dialog.setMinimumSize(QtCore.QSize(700, 500))
        Dialog.setStyleSheet("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-2, 0, 701, 501))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/Bg.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 681, 291))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/G.U.I Material/ExtraGui/Jarvis_Gui (2).gif"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 390, 511, 111))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/st and sti.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(170, 400, 111, 91))
        self.pushButton.setStyleSheet("border-image : url(C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/btn1.png)")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 400, 111, 91))
        self.pushButton_2.setStyleSheet("border-image : url(C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/btn2.png)")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(120, -10, 499, 100))
        self.label_4.setPixmap(QtGui.QPixmap("C:/Users/tarak/OneDrive/Desktop/ISHI Technology/IMAGES/logo.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
