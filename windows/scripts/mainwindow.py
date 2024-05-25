from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton

from ..layouts.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.toolbar = QToolBar("Панель инструментов")
        self.addToolBar(self.toolbar)

        self.selectRectangleButton = QPushButton(QIcon("./icons/rectangle.png"), "Прямоугольник", self)
        self.selectRectangleButton.path = "rectangle"
        self.selectRectangleButton.pressed.connect(self.buttonRectanglePushed)
        self.toolbar.addWidget(self.selectRectangleButton)

        self.selectTriangleButton = QPushButton(QIcon("./icons/triangle.png"), "Треугольник", self)
        self.selectTriangleButton.path = "triangle"
        self.selectTriangleButton.pressed.connect(self.buttonTrianglePushed)
        self.toolbar.addWidget(self.selectTriangleButton)

        self.selectCircleButton = QPushButton(QIcon("./icons/Circle.png"), "Окружность", self)
        self.selectCircleButton.path = "circle"
        self.selectCircleButton.pressed.connect(self.buttonCirclePushed)
        self.toolbar.addWidget(self.selectCircleButton)

        self.selectedShapeButton: QPushButton | None = None

    def buttonRectanglePushed(self):
        if self.selectedShapeButton != self.selectRectangleButton:
            self.selectedShapeButton = self.selectRectangleButton
        else:
            self.selectedShapeButton = None

        self.setShapeButtonsIcons()

    def buttonTrianglePushed(self):
        if self.selectedShapeButton != self.selectTriangleButton:
            self.selectedShapeButton = self.selectTriangleButton
        else:
            self.selectedShapeButton = None

        self.setShapeButtonsIcons()

    def buttonCirclePushed(self):
        if self.selectedShapeButton != self.selectCircleButton:
            self.selectedShapeButton = self.selectCircleButton
        else:
            self.selectedShapeButton = None

        self.setShapeButtonsIcons()

    def setShapeButtonsIcons(self):
        self.selectRectangleButton.setIcon(QIcon("./icons/rectangle.png"))
        self.selectTriangleButton.setIcon(QIcon("./icons/triangle.png"))
        self.selectCircleButton.setIcon(QIcon("./icons/circle.png"))

        if self.selectedShapeButton:
            self.selectedShapeButton.setIcon(QIcon(f"./icons/{self.selectedShapeButton.path}_selected.png"))
