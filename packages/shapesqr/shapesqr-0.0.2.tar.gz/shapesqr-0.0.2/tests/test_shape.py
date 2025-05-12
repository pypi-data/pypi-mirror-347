import unittest
from math import pi

from shapesqr.circle_shape import Circle
from shapesqr.shape_fabric import ShapeFabric
from shapesqr.triangle_shape import Triangle


class ShapeTestCase(unittest.TestCase):
    def setUp(self):
        self.expected_map = {
            Circle: {
                "params": (1,),
                "sqr": pi,
                "error_params": ("1",),
            },
            Triangle: {
                "params": (3, 4, 5),
                "sqr": 6,
                "error_params": ("3", 4, 5),
            },
        }

    def _test_shape(self, tested_class):
        try:
            shape = ShapeFabric().get_shape(self.expected_map[tested_class]["error_params"])
        except Exception as e:
            self.assertTrue(isinstance(e, TypeError))

        shape = ShapeFabric().get_shape(self.expected_map[tested_class]["params"])
        self.assertTrue(isinstance(shape, tested_class))

        shape.calculate_square()
        status, result = shape.get_calculated_result()
        self.assertEqual(status, tested_class.CALC_STATUS_OK)
        self.assertEqual(result, self.expected_map[tested_class]["sqr"])

        shape = tested_class(self.expected_map[tested_class]["error_params"])
        shape.calculate_square()
        status, result = shape.get_calculated_result()
        self.assertEqual(status, tested_class.CALC_STATUS_ERR)
        self.assertEqual(result, None)

    def test_circle(self):
        self._test_shape(Circle)

    def test_triangle(self):
        self._test_shape(Triangle)

        triangle = Triangle(self.expected_map[Triangle]["params"])
        self.assertTrue(triangle.is_right())
