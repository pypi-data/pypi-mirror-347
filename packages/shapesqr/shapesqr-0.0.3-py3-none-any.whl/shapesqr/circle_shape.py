from math import pi

from .abc_shapesqr import ShapeABC


class Circle(ShapeABC):
    TYPE = "circle"

    def _calculate_perimeter(self):
        self.last_calc_result = 2 * pi * self.params[0]

    def _calculate_square(self):
        self.last_calc_result = pi * (self.params[0] ** 2)
