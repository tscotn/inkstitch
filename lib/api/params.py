from flask import Blueprint, Response, g, jsonify

from ..commands import is_command
from ..elements import EmbroideryElement
from ..elements.clone import is_clone
from ..svg import thumbnail
from ..svg.tags import SVG_POLYLINE_TAG

params = Blueprint('params', __name__)


@params.route('/objects')
def get_objects():
    objects = []

    for node in g.extension.nodes:
        objects.append({"node_id": node.get('id'),
                        "name": node.get('name') or node.get('id')})

    return jsonify(objects)


@params.route('/object-types/<node_id>')
def get_object_types(node_id):
    node = g.extension.getElementById(node_id)
    element = EmbroideryElement(node)

    object_types = {}

    if not is_command(node):
        if node.tag == SVG_POLYLINE_TAG:
            object_types['polyline'] = True
        elif is_clone(node):
            object_types['clone'] = True
        else:
            if element.get_style("fill", 'black') and not element.get_style("fill-opacity", 1) == "0":
                object_types['fill'] = True
            if element.get_style("stroke") is not None:
                object_types['stroke'] = True

    return jsonify(object_types)


@params.route('/thumbnail/<node_id>')
def get_thumbnail(node_id):
    node = g.extension.getElementById(node_id)
    png_data = thumbnail(node)

    if png_data is None:
        return Response(status=500)
    else:
        return Response(png_data, mimetype="image/png")
