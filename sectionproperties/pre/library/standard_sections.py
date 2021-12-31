import numpy as np
from shapely.geometry import Polygon
from sectionproperties.pre.geometry import Geometry
import sectionproperties.pre.pre as pre
from sectionproperties.pre.library.utils import draw_radius


def rectangular_section(
    b, d, material: pre.Material = pre.DEFAULT_MATERIAL
) -> Geometry:
    """Constructs a rectangular section with the bottom left corner at the origin *(0, 0)*, with
    depth *d* and width *b*.

    :param float d: Depth (y) of the rectangle
    :param float b: Width (x) of the rectangle
    :param Optional[sectionproperties.pre.pre.Material]: Material to associate with this geometry

    The following example creates a rectangular cross-section with a depth of 100 and width of 50,
    and generates a mesh with a maximum triangular area of 5::

        from sectionproperties.pre.library.standard_sections import rectangular_section

        geometry = rectangular_section(d=100, b=50)
        geometry.create_mesh(mesh_sizes=[5])

    ..  figure:: ../images/sections/rectangle_geometry.png
        :align: center
        :scale: 75 %

        Rectangular section geometry.

    ..  figure:: ../images/sections/rectangle_mesh.png
        :align: center
        :scale: 75 %

        Mesh generated from the above geometry.
    """
    points = [[0, 0], [b, 0], [b, d], [0, d]]
    rectangle = Polygon(points)
    return Geometry(rectangle, material)


def circular_section(
    d: float, n: int, material: pre.Material = pre.DEFAULT_MATERIAL
) -> Geometry:
    """Constructs a solid circle centered at the origin *(0, 0)* with diameter *d* and using *n*
    points to construct the circle.

    :param float d: Diameter of the circle
    :param int n: Number of points discretising the circle
    :param Optional[sectionproperties.pre.pre.Material]: Material to associate with this geometry

    The following example creates a circular geometry with a diameter of 50 with 64 points,
    and generates a mesh with a maximum triangular area of 2.5::

        from sectionproperties.pre.library.standard_sections import circular_section

        geometry = circular_section(d=50, n=64)
        geometry.create_mesh(mesh_sizes=[2.5])

    ..  figure:: ../images/sections/circle_geometry.png
        :align: center
        :scale: 75 %

        Circular section geometry.

    ..  figure:: ../images/sections/circle_mesh.png
        :align: center
        :scale: 75 %

        Mesh generated from the above geometry.
    """
    x_off, y_off = (0, 0)
    points = []
    # loop through each point on the circle
    for i in range(n):
        # determine polar angle
        theta = i * 2 * np.pi * 1.0 / n

        # calculate location of the point
        x = 0.5 * d * np.cos(theta) + x_off
        y = 0.5 * d * np.sin(theta) + y_off

        # append the current point to the points list
        points.append([x, y])

    circle = Polygon(points)
    return Geometry(circle, material)


def elliptical_section(
    d_y: float, d_x: float, n: int, material: pre.Material = pre.DEFAULT_MATERIAL
) -> Geometry:
    """Constructs a solid ellipse centered at the origin *(0, 0)* with vertical diameter *d_y* and
    horizontal diameter *d_x*, using *n* points to construct the ellipse.

    :param float d_y: Diameter of the ellipse in the y-dimension
    :param float d_x: Diameter of the ellipse in the x-dimension
    :param int n: Number of points discretising the ellipse
    :param Optional[sectionproperties.pre.pre.Material]: Material to associate with this geometry

    The following example creates an elliptical cross-section with a vertical diameter of 25 and
    horizontal diameter of 50, with 40 points, and generates a mesh with a maximum triangular area
    of 1.0::

        from sectionproperties.pre.library.standard_sections import elliptical_section

        geometry = elliptical_section(d_y=25, d_x=50, n=40)
        geometry.create_mesh(mesh_sizes=[1.0])

    ..  figure:: ../images/sections/ellipse_geometry.png
        :align: center
        :scale: 75 %

        Elliptical section geometry.

    ..  figure:: ../images/sections/ellipse_mesh.png
        :align: center
        :scale: 75 %

        Mesh generated from the above geometry.
    """
    points = []

    # loop through each point on the ellipse
    for i in range(n):
        # determine polar angle
        theta = i * 2 * np.pi * 1.0 / n

        # calculate location of the point
        x = 0.5 * d_x * np.cos(theta)
        y = 0.5 * d_y * np.sin(theta)

        # append the current point to the points list
        points.append([x, y])

    ellipse = Polygon(points)
    return Geometry(ellipse, material)


def cruciform_section(
    d, b, t, r, n_r, material: pre.Material = pre.DEFAULT_MATERIAL
) -> Geometry:
    """Constructs a cruciform section centered at the origin *(0, 0)*, with depth *d*, width *b*,
    thickness *t* and root radius *r*, using *n_r* points to construct the root radius.

    :param float d: Depth of the cruciform section
    :param float b: Width of the cruciform section
    :param float t: Thickness of the cruciform section
    :param float r: Root radius of the cruciform section
    :param Optional[sectionproperties.pre.pre.Material]: Material to associate with this geometry

    The following example creates a cruciform section with a depth of 250, a width of 175, a
    thickness of 12 and a root radius of 16, using 16 points to discretise the radius. A mesh is
    generated with a maximum triangular area of 5.0::

        from sectionproperties.pre.library.standard_sections import cruciform_section

        geometry = cruciform_section(d=250, b=175, t=12, r=16, n_r=16)
        geometry.create_mesh(mesh_sizes=[5.0])

    ..  figure:: ../images/sections/cruciform_geometry.png
        :align: center
        :scale: 75 %

        Cruciform section geometry.

    ..  figure:: ../images/sections/cruciform_mesh.png
        :align: center
        :scale: 75 %
    """
    points = []

    # add first two points
    points.append([-t * 0.5, -d * 0.5])
    points.append([t * 0.5, -d * 0.5])

    # construct the bottom right radius
    pt = [0.5 * t + r, -0.5 * t - r]
    points += draw_radius(pt, r, np.pi, n_r, False)

    # add the next two points
    points.append([0.5 * b, -t * 0.5])
    points.append([0.5 * b, t * 0.5])

    # construct the top right radius
    pt = [0.5 * t + r, 0.5 * t + r]
    points += draw_radius(pt, r, 1.5 * np.pi, n_r, False)

    # add the next two points
    points.append([t * 0.5, 0.5 * d])
    points.append([-t * 0.5, 0.5 * d])

    # construct the top left radius
    pt = [-0.5 * t - r, 0.5 * t + r]
    points += draw_radius(pt, r, 0, n_r, False)

    # add the next two points
    points.append([-0.5 * b, t * 0.5])
    points.append([-0.5 * b, -t * 0.5])

    # construct the bottom left radius
    pt = [-0.5 * t - r, -0.5 * t - r]
    points += draw_radius(pt, r, 0.5 * np.pi, n_r, False)

    polygon = Polygon(points)
    return Geometry(polygon, material)
