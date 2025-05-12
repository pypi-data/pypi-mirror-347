from abc import ABC, abstractmethod
from typing import Callable

from typing_extensions import Self


class ShapeFabricABC(ABC):
    @abstractmethod
    def get_shape(self, params: tuple[float]) -> "ShapeABC": ...


class ShapeABC(ABC):
    DEFAULT_RESULT: float | None = None

    CALC_STATUS_DEFAULT: int = 0
    CALC_STATUS_OK: int = 1
    CALC_STATUS_ERR: int = -1

    TYPE: str

    def __init__(self, params: tuple[float]) -> Self:
        self.params = params
        self.last_calc_status: int = self.CALC_STATUS_DEFAULT
        self.last_calc_result: float = self.DEFAULT_RESULT

    # commands
    @abstractmethod
    def _calculate_perimeter(self) -> None: ...

    @abstractmethod
    def _calculate_square(self) -> None: ...

    def _process_calculation(self, calc_function: Callable) -> None:
        try:
            calc_function()
            assert isinstance(self.last_calc_result, float) is True

            self.last_calc_status = self.CALC_STATUS_OK
        except (TypeError, AssertionError):
            self.last_calc_result = self.DEFAULT_RESULT
            self.last_calc_status = self.CALC_STATUS_ERR

    def calculate_perimeter(self) -> None:
        """pre-conditions: properly created Shape object
        post-conditions: calculated and set as last_result perimeter,
        set proper status
        """

        self._process_calculation(self._calculate_perimeter)

    def calculate_square(self):
        """pre-conditions: properly created Shape object
        post-conditions: calculated and set as last_result square,
        set proper status
        """

        self._process_calculation(self._calculate_square)

    # queries
    def get_shape_type(self) -> str:
        """return verbose description of the shape"""
        return self.TYPE

    def get_calculated_result(self) -> tuple[int, float]:
        return (self.last_calc_status, self.last_calc_result)

    def is_right(self):
        """to be overridden in Triangle (maybe other if applies) classes"""
        raise NotImplementedError
