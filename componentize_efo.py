#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
from Lib.components import COMPS
#import Lib.generic.tab_completion
#
from argparse import ArgumentParser
#
#REMOVE
from pprint import pprint
#
parser = ArgumentParser()
parser.add_argument("-s", "--source", dest="source",
                    help="Source EFO", metavar="FILE")
parser.add_argument("-f", "--fonts", dest="fonts", 
                    help="EFO Fonts Instances to Export to UFOs comma separated")
parser.add_argument("-k", "--kerning_type", dest="kerning_type", 
                    help='Kerning Type to copy to UFOs')
#
args = parser.parse_args()
#
dir_path = os.path.dirname(os.path.realpath(__file__))
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
	print('=\n=> Please Provide the Font Instances to Componentize: -f "thn,reg,bld"\n=')	
	#
if faults == False:
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	EFO._efo_to_ufos(args.fonts)
	#
	UFO_to_COMPUFO = COMPS(args.source, EFO.all_exported_ufo_dst)
	#
	UFO_to_COMPUFO.ufos_comp()
	#
#