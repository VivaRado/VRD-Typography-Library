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

#!/usr/bin/env python
import os
from Lib.ufo2svg import UFO2SVG
from Lib.ufo2svg.glif2svg import convertUFOToSVGFiles
from fontParts.world import *
from Lib.ufo2svg.simple_path import *
from Lib.ufo2svg.svg2glif import *

from Lib.generic.generic_tools import dotdict
import pprint

import xml.etree.ElementTree as ET

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

def parse_svg_path(svg_dir):
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

def func1(l,n,x=False):
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	# transforming / CHANGING
	#

	#
	# saving / SAME
	save_svg_file(l,n,tree)
	#
	return l 

def func2(l,n,x=False):
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	# transforming / CHANGING
	#

	#
	# saving / SAME
	save_svg_file(l,n,tree)
	#
	return l 

def t_mirror(l, nam, ax):
	#
	print(l, nam, ax)
	# parsing / SAME
	tree, svg_data = parse_svg_path(l)
	#
	# transforming / CHANGING
	d = svg_data[0].attrib['d']
	_h = ax == "horizontal"
	_v = ax == "vertical"
	d = formatPath(flipPath(parsePath(d), horizontal=_h, vertical=_v))
	#
	# saving / SAME
	save_svg_file(l,nam,tree)
	#
	return l 

def id_change(f, t):
	#	
	pass
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

tdir = "Test/temp_b/"

ins = {
		"Π":{"":{"arg":[],"out":[tdir+"P_i"]}},
		"Ε":{"":{"arg":[],"out":[tdir+"E_psilon"]}},
		"Λ":{"":{"arg":[],"out":[tdir+"L_ambda"]}},
		"Μ":{"":{"arg":[],"out":[tdir+"M_u"]}},
		"Ο":{"":{"arg":[],"out":[tdir+"O_micron"]}},
		"Β":{"":{"arg":[],"out":[tdir+"B_eta"]}},
		"Л":{"":{"arg":[],"out":[tdir+"uni041B_"]}},
		"J":{"":{"arg":[],"out":[tdir+"J_"]}},
		"S":{"":{"arg":[],"out":[tdir+"S_"]}},
		"З":{"":{"arg":[],"out":[tdir+"uni0417_"]}},
		"Ч":{"":{"arg":[],"out":[tdir+"uni0427_"]}}, 
		"Ш":{"TM":{"arg":["vertical"],"out":[],"rec":"Π","nam":"uni0428"}}, # --
		"Щ":{"C":{"arg":[],"out":[],"rec":"Ш","nam":"uni0429"}},
		"Ц":{"C":{"arg":[],"out":[],"rec":"Π","nam":"uni0426"}},
		"F":{"C":{"arg":[],"out":[],"rec":"Ε","nam":"F_"}},
		"Γ":{"C":{"arg":[],"out":[],"rec":"F","nam":"G_amma"}},
		"Τ":{"C":{"arg":[],"out":[],"rec":"Γ","nam":"T_au"}},
		"Ι":{"C":{"arg":[],"out":[],"rec":"Τ","nam":"I_ota"}},
		"Ξ":{"C":{"arg":[],"out":[],"rec":"Ε","nam":"X_i"}},
		"Η":{"C":{"arg":[],"out":[],"rec":"Ε","nam":"E_ta"}},
		"V":{"C":{"arg":[],"out":[],"rec":"Λ","nam":"V_"}},
		"Υ":{"C":{"arg":[],"out":[],"rec":"V","nam":"Y_"}},
		"У":{"C":{"arg":[],"out":[],"rec":"Υ","nam":"uni0423"}},
		"Α":{"C":{"arg":[],"out":[],"rec":"Λ","nam":"A_lpha"}},
		"Δ":{"C":{"arg":[],"out":[],"rec":"Λ","nam":"D_eltagreek"}},
		"W":{"C":{"arg":[],"out":[],"rec":"Μ","nam":"W_"}},
		"Ν":{"C":{"arg":[],"out":[],"rec":"Μ","nam":"N_u"}},
		"И":{"C":{"arg":[],"out":[],"rec":"Ν","nam":"uni0418"}},
		"Ζ":{"C":{"arg":[],"out":[],"rec":"Ν","nam":"Z_eta"}},
		"Σ":{"C":{"arg":[],"out":[],"rec":"Μ","nam":"S_igma"}},
		"Κ":{"C":{"arg":[],"out":[],"rec":"Σ","nam":"K_appa"}},
		"Χ":{"C":{"arg":[],"out":[],"rec":"Σ","nam":"X_i"}},
		"Ж":{"C":{"arg":[],"out":[],"rec":"Χ","nam":"uni0416"}},
		"Ω":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"O_megagreek"}},
		"U":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"U_"}},
		"Q":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"Q_"}},
		"Θ":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"T_heta"}},
		"Φ":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"P_hi"}},
		"Ψ":{"C":{"arg":[],"out":[],"rec":"Φ","nam":"P_si"}},
		"C":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"C_"}},
		"Э":{"C":{"arg":[],"out":[],"rec":"C","nam":"uni042D"}},
		"D":{"C":{"arg":[],"out":[],"rec":"C","nam":"D_"}},
		"G":{"C":{"arg":[],"out":[],"rec":"C","nam":"G_"}},
		"Ю":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"uni042E"}},
		"Ρ":{"C":{"arg":[],"out":[],"rec":"Β","nam":"R_ho"}},
		"R":{"C":{"arg":[],"out":[],"rec":"Ρ","nam":"R_"}},
		"Я":{"C":{"arg":[],"out":[],"rec":"R","nam":"uni042F"}},
		"Ь":{"C":{"arg":[],"out":[],"rec":"Ρ","nam":"uni042C"}},
		"Ъ":{"C":{"arg":[],"out":[],"rec":"Ь","nam":"uni042A"}},
		"Ы":{"C":{"arg":[],"out":[],"rec":"Ь","nam":"uni042B"}},
		"Б":{"C":{"arg":[],"out":[],"rec":"Ь","nam":"uni0411"}}, 
		"Д":{"C":{"arg":[],"out":[],"rec":"Л","nam":"uni0414"}}, 
		"П":{"C":{"arg":[],"out":[],"rec":"Π","nam":"uni041F"}}, # -- 
		"E":{"C":{"arg":[],"out":[],"rec":"Ε","nam":"E_"}},
		"Е":{"C":{"arg":[],"out":[],"rec":"Ε","nam":"uni0415"}},
		"L":{"C":{"arg":[],"out":[],"rec":"Γ","nam":"L_"}},
		"Г":{"C":{"arg":[],"out":[],"rec":"Γ","nam":"uni0413"}},
		"T":{"C":{"arg":[],"out":[],"rec":"Τ","nam":"T_"}},
		"Т":{"C":{"arg":[],"out":[],"rec":"Τ","nam":"uni0422"}},
		"I":{"C":{"arg":[],"out":[],"rec":"Ι","nam":"I_"}},
		"H":{"C":{"arg":[],"out":[],"rec":"Η","nam":"H_"}},
		"Н":{"C":{"arg":[],"out":[],"rec":"Η","nam":"uni041D"}},
		"Y":{"C":{"arg":[],"out":[],"rec":"Υ","nam":"uni0059"}},
		"A":{"C":{"arg":[],"out":[],"rec":"Α","nam":"A_"}},
		"А":{"C":{"arg":[],"out":[],"rec":"Α","nam":"uni0410"}},
		"M":{"C":{"arg":[],"out":[],"rec":"Μ","nam":"M_"}},
		"М":{"C":{"arg":[],"out":[],"rec":"Μ","nam":"uni041C"}},
		"N":{"C":{"arg":[],"out":[],"rec":"Ν","nam":"N_"}},
		"Й":{"C":{"arg":[],"out":[],"rec":"И","nam":"uni0419"}},
		"Z":{"C":{"arg":[],"out":[],"rec":"Ζ","nam":"Z_ed"}},
		"K":{"C":{"arg":[],"out":[],"rec":"Κ","nam":"K_"}},
		"К":{"C":{"arg":[],"out":[],"rec":"Κ","nam":"uni041A"}},
		"X":{"C":{"arg":[],"out":[],"rec":"Χ","nam":"X_"}},
		"Х":{"C":{"arg":[],"out":[],"rec":"Χ","nam":"uni0425"}},
		"O":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"O_"}},
		"О":{"C":{"arg":[],"out":[],"rec":"Ο","nam":"uni041E"}},
		"С":{"C":{"arg":[],"out":[],"rec":"C","nam":"uni0421"}},
		"Ф":{"C":{"arg":[],"out":[],"rec":"Φ","nam":"uni0424"}},
		"B":{"C":{"arg":[],"out":[],"rec":"Β","nam":"B_"}},
		"В":{"C":{"arg":[],"out":[],"rec":"Β","nam":"uni0412"}},
		"P":{"C":{"arg":[],"out":[],"rec":"Ρ","nam":"P_"}},
		"Р":{"C":{"arg":[],"out":[],"rec":"Ρ","nam":"uni0420"}},		
	  }

ins = dotdict(ins)

for letter,funct in ins.items():
	if len(funct) > 0:
		prevout = letter
		for fnam,fdet in funct.items():
			fdet = dotdict(fdet)
			if "rec" in fdet.keys():
				p = list(ins[fdet["rec"]])[-1]
				prevout = ins[fdet["rec"]][p]["out"][0]

			if fnam != "":
				
				out = function_declaration[fnam](prevout,fdet.nam,*fdet.arg)
				prevout = out
				fdet.out.append(out)

pprint.pprint(ins)
