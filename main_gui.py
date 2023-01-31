import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QMenuBar, QSlider, QSpinBox, QComboBox,QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QFileDialog
from PySide6.QtGui import QPixmap, QAction
import os
import sys
import cv2
import PIL.Image as PImage
import numpy as np
from collections import OrderedDict

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
        self.path = "None"
        """ menubar """
        menu_list = OrderedDict(
            File = ["Open", "Save"],
        )
        self.menubar = QMenuBar(self)
        self.menubar.setNativeMenuBar(False)
        self.menu = []
        self.action = []
        for k, v in menu_list.items():
            self.menu.append(self.menubar.addMenu(k))
            for submenu in v:
                self.action.append(QAction(submenu))
                self.menu[-1].addAction(self.action[-1])
                if submenu == "Open":
                    self.action[-1].triggered.connect(self.openAction)
                elif submenu == "Save":
                    self.action[-1].triggered.connect(self.saveAction)

        self.initUI()
    
    def openAction(self):
        (fileName, selectedFilter) = QFileDialog.getOpenFileName(self, "Open file", os.path.expanduser('~'), ("Images (*.png *.jpg)"))
        if fileName != "":
            self.path = fileName
            self.out_img = cv2.imread(self.path)
            self.clear_labels()
            init_img = self.resize_image(QPixmap(self.path))
            self.layout.addWidget(Image(init_img))
            self.poster = Posterization(self.path)
    
    def saveAction(self):
        (fileName, selectedFilter) = QFileDialog.getSaveFileName(self, "Save file", os.path.expanduser('~'), "Images (*.png *.jpg)")
        if fileName != "":
            cv2.imwrite(fileName, self.out_img)

    def initUI(self):
        self.setWindowTitle("Posterization")
        self.X, self.Y = 100, 100
        self.W, self.H = 1000, 400
        self.X_2 = 650
        self.setGeometry(self.X, self.Y, self.W, self.H)
        # self.SetSlider()
        
        self.parameterbox = QVBoxLayout()

        """ button """
        hbox = QHBoxLayout()
        org_button = QPushButton()
        org_button.setText("original image")
        org_button.pressed.connect(self.CallbackButtonPressed)
        hbox.addWidget(org_button)
        pos_button = QPushButton()
        pos_button.setText("posterized image")
        pos_button.pressed.connect(self.CallbackValuechangedSlider)
        hbox.addWidget(pos_button)
        self.parameterbox.addLayout(hbox)

        """ gradation """
        hbox = QHBoxLayout()
        title_grd = QLabel("gradation")
        self.spinbox_grd = QSpinBox()
        self.spinbox_grd.setSingleStep(1)
        self.spinbox_grd.setValue(3)
        self.spinbox_grd.setRange(2, 10)
        self.spinbox_grd.valueChanged.connect(self.CallbackValuechangedSlider)
        hbox.addWidget(title_grd)
        hbox.addWidget(self.spinbox_grd)
        self.parameterbox.addLayout(hbox)

        """ edge """
        hbox = QHBoxLayout()
        title_edg = QLabel("edge")
        self.spinbox_edg = QSpinBox()
        self.spinbox_edg.setSingleStep(1)
        self.spinbox_edg.setValue(2)
        self.spinbox_edg.setRange(0, 5)
        self.spinbox_edg.valueChanged.connect(self.CallbackValuechangedSlider)
        hbox.addWidget(title_edg)
        hbox.addWidget(self.spinbox_edg)
        self.parameterbox.addLayout(hbox)

        """ shadow level """
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

        """ tone min """
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

        """ tone max """
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

        """ brightness """
        hbox = QHBoxLayout()
        title_4 = QLabel("brightness")
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

        """ color """
        hbox = QHBoxLayout()
        self.color = QComboBox()
        for s in ["Green", "Ocean", "Autumn"]:
            self.color.addItem(s)
        self.color.currentTextChanged.connect(self.CallbackValuechangedSlider)
        self.color.setCurrentIndex(0)
        hbox.addWidget(self.color)
        self.parameterbox.addLayout(hbox)

        """ right image """
        self.layout = QVBoxLayout()
        init_img = np.ones([self.H, self.X_2, 3]).astype(np.uint8) * 255
        init_img = QPixmap(self.cv_to_pixmap(init_img))
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
    
    def CallbackButtonPressed(self):
        self.clear_labels()
        init_img = self.resize_image(QPixmap(self.path))
        self.layout.addWidget(Image(init_img))
    
    def CallbackValuechangedSlider(self):
        n = self.spinbox_grd.value()
        edge = self.spinbox_edg.value()
        shadow_upper = self.slider_1.value()
        in_lower = self.slider_2.value()
        in_upper = self.slider_3.value()
        out_lower = self.slider_4.value()
        color = self.color.currentIndex()
        self.label_1.setText(str(self.slider_1.value()))
        self.label_2.setText(str(self.slider_2.value()))
        self.label_3.setText(str(self.slider_3.value()))
        self.label_4.setText(str(self.slider_4.value()))
        self.slider_2.setMaximum(self.slider_1.value()-1)
        self.slider_3.setMinimum(self.slider_2.value()+1)
        out_img = self.poster.get_output(n=n, edge=edge, shadow_upper=shadow_upper, in_lower=in_lower, in_upper=in_upper, out_lower=out_lower, color=color)
        self.out_img = out_img
        #cv2.imwrite("img/tmp.jpg", out_img)
        q_img = self.cv_to_pixmap(out_img)
        q_img = self.resize_image(q_img)
        self.q_img = QPixmap(QPixmap.fromImage(q_img))
        self.clear_labels()
        self.layout.addWidget(Image(self.q_img))

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