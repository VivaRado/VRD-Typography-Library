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
from Lib.components import comp_tools

from Lib.efo import EFO

from Lib.generic import generic_tools

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
# #
# def shear_kerning(height, slant_deg, Ko, L, Ln, R, Rn):
# 	#
# 	xs = math.sin(slant_deg*math.pi/180) * height
# 	xl = xs * 2
# 	d = (L - xs) + Ko
# 	b = xs + d + abs(Ko)
# 	g = xl + d
# 	calc = ((g-b)-(Rn-R)) - ((g-b)-(Ln-L))
# 	# if orig_kern < 0:
# 	# 	#
# 	# 	x= math.sin(slant_deg*math.pi/180) * height
# 	# 	u = ( x + abs(orig_kern) ) / 2
# 	# 	#
# 	# 	calc = int(u - abs(R - Rn) + abs(L - Ln))
# 	# 	#
# 	# 	print("+")
# 	# 	#
# 	# else:
# 	# 	#
# 	# 	print("-") 
# 	# 	#
# 	# 	calc = -int(abs(abs(R - Rn) - abs(L - Ln)))
# 	# 	#
# 	return int(calc)
# 	#
# # (int(args.deg), args.fonts, args.target_fonts)
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
transfer_dict = {"orig":{},"dest":{}}
#
def get_glif_top_point(_in, tree, cap_height, name, font):
	#
	in_glif_filename = os.path.join(_in,"glyphs",get_glif_file_name(tree, name))
	#
	in_glif_file = ET.parse(in_glif_filename)
	#
	nums = []
	#
	for _o in in_glif_file.findall('outline'):
		#
		for _c in _o.findall('contour')[0]:
			#
			nums.append([int(_c.get('y')), int(_c.get('x'))])
			#
		#
	#
	
	#
	if name not in transfer_dict["orig"]:
		#
		transfer_dict["orig"][name] = {"data": min(nums, key=lambda x: cap_height - x[0])}
		#
	#
	#for g in in_glif_file.findall('advance')
	#
	#return int(in_glif_file.findall('advance')[0].get('width'))
	#
#
def split_input (inp):
	#
	if "," in inp:
		#
		inp = inp.split(',')
		#
	else:
		#
		inp = [inp]
		#
	#
	return inp
	#
#
def do_kerning_alterations(EFO, deg, in_fonts, targ_fonts):
	#
	'''
	open flat kerning for in_fonts
		get fontinfo capHeight
		for each pair get pair widths
			find highest point location, move kerning by the diff
	'''
	#
	read_efo_json_fontinfo(EFO, "Downstream")
	fonts = get_font_file_array(EFO)
	#
	cap_height = EFO.fontinfo[0]["shared_info"]["capHeight"]
	source_glyphflib = os.path.join(EFO._in,"glyphlib.xml")
	glyphlib = ET.parse(source_glyphflib)
	#
	in_fonts = split_input(in_fonts)
	targ_fonts = split_input(targ_fonts)
	#
	EFO._efo_to_ufos(','.join(in_fonts+targ_fonts), False, "class")
	#
	for z in in_fonts+targ_fonts:
		#
		instance_name = generic_tools.sanitize_string(EFO.current_font_family_name+' '+z)
		instance_directory = os.path.join(EFO.current_font_family_directory, instance_name+'.ufo')
		#
		comp_tools.flatten_components(instance_directory)
		#
	#
	#
	for s_f in fonts:
		#
		if s_f in in_fonts:
			#
			#
			#
			in_flat_kerning = os.path.join(EFO._in,"kerning","flat",s_f+'.plist')
			s_p_f = plistlib.readPlist(in_flat_kerning)
			#
			for t_f in targ_fonts:
				#
				if t_f in targ_fonts:
					#
					for x in s_p_f:
						#
						i_n = generic_tools.sanitize_string(EFO.current_font_family_name+' '+s_f)
						i_n_dir = os.path.join(EFO.current_font_family_directory, i_n+'.ufo')
						#res_L = get_glif_width(EFO._in, glyphlib, x, s_f) # source_font_L_width
						#res_Ln = get_glif_width(EFO._in, glyphlib, x, t_f) # target_font_L_width
						#
						res_L = get_glif_top_point(i_n_dir, glyphlib, cap_height, x, s_f) # source_font_L_width
			#
			for t_f in targ_fonts:
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
							i_n = generic_tools.sanitize_string(EFO.current_font_family_name+' '+s_f)
							i_n_dir = os.path.join(EFO.current_font_family_directory, i_n+'.ufo')
							#res_L = get_glif_width(EFO._in, glyphlib, x, s_f) # source_font_L_width
							#res_Ln = get_glif_width(EFO._in, glyphlib, x, t_f) # target_font_L_width
							#
							#res_L = get_glif_top_point(i_n_dir, glyphlib, cap_height, x, s_f) # source_font_L_width
							#
							#res_Ln = get_glif_top_point(current_font_instance_directory, glyphlib, cap_height, x, t_f) # target_font_L_width
							#
							#res_R = get_glif_width(EFO._in, glyphlib, y, s_f) # source_font_R_width
							#res_Rn = get_glif_width(EFO._in, glyphlib, y, t_f) # target_font_R_width
							#
							#new_kern_val = shear_kerning(cap_height, deg, res_kern, res_L, res_Ln, res_R, res_Rn)
							#
							#t_p_f[x][y] = new_kern_val
							#
							#print(res_kern, new_kern_val)
							#
						#
					#
					#plistlib.writePlist(t_p_f, targ_flat_kerning)
					#
				#
			#
		#
	#
	print(transfer_dict["orig"])
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
