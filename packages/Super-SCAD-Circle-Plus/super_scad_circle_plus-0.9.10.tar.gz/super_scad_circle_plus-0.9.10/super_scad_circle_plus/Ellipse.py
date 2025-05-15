from typing import Any, Dict

from super_scad.d2.Circle import Circle
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Resize2D import Resize2D
from super_scad.type.Vector2 import Vector2


class Ellipse(ScadWidget):
    """
    Widget for creating ellipses.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius_x: float | None = None,
                 radius_y: float | None = None,
                 diameter_x: float | None = None,
                 diameter_y: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param radius_x: The radius of the ellipsis along the x-axis.
        :param radius_y: The radius of the ellipsis along the y-axis.
        :param diameter_x: The diameter of the ellipsis along the x-axis.
        :param diameter_x: The diameter of the ellipsis along the y-axis.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create an ellipse with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._radius_x: float | None = radius_x
        """
        The radius of the ellipse along the x-axis.
        """

        self._radius_y: float | None = radius_y
        """
        The radius of the ellipse along the y-axis.
        """

        self._diameter_x: float | None = diameter_x
        """
        The diameter of the ellipse along the x-axis.
        """

        self._diameter_y: float | None = diameter_y
        """
        The diameter of the ellipse along the y-axis.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fs
        """
        The minimum circumferential length of each fragment.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create an ellipse with a multiple of 4 vertices.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'radius_x'}, {'diameter_x'})
        validator.validate_exclusive({'radius_y'}, {'diameter_y'})
        validator.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        validator.validate_required({'radius_x', 'diameter_x'}, {'radius_y', 'diameter_y'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_x(self) -> float:
        """
        Returns the radius of the ellipsis in x-direction.
        """
        if self._radius_x is None:
            self._radius_x = 0.5 * self._diameter_x

        return self._radius_x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_y(self) -> float:
        """
        Returns the radius of the ellipsis in y-direction.
        """
        if self._radius_y is None:
            self._radius_y = 0.5 * self._diameter_y

        return self._radius_y

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_x(self) -> float:
        """
        Returns the length of the ellipsis in x-direction.
        """
        if self._diameter_x is None:
            self._diameter_x = 2.0 * self._radius_x

        return self._diameter_x

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_y(self) -> float:
        """
        Returns the length of the ellipsis in y-direction.
        """
        if self._diameter_y is None:
            self._diameter_y = 2.0 * self._radius_y

        return self._diameter_y

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        diameter: float = max(self.diameter_x, self.diameter_y)

        return Resize2D(new_size=Vector2(self.diameter_x, self.diameter_y),
                        child=Circle(diameter=diameter, fa=self.fa, fs=self.fs, fn=self.fn, fn4n=self.fn4n))

# ----------------------------------------------------------------------------------------------------------------------
