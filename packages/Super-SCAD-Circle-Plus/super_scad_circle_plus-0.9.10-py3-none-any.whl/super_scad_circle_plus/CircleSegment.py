import math

from super_scad.boolean.Intersection import Intersection
from super_scad.d2.Circle import Circle
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2


class CircleSegment(ScadWidget):
    """
    Widget for creating circle segments.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float | None = None,
                 diameter: float | None = None,
                 central_angle: float | None = None,
                 chord_length: float | None = None,
                 arc_length: float | None = None,
                 sagitta: float | None = None,
                 apothem: float | None = None,
                 minor_segment: bool = True,
                 align_on_x_axis: bool = True,
                 extend_by_eps_radius: bool = False,
                 extend_by_eps_cord: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param radius: The radius of the circle.
        :param diameter: The diameter of the circle.
        :param diameter: The diameter of the circle.
        :param central_angle: The central angle of the circle segment.
        :param chord_length: The chord length of the circle segment.
        :param arc_length: The arc length of the circle segment.
        :param sagitta: The sagitta of the circle segment, a.k.a., the height of the circle segment.
        :param apothem: The apothem of the circle segment, a.k.a., the radius minus height of the circle segment.
        :param minor_segment: Whether the circle segment is the minor segment.
        :param align_on_x_axis: Whether the circle segment is aligned on x-axis.
        :param extend_by_eps_radius: Whether to extend the radius by eps for a clear overlap.
        :param extend_by_eps_cord: Whether to extend the circle segment along the cord by eps for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a circle with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._radius = radius
        """
        The radius of the circle.
        """

        self._diameter = diameter
        """
        The diameter of the circle.
        """

        self._central_angle = central_angle
        """
        The central angle of the circle segment.
        """

        self._chord_length = chord_length
        """
        The chord length of the circle segment.
        """

        self._arc_length = arc_length
        """
        The arc length of the circle segment.
        """

        self._sagitta = sagitta
        """
        The sagitta of the circle segment.
        """

        self._apothem = apothem
        """
        The apothem of the circle segment.
        """

        self._minor_segment = minor_segment
        """
        Whether the circle segment is the minor segment.
        """

        self._align_on_x_axis = align_on_x_axis
        """
        Whether the circle segment is aligned on x-axis.
        """

        self._extend_by_eps_radius = extend_by_eps_radius
        """
        Whether to extend the radius by eps for a clear overlap.
        """

        self._extend_by_eps_cord = extend_by_eps_cord
        """
        Whether to extend the circle segment along the cord by eps for a clear overlap.
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
        Whether to create a circle with a multiple of 4 vertices.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the circle.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the circle.
        """
        if self._diameter is None:
            self._diameter = 2.0 * self._radius

        return self._diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def central_angle(self) -> float:
        """
        Returns the central angle of the circle segment.
        """
        if self._central_angle is None:
            if self._chord_length is not None:
                self._central_angle = math.degrees(2.0 * math.asin(self._chord_length / (2.0 * self.radius)))
            elif self._arc_length is not None:
                self._central_angle = math.degrees(self._arc_length / self.radius)
            elif self._sagitta is not None:
                self._central_angle = math.degrees(2.0 * math.acos(1 - self._sagitta / self.radius))
            elif self._apothem is not None:
                self._central_angle = math.degrees(2.0 * math.acos(self._apothem / self.radius))
            else:
                raise ValueError('Math is broken!')

        return self._central_angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def chord_length(self) -> float:
        """
        Returns the chord length of the circle segment.
        """
        if self._chord_length is None:
            if self._central_angle is not None:
                self._chord_length = 2.0 * self.radius * math.sin(math.radians(0.5 * self._central_angle))
            elif self._arc_length is not None:
                self._chord_length = 2.0 * self.radius * math.sin(0.5 * self._arc_length / self.radius)
            elif self._sagitta is not None:
                self._chord_length = 2.0 * math.sqrt(2.0 * self.radius * self._sagitta - self._sagitta ** 2)
            elif self._apothem is not None:
                self._chord_length = 2.0 * math.sqrt(self.radius ** 2 - self._apothem ** 2)
            else:
                raise ValueError('Math is broken!')

        return self._chord_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def arc_length(self) -> float:
        """
        Returns the arc length of the circle segment.
        """
        if self._arc_length is None:
            if self._central_angle is not None:
                self._arc_length = math.radians(self._central_angle) * self.radius
            elif self._chord_length is not None:
                self._arc_length = 2.0 * math.asin(self._chord_length / (2.0 * self.radius)) * self.radius
            elif self._sagitta is not None:
                self._arc_length = 2.0 * self.radius * math.acos(1.0 - self._sagitta / self.radius)
            elif self._apothem is not None:
                self._arc_length = 2.0 * math.acos(self._apothem / self.radius) * self.radius
            else:
                raise ValueError('Math is broken!')

        return self._arc_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sagitta(self) -> float:
        """
        Returns the sagitta of the circle segment.
        """
        if self._sagitta is None:
            if self._central_angle is not None:
                self._sagitta = self.radius * (1.0 - math.cos(math.radians(0.5 * self._central_angle)))
            elif self._chord_length is not None:
                self._sagitta = self.radius - math.sqrt(self.radius ** 2 - 0.25 * self._chord_length ** 2)
            elif self._arc_length is not None:
                self._sagitta = self.radius * (1.0 - math.cos(0.5 * self._arc_length / self.radius))
            elif self._apothem is not None:
                self._sagitta = self.radius - self._apothem
            else:
                raise ValueError('Math is broken!')

        return self._sagitta

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def apothem(self) -> float:
        """
        Returns the apothem of the circle segment.
        """
        if self._apothem is None:
            if self._central_angle is not None:
                self._apothem = self.radius * math.cos(math.radians(0.5 * self._central_angle))
            elif self._chord_length is not None:
                self._apothem = math.sqrt(self.radius ** 2 - 0.25 * self._chord_length ** 2)
            elif self._arc_length is not None:
                self._apothem = self.radius * math.cos(0.5 * self._arc_length / self.radius)
            elif self._sagitta is not None:
                self._apothem = self.radius - self._sagitta
            else:
                raise ValueError('Math is broken!')

        return self._apothem

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def minor_segment(self) -> bool:
        """
        Returns whether the circle segment is the minor segment.
        """
        return self._minor_segment

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def align_on_x_axis(self) -> bool:
        """
        Returns whether the circle segment is aligned on x-axis.
        """
        return self._align_on_x_axis

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_radius(self) -> bool:
        """
        Returns whether to extend the radius by eps for a clear overlap.
        """
        return self._extend_by_eps_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_cord(self) -> bool:
        """
        Returns whether to extend the circle segment along the cord by eps for a clear overlap.
        """
        return self._extend_by_eps_cord

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
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._fn4n

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def area(self) -> float:
        """
        Returns the area of the circle segment.
        """
        area = 0.5 * self.radius ** 2 * (self.central_angle - math.sin(math.radians(self.central_angle)))

        if not self.minor_segment:
            area = math.pi * self.radius ** 2 - area

        return area

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def perimeter(self) -> float:
        """
        Returns the perimeter of the circle segment.
        """
        if self.minor_segment:
            perimeter = self.chord_length + self.arc_length
        else:
            perimeter = 2.0 * math.pi * self.radius - self.arc_length + self.chord_length

        return perimeter

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        radius = self.radius
        if self.extend_by_eps_radius:
            radius += context.eps

        circle = Circle(radius=radius, fa=self.fa, fs=self.fs, fn4n=self.fn4n, fn=self.fn)
        mask = self._build_mask(context)
        circle_segment = Intersection(children=[circle, mask])

        if self.align_on_x_axis:
            circle_segment = Translate2D(y=-self.apothem, child=circle_segment)

        return circle_segment

    # ------------------------------------------------------------------------------------------------------------------
    def _build_mask(self, context: Context) -> ScadWidget:
        """
        Builds the mask for intersection with the circle.

        :param context: The build context.
        """
        radius = self.radius
        if self.extend_by_eps_radius:
            radius += context.eps

        chord_length = 2.0 * radius * math.sin(math.radians(0.5 * self.central_angle))
        real_apothem = self._real_apothem(context)

        if self.minor_segment:
            if self.central_angle < 180.0:
                x = 0.5 * chord_length
                mask = Polygon(points=[Vector2(-x, real_apothem),
                                       Vector2(-x, radius),
                                       Vector2(x, radius),
                                       Vector2(x, real_apothem)])
            else:
                mask = Polygon(points=[Vector2(-radius, real_apothem),
                                       Vector2(-radius, radius),
                                       Vector2(radius, radius),
                                       Vector2(radius, real_apothem)])

        else:
            if self.central_angle < 180.0:
                mask = Polygon(points=[Vector2(-radius, -radius),
                                       Vector2(-radius, real_apothem),
                                       Vector2(radius, real_apothem),
                                       Vector2(radius, -radius)])
            else:
                x = 0.5 * chord_length
                mask = Polygon(points=[Vector2(-x, -radius),
                                       Vector2(-x, real_apothem),
                                       Vector2(x, real_apothem),
                                       Vector2(x, -radius)])

        return mask

    # ------------------------------------------------------------------------------------------------------------------
    def _real_apothem(self, context: Context) -> float:
        """
        Returns the real apothem of the circle segment.

        :param context: The build context.
        """
        central_angle = self.central_angle
        if self.extend_by_eps_cord:
            vector = Vector2.from_polar(self.radius, 90.0 - 0.5 * central_angle)
            vector += Vector2(0.0, -context.eps if self.minor_segment else context.eps)
            central_angle = math.degrees(2.0 * math.acos(vector.y / self.radius))

        return self.radius * math.cos(math.radians(0.5 * central_angle))

# ----------------------------------------------------------------------------------------------------------------------
