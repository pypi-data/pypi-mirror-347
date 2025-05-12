from typing import Any

from .abc_shapesqr import ShapeABC, ShapeFabricABC
from .circle_shape import Circle
from .triangle_shape import Triangle


class ShapeFabric(ShapeFabricABC):
    def _validate_params(self, params: Any) -> None:
        if not (isinstance(params, tuple) and (all((isinstance(x, (float, int)) for x in params)))):
            raise TypeError

    def get_shape(self, params: tuple[float]) -> ShapeABC:
        self._validate_params(params)

        match params:
            case (_,):
                return Circle(params)
            case (_, _, _):
                return Triangle(params)
            case _:
                raise NotImplementedError
