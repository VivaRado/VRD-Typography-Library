import os
import sys
from os.path import dirname, join, abspath
#
import datetime
#
import json
import plistlib
import shutil
#
from Lib.efo import efo_fontinfo
from Lib.compress_kerning import COMPRESS
#
from Lib.generic import generic_tools
#
from .Autokern import *
from .AutokernSettings import *
import tfs3.common.TFSProject as TFSProject
from tfs3.common.TFSMap import TFSMap
#
test_pairs_b = '''ST
UV
QY
We
QV
QW
AC
AG
AO
AQ
AT
AU
AV
AW
AY
BA
BE
BL
BP'''

test_pairs = '''FG
ST
UV
QV
QW
JA
KO
VC
VG
AY
AC
Va
Vc
Vb
VA
AV
VA
VW
WA
AW
AG
AO
AQ
AT
AU
AV
AW
AY
BA
BE
BL
BP
BR
BU
BV
BW
BY
CA
CO
CR
DA
DD
DE
DI
DL
DM
DN
DO
DP
DR
DU
DV
DW
DY
EC
EO
FA
FC
FG
FO
GE
GO
GR
GU
HO
IC
IG
IO
JA
JO
KO
LC
LT
LV
LW
LY
LG
LO
LU
MG
MO
NC
NG
NO
OA
OB
OD
OE
OF
OH
OI
OK
OL
OM
ON
OP
OR
OT
OU
OV
OW
OX
OY
PA
PE
PL
PO
PP
PU
PY
QU
RC
RG
RY
RT
RU
RV
RW
RY
SI
SM
ST
SU
TA
TC
TO
UA
UC
UG
UO
US
VA
VC
VG
VO
VS
WA
WC
WG
WO
YA
YC
YO
YS
ZO
Ac
Ad
Ae
Ag
Ao
Ap
Aq
At
Au
Av
Aw
Ay
Bb
Bi
Bk
Bl
Br
Bu
By
Ca
Cr
Da
Eu
Ev
Fa
Fe
Fi
Fo
Fr
Ft
Fu
Fy
Gu
He
Ho
Hu
Hy
Ic
Id
Iq
Io
It
Ja
Je
Jo
Ju
Ke
Ko
Ku
Lu
Ly
Ma
Mc
Md
Me
Mo
Nu
Na
Ne
Ni
No
Nu
Oa
Ob
Oh
Ok
Ol
Pa
Pe
Po
Rd
Re
Ro
Rt
Ru
Si
Sp
Su
Ta
Tc
Te
Ti
To
Tr
Ts
Tu
Tw
Ty
Ua
Ug
Um
Un
Up
Us
Va
Ve
Vi
Vo
Vr
Vu
Wd
Wi
Wm
Wr
Wt
Wu
Wy
Xa
Xe
Xo
Xu
Xy
Yd
Ye
Yi
Yp
Yu
Yv
ac
ad
ae
ag
ap
af
at
au
av
aw
ay
ap
bl
br
bu
by
ca
ch
ck
da
dc
de
dg
do
dt
du
dv
dw
dy
ea
ei
el
em
en
ep
er
et
eu
ev
ew
ey
fa
fe
ff
fi
fl
fo
ga
ge
gh
gl
go
gg
hc
hd
he
hg
ho
hp
ht
hu
hv
hw
hy
ic
id
ie
ig
io
ip
it
iu
iv
ja
je
jo
ju
ka
kc
kd
ke
kg
ko
la
lc
ld
le
lf
lg
lo
lp
lq
lu
lv
lw
ly
ma
mc
md
me
mg
mn
mo
mp
mt
mu
mv
my
nc
nd
ne
ng
no
np
nt
nu
nv
nw
ny
ob
of
oh
oj
ok
ol
om
on
op
or
ou
ov
ow
ox
oy
pa
ph
pi
pl
pp
pu
qu
ra
rd
re
rg
rk
rl
rm
rn
ro
rq
rr
rt
rv
ry
sh
st
su
td
ta
te
to
ua
uc
ud
ue
ug
uo
up
uq
ut
uv
uw
uy
va
vb
vc
vd
ve
vg
vo
vv
vy
wa
wx
wd
we
wg
wh
wo
xa
xe
xo
ya
yc
yd
ye
yo'''
#
#
ignore_glyphs_list = ["brevecomb",
"caroncomb",
"circumflexcomb",
"commaturnedabovecomb",
"commaturnedbelowcomb",
"dieresiscomb",
"dotaccentcomb", 
"gravecomb",
"hungarumlautcomb",
"macroncomb",
"ringcomb",
"tildecomb",
"cedillacomb",
"ogonekcomb",
"tonoscomb",
"acutecomb",
"dieresistonoscomb"]
#
class AUTOKERN(object):
	def __init__(self, _in, _fonts='', _compress_class_plist='No'):
		#
		self._in = _in
		self.EFO_fontinfo = "fontinfo.json"
		self.KERN_temp = "temp_kern"
		self.EFO_temp = "temp"
		self._compress_class_plist = _compress_class_plist
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		self.current_font_family_directory = os.path.join(self._in,self.current_font_family_name)
		#
		if len(_fonts) > 0:
			#
			self._fonts = _fonts
			#
		#
	#
	def extract_test_pairs(self, test_list, weights):
		#
		weights_perm = {}
		#
		for z in range(len(weights)):
			#
			weights_perm[weights[z]] = []
			#
		#
		x = 0
		#
		total_permut = ''
		#
		for w in weights:	
			#
			self.return_self_dirs(w)
			#
			orig_w = w
			#
			result_lines = ''
			result_keys = []
			#
			for x in test_list.split('\n'):
				#
				permu_list = list(x)
				#
				#print(permu_list)
				#
				permut_str = '"'+permu_list[0]+'","'+permu_list[1]+'"'+'\n'
				#
				total_permut = total_permut + permut_str
				#
				weights_perm[orig_w].append(permu_list)
				#
			#
		#
		return weights_perm
		#
	#
	def extract_pairs(self, dir_path, weights):
		#
		_dir = dir_path
		#
		weights_perm = {}
		#
		for z in range(len(weights)):
			#
			weights_perm[weights[z]] = []
			#
		#
		x = 0
		#
		total_permut = ''
		#
		for w in weights:	
			#
			self.return_self_dirs(w)
			#
			orig_w = w
			#
			result_lines = ''
			result_keys = []
			#
			if os.path.isdir(os.path.join(self.current_font_instance_directory,'kerning.plist')):
				#
				pl = plistlib.readPlist(os.path.join(self.current_font_instance_directory,'kerning.plist'))
				#
				for x,v in pl.items():
					#
					for z,y in v.items():
						#
						permu_list = [x,z]
						permut_str = '"'+x+'","'+z+'"'+'\n'
						#
						total_permut = total_permut + permut_str
						#
						weights_perm[orig_w].append(permu_list)
						#
					#
				#
			#
		#
		return weights_perm
		#
	#
	def pairlist_tuple(self, pairs):
		#
		pairlist = {}
		#
		l = []
		#
		for li in pairs:
			#
			for g in li:
				#
				if g not in ignore_glyphs_list:
					#
					l.append(g)
					#
				#
		#

		#
		data = tuple(filter(None, l))
		#
		return data
		#
	#
	def flat_kern_to_efo(self, _source_efo, EFO):
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
		source_efo_flat_kern_dir = os.path.join(_source_efo, "kerning/flat")
		source_efo_similarity_kern_plist = os.path.join(_source_efo, "groups/kerning.plist")
		#
		for x in self.all_dst:
			#
			for k, v in x.items():
				#
				#print(">>", k, v)
				#
				current_font_flat_kerning = os.path.join(v,'kerning'+'.plist')
				#
				source_font_flat_kerning = os.path.join(source_efo_flat_kern_dir,k+'.plist')
				#
				shutil.copyfile(current_font_flat_kerning, source_font_flat_kerning)
				#
				current_font = generic_tools.sanitize_string(self.current_font_family_name+' '+k)
				#
				print('\tREPLACED FLAT KERNING FOR EFO:', current_font, ' AT:', source_font_flat_kerning)
				#
			#
		#
		if self._compress_class_plist == "Yes":
			#
			print('Hello')
			#
			f_files_class = []
			#
			for x in self.all_dst:
				#
				for k, v in x.items():
					#
					copy_ufo_for_class_compress = v.split('.ufo')[0]+'_class.ufo'
					#
					source_font_flat_kerning = os.path.join(source_efo_flat_kern_dir,k+'.plist')
					#
					generic_tools.copyDirectory(v, copy_ufo_for_class_compress)
					#
					f_files_class.append(k+'_krn_class')
					#
					_COMPRESS = COMPRESS(k,v, copy_ufo_for_class_compress, source_efo_similarity_kern_plist)
					#EFO = EFO(args.source,EFO_temp)
					#
					_COMPRESS.do_class_kern_replacement()
					#
			#
			new_class_fontinfo[0]["shared_info"]["familyName"] = self.current_font_family_name
			new_class_fontinfo[1]["font_files"] = f_files_class
			#
			print(new_class_fontinfo)
			#
			c_fontinfo_dir = os.path.join(*(EFO._in,"temp",EFO.current_font_family_name,"fontinfo.json"))
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
			EFO._out = EFO._in
			EFO._in = c_fontinfo_dir
			EFO.current_source_ufo_family = c_source_ufo_family
			#
			EFO._ufos_to_efo(["kerning","features"], False, True, False)
			#
		#
	#
	def do_kern_for_pairs(self):
		#
		efo_fontinfo.read_efo_json_fontinfo(self)
		#
		print('AUTOKERN: Started Automatic Kerning')
		#
		self.font_files = efo_fontinfo.get_font_file_array(self)
		self.given_fonts = self._fonts.split(',')
		#
		faults = generic_tools.check_given_fonts_exist(self._fonts, self.font_files)
		#
		if faults == False:
			#
			print('\tGIVEN FONTS EXIST CONTINUING')
			#
			self.all_dst = []
			#
			x = 0
			#
			#pairlist = self.extract_pairs(self._in, self.given_fonts)
			pairlist = self.extract_test_pairs(test_pairs_b, self.given_fonts)
			#
			for gf in self.given_fonts:
				#
				print('\tAUTOKERN: Automatic Kerning for:', gf)
				#
				self.return_self_dirs(gf)
				#
				ufo_src_path = self.current_font_instance_directory
				self.out_fnt_flat_kerned=ufo_src_path.split('.ufo')[0]+"_krn.ufo"
				#
				self.all_dst.append({gf:self.out_fnt_flat_kerned})
				#
				pseudo_argv = ('--ufo-src-path',
								ufo_src_path,
								'--ufo-dst-path',
								self.out_fnt_flat_kerned,
								'--min-distance-ems',
								str(self.current_kerning_settings["--min-distance-ems"]),
								'--max-distance-ems',
								str(self.current_kerning_settings["--max-distance-ems"]),
								'--max-x-extrema-overlap-ems',
								str(self.current_kerning_settings["--max-x-extrema-overlap-ems"]),
								'--intrusion-tolerance-ems',
								str(self.current_kerning_settings["--intrusion-tolerance-ems"]),
								'--precision-ems',
								str(self.current_kerning_settings["--precision-ems"]),
								#
								'--kerning-threshold-ems',
								str(self.current_kerning_settings["--kerning-threshold-ems"]),
								#
								'--x-extrema-overlap-scaling',
								str(self.current_kerning_settings["--x-extrema-overlap-scaling"]),
								# #
								'--log-path',
								os.path.join(self._in,"temp","logs","log"),
								'--log-basic-pairs',
								'--write-kerning-pair-logs'
								)
				#
				pairlist_tup = self.pairlist_tuple(pairlist[gf])
				#
				#print(pairlist_tup)
				#parlist_test = ("A","A","A","AE","A","Aacute","A","Abreve","A","Acircumflex","A","Adieresis","A","Agrave","A","Alpha","A","Alphatonos","A","Amacron","A","Aogonek","A","Aring","A","Atilde","A","B","A","Beta","A","C")
				#
				pairlist_tuple_to_kern = ('--glyph-pairs-to-kern',*pairlist_tup)
				ignore = ('--glyphs-to-ignore',*tuple(ignore_glyphs_list))
				#
				if len(pairlist[gf]) == 0:
					#
					pairlist_tuple_to_kern = ()
					#
				#
				autokernArgs = TFSMap()
				#AutokernSettings(autokernArgs).getCommandLineSettings(*pseudo_argv)
				#
				#
				AutokernSettings(autokernArgs).getCommandLineSettings(*(pseudo_argv+pairlist_tuple_to_kern+ignore))
				autokern = Autokern(autokernArgs)
				autokern.process()
				#
				x = x + 1
				#
				print ('Completed:'+gf+', '+str(x)+'/'+str(len(self.given_fonts))+'\n'+' Produced Kerned UFO:'+self.out_fnt_flat_kerned)
				#
			#

			#
	def return_self_dirs(self, gf):
		#
		self.current_font_file_name = gf
		self.current_font_family_directory = os.path.join(os.path.join(self._in, self.EFO_temp),self.current_font_family_name)
		self.current_font_instance_name = generic_tools.sanitize_string(self.current_font_family_name+' '+self.current_font_file_name)
		self.current_font_instance_directory = os.path.join(self.current_font_family_directory,self.current_font_instance_name+'.ufo')
		self.current_fontinfo = efo_fontinfo.get_font_info_for_weight(self)
		#
		for x in self.kerning_settings:
			#
			for k,v in x.items():
				#
				if k == gf:
					#
					self.current_kerning_settings = v	
					#
				#
			#
		#