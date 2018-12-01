# from __future__ import absolute_import
# from fontTools.misc.py23 import *
# import gzip
# import tempfile
# from xml.etree.ElementTree import ElementTree, Element
#
import os
import sys
from os.path import dirname, join, abspath
#
#
#sys.path.insert(0, abspath(join(dirname("generic"), '..')))
#
from Lib.generic import generic_tools
from Lib.efo import efo_fontinfo
#
from .comp_ufo import run_ufo_glyphs
#
#REMOVE
from pprint import pprint
#
import ufoLib
# from .glyphs import writeMissingGlyph, writeGlyphPath
# from .kerning import writeHKernElements
# from .tools import valueToString
#
#
class COMPS(object):
	#
	read_efo_json_fontinfo = ""
	#
	def __init__(self, _in, _ufo_dst):
		#
		self._in = _in
		self._ufo_dst = _ufo_dst
		#
		#self._fonts = _fonts
		#
		self.EFO_fontinfo = "fontinfo.json"
		self.EFO_features_dir = "features"
		self.EFO_groups_dir = "groups"
		self.EFO_kerning_dir = "kerning"
		self.EFO_glyphs_dir = "glyphs"
		self.EFO_temp = "temp"
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		# if _fonts != '':
		# 	#
		# 	self._fonts = _fonts
		# 	#
		# 	if "," in self._fonts:
		# 		#
		# 		self.font_files = self._fonts.split(',')
		# 		#
		# 	else:
		# 		#
		# 		self.font_files = [self._fonts]
		# 		#
		# 	#
		# 	faults = generic_tools.check_given_fonts_exist(_fonts, self.font_files)
		# 	#_font_files = self.font_files

		# else:

		# 	faults = False
		# 	#_font_files = self.font_files
		# #
		# if faults == False:
		# 	#
		# 	print('\tCOMPONENTIZING: ',self.font_files)
		# 	#
	#
	#
	def ufos_comp(self):
		#
		print(self._ufo_dst)
		#
		for ff in self._ufo_dst:
			#
			for k, v in ff.items():
				#
				print(v)
				#
				ufo_src_path = v
				#
				comp_class_file = os.path.join(*(self._in,self.EFO_groups_dir,"components.plist"))#input("components class group plist file: ")
				#
				run_ufo_glyphs(comp_class_file, ufo_src_path)
				#
				