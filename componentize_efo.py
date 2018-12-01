#
#!/usr/bin/env python
import os
#
from Lib.efo import EFO
from Lib.components import COMPS
from Lib.generic import generic_tools
#
import json
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

new_class_fontinfo = [
    {
        "shared_info": {
            "familyName": ""
        }
    },
    {
        "font_files": []
    },
    {
        "font_info": []
    },
    {
        "font_kerning_settings": []
    }
]
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
	#
	EFO_temp = os.path.join(args.source,"temp")
	#
	EFO = EFO(args.source,EFO_temp)
	#
	EFO._efo_to_ufos(args.fonts, True, "class")
	#
	f_files_class = []
	#
	for x in EFO.all_exported_ufo_dst:
		#
		for k, v in x.items():
			#
			copy_ufo_for_componentization = v.split('.ufo')[0]+'_compo.ufo'
			#
			generic_tools.copyDirectory(v, copy_ufo_for_componentization)
			#
			f_files_class.append(k+'_compo')
			#
			#
			UFO_to_COMPUFO = COMPS(args.source, copy_ufo_for_componentization)
			#
			UFO_to_COMPUFO.ufos_comp()
			#
		#
	#
	new_class_fontinfo[0]["shared_info"]["familyName"] = EFO.current_font_family_name
	new_class_fontinfo[1]["font_files"] = f_files_class
	#
	#print(new_class_fontinfo)
	#
	c_fontinfo_dir = os.path.join(*(EFO._in,"temp","fontinfo.json"))
	#
	with open(c_fontinfo_dir, 'w') as outfile:
		#
		json.dump(new_class_fontinfo, outfile)
		#
	#
	#print(c_fontinfo_dir,args.source)
	#
	c_source_ufo_family = os.path.join(*(EFO._in,"temp",EFO.current_font_family_name))
	#
	EFO._in = c_fontinfo_dir
	EFO._out = args.source
	EFO.current_source_ufo_family = c_source_ufo_family
	#
	EFO._ufos_to_efo(["glyphs"], False, False, True)
	#
#