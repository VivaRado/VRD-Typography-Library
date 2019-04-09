#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
import Lib.generic.generic_tools as generic_tools
#
from argparse import ArgumentParser
#
import xml.etree.cElementTree as ET
#
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
                    help="Source EFO", metavar="FILE")
parser.add_argument("-n", "--nam", dest="nam", 
                    help="NAM files to compare to")
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
#
faults = False
#
def check_uni(_u, glyphlib):
	#
	for glyph in glyphlib.findall("glyph"):
		#
		if glyph.attrib['unicode']:
			#
			glyphlib_uni = ('\\u'+glyph.attrib['unicode']).encode("utf-8").decode('unicode-escape')
			#
			if glyphlib_uni == _u:
				#
				return True
				#
			#
		#
	#
	return False
	#
def check_name(_n, glyphlib):
	#
	for glyph in glyphlib.findall("glyph"):
		#
		if glyph.attrib['name']:
			#
			name = generic_tools.GLIFFileNametoglyphName(_n)
			#
			if name == _n:
				#
				return True
				#
			#
		#
	#
	return False
	#
#
if  args.source is None:
	#
	faults = True
	#
	print('=\n=> Please Provide Source EFO File: -s "/font.efo"\n=')	
	#
if  args.nam is None:
	#
	faults = True
	#
	print('=\n=> Please Provide a NAM file: -n "dir/file.nam"\n=')	
	#
#
if faults == False:
	#
	print('ok')
	#
	EFO = EFO(args.source)
	#
	source_glyphflib = os.path.join(EFO._in,"glyphlib.xml")
	glyphlib = ET.parse(source_glyphflib)
	#
	given_nam = generic_tools.parse_nam(args.nam)
	#
	for item_nam in given_nam:
		#
		codepoint = item_nam[0]
		#
		if codepoint != None:
			#
			p_cp = chr(codepoint)
			#
		else:
			#
			p_cp = item_nam[2].strip()
			#
		#
		if codepoint != None:
			#
			checked = check_uni(p_cp, glyphlib)
			#
		else:
			#
			checked = check_name(p_cp, glyphlib)
			#
		if checked == False:
			#
			print('\t', item_nam[0], item_nam[2], checked)
			#
		#
	#
#

