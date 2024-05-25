class Shape:
    center: (int, int) = ...

    def move(self, dx: int, dy: int):
        self.center[0] += dx
        self.center[1] += dy

    def draw(self):
        pass


class DecoratedShape(Shape):
    decoratedShape: Shape = ...

    def __init__(self, shape: Shape):
        self.decoratedShape = shape

    def draw(self):
        self.decoratedShape.draw()
        # TODO: отрисовка рамки


class Rectangle(Shape):
    pass


class Triangle(Shape):
    pass


class Circle(Shape):
    pass
