# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
from pathlib import Path

import inkex
from inkex import errormsg

from ..commands import ensure_symbol
from ..i18n import _
from ..stitch_plan import generate_stitch_plan
from ..svg import get_correction_transform
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL
from .base import InkstitchExtension


class LettersToFont(InkstitchExtension):
    '''
    This extension will create a json file to store a custom directory path for additional user fonts
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-d", "--font-dir", type=str, default="", dest="font_dir")
        self.arg_parser.add_argument("-f", "--file-format", type=str, default="", dest="file_format")

    def effect(self):
        font_dir = self.options.font_dir
        file_format = self.options.file_format

        if not os.path.isdir(font_dir):
            errormsg(_("Font directory not found. Please specify an existing directory."))

        glyphs = list(Path(font_dir).rglob(file_format))
        if not glyphs:
            glyphs = list(Path(font_dir).rglob(file_format.lower()))

        document = self.document.getroot()
        for glyph in glyphs:
            letter = self.get_glyph_element(glyph)
            label = "GlyphLayer-%s" % letter.get(INKSCAPE_LABEL, ' ').split('.')[0][-1]

            group = inkex.Group(attrib={
                INKSCAPE_LABEL: label,
                INKSCAPE_GROUPMODE: "layer",
                "transform": get_correction_transform(document, child=True)
            })
            group.insert(0, letter[-1])
            document.insert(0, group)
            group.set('style', 'display:none')

        # users may be confused if they get an empty document
        # make last letter visible again
        group.set('style', None)

        # In most cases trims are inserted with the imported letters.
        # Let's make sure the trim symbol exists in the defs section
        ensure_symbol(document, 'trim')

        self.insert_baseline(document)

    def get_glyph_element(self, glyph):
        stitch_plan = generate_stitch_plan(str(glyph))
        # we received a stitch plan wrapped in an svg document, we only need the last group
        stitch_plan = stitch_plan.getchildren()
        return stitch_plan[-1]

    def insert_baseline(self, document):
        document.namedview.new_guide(position=0.0, name="baseline")
