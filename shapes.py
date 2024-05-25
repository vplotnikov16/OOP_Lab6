from PyQt5.QtCore import QPoint
import math


class Shape:
    center: QPoint = ...
    topLeftCorner: QPoint = ...
    bottomRightCorner: QPoint = ...

    def move(self, dx: int, dy: int):
        raise NotImplemented("Метод move абстрактного классна Shape не перекрыт")

    def draw(self):
        raise NotImplemented("Метод draw абстрактного класса Shape не перекрыт")


class DecoratedShape(Shape):
    decoratedShape: Shape = ...

    def __init__(self, shape: Shape):
        self.decoratedShape = shape

    def draw(self):
        self.decoratedShape.draw()
        # TODO: отрисовка рамки


class Rectangle(Shape):
    _width: int = ...
    _height: int = ...

    def __init__(self, center: QPoint, width: int, height: int):
        self.center = center
        self._width = width
        self._height = height
        self.topLeftCorner = QPoint(center.x() - width // 2, center.y() - height // 2)
        self.bottomRightCorner = QPoint(center.x() + width // 2, center.y() + height // 2)

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height


class Triangle(Shape):
    _vertex1: QPoint = ...
    _vertex2: QPoint = ...
    _vertex3: QPoint = ...
    _circumScribedCircleRadius: int = ...

    def __init__(self, center: QPoint, circumScribedCircleRadius: int):
        self.center = center
        self._circumScribedCircleRadius = circumScribedCircleRadius
        angle_offset = math.pi / 2
        angle_between_vertices = 2 * math.pi / 3

        self._vertex1 = QPoint(
            center.x() + self._circumScribedCircleRadius * math.cos(angle_offset),
            center.y() - self._circumScribedCircleRadius * math.sin(angle_offset)
        )

        self._vertex2 = QPoint(
            center.x() + self._circumScribedCircleRadius * math.cos(angle_offset + angle_between_vertices),
            center.y() - self._circumScribedCircleRadius * math.sin(angle_offset + angle_between_vertices)
        )

        self._vertex3 = QPoint(
            center.x() + self._circumScribedCircleRadius * math.cos(angle_offset + 2 * angle_between_vertices),
            center.y() - self._circumScribedCircleRadius * math.sin(angle_offset + 2 * angle_between_vertices)
        )

        min_x = min(self._vertex1.x(), self._vertex2.x(), self._vertex3.x())
        max_x = max(self._vertex1.x(), self._vertex2.x(), self._vertex3.x())
        min_y = min(self._vertex1.y(), self._vertex2.y(), self._vertex3.y())
        max_y = max(self._vertex1.y(), self._vertex2.y(), self._vertex3.y())

        self.topLeftCorner = QPoint(min_x, min_y)
        self.bottomRightCorner = QPoint(max_x, max_y)

    def getVertex1(self):
        return self._vertex1

    def getVertex2(self):
        return self._vertex2

    def getVertex3(self):
        return self._vertex3


class Circle(Shape):
    _radius: int = ...

    def __init__(self, center: QPoint, radius: int):
        self.center = center
        self._radius = radius
        self.topLeftCorner = QPoint(center.x() - self._radius, center.y() - self._radius)
        self.bottomRightCorner = QPoint(center.x() + self._radius, center.y() + self._radius)

    def getRadius(self):
        return self._radius
