#
#!/usr/bin/env python
import os
import json
from json import JSONEncoder
import copy
import re
import xml.etree.cElementTree as ET
#
from collections import OrderedDict
import math
import plistlib
#
from argparse import ArgumentParser
#
from pprint import pprint
#
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../..')))
#
print(abspath(join(dirname(__file__), '../..')))
#
from Lib.efo.efo_fontinfo import read_efo_json_fontinfo
from Lib.efo.efo_fontinfo import get_font_file_array
from Lib.efo import EFO

'''
Prerequisites:
	Have an Upright kerned font with the width of the glyph is exactly as the width of the countours.
	Have a Slanted font with the width of glyph is exactly as the width of the countours.
	Know the slant value in deg
'''
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
					help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
					help="UFO Fonts to get kerning")
parser.add_argument("-t", "--target_fonts", dest="target_fonts", 
					help="UFO Fonts to apply altered kerning")
parser.add_argument("-d", "--deg", dest="deg", 
					help="Slant Degrees")
#
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
def shear_kerning(height, slant_deg, Ko, L, Ln, R, Rn):
	#
	xs = math.sin(slant_deg*math.pi/180) * height
	xl = xs * 2
	d = (L - xs) + Ko
	b = xs + d + abs(Ko)
	g = xl + d
	calc = ((g-b)-(Rn-R)) - ((g-b)-(Ln-L))
	# if orig_kern < 0:
	# 	#
	# 	x= math.sin(slant_deg*math.pi/180) * height
	# 	u = ( x + abs(orig_kern) ) / 2
	# 	#
	# 	calc = int(u - abs(R - Rn) + abs(L - Ln))
	# 	#
	# 	print("+")
	# 	#
	# else:
	# 	#
	# 	print("-") 
	# 	#
	# 	calc = -int(abs(abs(R - Rn) - abs(L - Ln)))
	# 	#
	return int(calc)
	#
# (int(args.deg), args.fonts, args.target_fonts)
#
def get_glif_file_name(xmlTree, glif_name):
	#
	for elem in xmlTree.iter():
		#
		if elem.tag == "glyph":
			#
			if elem.attrib.get("name") == glif_name:
				#
				return elem.attrib.get("glif")+'.glif'
				#
			#
		#
	#
#
def get_glif_width(_in, tree, name, font):
	#
	in_glif_filename = os.path.join(_in,"glyphs",font,get_glif_file_name(tree, name))
	in_glif_file = ET.parse(in_glif_filename)
	return int(in_glif_file.findall('advance')[0].get('width'))
	#
#
def do_kerning_alterations(EFO, deg, in_fonts, targ_fonts):
	#
	'''
	open flat kerning for in_fonts
		get fontinfo capHeight
		for each pair get pair widths
			run shear_kerning(height, slant_deg, orig_kern, L, Ln, R, Rn)
	'''
	#
	read_efo_json_fontinfo(EFO, "Downstream")
	fonts = get_font_file_array(EFO)
	#
	cap_height = EFO.fontinfo[0]["shared_info"]["capHeight"]
	source_glyphflib = os.path.join(EFO._in,"glyphlib.xml")
	glyphlib = ET.parse(source_glyphflib)
	#
	for s_f in fonts:
		#
		if s_f in in_fonts:
			#
			in_flat_kerning = os.path.join(EFO._in,"kerning","flat",s_f+'.plist')
			s_p_f = plistlib.readPlist(in_flat_kerning)
			#
			for t_f in targ_fonts.split(','):
				#
				if t_f in targ_fonts:
					#
					targ_flat_kerning = os.path.join(EFO._in,"kerning","flat",t_f+'.plist')
					t_p_f = plistlib.readPlist(targ_flat_kerning)
					#
					for x in s_p_f:
						#
						for y in s_p_f[x]:
							#
							res_kern = s_p_f[x][y]
							#
							res_L = get_glif_width(EFO._in, glyphlib, x, s_f) # source_font_L_width
							res_Ln = get_glif_width(EFO._in, glyphlib, x, t_f) # target_font_L_width
							#
							res_R = get_glif_width(EFO._in, glyphlib, y, s_f) # source_font_R_width
							res_Rn = get_glif_width(EFO._in, glyphlib, y, t_f) # target_font_R_width
							#
							new_kern_val =shear_kerning(cap_height, deg, res_kern, res_L, res_Ln, res_R, res_Rn)
							#
							t_p_f[x][y] = new_kern_val
							#
							print(res_kern, new_kern_val)
							#
						#
					#
					plistlib.writePlist(t_p_f, targ_flat_kerning)
					#
				#
			#
		#
	#
#
faults = False
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source EFO File: -s "/font.efo"\n=')	
	#
if  args.fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to Shift Anchor Offsets: -f "thn,reg,bld"\n=')	
	#
#
if  args.target_fonts is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Fonts to apply altered kerning: -t "thn,reg,bld"\n=')	
	#
#
if  args.deg is None:
	#
	faults = True
	#
	print('=\n=> Please Provide the Slant Degrees: -d "12"\n=')	
	#
#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	do_kerning_alterations(EFO, int(args.deg), args.fonts, args.target_fonts)
	#
#
