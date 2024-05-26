from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QColor, QPainter, QKeyEvent
from PyQt5.QtWidgets import QWidget

from shapes import Shape, Rectangle, Triangle, Circle, SelectedShape


class Canvas(QWidget):
    selectAll = False
    multipleSelection = False
    def __init__(self, parent: QWidget | None = None):
        super(Canvas, self).__init__(parent=parent)
        self.container: list[Shape] = []
        self.currentColor = QColor(0, 0, 0)
        self.chosenShape: str | None = None

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        self.drawShapes()

    def clear(self):
        self.container.clear()
        self.update()

    def drawShapes(self):
        qp = QPainter(self)
        for shape in self.container:
            shape.draw(qp)

    def moveSelectedShapes(self, dx: int, dy: int):
        for shape in self.container:
            if isinstance(shape, SelectedShape):
                shape.move(dx, dy, self.width(), self.height())
        self.update()

    def deselectAllShapes(self):
        for index in range(len(self.container)):
            shape = self.container[index]
            if isinstance(shape, SelectedShape):
                self.container[index] = shape.getRealShape()

    def createNewShape(self, pos: QPoint):
        if not self.chosenShape:
            if not self.multipleSelection:
                self.deselectAllShapes()
            return

        if not self.multipleSelection:
            self.deselectAllShapes()

        if self.chosenShape == "rectangle":
            shape = Rectangle(self.currentColor, pos, 80, 40)
        elif self.chosenShape == "triangle":
            shape = Triangle(self.currentColor, pos, 30)
        elif self.chosenShape == "circle":
            shape = Circle(self.currentColor, pos, 30)
        self.container.append(SelectedShape(self.currentColor, shape))

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        intersections = list(filter(lambda _shape: _shape.isPointInside(event.pos()), self.container))
        if intersections:
            if not self.multipleSelection:
                self.deselectAllShapes()
            if self.selectAll:
                for index in range(len(self.container)):
                    shape = self.container[index]
                    if shape in intersections and not isinstance(shape, SelectedShape):
                        selectedShape = SelectedShape(self.currentColor, shape)
                        self.container[index] = selectedShape
                    index += 1
            else:
                closestShape = min(intersections, key=lambda _shape: _shape.getSquaredDistTo(event.pos()))
                for index in range(len(self.container)):
                    shape = self.container[index]
                    if shape == closestShape and not isinstance(shape, SelectedShape) :
                        selectedShape = SelectedShape(self.currentColor, shape)
                        self.container[index] = selectedShape
                        break
        else:
            self.createNewShape(event.pos())
        self.update()
