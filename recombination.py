'''
Get a few basic letters and distribute the shapes to create all other shared letters in Latin, Greek and Cyrillic

Current state testing on Capital letters

Capital Set

C01 Π ['Π' '03A0' 'Pi']
C02 Ε ['Ε' '0395' 'Epsilon']
C03 Λ ['Λ' '039B' 'Lambda']
C04 Μ ['Μ' '039C' 'Mu']
C05 Ο ['Ο' '039F' 'Omicron']
C06 Β ['Β' '0392' 'Beta']
C07 Л ['Л' '041B' 'Elcyrillic']
C08 J ['J' '004a' 'Jay']
C09 S ['S' '0053' 'Es']
C10 З ['З' '0417' 'Zecyrillic']
C11 Ч ['Ч' '0427' 'Checyrillic']

Assuming there will be a list of commands that take an initial vector shape transform and place it into a UFO structure

likely using simple_path.py

flip_path = formatPath(flipPath(parsePath(rev_path), horizontal=True, vertical=False))

REQ/INIT_UFO: Get an initial UFO
REQ/COMMANDS: Using a list of commands per preset glyph iterate
	prepare glif
	get SVG data from UFO glif
	apply transforms to SVG via formatPath
	convert new SVG into UFO glif
	add into new UFO font

To create recombination we store the result and then point to that result in the subsequent instructions.

'''

tdir = "Test/temp_b/"


#!/usr/bin/env python
import os
from Lib.ufo2svg import UFO2SVG
from Lib.ufo2svg.glif2svg import convertUFOToSVGFiles
from fontParts.world import *
from Lib.ufo2svg.simple_path import *
from Lib.ufo2svg.svg2glif import *
import numpy as np

from Lib.helpers.svgpath2mpl import parse_path as mpl_parse_path

from svg.path import parse_path


import matplotlib.pyplot as plt



from Lib.generic.generic_tools import dotdict

from ufoLib.filenames import userNameToFileName

import pprint

import xml.etree.ElementTree as ET

import copy
import re

class Recomb(object):
	def __init__(self):
		
		dir_path = os.path.dirname(os.path.realpath(__file__))
		_s = os.path.join(dir_path, "Test", "advent_pro_fmm")
		_t = os.path.join(dir_path, "Test", "temp_a")
		
		self.current_font_instance_vectors_directory = os.path.join(_s, _t)
		self.current_font_instance_name = "advent_pro_fmm_bld.ufo"
		self.current_font_instance_temp_directory = _t

		f = OpenFont(os.path.join(_s,self.current_font_instance_name))

		convertUFOToSVGFiles(self, f, self.current_font_instance_name)


#rc = Recomb()

'''
Dummy functions will alter to:


FIRST ORDER
	Exact Copy
	Mirror (Hrz, Vrt)

SECOND ORDER
	Partial Addition/Removal
	Mirror (Hrz, Vrt)

THIRD ORDER
	MINOR ALTERATION
		ELONGATION
	COMBINATION


And possible custom functions that go into more detail.

'''

ET.register_namespace("","http://www.w3.org/2000/svg")

def f7(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]
	
def path_to_coord(d):

	# parsed = parse_path(d)
	# print('Objects:\n', parsed, '\n' + '-' * 20)
	# for obj in parsed:
	# 	print(type(obj).__name__, ', start/end coords:', ((round(obj.start.real, 3), round(obj.start.imag, 3)), (round(obj.end.real, 3), round(obj.end.imag, 3))))
	# print('-' * 20)
	
	_path = mpl_parse_path(d)

	print(_path)

	crd_mpl_vrt = _path.__dict__['_vertices'].tolist()
	crd_mpl_cds = _path.__dict__['_codes'].tolist()


	#Z = [x for _,x in sorted(zip(Y,X))]
	print("VRT===")
	print(crd_mpl_vrt)
	print("CDS===")
	print(crd_mpl_cds)

	Z = [x for _,x in sorted(zip(crd_mpl_cds,crd_mpl_vrt))]

	#print(Z)

	unique_data = [list(x) for x in set(tuple(x) for x in Z)]

	print("RESTULS", Z)

	return unique_data
	
	# split_by_letters = re.findall('[A-Z|a-z][^A-Z|a-z]*', d)
	# split_as_you_want = []
	# for x in split_by_letters:
	# 	nums = x[1:].replace(',',' ').split()  # list of numbers after letter
	# 	for k in range(len(nums) // 2):
	# 		split_as_you_want.append([x[0]] +  [nums[k]] + [nums[k+1]])
	
	# print(d)
	# return split_as_you_want


def parse_svg_path(svg_dir):
	#
	print("PARSE PATH", svg_dir)
	#
	glyphName = svg_dir.split("/")[-1]
	svg_file = os.path.join(svg_dir+'.svg')
	#
	tree = ET.parse(svg_file)
	#
	svg_data = tree.getroot()
	#
	if 'd' in svg_data[0].attrib:
		#
		path_d = svg_data[0].attrib['d']
		#
		if len(path_d) > 1:
			#
			return tree, svg_data
			#
			

def save_svg_file(svg_dir, newname, tree):
	#
	ET.indent(tree)
	#
	new_file = os.path.join("/".join(svg_dir.split("/")[:-1]+[newname]))
	#
	tree.write(new_file+'.svg', xml_declaration=True, encoding='utf-8')
	#

def func1(l,nam, uni,x=False):
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	# transforming / CHANGING
	#

	#
	# saving / SAME
	glifnam = userNameToFileName(nam)

	save_svg_file(l,glifnam,tree)
	#
	return glifnam

def func2(l,nam, uni=False,ax=False):
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	print(l, nam, ax, userNameToFileName(nam))
	#
	glifnam = userNameToFileName(nam)
	# transforming / CHANGING
	#
	svg_data.attrib['glyph'] = make_id(svg_data.attrib['glyph'], nam, uni)
	#
	# saving / SAME
	save_svg_file(l,glifnam,tree)
	#
	return glifnam

def cp(l, nam, uni, ax=False):
	#
	print(l, nam, ax, userNameToFileName(nam))
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	# transforming / CHANGING
	svg_data.attrib['glyph'] = make_id(svg_data.attrib['glyph'], nam, uni)
	#
	# saving / SAME
	glifnam = userNameToFileName(nam)
	save_svg_file(l,glifnam,tree)
	#
	return glifnam

def t_mirror(l, nam, uni, ax=False):
	#
	print(l, nam, ax, userNameToFileName(nam))
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	#print("---")
	#print(svg_data.attrib)
	#
	# transforming / CHANGING
	svg_data.attrib['glyph'] = make_id(svg_data.attrib['glyph'], nam, uni)
	#
	_h = ax == "horizontal"
	_v = ax == "vertical"
	#
	for x in svg_data:
		#
		x.attrib['d'] = formatPath(flipPath(parsePath(x.attrib['d']), horizontal=_h, vertical=_v))
		#
		print("------------------")
		print(x.attrib['id'])
		print(path_to_coord((x.attrib['d'])) )
		#
	#
	# saving / SAME
	glifnam = userNameToFileName(nam)
	save_svg_file(l,glifnam,tree)
	#
	return tdir+glifnam

def make_id(_id, nam, uni):
	#
	return '__'.join([nam,uni,_id.split("__")[2]])
	#

'''

Letter: Function, Function
Letter: {Function: { Arguments, Out, Recombine }, Function:{ Arguments, Out, Recombine }}

'''

function_declaration = {"H":(func1),
						"V":(func2),
						"S":(),
						"R":(),
						"C":(func2),
						"CP":(cp),
						"TM": (t_mirror),
						"":(),
						}

'''
Π	Ш	Щ
	Ц	

Ε	F	Γ	Τ	Ι
	Ξ
	Η

Λ	V	Υ	У
	Α
	Δ

Μ	W
	Ν	И	
		Ζ

	Σ	Κ
		Χ	Ж

Ο	Ω
	U

	C	Э
		D
		G

	Q
	Θ
	Φ	Ψ
	Ю

Β	Ρ	R	Я

		Ь	Ъ
			Ы
			Б
Л
J
S
З
Ч


'''



ins = {
		"Π":{1:{"fnc":"","arg":[],"out":["P_i"]}},
		"Ε":{1:{"fnc":"","arg":[],"out":["E_psilon"]}},
		"Λ":{1:{"fnc":"","arg":[],"out":["L_ambda"]}},
		"Μ":{1:{"fnc":"","arg":[],"out":["M_u"]}},
		"Ο":{1:{"fnc":"","arg":[],"out":["O_micron"]}},
		"Β":{1:{"fnc":"","arg":[],"out":["B_eta"]}},
		"Л":{1:{"fnc":"","arg":[],"out":["uni041B_"]}},
		"J":{1:{"fnc":"","arg":[],"out":["J_"]}},
		"S":{1:{"fnc":"","arg":[],"out":["S_"]}},
		"З":{1:{"fnc":"","arg":[],"out":["uni0417"]}},
		"Ч":{1:{"fnc":"","arg":[],"out":["uni0427"]}},
		"Ш":{1:{"fnc":"TM","arg":["horizontal"],"out":[],"rec":"Π","nam":"uni0428", "uni":"0428"}, 
			 2:{"fnc":"TM","arg":["horizontal"],"out":[],"nam":"uni0428", "uni":"0428"}
			 }, # --
		"Щ":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ш","nam":"uni0429","uni":"0429"}},
		
		# "Ц":{1:{"fnc":"TM","arg":["horizontal"],"out":[],"rec":"Π","nam":"uni0426","uni":"0426"}},
		# "F":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ε","nam":"F","uni":"0046"}}, # resolve func
		# "Γ":{1:{"fnc":"C","arg":[],"out":[],"rec":"F","nam":"Gamma","uni":"0393"}}, # resolve func
		# "Τ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Γ","nam":"Tau","uni":"03A4"}}, # resolve func
		# "Ι":{1:{"fnc":"C","arg":[],"out":[],"rec":"Τ","nam":"Iota","uni":"0399"}}, # resolve func
		# "Ξ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ε","nam":"Xi","uni":"039E"}}, # resolve func
		# "Η":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ε","nam":"Eta","uni":"0397"}}, # resolve func
		# "V":{1:{"fnc":"TM","arg":["horizontal"],"out":[],"rec":"Λ","nam":"V","uni":"0056"}},
		# "Υ":{1:{"fnc":"C","arg":[],"out":[],"rec":"V","nam":"Upsilon","uni":"03A5"}}, # resolve func
		# "У":{1:{"fnc":"C","arg":[],"out":[],"rec":"Υ","nam":"uni0423","uni":"0423"}}, # resolve func
		# "Α":{1:{"fnc":"C","arg":[],"out":[],"rec":"Λ","nam":"Alpha","uni":"0391"}}, # resolve func
		# "Δ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Λ","nam":"Deltagreek","uni":"0394"}}, # resolve func
		# "W":{1:{"fnc":"C","arg":[],"out":[],"rec":"Μ","nam":"W","uni":"0057"}}, # resolve func
		# "Ν":{1:{"fnc":"C","arg":[],"out":[],"rec":"Μ","nam":"Nu","uni":"039D"}}, # resolve func
		# "И":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ν","nam":"uni0418","uni":"0418"}}, # resolve func
		# "Ζ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ν","nam":"Zeta","uni":"0396"}}, # resolve func
		# "Σ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Μ","nam":"Sigma","uni":"03A3"}}, # resolve func
		# "Κ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Σ","nam":"Kappa","uni":"039A"}}, # resolve func
		# "Χ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Σ","nam":"Xi","uni":"03A7"}}, # resolve func
		# "Ж":{1:{"fnc":"C","arg":[],"out":[],"rec":"Χ","nam":"uni0416","uni":"0416"}}, # resolve func
		# "Ω":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"Omegagreek","uni":"03A9"}}, # resolve func
		# "U":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"U","uni":"0055"}}, # resolve func
		# "Q":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"Q","uni":"0051"}}, # resolve func
		# "Θ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"Theta","uni":"0398"}}, # resolve func
		# "Φ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"Phi","uni":"03A6"}}, # resolve func
		# "Ψ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Φ","nam":"Psi","uni":"03A8"}}, # resolve func
		# "C":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"C","uni":"0043"}}, # resolve func
		# "Э":{1:{"fnc":"C","arg":[],"out":[],"rec":"C","nam":"uni042D","uni":"042D"}}, # resolve func
		# "D":{1:{"fnc":"C","arg":[],"out":[],"rec":"C","nam":"D","uni":"0044"}}, # resolve func
		# "G":{1:{"fnc":"C","arg":[],"out":[],"rec":"C","nam":"G","uni":"0047"}}, # resolve func
		# "Ю":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ο","nam":"uni042E","uni":"042E"}}, # resolve func
		# "Ρ":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Β","nam":"Rho","uni":"03A1"}},
		# "R":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ρ","nam":"R","uni":"0052"}},
		# "Я":{1:{"fnc":"C","arg":[],"out":[],"rec":"R","nam":"uni042F","uni":"042F"}}, # resolve func
		# "Ь":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ρ","nam":"uni042C","uni":"042C"}}, # resolve func
		# "Ъ":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ь","nam":"uni042A","uni":"042A"}}, # resolve func
		# "Ы":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ь","nam":"uni042B","uni":"042B"}}, # resolve func
		# "Б":{1:{"fnc":"C","arg":[],"out":[],"rec":"Ь","nam":"uni0411","uni":"0411"}},  # resolve func
		# "Д":{1:{"fnc":"C","arg":[],"out":[],"rec":"Л","nam":"uni0414","uni":"0414"}},  # resolve func
		# "П":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Π","nam":"uni041F","uni":"041F"}}, # -- 
		# "E":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ε","nam":"E","uni":"0045"}},
		# "Е":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ε","nam":"uni0415","uni":"0415"}},
		# "L":{1:{"fnc":"C","arg":[],"out":[],"rec":"Γ","nam":"L","uni":"004c"}}, # resolve func
		# "Г":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Γ","nam":"uni0413","uni":"0413"}},
		# "T":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Τ","nam":"T","uni":"0054"}},
		# "Т":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Τ","nam":"uni0422","uni":"0422"}},
		# "I":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ι","nam":"I","uni":"0049"}},
		# "H":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Η","nam":"H","uni":"0048"}},
		# "Н":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Η","nam":"uni041D","uni":"041D"}},
		# "Y":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Υ","nam":"uni0059","uni":"0059"}},
		# "A":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Α","nam":"A","uni":"0041"}},
		# "А":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Α","nam":"uni0410","uni":"Acyrilli"}},
		# "M":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Μ","nam":"M","uni":"004d"}},
		# "М":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Μ","nam":"uni041C","uni":"041C"}},
		# "N":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ν","nam":"N","uni":"004e"}},
		# "Й":{1:{"fnc":"C","arg":[],"out":[],"rec":"И","nam":"uni0419","uni":"0419"}}, # resolve func
		# "Z":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ζ","nam":"Zed","uni":"005a"}},
		# "K":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Κ","nam":"K","uni":"004b"}},
		# "К":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Κ","nam":"uni041A","uni":"041A"}},
		# "X":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Χ","nam":"X","uni":"0058"}},
		# "Х":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Χ","nam":"uni0425","uni":"0425"}},
		# "O":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ο","nam":"O","uni":"004f"}},
		# "О":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ο","nam":"uni041E","uni":"041E"}},
		# "С":{1:{"fnc":"CP","arg":[],"out":[],"rec":"C","nam":"uni0421","uni":"0421"}},
		# "Ф":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Φ","nam":"uni0424","uni":"0424"}},
		# "B":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Β","nam":"B","uni":"0042"}},
		# "В":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Β","nam":"uni0412","uni":"0412"}},
		# "P":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ρ","nam":"P","uni":"0050"}},
		# "Р":{1:{"fnc":"CP","arg":[],"out":[],"rec":"Ρ","nam":"uni0420","uni":"0420"}},		
	  }

ans = copy.deepcopy(ins)
ins_d = dotdict(ins)


for letter,funct in ins.items():
	if len(funct) > 0:
		prevlet = letter
		for fnam,fdet in funct.items():
			fdet_d = dotdict(fdet)
			#
			if "rec" in fdet.keys():
				p = list(ins[fdet["rec"]])[-1]

				prevlet = tdir+ans[fdet["rec"]][p]["out"][0].split("/")[-1]

			if fdet["fnc"] != "":
				
				out = function_declaration[fdet["fnc"]](prevlet,fdet_d.nam,fdet_d.uni,*fdet_d.arg)
				#
				prevlet = out
				#
				ans[letter][fnam]["out"].append(out)
			

pprint.pprint(ans, sort_dicts=False)

#
#from svgpathtools import svg2paths
#paths, attributes = svg2paths('some_svg_file.svg')
#