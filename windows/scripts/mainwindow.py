from PyQt5.QtCore import Qt, QEvent, QObject
from PyQt5.QtGui import QIcon, QMouseEvent, QKeyEvent, QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QVBoxLayout, QWidget, QCheckBox, QColorDialog

from rendering import Canvas
from ..layouts.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    ctrlPressed = False

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.toolbar = QToolBar("Панель инструментов")
        self.addToolBar(self.toolbar)

        self.chooseRectangleButton = QPushButton(QIcon("./icons/rectangle.png"), "Прямоугольник", self)
        self.chooseRectangleButton.name = "rectangle"
        self.chooseRectangleButton.pressed.connect(self.buttonRectanglePushed)
        self.toolbar.addWidget(self.chooseRectangleButton)

        self.chooseTriangleButton = QPushButton(QIcon("./icons/triangle.png"), "Треугольник", self)
        self.chooseTriangleButton.name = "triangle"
        self.chooseTriangleButton.pressed.connect(self.buttonTrianglePushed)
        self.toolbar.addWidget(self.chooseTriangleButton)

        self.chooseCircleButton = QPushButton(QIcon("./icons/circle.png"), "Окружность", self)
        self.chooseCircleButton.name = "circle"
        self.chooseCircleButton.pressed.connect(self.buttonCirclePushed)
        self.toolbar.addWidget(self.chooseCircleButton)

        self.checkBoxSelectAll = QCheckBox("Выделять всех в пересечении", self)
        self.checkBoxSelectAll.stateChanged.connect(self.checkBoxSelectAllStateChanged)
        self.toolbar.addWidget(self.checkBoxSelectAll)

        self.action_chooseColor.triggered.connect(self.action_chooseColorTriggered)

        self.chosenShapeButton: QPushButton | None = None

        self.canvas = Canvas(self)
        self.canvas.setObjectName("canvas")
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.installEventFilter(self)

    def buttonRectanglePushed(self):
        if self.chosenShapeButton != self.chooseRectangleButton:
            self.chosenShapeButton = self.chooseRectangleButton
        else:
            self.chosenShapeButton = None
        self.processSelectionChanges()

    def buttonTrianglePushed(self):
        if self.chosenShapeButton != self.chooseTriangleButton:
            self.chosenShapeButton = self.chooseTriangleButton
        else:
            self.chosenShapeButton = None

        self.processSelectionChanges()

    def buttonCirclePushed(self):
        if self.chosenShapeButton != self.chooseCircleButton:
            self.chosenShapeButton = self.chooseCircleButton
        else:
            self.chosenShapeButton = None

        self.processSelectionChanges()

    def setShapeButtonsIcon(self):
        self.chooseRectangleButton.setIcon(QIcon("./icons/rectangle.png"))
        self.chooseTriangleButton.setIcon(QIcon("./icons/triangle.png"))
        self.chooseCircleButton.setIcon(QIcon("./icons/circle.png"))

        if self.chosenShapeButton:
            self.chosenShapeButton.setIcon(QIcon(f"./icons/{self.chosenShapeButton.name}_chosen.png"))

    def processSelectionChanges(self):
        self.setShapeButtonsIcon()
        self.canvas.chosenShape = self.chosenShapeButton.name if self.chosenShapeButton else None

    def checkBoxSelectAllStateChanged(self):
        self.canvas.selectAll = self.checkBoxSelectAll.isChecked()

    def keyPressEvent(self, a0: QKeyEvent):
        super().keyPressEvent(a0)
        if a0.key() == Qt.Key_Delete:
            self.canvas.clear()
        elif a0.key() == Qt.Key_Control:
            self.canvas.multipleSelection = True
        elif a0.key() == Qt.Key_D:  # Вправо
            self.canvas.moveSelectedShapes(10, 0)
        elif a0.key() == Qt.Key_S:  # Вниз
            self.canvas.moveSelectedShapes(0, 10)
        elif a0.key() == Qt.Key_A:  # Влево
            self.canvas.moveSelectedShapes(-10, 0)
        elif a0.key() == Qt.Key_W:  # Вверх
            self.canvas.moveSelectedShapes(0, -10)
        elif a0.key() == Qt.Key_Q: # Уменьшить фигуру
            self.canvas.scaleSelectedShapes(-1)
        elif a0.key() == Qt.Key_E: # Увеличить фигуру
            self.canvas.scaleSelectedShapes(1)
        print("problem fixed")

    def keyReleaseEvent(self, event: QKeyEvent):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Control:
            self.canvas.multipleSelection = False

    def resizeEvent(self, a0: QResizeEvent):
        self.canvas.sizeChanged(a0)

    def eventFilter(self, obj: QObject, event: QEvent):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        elif event.type() == QEvent.KeyRelease:
            self.keyReleaseEvent(event)
            return True
        return super(MainWindow, self).eventFilter(obj, event)

    def action_chooseColorTriggered(self):
        self.canvas.setCurrentColor(QColorDialog.getColor(initial=self.canvas.currentColor))
