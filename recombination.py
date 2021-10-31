'''
Get a few basic letters and distribute the shapes to create all other shared letters in Latin, Greek and Cyrillic

Current state testing on Capital letters

Capital Set

C01 Π
C02 Ε
C03 Λ
C04 Μ
C05 Ο
C06 Β
C07 Л
C08 J
C09 S
C10 З
C11 Ч


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

To create recombination we store the result and then point to that result in the subsequent instructions, we loop until all have results.

'''

#!/usr/bin/env python
import os
from Lib.ufo2svg import UFO2SVG
from Lib.ufo2svg.glif2svg import convertUFOToSVGFiles
from fontParts.world import *


supportedUFOFormatVersions = [1, 2, 3]
supportedGLIFFormatVersions = [1, 2]

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

def func1(l,n,x):
	return l + str(n) + "H" + str(x)

def func2(l):
	return l + "V"

def func3(l):
	return l + "C"


class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.__getitem__
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__


t = {"H":(func1),"V":(func2),"S":(),"R":(),"C":(func3)}

l = ["a","b","c"]

ins = {
		"a":{"H":{"arg":[1,2],"res":[]}, "V":{"arg":[],"res":[]}},
		"b":{"C":{"arg":[],"res":[],"rec":"a"}}
	  }

ins = dotdict(ins)

for letter,funct in ins.items():
	#
	if len(funct) > 0:
		#
		prevres = letter
		#
		for fnam,fdet in funct.items():
			#
			fdet = dotdict(fdet)

			if "rec" in fdet.keys():
				
				p = list(ins.a)[-1]
				
				prevres = ins.a[p]["res"][0]
			
			res = t[fnam](prevres,*fdet.arg)

			prevres = res
			fdet.res.append(res)
		#
	#

print(ins)