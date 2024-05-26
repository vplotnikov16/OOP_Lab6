from PyQt5.QtCore import QPoint, Qt
import math

from PyQt5.QtGui import QPainter, QPen, QColor


def sign(p1: QPoint, p2: QPoint, p3: QPoint):
    return (p1.x() - p3.x()) * (p2.y() - p3.y()) - (p2.x() - p3.x()) * (p1.y() - p3.y())


class Shape:
    center: QPoint = ...
    topLeftCorner: QPoint = ...
    _width: int = ...
    _height: int = ...
    color: QColor = ...

    def __init__(self, color: QColor):
        self.color = color

    def isAbleToMove(self, dx: int, dy: int, formW: int, formH: int):
        s1 = 0 <= self.topLeftCorner.x() + dx and 0 <= self.topLeftCorner.y() + dy
        s2 = self.topLeftCorner.x() + self._width + dx <= formW and self.topLeftCorner.y() + self._height + dy <= formH
        return s1 and s2

    def move(self, dx: int, dy: int, formW: int, formH: int) -> bool:
        if not self.isAbleToMove(dx, dy, formW, formH):
            return False
        self.center = QPoint(self.center.x() + dx, self.center.y() + dy)
        self.topLeftCorner = QPoint(self.topLeftCorner.x() + dx, self.topLeftCorner.y() + dy)
        return True

    def draw(self, qp: QPainter):
        pass

    def isPointInside(self, point: QPoint):
        statement_x = self.topLeftCorner.x() <= point.x() <= self.topLeftCorner.x() + self._width
        statement_y = self.topLeftCorner.y() <= point.y() <= self.topLeftCorner.y() + self._height
        return statement_x and statement_y

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getRealShape(self):
        return self

    def getSquaredDistTo(self, point: QPoint):
        return (self.center.x() - point.x()) ** 2 + (self.center.y() - point.y()) ** 2


class SelectedShape(Shape):
    decoratedShape: Shape = ...

    def __init__(self, color: QColor, shape: Shape):
        super().__init__(color)
        self.decoratedShape = shape
        self.topLeftCorner = QPoint(shape.topLeftCorner.x() - 2, shape.topLeftCorner.y() - 2)
        self._width = shape.getWidth() + 2
        self._height = shape.getHeight() + 2
        self.center = QPoint(self.topLeftCorner.x() + self._width // 2, self.topLeftCorner.y() + self._height // 2)

    def getWidth(self):
        return self.decoratedShape.getHeight()

    def getHeight(self):
        return self.decoratedShape.getHeight()

    def getSquaredDistTo(self, point: QPoint):
        return self.decoratedShape.getSquaredDistTo(point)

    def draw(self, qp: QPainter):
        self.decoratedShape.draw(qp)
        pen = QPen(QColor(127, 127, 127), 1, Qt.DashLine)
        qp.setPen(pen)
        qp.drawRect(self.topLeftCorner.x(), self.topLeftCorner.y(), self._width, self._height)

    def move(self, dx: int, dy: int, formW: int, formH: int) -> bool:
        canMove = self.decoratedShape.move(dx, dy, formW, formH)
        if not canMove:
            return False

        self.center = QPoint(self.center.x() + dx, self.center.y() + dy)
        self.topLeftCorner = QPoint(self.topLeftCorner.x() + dx, self.topLeftCorner.y() + dy)
        return True

    def getRealShape(self):
        return self.decoratedShape.getRealShape()


class Rectangle(Shape):

    def __init__(self, color: QColor, center: QPoint, width: int, height: int):
        super().__init__(color)
        self.center = center
        self._width = width
        self._height = height
        self.topLeftCorner = QPoint(center.x() - width // 2, center.y() - height // 2)

    def draw(self, qp: QPainter):
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(self.topLeftCorner.x(), self.topLeftCorner.y(), self._width, self._height)

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height


class Triangle(Shape):
    _vertex1: QPoint = ...
    _vertex2: QPoint = ...
    _vertex3: QPoint = ...
    _circumScribedCircleRadius: int = ...

    def __init__(self, color: QColor, center: QPoint, circumScribedCircleRadius: int):
        super().__init__(color)
        self.center = center
        self._circumScribedCircleRadius = circumScribedCircleRadius
        angle_offset = 0
        angle_between_vertices = 2 * math.pi / 3

        self._vertex1 = QPoint(
            center.x() + int(self._circumScribedCircleRadius * math.cos(angle_offset)),
            center.y() - int(self._circumScribedCircleRadius * math.sin(angle_offset))
        )

        self._vertex2 = QPoint(
            center.x() + int(self._circumScribedCircleRadius * math.cos(angle_offset + angle_between_vertices)),
            center.y() - int(self._circumScribedCircleRadius * math.sin(angle_offset + angle_between_vertices))
        )

        self._vertex3 = QPoint(
            center.x() + int(self._circumScribedCircleRadius * math.cos(angle_offset + 2 * angle_between_vertices)),
            center.y() - int(self._circumScribedCircleRadius * math.sin(angle_offset + 2 * angle_between_vertices))
        )

        min_x = min(self._vertex1.x(), self._vertex2.x(), self._vertex3.x())
        max_x = max(self._vertex1.x(), self._vertex2.x(), self._vertex3.x())
        min_y = min(self._vertex1.y(), self._vertex2.y(), self._vertex3.y())
        max_y = max(self._vertex1.y(), self._vertex2.y(), self._vertex3.y())

        self.topLeftCorner = QPoint(min_x, min_y)
        self._width = max_x - min_x
        self._height = max_y - min_y

    def draw(self, qp: QPainter):
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawPolygon(self._vertex1, self._vertex2, self._vertex3)

    def move(self, dx: int, dy: int, formW: int, formH: int) -> bool:
        canMove = super().move(dx, dy, formW, formH)
        if not canMove:
            return False

        self._vertex1 = QPoint(self._vertex1.x() + dx, self._vertex1.y() + dy)
        self._vertex2 = QPoint(self._vertex2.x() + dx, self._vertex2.y() + dy)
        self._vertex3 = QPoint(self._vertex3.x() + dx, self._vertex3.y() + dy)
        return True

    def getVertex1(self):
        return self._vertex1

    def getVertex2(self):
        return self._vertex2

    def getVertex3(self):
        return self._vertex3

    def isPointInside(self, point: QPoint):
        s1 = sign(point, self._vertex1, self._vertex2)
        s2 = sign(point, self._vertex2, self._vertex3)
        s3 = sign(point, self._vertex3, self._vertex1)

        any_neg = (s1 < 0) or (s2 < 0) or (s3 < 0)
        any_pos = (s1 > 0) or (s2 > 0) or (s3 > 0)

        return not (any_neg and any_pos)


class Circle(Shape):
    _radius: int = ...

    def __init__(self, color: QColor, center: QPoint, radius: int):
        super().__init__(color)
        self.center = center
        self._radius = radius
        self.topLeftCorner = QPoint(center.x() - self._radius, center.y() - self._radius)
        self._width = 2 * self._radius
        self._height = 2 * self._radius

    def draw(self, qp: QPainter):
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawEllipse(self.topLeftCorner.x(), self.topLeftCorner.y(), 2 * self._radius, 2 * self._radius)

    def getRadius(self):
        return self._radius

    def isPointInside(self, point: QPoint):
        return self.getSquaredDistTo(point) < self._radius ** 2
