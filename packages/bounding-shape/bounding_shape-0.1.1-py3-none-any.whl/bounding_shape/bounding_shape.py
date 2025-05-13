from dataclasses import dataclass
import math
import numpy as np
from typing import Any
from functools import cached_property
from shapely import MultiPoint, MultiPolygon, Polygon
from collections.abc import Callable
from scipy.spatial import Delaunay
from shapely.ops import unary_union
import shapely

@dataclass
class Triangle():
    coords: np.ndarray 
    "Contains an array of 3 values, each of which contains the x y coordinates of the triangle's vertices."

    @cached_property
    def area(self) -> float: 
        """Calculate the area of a triangle given its vertices using the cross-product method."""
        v0, v1, v2 = self.coords
        return 0.5 * abs( (v1[0] - v0[0]) * (v2[1] - v0[1]) 
                        - (v2[0] - v0[0]) * (v1[1] - v0[1]))

    @cached_property
    def max_length(self) -> float:
        """Gets the maximum side length."""
        return max(self.side_lengths)
    
    @cached_property
    def side_lengths(self) -> list[float]:
        """Gets the side lengths."""
        v0, v1, v2 = self.coords
        side_lengths = [
            np.linalg.norm(v0 - v1),
            np.linalg.norm(v1 - v2),
            np.linalg.norm(v2 - v0)
        ]
        return side_lengths
  
    @cached_property
    def shape(self) -> Polygon:
        return Polygon(self.coords)


@dataclass
class DelaunayResult:
    name: str
    triangles: list[Triangle]
    point_coords: list[tuple[float, float]]
    
    def filter_triangles(self, filter: Callable[[Triangle], bool]) -> list[Triangle]:
        return [t for t in self.triangles if filter(t)]
    
    @cached_property
    def max_triangle_side_length(self) -> float:
        return max([t.max_length for t in self.triangles]) 
    
    @cached_property
    def max_triangle_area(self) -> float:
        return max([t.area for t in self.triangles])
    
    @cached_property
    def all_triangle_side_lengths(self) -> list[float]:
        all_side_lengths = []
        for t in self.triangles:
            all_side_lengths.extend(t.side_lengths)
        return all_side_lengths
    
    @cached_property
    def source_points(self) -> MultiPoint:
        return MultiPoint(self.point_coords)

# Option 1

@dataclass
class APIClass: # TODO name
    """This class would perform the operations as they are needed, perhaps with caching.
    Main issue is grid spacing and buffer are likely to change frequently, so no caching"""
    dr: DelaunayResult
    pass

    def create_bounding_area(self, buffer, include_outlier_points, relative_distance_threshold):
        return _create_bounding_area(self.dr, buffer, include_outlier_points, relative_distance_threshold)
    
    def create_spaced_points():
        pass

# Option 2 

class APIReponseClass: # TODO name
    """This class would get the result and hold on to the inputs.
    Could subclass multipoint/polygon to make changes without breaking APIs"""
    points: MultiPoint
    buffer: float
    distance: float
    include_outlier_points: bool
    relative_distance_threshold: float

    grid: MultiPoint
    shape: Polygon

    # TODO consider resuing polygon when changing grid spacing 
    # TODO frozen object? Or mutate when grid changes (if going that route) ?

# Option 3 
# NB with this option: Buffers must be consistent with Polygon and Grid

class LibraryDelaneyResult:
    """Could return the DR class as another method potentially, allowing for user-defined
    custom filtering? """
    # TODO just two below

class PolygonResult:
    polygon: Polygon 
    """Returned instead of Shapely.Polygon after calling `create_bounding_area`"""


class GridResult:
    grid: MultiPoint
    """Returned instead of Shapely.Multipoint after calling `create_spaced_points`"""





def create_bounding_area(points: MultiPoint, 
                         buffer: float|None = None,
                         include_outlier_points: bool = True,
                         relative_distance_threshold: float = 1.5) -> Polygon:
    """
    Creates an area around the input points. The area may exclude some points if they are far away from other points
    
    Returns a Shapely Polygon bounding around all of the points (except outlier points if not requested)
    
    Parameters
    ----------
        points : Multipoint
                 The shapely Multipoint containing the points to create an area around.
        buffer : float|None
                 The distance to buffer around the generated shape. 
                 If None, buffers by the lower quartile distance between the triangluated points.
        include_outlier_points : bool
                                 If true, then the shape generated will also include shapes around 
                                 points that are isolated, i.e. outside groups of nearby points.
        relative_distance_threshold : float
                                      The distance at which to cull triangles from the area. 
                                      Higher values will generate a larger, more loosely fitting 
                                      shape(s) whilst lower values will create smaller,
                                      more tightly fitting shape(s) with a higher likelihood of separate shapes.
    
    Returns
    ----------
    Returns a Shapely Polygon bounding around all of the points (except outlier points if not requested).
    The polygon that is returned may be made up of more than one shape internally, however it will be returned
    as a Shapely Polygon regareless of the number of distinct shapes.
    """
    
    dr = _calculate_delaunay_result(points)

    buffer = buffer if buffer is not None else _get_default_buffer(side_lengths=dr.all_triangle_side_lengths)

    area = _create_bounding_area(dr=dr, buffer=buffer,
                                 include_outlier_points=include_outlier_points, 
                                 relative_distance_threshold=relative_distance_threshold)
    
    return area
 

# Remove method, method will be on PolygonResult
def create_spaced_points(points: MultiPoint,
                          grid_spacing: float|None = None,
                          buffer: float|None = None,
                          include_outlier_points: bool = True,
                          relative_distance_threshold: float = 1.5) -> MultiPoint:
    """
    Creates a grid of points around the points given. 

    Returns a Shapely Multipoint containing points that fill the area returned by create_bounding_area
    
    Parameters
    ----------
    points : Multipoint
             The shapely Multipoint containing the points to create an area around.
    grid_spacing : float|None 
                   The distance between points on the grid. If None a default will be picked 
                   based on the magnitude of the range of the points.
    buffer : float|None
             The distance to buffer around the generated shape. 
             If None, buffers by the lower quartile distance between the triangluated points.
    include_outlier_points : bool
                             If true, then the shape generated will also include shapes around 
                             points that are isolated, i.e. outside groups of nearby points.
    relative_distance_threshold : float
                                  The distance at which to cull triangles from the area. 
                                  Higher values will generate a larger, more loosely fitting 
                                  shape(s) whilst lower values will create smaller,
                                  more tightly fitting shape(s) with a higher likelihood of separate shapes.
    
    Returns
    -------
    Returns a Shapely Multipoint containing points that fill the area returned by create_bounding_area.
    The grid of points that is created is the intersection of a rectangular grid of points and the bounding shape
    created by create_bounding_area.
    """
    
    x, y = zip(*[(p.x, p.y) for p in points.geoms])

    dr = _calculate_delaunay_result(points)
    
    buffer = buffer if buffer is not None else _get_default_buffer(side_lengths=dr.all_triangle_side_lengths)

    grid_spacing = grid_spacing if grid_spacing is not None else get_grid_spacing_for_points(points=points)

    area = _create_bounding_area(dr=dr, 
                                 buffer=buffer,
                                 include_outlier_points=include_outlier_points,
                                 relative_distance_threshold=relative_distance_threshold)
    
    multipoint = _create_grid_of_points(x=x, y=y, 
                                       distance=grid_spacing,
                                       buffer=buffer)
    
    masked_points = multipoint.intersection(area)

    return masked_points


def get_grid_spacing_for_points(points: MultiPoint, magnitude: int | None = None) -> float:
    """
    Calculated the grid spacing for a given set of points. This method is designed to allow the calculation
    of a default value for the `grid_spacing` parameter of `create_spaced_points` to be done outside of the 
    `create_spaced_points` method so the value can be used elsewhere. 

    Returns the grid spacing.
    
    Parameters
    ----------
    points : Multipoint
             The shapely Multipoint containing the points to calculate the grid spacing for
    magnitude : int|None 
                Represents how many points there should be alongside the extents of the points
                . Default: 100

    Returns
    -------
    The grid spacing for the given magnitude, which is the default value calculated in `grid_spacing`.
    """
    if magnitude is None:
        magnitude = 100

    assert magnitude is not None

    x_coords = [p.x for p in points.geoms]
    y_coords = [p.y for p in points.geoms]

    minx = min(x_coords)
    maxx = max(x_coords)
    miny = min(y_coords)
    maxy = max(y_coords)

    width = abs(minx - maxx)
    height = abs(miny - maxy)

    largest_extent = max(width, height)

    grid_spacing = largest_extent / magnitude 

    return grid_spacing


def _get_default_buffer(side_lengths: list[float]) -> float:
    return np.percentile(side_lengths, 25)


def _create_grid_of_points(x,y, buffer: float, distance: float):
    # Create bounding box of coordinates to predict in
    minx = min(x)
    maxx = max(x)
    miny = min(y)
    maxy = max(y)

    # construct rectangle of points to predict over 
    x_coords = list(np.arange(minx - buffer + distance / 2, maxx + buffer - distance / 2, distance))
    y_coords = list(np.arange(miny - buffer + distance / 2, maxy + buffer - distance / 2, distance))
    
    # If distance > range then coords list will be empty, set coords to middle of range
    x_coords = x_coords if x_coords != [] else [minx + (maxx - minx) / 2] 
    y_coords = y_coords if y_coords != [] else [miny + (maxy - miny) / 2] 

    x, y = np.meshgrid(x_coords, y_coords)
                                
    return MultiPoint(list(zip(x.flatten(),y.flatten())))


def _create_bounding_area(dr: DelaunayResult,
                         buffer: float,
                         include_outlier_points: bool,
                         relative_distance_threshold: float):
    
    upper_threshold = _get_upper_outlier_threshold(dr.all_triangle_side_lengths, relative_distance_threshold=relative_distance_threshold)
    
    included_triangles = dr.filter_triangles(lambda t: t.max_length <= upper_threshold)
    triangluated_area = MultiPolygon([t.shape for t in included_triangles])
    bounding_area = unary_union(triangluated_area)
    
    if include_outlier_points:
        outlier_points = shapely.difference(dr.source_points, bounding_area)
        bounding_area = unary_union([outlier_points, bounding_area])
    
    return bounding_area.buffer(buffer)


def _calculate_delaunay_result(points: MultiPoint, name: str = "") -> DelaunayResult:
    point_coords = [(p.x, p.y) for p in points.geoms]

    delaunay = Delaunay(point_coords)
    triangles: list[Triangle] = []

    for simplex in delaunay.simplices:
        # 'simplex' is a list of indices. Use it to index the points array:
        coords = delaunay.points[simplex]
        triangles.append(Triangle(coords=coords))
        
    return DelaunayResult(name=name, triangles=triangles, point_coords=point_coords)


def _get_upper_outlier_threshold(values: list[float], relative_distance_threshold: float):
    # Type is actually np array
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1
    upper_threshold = Q3 + relative_distance_threshold * IQR

    return upper_threshold

