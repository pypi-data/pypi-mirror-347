from math import sqrt

from .abc_shapesqr import ShapeABC


class Triangle(ShapeABC):
    TYPE = "triangle"

    def _calculate_perimeter(self):
        self.last_calc_result = sum(self.params)

    def _calculate_square(self):
        self._calculate_perimeter()
        semi_perimeter = self.last_calc_result / 2
        a, b, c = self.params
        self.last_calc_result = sqrt(
            semi_perimeter * (semi_perimeter - a) * (semi_perimeter - b) * (semi_perimeter - c)
        )

    def is_right(self):
        a, b, c = self.params
        return any((a**2 == b**2 + c**2, b**2 == a**2 + c**2, c**2 == a**2 + b**2))
