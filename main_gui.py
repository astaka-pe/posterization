import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QSlider, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout
from PySide6.QtGui import QPixmap
import os
import sys
import cv2

from posterization import Posterization

class Image(QLabel):
    def __init__(self, q_img, parent=None):
        super(Image, self).__init__(parent)
        self.setImage(q_img)

    def setImage(self, q_img):
        self.setPixmap(q_img)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = "img/zurich.jpg"
        self.poster = Posterization(self.path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Posterization")
        self.X, self.Y = 100, 100
        self.W, self.H = 1000, 600
        self.X_2 = 650
        self.setGeometry(self.X, self.Y, self.W, self.H)
        # self.SetSlider()
        
        self.parameterbox = QVBoxLayout()
        hbox = QHBoxLayout()
        title_1 = QLabel("shadow level")
        self.label_1 = QLabel()
        self.slider_1 = QSlider()
        self.slider_1.setTickInterval(1)
        self.slider_1.setValue(25)
        self.slider_1.setMinimum(1)
        self.slider_1.setMaximum(255)
        self.slider_1.setOrientation(Qt.Horizontal)
        self.slider_1.valueChanged.connect(self.CallbackValuechangedSlider)
        self.label_1.setText(str(self.slider_1.value()))

        hbox.addWidget(title_1)
        hbox.addWidget(self.slider_1)
        hbox.addWidget(self.label_1)
        self.parameterbox.addLayout(hbox)

        hbox = QHBoxLayout()
        title_2 = QLabel("tone_min")
        self.label_2 = QLabel()
        self.slider_2 = QSlider()
        self.slider_2.setTickInterval(1)
        self.slider_2.setValue(20)
        self.slider_2.setMinimum(0)
        self.slider_2.setMaximum(self.slider_1.value()-1)
        self.slider_2.setOrientation(Qt.Horizontal)
        self.slider_2.valueChanged.connect(self.CallbackValuechangedSlider)
        self.label_2.setText(str(self.slider_2.value()))

        hbox.addWidget(title_2)
        hbox.addWidget(self.slider_2)
        hbox.addWidget(self.label_2)
        self.parameterbox.addLayout(hbox)

        hbox = QHBoxLayout()
        title_3 = QLabel("tone_max")
        self.label_3 = QLabel()
        self.slider_3 = QSlider()
        self.slider_3.setTickInterval(1)
        self.slider_3.setValue(85)
        self.slider_3.setMinimum(self.slider_2.value()+1)
        self.slider_3.setMaximum(255)
        self.slider_3.setOrientation(Qt.Horizontal)
        self.slider_3.valueChanged.connect(self.CallbackValuechangedSlider)
        self.label_3.setText(str(self.slider_3.value()))

        hbox.addWidget(title_3)
        hbox.addWidget(self.slider_3)
        hbox.addWidget(self.label_3)
        self.parameterbox.addLayout(hbox)

        hbox = QHBoxLayout()
        title_4 = QLabel("blightness")
        self.label_4 = QLabel()
        self.slider_4 = QSlider()
        self.slider_4.setTickInterval(1)
        self.slider_4.setValue(85)
        self.slider_4.setMinimum(0)
        self.slider_4.setMaximum(255)
        self.slider_4.setOrientation(Qt.Horizontal)
        self.slider_4.valueChanged.connect(self.CallbackValuechangedSlider)
        self.label_4.setText(str(self.slider_3.value()))

        hbox.addWidget(title_4)
        hbox.addWidget(self.slider_4)
        hbox.addWidget(self.label_4)
        self.parameterbox.addLayout(hbox)


        self.layout = QVBoxLayout()
        init_img = self.resize_image(QPixmap(self.path))
        self.layout.addWidget(Image(init_img))

        self.parentlayout = QHBoxLayout()
        self.parentlayout.addLayout(self.layout)
        self.parentlayout.addLayout(self.parameterbox)
        self.setLayout(self.parentlayout)
        self.setGeometry(self.X, self.Y, self.W, self.H)
        self.show()
    
    def resize_image(self, q_img):
        im_w, im_h = q_img.size().width(), q_img.size().height()
        scale = im_w / self.X_2
        img = q_img.scaled(im_w/scale, im_h/scale)
        return img

    def SetImage(self):
        label = QLabel(self)
        image = QPixmap("img/fukushima.JPG")
        im_w, im_h = image.size().width(), image.size().height()
        scale = im_w / self.X_2
        image = image.scaled(im_w/scale, im_h/scale)
        label.setPixmap(image)

    def SetOutImage(self):
        image = self.out_img
        label = QLabel(self)
        im_w, im_h = image.size().width(), image.size().height()
        scale = im_w / self.X_2
        image = image.scaled(im_w/scale, im_h/scale)
        label.setPixmap(image)

    def SetButton(self):
        button = QPushButton(self)
        button.setText("Posterization")
        button.pressed.connect(self.CallbackButtonPressed)
    
    def CallbackValuechangedSlider(self):
        shadow_upper = self.slider_1.value()
        in_lower = self.slider_2.value()
        in_upper = self.slider_3.value()
        out_lower = self.slider_4.value()
        self.label_1.setText(str(self.slider_1.value()))
        self.label_2.setText(str(self.slider_2.value()))
        self.label_3.setText(str(self.slider_3.value()))
        self.label_4.setText(str(self.slider_4.value()))
        self.slider_2.setMaximum(self.slider_1.value()-1)
        self.slider_3.setMinimum(self.slider_2.value()+1)
        out_img = self.poster.get_output(shadow_upper=shadow_upper, in_lower=in_lower, in_upper=in_upper, out_lower=out_lower)
        #cv2.imwrite("img/tmp.jpg", out_img)
        q_img = self.cv_to_pixmap(out_img)
        q_img = self.resize_image(q_img)
        self.out_img = QPixmap(QPixmap.fromImage(q_img))
        self.clear_labels()
        self.layout.addWidget(Image(self.out_img))

    def clear_labels(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

    @staticmethod
    def cv_to_pixmap(cv_image):
        height, width, bytesPerComponent = cv_image.shape
        bytesPerLine = bytesPerComponent * width
        cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB, cv_image)
        q_img = QtGui.QImage(cv_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        return q_img

def main():
    dirname = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(dirname, "plugins", "platforms")
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()