import os
import random
import sys
from sys import argv
import re
import plistlib
import glob
from lxml import html
from lxml import etree
from os.path import basename
import difflib
#
import xml.etree.ElementTree as ET
#
#
_format = 1
base_top_accent_tall_pos_y = 735
base_top_accent_tall_tonos_pos_y = 700
base_top_accent_short_pos_y = 545
comb_top_accent_pos_y = 600
comb_bottom_accent_pos_y = 0
tall_small_case = ['l','t', 'd', 'h']
l_dots_list = ['Ldot','ldot']
#
flush_space = '                                      '
#
comb_anchors_top = '''<anchor x="{0}" y="750" name="top"/><anchor x="{0}" y="600" name="_top"/>'''
#
comb_anchors_bot = '''<anchor x="{0}" y="0" name="_bottom"/><anchor x="{0}" y="-250" name="bottom"/>'''
#
comp_anchors_top = '''<contour>
      <point x="{0}" y="750" type="move" name="top"/>
    </contour>
    <contour>
      <point x="{0}" y="{1}" type="move" name="_top"/>
    </contour>'''
#
##
comp_anchors_top_tonos = '''<contour>
      <point x="{0}" y="750" type="move" name="tonos"/>
    </contour>
    <contour>
      <point x="{0}" y="{1}" type="move" name="_tonos"/>
    </contour>'''
#
# ##
# comp_anchors_center = '''<contour>
#       <point x="{1}" y="750" type="move" name="center"/>
#     </contour>
#     <contour>
#       <point x="{1}" y="{0}" type="move" name="_center"/>
#     </contour>'''
# #
#
comp_anchors_bot = '''<contour>
      <point x="{1}" y="-250" type="move" name="bottom"/>
    </contour>
    <contour>
      <point x="{1}" y="{0}" type="move" name="_bottom"/>
    </contour>'''
#
#
comp_anchors_bot_ogonek = '''<contour>
      <point x="{1}" y="-250" type="move" name="ogonek"/>
    </contour>
    <contour>
      <point x="{1}" y="{0}" type="move" name="_ogonek"/>
    </contour>'''
#
base_anchors_contour = '''<contour>
      <point x="{2}" y="0" type="move" name="ogonek"/>
    </contour>
    <contour>
      <point x="{0}" y="0" type="move" name="bottom"/>
    </contour>
    <contour>
      <point x="{0}" y="{1}" type="move" name="top"/>
    </contour>
    <contour>
      <point x="{3}" y="{4}" type="move" name="tonos"/>
    </contour>'''
#
base_anchors = '''
  <anchor x="{2}" y="0" name="ogonek"/>
  <anchor x="{0}" y="0" name="bottom"/>
  <anchor x="{0}" y="{1}" name="top"/>
  <anchor x="{3}" y="{4}" name="tonos"/>
  '''
#
comb_top = ['acutecomb',
			'tonoscomb',
			'dieresistonoscomb',
			'brevecomb',
			'caroncomb',
			'circumflexcomb',
			'commaturnedabovecomb',
			'dieresiscomb',
			'dotaccentcomb',
			'gravecomb',
			'hungarumlautcomb',
			'macroncomb',
			'croat',
			'ringcomb',
			'tildecomb'];

comb_top_rebase = ['acute',
			'tonos',
			'dieresistonos',
			'breve',
			'caron',
			'circumflex',
			'quoteleft',
			'dieresis',
			'dotaccent',
			'grave',
			'hungarumlaut',
			'overscore',
			'overscore',
			'ring',
			'tilde'];

comb_bot = ['cedillacomb',
			'ogonekcomb',
			'commaturnedbelowcomb'
			# 'slashlongcomb',
			# 'slashshortcomb',
			# 'strokelongcomb',
			# 'strokeshortcomb'
			];
comb_bot_rebase = ['cedilla',
			'ogonek',
			'commaaccent'
			# 'slashlongcomb',
			# 'slashshortcomb',
			# 'strokelongcomb',
			# 'strokeshortcomb'
			];
#
non_exist = []
non_comp = []
#
def get_between(_start, _end, _str):
	#
	return _str[_str.find(_start)+len(_start):_str.find(_end)]
	#
#
def get_base_glif_width(_dir_glif, glif, exact_loc = False):
	#
	res_width = 0
	res_name = ''
	#
	if exact_loc == True:
		#
		with open(_dir_glif, 'r') as f:
			#
			glif_data = f.read()
			#
			#
			glif_parse = ET.fromstring(glif_data)
			#
			res_name = glif_parse.get('name')
			res_width = int(glif_parse.findall('advance')[0].get('width'))
			#
		#
	else:
		#
		for file in glob.glob(_dir_glif+"/*.glif"):
			#
			with open(file, 'r') as the_file:
				#
				glif_data = the_file.read()
				#
				glif_parse = ET.fromstring(glif_data)
				#
				res_name = glif_parse.get('name')
				#
				if res_name == glif:
					#
					res_width = int(glif_parse.findall('advance')[0].get('width'))
					#
					break
					#
				#
				#

			#
	return res_name,res_width
#
def get_base_glif_contours(_dir_glif, needed_glifs):
	#
	base_contours = {}
	#
	seen_glifs = []
	#
	res_width = 0
	#
	for file in glob.glob(_dir_glif+"/*.glif"):
		#
		with open(file, 'r') as the_file:
			#
			glif_data = the_file.read()
			#
			glif_parse = ET.fromstring(glif_data)
			#
			name = glif_parse.get('name')
			res_width = int(glif_parse.findall('advance')[0].get('width'))
			#
			if name not in seen_glifs:
				#
				if name in needed_glifs:
					#
					#
					try:
						#
						out_start = "<outline>"
						out_end = "</outline>"
						#
						result=get_between(out_start, out_end, glif_data)
						#
						base_contours[name] = [basename(file),result,res_width]
						#
					except Exception:
						#
						print('FAILED FOR GLIF: ', name)
						#
					#
					seen_glifs.append(name)
					#
				#
			#
			the_file.close()
			#
	return base_contours, res_width

#
def rebase_accent(acc_orig, acc_dest, glif_loc, _acc_pos):
	#
	
	#print(acc_orig, acc_dest, glif_loc)
	#
	acc_orig_glif = os.path.join(glif_loc, acc_orig+'.glif')
	acc_dest_glif = os.path.join(glif_loc, acc_dest+'.glif')
	#
	exist_orig = os.path.isfile(acc_orig_glif)
	exist_orig_comp = False
	exist_dest = os.path.isfile(acc_dest_glif)
	exist_dest_comp = False
	#
	if exist_orig:
		#
		with open(acc_orig_glif, 'r') as o_f:
			#
			o_f_r = o_f.read()
			#
			comp_o = '<component base="'+acc_dest+'"/>'
			#
			if comp_o in o_f_r:
				#
				#print(acc_orig+'INCLUDES: '+acc_dest, end='')
				#
				exist_orig_comp = True
				#
			#
		#
	#
	else:
		#
		#print('NON EXIST: '+ acc_orig, end='')
		#
		if acc_orig not in non_exist:
			#
			non_exist.append(acc_orig)
			#
		#
	#
	if exist_dest:
		#
		with open(acc_dest_glif, 'r') as d_f:
			#
			d_f_r = d_f.read()
			#
			comp_d = '<component base="'+acc_orig+'"/>'
			#
			if comp_d in d_f_r:
				#
				#print(acc_dest+'INCLUDES: '+acc_orig, end='')
				#
				exist_dest_comp = True
				#
			#
		#
	#
	else:
		#
		print('NON EXIST: ', acc_dest)
		#
	#
	if exist_orig and exist_dest:
		#
		if exist_dest_comp:
			#
			pass
			#print('\r\t\t'+'>>>>>' + 'OK'+flush_space+'\n',end='' )
			#
		else:
			#
			print('\r\t\t'+'>>>>>' + 'NOK')
			print('\r\t\t'+'>>>>>' + 'combs should not include components, original accents should include comb components'+flush_space+'\n')
			#
			#print(acc_dest_glif)
			#print(acc_orig_glif)
			#
			exchange_replace_contour(acc_dest, acc_dest_glif, acc_orig_glif, acc_orig, _acc_pos)
			#
		#
#
def exchange_replace_contour(acc_dest, acc_dest_glif, acc_orig_glif, comb_accent_name, _acc_pos):
	#
	accent_comp = '\n    <component base="{0}"/>\n  '.format(comb_accent_name)
	pos_anchors = ''
	eventual_pos_y = comb_top_accent_pos_y
	#
	is_accent_info = get_base_glif_width(acc_dest_glif, comb_accent_name, True)
	#
	if _acc_pos == 'top':
		#
		eventual_pos_x = 0
		#
		if 'tonos' in is_accent_info[0]:
			#
			pos_anchors = comp_anchors_top_tonos.format(int(is_accent_info[1]/2), int(eventual_pos_y))
			#
		else:
			#
			pos_anchors = comp_anchors_top.format(int(is_accent_info[1]/2), int(eventual_pos_y))
			#
		#
	else: 
		#
		eventual_pos_y = 0
		#
		if "ogonek" in is_accent_info[0]:
			#
			#print('IS OGONEK')
			#
			pos_anchors = comp_anchors_bot_ogonek.format(int(eventual_pos_y), int(is_accent_info[1]/2))
			#
		else:
			#
			pos_anchors = comp_anchors_bot.format(int(eventual_pos_y), int(is_accent_info[1]/2))
			#
		#
	#
	replaced_a = replace_contour(accent_comp, acc_dest_glif, True) +'  '+ pos_anchors + '\n'
	#
	replace_contour(replaced_a, acc_orig_glif, False)
	#
def replace_contour(_this, _here, _return_replaced, _clean = False):
	#
	out_start = "<outline>"
	out_end = "</outline>"
	#
	replacement = ''
	#
	with open(_here, 'r') as rf:
		#
		glif_data = rf.read()
		#
		result=get_between(out_start, out_end, glif_data)
		#
		#
		if _clean:

			# #
			# tree = ET.fromstring(glif_data)
			# etree_str = ET.tostring(tree, encoding="unicode", method='xml')
			# #
			replacement = clean_base_contour(result)

			print('==============')
			print(replacement)
			print('==============')

		else:

			replacement = result
		#
		rf.close()
		#
		#
		with open(_here, 'w') as wf:
			#
			result = glif_data.replace(replacement, _this)
			#
			if _return_replaced and _clean:
				#
				return result
				#
			#
			wf.write(result)
			#
			wf.close()
			#
	#
	if _return_replaced:
		#
		return result
		#
	#
#

def replace_contour_b(_this, _here, _return_replaced):
	#
	with open(_here, 'w') as wf:
		#
		wf.write(_this)
		#
		wf.close()
		#
#
def get_matching_contour(base_cont, rep_cont):
	#
	parser = etree.XMLParser(remove_blank_text=True)
	#
	base_cont_list = [ e for e in html.fromstring(base_cont).iter() if e.tag == 'contour']
	rep_cont_list = [ e for e in html.fromstring(rep_cont).iter() if e.tag == 'contour']
	#
	final_match = []
	seen_ = []
	#
	keep_index = []
	#
	for x in base_cont_list:
		#
		_e_base = etree.tostring(x, encoding='unicode', pretty_print=True)
		_e_base_test = ''.join([i for i in _e_base if not i.isdigit()])
		#
		for y in rep_cont_list:
			#
			_e_rep = etree.tostring(y, encoding='unicode', pretty_print=True)
			_e_rep_test =  ''.join([i for i in _e_rep if not i.isdigit()])
			#
			inner_diff_ratio = difflib.SequenceMatcher(a=_e_base_test,b=_e_rep_test).ratio()		
			#
			if _e_rep in seen_ :
				pass
			else:
				if inner_diff_ratio > 0.7:
					#
					keep_index.append(1)
					#
					final_match.append(_e_rep)
					#
				else:
					#
					keep_index.append(0)
					#
					final_match.append(_e_rep)
					#
				#
			seen_.append(_e_rep)
			#
	final_string = ''
	#
	c = 0
	#
	for x in keep_index:
		#
		if x == 0:
			#
			try:

				final_string = final_string + final_match[ c ]

			except Exception:
				pass
			#
		#
		c = c + 1
		#
	#
	return final_string
	#
#
def do_repos_anchors(self,name, _type, _comb_name=""):
	#
	_x = 0
	_y = 0
	#
	if len(self.anchor_offsets) > 0:
		#
		if self.anchor_offsets[self.current_font_name]:
			#
			if name in self.anchor_offsets[self.current_font_name][_type]:
				#
				if _type == "base":
					#
					_x = self.anchor_offsets[self.current_font_name][_type][name][_comb_name][0]
					_y = self.anchor_offsets[self.current_font_name][_type][name][_comb_name][1]
					#
				else:
					#
					_x = self.anchor_offsets[self.current_font_name][_type][name][0]
					_y = self.anchor_offsets[self.current_font_name][_type][name][1]
					#
					#print('\n'+name)
					#
			#
			#print(">>>>>>>>>>>>>>>", name[0].isupper())
			#
			if name[0].isupper() == False:
				#
				#print(name, _y)
				#print('+===============================')
				#
				if name not in tall_small_case:
					#
					_y = _y - self.anchor_offsets[self.current_font_name]["metric"]["x_height_accent_pos_y"]
					#
				#
			
		#
	#
	_x = _x + self.anchor_offsets[self.current_font_name]["metric"]["x_offset"]
	_y = _y + self.anchor_offsets[self.current_font_name]["metric"]["y_offset"] # 
	#
	return _x, _y
	#
#
def accent_logic(name,_pos):
	#
	accent_name = ''
	rebased = ''
	#
	if _pos == "top":
		#
		combs = comb_top
		rebase_combs = comb_top_rebase
		#
	else:
		#
		combs = comb_bot
		rebase_combs = comb_bot_rebase
		#
	#
	if 'uni' in name:
		#
		if name == 'uni021B' or name == 'uni021A':
			#
			if name == 'uni021B':
				#
				u_name = 'tcommaaccent'
				accent_name = 'commaturnedbelowcomb'
				#
			#
			if name == 'uni021A':
				#
				u_name = 'Tcommaaccent'
				accent_name = 'commaturnedbelowcomb'
				#
			#
		#
		name = u_name
		#
		rebased = 'commaaccent'
		#
	elif name in l_dots_list:
		#
		u_name = 'dotaccentcomb'
		accent_name = 'dotaccentcomb'
		#
		rebased = u_name
		#
	elif "tonos" in name:
		#
		if "dieresis" in name:
			#
			u_name = 'dieresistonoscomb'
			accent_name = 'dieresistonoscomb'
			#
		else:
			#
			u_name = 'tonoscomb'
			accent_name = 'tonoscomb'
			#
		#
		rebased = u_name
		#
	elif 'commaaccent' in name:
		#
		#
		if name == 'gcommaaccent':
			#
			rebased = 'commaturnedabove'
			accent_name = 'commaturnedabovecomb'
			#
		else:
			#
			rebased = 'commaaccent'
			accent_name = 'commaturnedbelowcomb'
			#
		#
	else:
		#
		x = 0
		#
		for c_t in combs:
			#
			if 'comb' in c_t:
				#
				accent = c_t.replace('comb', '')
				#
			#
			else:
				#
				accent = c_t
				#
			#
			if accent in name: 
				#
				rebased = rebase_combs[x]
				#
				accent_name = c_t
				#
				if 'croat' in c_t:
					#
					rebased = 'macroncomb'
					accent_name = 'macroncomb'
					#
				#
			#
			x = x + 1
		#
	#
	return accent_name, rebased, name
	#
#
def check_accents (self, name, combs, rebase_combs, _dir_glif, glif_width):
	#
	created_accent = ''
	#
	for _pos in ["top", "bot"]:
		#
		acl = accent_logic(name, _pos)
		#
		accent_name = acl[0]
		rebased = acl[1]
		name = acl[2]
		#
		if len(accent_name) > 0: 
			#
			created_accent = create_accent_comp(self, name, accent_name, _dir_glif, rebased, _pos, glif_width)
			#
		#
	#
	return created_accent, accent_name
	#
#
def create_accent_comp(self, name, accent_name, _dir_glif, rebased, _pos, glif_width):
	#
	#
	_x = 0
	_y = 0
	#
	accent_comp = ''
	#
	accent_location = os.path.join(self._dir_glif, accent_name+'.glif')
	#
	accent_width = int(get_base_glif_width(accent_location, accent_name, True)[1])
	#
	#print('accent_width', accent_width)
	#
	rebase_accent(accent_name, rebased, _dir_glif, _pos)
	#
	#
	if _pos == 'top':
		#
		_x = int(glif_width/2) - (accent_width/2)
		_y = 0#- self.anchor_offsets[self.current_font_name]["metric"]["y_offset"]
		#
		if name[0].isupper():
			#
			_y = 0
			#
		#
		if name[0] in tall_small_case:
			#
			if "caron" in name or "circumflex" in name or "acute" in name:
				#
				_y = _y + 140
				#
			#
		#
	else:
		#
		_x = int(glif_width/2) - (accent_width/2)
		_y = - 150#- self.anchor_offsets[self.current_font_name]["metric"]["y_offset"]
		#
		if name[0].isupper() == False:
			#
			#print(name, _y)
			#print('+===============================')
			#
			if name not in tall_small_case:
				#
				_y = _y + 150
				#
			#
	#
	if "tonos" in name:
		#
		if name[0].isupper():
			#
			_y = _y + 100
			#
		#
	#

	repos = do_repos_anchors(self,name, "component")
	#
	_x = _x + repos[0]
	_y = _y + repos[1]
	#
	accent_comp = '<component base="{0}" xOffset="{1}" yOffset="{2}"/>'.format(accent_name, str(_x), str(_y))
	#
	return accent_comp
	#
#
def check_anchors_exist(_comb_glif, _comb_name):
	#
	with open(_comb_glif, 'r') as f:
		#
		glif_data = f.read()
		#
		tree = ET.fromstring(glif_data)
		#
		anchors = tree[0].find('anchor')
		#
		if anchors == None:
			#
			print ("COMB Should Include Anchors")
			#
			glif_info_width = str(get_base_glif_width(_comb_glif, _comb_name, True)[1] / 2)
			#
			if _comb_name in comb_top:
				#
				if "tonoscomb" in _comb_name:
					#
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="750", name="tonos")
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="600", name="_tonos")
					#
				else:
					#
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="750", name="top")
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="600", name="_top")
					#
				#
			elif _comb_name in comb_bot:
				#
				if "ogonek" in _comb_name:
					#	
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="-250", name="ogonek")
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="0", name="_ogonek")
					#
				else:
					#	
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="-250", name="bottom")
					ET.SubElement(tree[0], "anchor", x=glif_info_width, y="0", name="_bottom")
					#
				#
			#
			f.close()
			#
			with open(_comb_glif, 'w') as f:
				#
				f.write('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(tree, encoding="unicode", method='xml'))
				f.close()
				#
			#
		else:
			#
			pass
			#
		#
	#
#
def create_appropriate_anchors():
	#
	pass
	#
#
def determine_accent():
	#
	pass
	#
#
#
out_start = "<outline>"
out_end = "</outline>"
#
def clean_base_contour(base_contour):
	tree = ET.fromstring(out_start+base_contour+out_end)
	#
	#
	etree_str = ET.tostring(tree, encoding="unicode", method='xml')
	print(etree_str)
	#
	contours = tree.findall('contour')
	anchors = tree.findall('anchor')
	#
	#
	for elem in tree.iter():
		for child in list(elem):
			if child.tag == 'component':
				elem.remove(child)
			elif child.tag == 'contour':
				#
				for point in list(child):
					#	
					if "move" in str(point.attrib):
						elem.remove(child)
						break
		if elem.tag == 'anchor':
			#
			tree.remove(elem)
			#
	#
	
	#
	etree_str = ET.tostring(tree, encoding="unicode", method='xml')
	print(etree_str)
	#
	result=get_between(out_start, out_end, etree_str)
	#
	#print(result)
	#
	return result
	#base_anchors_contour_calc = base_anchors_contour.format(center_pos_x, pos_y, ogonek_pos_x, pos_tonos_x, pos_tonos_y)
	#
	#
#
def run_ufo_glyphs(self, comp_dir_path, ufo_dir_path):
	#
	print('COMP: Componentize')
	#
	self._dir_glif = os.path.abspath(os.path.join(ufo_dir_path, 'glyphs'))
	#
	pl = plistlib.readPlist(comp_dir_path)
	#
	needed_glifs = list(pl)
	#
	run_base = get_base_glif_contours(self._dir_glif, needed_glifs)
	#
	base_contours = run_base[0]
	#
	for x in comb_top + comb_bot:
		#
		if x != "croat":
			#
			comb_dir = os.path.join(self._dir_glif, x+".glif")
			#
			check_anchors_exist(comb_dir, x)
			#
	#
	for o,p in pl.items():
		#
		glif_info = get_base_glif_width(self._dir_glif, o)
		#
		to_replace = list(p)
		#
		to_replace.pop(0)
		#
		run_rep = get_base_glif_contours(self._dir_glif, to_replace)
		get_contours_to_rep = run_rep[0]
		#
		g_width = glif_info[1]
		#
		base_conts = base_contours.get(o)
		#
		for u,t in get_contours_to_rep.items():
			#
			print('\r\t'+'COMP: Base = '+o+', Comp = '+u+flush_space,end='')
			#
			u_name = u
			#
			created_accent = check_accents(self, u_name, comb_bot, comb_bot_rebase, self._dir_glif, t[2])
			#
			base_cont = base_conts[1]
			rep_cont = t[1]
			#
			diff_ratio = difflib.SequenceMatcher(a=base_cont,b=rep_cont).ratio()
			#
			if diff_ratio == 1:
				#
				match_cont = ''
				add_comp = '\n    <component base="{0}"/>'.format(o)
				#
			else:
				#
				match_cont = get_matching_contour(base_cont, rep_cont)
				#
				if len(created_accent[0]) > 0:
					#
					match_cont = ''
					add_comp = '\n    <component base="{0}"/>\n    {1}'.format(o, created_accent[0])
					#
				else:
					#
					add_comp = '\n    <component base="{0}"/>'.format(o)
					#
				#
				glif_now_loc = os.path.join(self._dir_glif,t[0])
				#
			#
			replacement_contour = add_comp+match_cont
			#
			target_glif = os.path.join(self._dir_glif, t[0])
			base_glif = os.path.join(self._dir_glif, base_conts[0])
			#
			replace_contour(replacement_contour, target_glif, False)
			#
			all_combs = comb_top + comb_top_rebase + comb_bot + comb_bot_rebase
			#
			if o not in all_combs and u not in all_combs:
				#
				if glif_info[0][0].isupper() and glif_info[0][0] not in tall_small_case:
					#
					pos_y = base_top_accent_tall_pos_y
					#
				else:
					#
					pos_y = base_top_accent_short_pos_y
					#
				#
				center_pos_x = int(g_width/2)
				ogonek_pos_x = int(g_width/3) + int(g_width/6) 
				#
				#
				if glif_info[0][0].isupper() == False and glif_info[0][0] not in tall_small_case:
					#
					pos_tonos_y = pos_y
					pos_tonos_x = center_pos_x
					#
				else:
					#
					pos_tonos_y = base_top_accent_tall_tonos_pos_y
					pos_tonos_x =  int(g_width/6) 
					pos_y = base_top_accent_tall_pos_y
					#
				#
				clean_base_cont = clean_base_contour(base_cont)
				#
				if (_format == 2):
					base_anchors_contour_calc = ''
					base_anchors_calc = '' #base_anchors.format(center_pos_x, pos_y, ogonek_pos_x, pos_tonos_x, pos_tonos_y)
				else:
					base_anchors_contour_calc = base_anchors_contour.format(center_pos_x, pos_y, ogonek_pos_x, pos_tonos_x, pos_tonos_y)
					base_anchors_calc = ''
				#
				#
				#
				base_anchors_calc = base_anchors.format(center_pos_x, pos_y, ogonek_pos_x, pos_tonos_x, pos_tonos_y)
				#
				replace_contour(base_cont, base_glif, False, True)
				#
				#data = replace_contour(base_anchors_calc+clean_base_cont+base_anchors_contour_calc, base_glif, True, True)
				#
				#print(data)
			#
		#
	#
	print('\nNOT EXISTING GLYPHS')
	print(non_exist)
	print('\nNOT COMPONENTIZED GLYPHS')
	print(non_comp)
#
