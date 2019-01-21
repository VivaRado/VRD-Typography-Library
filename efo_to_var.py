#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
from Lib.components import COMPS
from Lib.generic import generic_tools
#
from subprocess import call
import fontmake
#
import json
#
from argparse import ArgumentParser
#
import xml.etree.ElementTree as ET
import lxml.etree as LET
#
#REMOVE
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
                    help="Source EFO", metavar="FILE")
parser.add_argument("-o", "--output", dest="output",
                    help="Output Directory", metavar="FILE")
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
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
if faults == False:
	#
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	dspace_file = os.path.join(args.source,EFO.EFO_designspace)
	new_dspace = os.path.join(*(args.source, EFO.EFO_temp, EFO.EFO_designspace))
	#
	print(dspace_file)
	#
	dspace_fonts = []
	#
	with open(dspace_file, 'r') as xml_dspace_file:
		#
		tree = ET.parse(xml_dspace_file)
		#
		sources = tree.find("sources")
		#
		for z in sources.iter():
			#
			for source in list(z):
				#
				if source.tag == 'source':
					#
					print(source)
					#
					font = source.attrib['filename'].split('.ufo')[0]
					#
					dspace_fonts.append(font)
					#
				#
			#
		#
		xml_dspace_file.close()
		#
		dspace_fonts = ','.join(dspace_fonts)
		#
		faults = generic_tools.check_given_fonts_exist(dspace_fonts, EFO.font_files)
		#
		if faults == False:
			#
			EFO._efo_to_ufos(dspace_fonts, False, "class", True)
			#
			for x in EFO.all_exported_ufo_dst:
				#
				for k, v in x.items():
					#
					copy_ufo_for_componentization = v.split('.ufo')[0]
					#
					for y in sources.iter():
						#
						for source in list(y):
							#
							if source.tag == 'source':
								#
								font = str(source.attrib['filename']).split('.ufo')[0]
								#
								if k == font:
									#
									source.set('filename', x[k])
									#
								#
							#
						#
					#
				#
			#
			tree.write(new_dspace)
			#
			fontmake_main = os.path.join(os.path.dirname(fontmake.__file__), "__main__.py")
			#
			if args.output:
				#
				if os.name == 'nt':
					#
					call(["py", fontmake_main, "-o", "variable", "-m", new_dspace, "--output-path", os.path.normpath(args.output)])

				else:

					call(["fontmake", "-o", "variable", "-m", new_dspace, "--output-path", os.path.normpath(args.output)])

				#
			else:
				#
				if os.name == 'nt':

					call(["py", fontmake_main, "-o", "variable", "-m", new_dspace])

				else:

					call(["fontmake", "-o", "variable", "-m", new_dspace])

				#
			#
			#
		else:
			#
			print('ERROR: DESIGNSPACE FILE AND FONTINFO FONTS NOT IN AGREEMENT, MISSING FONTS')
			#
		#