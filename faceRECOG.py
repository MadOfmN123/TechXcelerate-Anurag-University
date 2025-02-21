import os.path
import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
import cv2
import face_recognition
import numpy

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSlot


from FaceRecogGUI import Ui_Form


def nameList(nameofImg):
    if nameofImg.startswith('Sai', 0):
        return "Sai Suhas"
    elif nameofImg.startswith('Prakash', 0):
        return "Prakash"
    elif nameofImg.startswith('Tarak', 0):
        return "Tarak Krishna"


class FaceRECOG(QDialog):
    def __init__(self):
        super(FaceRECOG, self).__init__()
        self.firstUi = Ui_Form()
        self.firstUi.setupUi(self)

        self.name = None
        self.camCapture = None
        self.name = None

        self.firstUi.pushButton_2.clicked.connect(self.close)
        self.runProgram()

    def runProgram(self):
        videoPath = "0"
        self.camCapture = videoPath
        self.encodeImages(self.camCapture)

    @pyqtSlot()
    def encodeImages(self, cameraName):
        print("encoding Started")
        if len(cameraName) == 1:
            self.capture = cv2.VideoCapture(int(cameraName))
        else:
            self.capture = cv2.VideoCapture(cameraName)
        self.timer = QTimer(self)
        path = 'C:\\Users\\tarak\\Downloads\\AKK-main\\AKK-main\\imagesSS'
        if not os.path.exists(path):
            os.mkdir(path)

        images = []
        self.classNames = []
        self.encodeList = []

        photoList = os.listdir(path)

        for cl in photoList:
            currentImage = cv2.imread(f'{path}/{cl}')
            images.append(currentImage)
            self.classNames.append(os.path.splitext(cl)[0])

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            box = face_recognition.face_locations(img)
            encodeCurFrame = face_recognition.face_encodings(img, box)[0]
            self.encodeList.append(encodeCurFrame)

        print("Image Encoded Successfully")
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(5)

    def updateFrame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encodeList, self.classNames, 1)

    def displayImage(self, image, encodeList, classNames, window=1):
        image = cv2.resize(image, (661, 501))
        try:
            self.faceRecognition(image, encodeList, classNames)
        except Exception as e:
            print(e)

        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.firstUi.label_3.setPixmap(QPixmap.fromImage(outImage))
            self.firstUi.label_3.setScaledContents(True)
            if self.name == "Sai Suhas":
                self.connectToIshi()
                self.timer.stop()
            elif self.name == "Tarak Krishna":
                self.connectToIshi()
                self.timer.stop()

    def faceRecognition(self, image, encodeList, className):
        facesOfCurrentFrame = face_recognition.face_locations(image)
        encodeCurrentFrame = face_recognition.face_encodings(image, facesOfCurrentFrame)

        for encodeFace, faceLocation in zip(encodeCurrentFrame, facesOfCurrentFrame):
            match = face_recognition.compare_faces(encodeList, encodeFace, tolerance=0.5)
            faceDistance = face_recognition.face_distance(encodeList, encodeFace)
            self.name = "Unknown"
            bestMatchIndex = numpy.argmin(faceDistance)

            if match[bestMatchIndex]:
                self.name = className[bestMatchIndex]
                self.name = nameList(self.name)
                y1, x2, x1, y2 = faceLocation
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, self.name, (x1 - 6, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        return image

    def connectToIshi(self):
        from subprocess import call
        self.close()
        call(["python", "ISHITechnologyMAIN.py"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = FaceRECOG()
    ui.show()
    sys.exit(app.exec_())
