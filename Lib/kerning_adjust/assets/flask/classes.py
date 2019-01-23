# coding=utf-8
#
import os
import sys
import plistlib
import json
import xml.etree.ElementTree as ET  
import xmltodict
from copy import deepcopy
#
import pprint
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
efo_lib_dir = os.path.abspath(os.path.join(dir_path, '../../../..')) # Lib
sys.path.insert(0, efo_lib_dir)
#
def dict_of_dicts_merge(dict1, dict2):
	#
	dict3 = deepcopy(dict1)
	#
	for key in dict1:
		#
		dict1[key].update(dict2[key])
		#
		if key in dict2:
			#
			for x in dict2[key]:
				#
				if x in dict3[key]:
					#
					dict1[key][x] = dict2[key][x] + dict3[key][x]
					#
				#
			#
		#
	return dict1
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
		tree = ET.parse(os.path.join(self._efo,"glyphlib.xml"))  
		root = tree.getroot()
		#
		#
		def get_uni_chr(_chr):
			#
			return str('\\u'+_chr).encode('utf-8').decode("unicode-escape")
			#
		#
		def get_glyphlib_info( name):
			#
			#
			for x in root:
				#
				if x.attrib['name'] == name:
					#
					uni_char = ""
					#
					if len(x.attrib["unicode"]):
						#
						uni_char = get_uni_chr(x.attrib["unicode"])
						#
					#
					return [x.attrib["glif"],name,uni_char, x.attrib["unicode"]]
					#
				#
			#
		#
		def get_glyphlib():
			#
			json_glyphlib = {}
			#
			for x in root:
				#
				uni_char = ""
				#
				if len(x.attrib["unicode"]):
					#
					uni_char = get_uni_chr(x.attrib["unicode"])
					#
				#
				json_glyphlib.update({x.attrib["name"] : [uni_char, x.attrib["glif"], x.attrib["unicode"]]})
				#
			#
			return json_glyphlib
			#
		#
		from Lib.efo import EFO
		from Lib.efo.efo_fontinfo import get_font_file_array
		from Lib.generic.generic_tools import plist_to_json
		#
		EFO = EFO(self._efo)
		#
		fontinfo_json = EFO.fontinfo
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
		return json.dumps({"get_classes":new_plist,"get_weights":get_font_file_array(EFO), "get_glyphlib": get_glyphlib() })
		#
	#
	def get_glif_width(self):
		#
		tree = ET.parse(os.path.join(self._efo,"glyphs", "reg", "A_.glif"))  
		root = tree.getroot()
		#
		width = root.findall('advance')[0].attrib["width"]
		#
		print({"get_glif_width":width})
		#
		return json.dumps({"get_glif_width":width})
		#
	def update_adjustments_json(self):
		#
		adjustments_json = os.path.join(self._efo,"kerning","adjustments.json")
		#
		def save_(save_data):
			#
			with open(adjustments_json, "w") as in_json:
				#
				json.dump(save_data, in_json, indent=4)
				#
				in_json.close()
				#
			#
		#
		exists = os.path.isfile(adjustments_json)
		#
		data_to_json = json.loads(self._data)
		#
		if exists:
			#
			with open(adjustments_json, "r") as in_json:
				#
				json_data = json.load(open(adjustments_json, 'r'))
				#
				d_save = dict_of_dicts_merge(json_data, data_to_json)
				#
				in_json.close()
				#
				save_(d_save)
				#
			#
		else:
			#
			save_(data_to_json)
			#
		#
		return json.dumps({"update_adjustments_json":data_to_json})
		#