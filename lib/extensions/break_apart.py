import logging
from copy import deepcopy

from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize, unary_union

import inkex

from ..elements import AutoFill, Fill
from ..i18n import _
from ..svg import get_correction_transform
from .base import InkstitchExtension


class BreakApart(InkstitchExtension):
    '''
    This will solve crossing border and holes lies outside shell errors for fill shapes
    and breaks them into multiple elements if necessary.
    '''
    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select one or more fill areas to break apart."))
            return

        for element in self.elements:
            if not isinstance(element, AutoFill) and not isinstance(element, Fill):
                continue

            # ignore valid elements
            logger = logging.getLogger('shapely.geos')
            level = logger.level
            logger.setLevel(logging.CRITICAL)
            valid = element.shape.is_valid
            logger.setLevel(level)
            if valid:
                continue

            multipolygons = self.break_apart_element(element)
            if multipolygons:
                self.element_to_nodes(multipolygons, element)

    def break_apart_element(self, element):
        polygons = []

        for path in element.paths:
            linestring = LineString(path)
            if not linestring.is_simple:
                linestring = unary_union(linestring)
                for polygon in polygonize(linestring):
                    polygons.append(polygon)
            else:
                polygons.append(Polygon(path))

        # sort paths by size and convert to polygons
        polygons.sort(key=lambda polygon: polygon.area, reverse=True)

        return self.recombine_polygons(polygons)

    def recombine_polygons(self, polygons):
        multipolygons = []
        holes = []

        for polygon in polygons:
            if polygon in holes:
                continue

            polygon_list = [polygon]
            for other in polygons:
                if polygon != other and polygon.contains(other) and other not in holes:
                    # dont't add to holes if "other" is inside a hole or intersects with an outer polygon
                    if any(p.contains(other) or p.intersects(other) for p in polygon_list[1:]):
                        continue
                    polygon_list.append(other)
                    holes.append(other)
            multipolygons.append(polygon_list)

        return multipolygons

    def element_to_nodes(self, multipolygons, element):
        for polygons in multipolygons:
            # ignore very small areas
            if polygons[0].area < 5:
                continue
            el = deepcopy(element)
            d = ""
            for polygon in polygons:
                # copy element and replace path
                el.node.set('id', self.uniqueId(element.node.get('id') + '_'))
                d += "M"
                for x, y in polygon.exterior.coords:
                    d += "%s,%s " % (x, y)
                    d += " "
                d += "Z"
            el.node.set('d', d)
            el.node.set('transform', get_correction_transform(element.node))
            element.node.getparent().insert(0, el.node)
        element.node.getparent().remove(element.node)
