# coding=utf-8
#
import os
import sys
import plistlib
import json
import xml.etree.ElementTree as ET  
#
import pprint
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
efo_lib_dir = os.path.abspath(os.path.join(dir_path, '../../../..')) # Lib
sys.path.insert(0, efo_lib_dir)
#
#
class kern_adjust:
	#
	def __init__(self):
		#
		print("initiated")
		#
	def get_classes(self):
		#
		def get_glyphlib_info( name):
			#
			tree = ET.parse(os.path.join(self._efo,"glyphlib.xml"))  
			root = tree.getroot()
			#
			for x in root:
				#
				if x.attrib['name'] == name:
					#
					uni_char = ""
					#
					if len(x.attrib["unicode"]):
						#
						uni_char = str('\\u'+x.attrib["unicode"]).encode('utf-8').decode("unicode-escape")#.decode("hex")
						#
					#
					return [x.attrib["glif"],name,uni_char, x.attrib["unicode"]]
					#
				#
			#
		#
		from Lib.efo import EFO
		from Lib.efo.efo_fontinfo import get_font_file_array
		from Lib.generic.generic_tools import plist_to_json
		#
		EFO = EFO(self._efo)
		#
		fontinfo_json = EFO.fontinfo
		#pprint.pprint()
		#
		kerning_plist = plist_to_json(os.path.join(self._efo,"groups","kerning.plist"))
		#
		new_plist = {}
		#
		for k, v in kerning_plist.items():
			#
			new_v = []
			#
			for y in v:
				#
				new_v.append( get_glyphlib_info(y) )
				#
			#
			new_plist[k] = new_v
			#
		#
		return json.dumps({"get_classes":new_plist,"get_weights":get_font_file_array(EFO)})
		#
	#
	def get_glif_width(self):
		#
		print({"get_glif_width":545})
		#
		return json.dumps({"get_glif_width":545})
		#
		