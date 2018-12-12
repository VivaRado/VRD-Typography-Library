import os
import sys
from os.path import dirname, join, abspath
#
import datetime
#
import json
#
#from Lib.efo import efo_fontinfo
#
from Lib.generic import generic_tools
#
#import os
# import io
import random
from math import sqrt, ceil, floor
#import datetime
import string
#
import itertools
#
import sys
from sys import argv
import re
#
import readline 
import rlcompleter 
from argparse import ArgumentParser
import atexit
#
import io
#
from shutil import copyfile
#
import copy
#
import difflib
import plistlib
import pprint
#import json
#
import collections
from collections import Counter
#
ignore_glyphs = []
#
plist_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>\n'''
#
#
plist_footer = '''\n</dict>\n</plist>'''
#
plist_string = '''		<key>{0}</key>
		<integer>{1}</integer>'''
#
plist_group = '''	<key>{0}</key>
	<dict>
{1}\n	</dict>\n'''
	#
#
fea_pos_line = '''pos {0} {1} {2};'''
do_fea_groups = ''
do_fea_kern = ''
#
flc_file_header = '''%%FONTLAB CLASSES\n\n'''
#
flc_content = '''%%CLASS _{0}
%%GLYPHS  {1}' {2}
%%KERNING {3} 0
%%END\n\n'''
#
fea_class_content = '''@{0} = [{1} {2}];\n'''
#
fea_prefix = '''# Languagesystems Start
# Prefix: Languagesystems
languagesystem DFLT dflt;
languagesystem grek dflt;
languagesystem latn dflt;
# Languagesystems End\n\n'''
#
class COMPRESS(object):
	#
	def __init__(self, _f_name, _temp_source, _temp_source_copy, _source_efo_similarity_kern_plist):
		#
		self._current_font_instance_weight = _f_name
		self._temp_source = _temp_source
		self._temp_source_copy = _temp_source_copy
		self._source_efo_similarity_kern_plist = _source_efo_similarity_kern_plist
		#
	#
	#
	def get_kern_name_and_dir(self, k):
		#
		ld = k.split('@MMK_')[1]
		ds = ld.split('_', 1)
		kd = ds[0]
		lt = ds[1]
		#
		return[lt, kd]
		#
	#
	def make_fea_class_lines(self,p_g):
		# #
		all_kern_flc = ''
		#
		for k,v in p_g.items():
			#
			k_spl = self.get_kern_name_and_dir(k)
			kern_name = k_spl[0]
			kern_dir = k_spl[1]
			#
			v.sort()
			#
			try:
				#
				v.remove(kern_name)
				v.insert(0, kern_name)
				#
			except Exception:
				#
				v.insert(0, kern_name)
				#
			#
			v.pop(0)
			#
			num_dir = ''
			#
			if kern_dir == 'R':
				#
				num_dir = '1'
				#
			#
			all_kern_flc = all_kern_flc + fea_class_content.format(kern_name+num_dir, kern_name, ' '.join(v), kern_dir)
			#
		#
		return all_kern_flc
	#
	def make_kern_lines_dict(self, f_kern_data):
		#
		all_kern_plist = ''
		plist_strings = ''
		#
		kern_dict = {}
		#
		for x in f_kern_data:
			#
			let_a = x[0]
			let_b = x[1]
			k_int = x[2]
			#
			if let_a in kern_dict:
				#
				kern_dict[let_a].update({let_b:k_int})
				#
			else:
				#
				kern_dict[let_a] = {let_b:k_int}
				#
			#
		#
		return kern_dict
	#
	#
	def make_kern_lines(f_kern_data):
		#
		all_kern_plist = ''
		plist_strings = ''
		#
		for x in f_kern_data:
			#
			let_a = x[0]
			let_b = x[1]
			k_int = x[2]
			#
			plist_strings = plist_string.format(let_b,k_int)
			#
			all_kern_plist = all_kern_plist + plist_group.format(let_a, plist_strings)
			#
			#
		#
		all_kern_plist = plist_header + all_kern_plist + plist_footer
		#
		return all_kern_plist
	#
	def get_kern_int(self, left, right, p_k):
		#
		found_int = 0
		#
		for k,v in p_k.items():
			#
			if k == left:
				#
				for x,y in v.items():
					#
					if x == right:
						#
						found_int = y
						#
						break
						#
					#
				#
			#
		#
		return found_int
		#
		#
	#
	def remove_redundant_kern_values(self, final_ckp, _dict):
		#
		tmpDict = _dict.copy()
		#
		for z in final_ckp:
			#
			left = z[0]
			right = z[1]
			#
			for k,v in tmpDict.items():
				#
				if k == left:
					#
					for x,y in v.items():
						#
						if x == right:
							#
							_dict = generic_tools.get_dict_wo_key(_dict, k)
							#
						#
					#
				#
			#
		return _dict
		#
	#
	def do_fea_kern_file(self, final_class_kern_pairs):
		#
		for y in final_class_kern_pairs:
			#
			k_dir = y[3]
			k_int = y[2]
			#
			let_a = self.get_kern_name_and_dir(y[0])
			let_b = self.get_kern_name_and_dir(y[1])
			#
			fea_line = fea_pos_line.format('@_'+let_a[0], '@_'+let_b[0]+'1', str(k_int))
			#
			self.final_class_kerning.append(fea_line)
			#
		#
	#
	def fea_kern_list_to_file(self, final_kerning_list):
		#
		kern_strings = '''# Kerning Start

feature kern { # Kerning
# DEFAULT
lookup kern1 {\n'''
		#
		for y in final_kerning_list:
			#
			kern_strings = kern_strings +'    '+y + '\n'
			#
		#
		kern_strings = kern_strings + '''}kern1;
script grek; # Greek
lookup kern1;
script latn; # Latin
lookup kern1;
} kern;
# Kerning End'''
		#
		return kern_strings
		#
	#
	def permut_plist_keys(self, g_plist_keys):
		#
		g_plist_permut = []
		#
		for o in g_plist_keys:
			#
			ltkd_a = self.get_kern_name_and_dir(o)
			#
			for p in g_plist_keys:
				#
				ltkd_b = self.get_kern_name_and_dir(p)
				#
				if ltkd_a[1] == 'R' and ltkd_b[1] == 'R':
					#
					pass
					#
				elif ltkd_a[1] == 'L' and ltkd_b[1] == 'L':
					#
					pass
					#
				else:
					#
					if ltkd_a[1] == 'R' and ltkd_b[1] == 'L':
						#
						g_plist_permut.append([p,o])
						#
					#
					elif ltkd_a[1] == 'L' and ltkd_b[1] == 'R':
						#
						g_plist_permut.append([o,p])
						#
					#
			#
		#
		g_plist_permut.sort()
		#
		result_permut = list(g_plist_permut for g_plist_permut,_ in itertools.groupby(g_plist_permut))
		#
		return result_permut
		#
	#
	def remove_class_replace(self, p_k_clean, class_groups):
		#
		for x,j in class_groups.items():
			#
			if '@MMK_R_' in x:
				#
				first_letter = x.replace('@MMK_R_','')
				#
			else:
				#
				first_letter = x.replace('@MMK_L_','')
				#
			#
			j.append(first_letter)
			#
		#
		for k,v in p_k_clean.items():
			#
			wanted_list = []
			#
			for d,b in v.items():
				#
				wanted_list.append(d)
				#
			#
			this_num = 0
			#
			for f,g in class_groups.items():
				#
				match_list = []
				#
				for p in g:
					#
					if p in wanted_list:
						#
						if p not in match_list:
							#
							this_num = p_k_clean[k][p]
							#
							match_list.append(p)
							wanted_list.remove(p)
							#
							del p_k_clean[k][p]
						#
					#
					if match_list == g:
						#
						_right_f = f.replace('_L_','_R_')
						#
						p_k_clean[k][_right_f] = this_num
						#
					#
			#
		#
		return p_k_clean
		#
	#
	def do_fea_kern_file_additions(self, final_class_kern_pairs):
		#
		for k,y in final_class_kern_pairs.items():
			#
			for x,z in y.items():
				#
				k_int = z
				#
				let_a = k
				let_b = x
				#
				if '@MMK_L_' in let_a or '@MMK_R_' in let_a:
					#
					ltkd_a = self.get_kern_name_and_dir(let_a)
					#
					let_a = '@_'+ltkd_a[0]
					#
				if '@MMK_L_' in let_b or '@MMK_R_' in let_b:
					#
					ltkd_b = self.get_kern_name_and_dir(let_b)
					#
					let_b = '@_'+ltkd_b[0]+'1'
					#
				#
				fea_add_line = fea_pos_line.format(let_a, let_b, str(k_int))
				#
				self.final_class_kerning.append(fea_add_line)
				#
			#
		#
	#
	def do_compress(self, p_groups, p_kerning, dir_to_comp_ufo_file):
		#
		p_g = plistlib.readPlist(p_groups)
		p_k = plistlib.readPlist(p_kerning)
		#
		all_kern_plist = ''
		#
		g_plist_keys = []
		all_affected_glyphs = []
		#
		for k,v in p_g.items():
			#
			g_plist_keys.append(k)
			all_affected_glyphs.append(k)
			all_affected_glyphs = all_affected_glyphs + v
			#
		#
		g_plist_permut = self.permut_plist_keys(g_plist_keys)
		#
		final_class_kern_pairs = []
		self.final_class_kerning = []
		#
		for pk in g_plist_permut:
			#
			ltkd_a = self.get_kern_name_and_dir(pk[0])
			ltkd_b = self.get_kern_name_and_dir(pk[1])
			#
			kern_int = self.get_kern_int(ltkd_a[0], ltkd_b[0], p_k)
			#
			#
			if kern_int == 0:
				pass
			else:
				#
				k_dir = ltkd_a[1]
				#
				if k_dir == "L":
					#
					kern_detail = [pk[0], pk[1], kern_int, k_dir]
					#
				else:
					#
					kern_detail = [pk[1], pk[0], kern_int, k_dir]
					#
				#
				final_class_kern_pairs.append(kern_detail)
				#
			#
		#
		all_affected_glyphs_permut = []
		#
		for x in all_affected_glyphs:
			#
			for y in all_affected_glyphs:
				#
				all_affected_glyphs_permut.append([x,y])
				#
			#
		#
		old_pg = generic_tools.copy_dict(p_g)
		old_p_k = generic_tools.copy_dict(p_k)
		#
		fea_classes = '# Classes Start\n'+self.make_fea_class_lines(old_pg)+'# Classes End\n\n'
		#
		p_k_clean = self.remove_redundant_kern_values(all_affected_glyphs_permut,old_p_k)
		p_k_class_replace = self.remove_class_replace(p_k_clean, old_pg)
		#
		self.do_fea_kern_file(final_class_kern_pairs)
		self.do_fea_kern_file_additions(p_k_class_replace)
		#
		#
		new_data = fea_prefix+fea_classes+self.fea_kern_list_to_file(sorted(self.final_class_kerning, key=lambda x: x.count('@_')))
		generic_tools.save_file(dir_to_comp_ufo_file, 'features'+'.fea', new_data)
		#
		#
		class_kerning_plist = self.make_kern_lines_dict(final_class_kern_pairs)
		total_kerning = class_kerning_plist.update(p_k_class_replace)
		k_c_temp = 'kerning'+'.plist'
		dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(dir_to_comp_ufo_file,k_c_temp)))
		plistlib.writePlist(class_kerning_plist, dstFile)
		#
		self.compressed_plist = dstFile
		#
	#
	def permute_direction(self,l):
		#
		'''
		split the simex group keys list to Left and Right lists
		'''
		#
		directional_permute = []
		#
		avoid_r = []
		#
		for _left in l:
			#
			for _right in l:
				#
				if "@MMK_L_" in _right or "@MMK_R_" in _left: # if left in right or right in left pass
					#
					pass
					#
				else:
					#
					directional_permute.append([_left,_right])
					#
				#
			#
		#
		dups = sum(y for y in Counter(tuple(x) for x in directional_permute).values() if y > 1)
		#
		print("Directional Permutation Result Size:", len(directional_permute), "Duplicates:", dups)
		#
		return directional_permute
		#
	#
	def get_group_items_unique_keep_order(self, _dict, _pair):
		#
		'''
		get group items from simex group list for each given pair,
		keep order and combine each items pair.
		'''
		#
		g_lst = []
		#
		for k,v in _dict.items():
			#
			if k == _pair[0] or k == _pair[1]:
				#
				g_lst.append(v)
				#
			#
		#
		ts = set()
		rm_duplicate = lambda l:[x for x in l if not (x in ts or ts.add(x))]
		clean_data = rm_duplicate(g_lst[1])+[i for i in rm_duplicate(g_lst[0]) if i not in g_lst[1]]
		#
		return clean_data
		#
	#
	def get_group_items(self, _dict, _letter):
		#
		'''
		get group items from simex group list for letter
		'''
		#
		g_lst = []
		#
		for k,v in _dict.items():
			#
			if k == _letter:
				#
				g_lst.extend(v)
				#
			#
		#
		return g_lst
		#
	#
	def transfer_delete_kern_value(self, _p_f, _input, _g_items, _type):
		#
		if isinstance(_input, list):
			#
			p_L = _input[0]
			p_R = _input[1]

			if _type == "GG":

				pair_L = p_L.split("@MMK_L_")[1]

			else:
				
				pair_L = p_L

			#
			pair_R = p_R.split("@MMK_R_")[1]
			#
			if _type == "GG":
				op_long = "GROUP TO GROUP"
			elif _type == "LG":
				op_long = "LETTER TO GROUP"
			#
			print('===')
			print("PROCESSING "+op_long+":", ",".join(_input))
			#
		else:
			#
			p_L = _input
			p_R = False
			pair_L = p_L.split("@MMK_L_")[1]
			pair_R = False
			#_type = "GL"
			#
			print('===')
			print("PROCESSING GROUP TO ANY LETTER:", p_L)
			#
		#
		for k,v in _p_f.items():
			#
			if k == pair_L:
				#
				len_before = len(self.p_f_copy[k])
				#
				for x in v:
					#
					if p_R == False:
						#
						pair_R = x
						p_R = x
						#
					#
					if x == pair_R:
						#
						if x in self.p_f_copy[k]:
							#
							print('===')
							#
							k_int = int(self.p_f_copy[k][x])
							#
							print("\tTRANSFERING: ", p_L, p_R, "VALUE: ", k_int)
							#
							# transfer pair and value to compressed dictionary
							if p_L in self.p_c[_type]:
								#
								self.p_c[_type][p_L].update( {p_R:k_int} ) #0003 #0006
								#
							else:
								#
								self.p_c[_type][p_L] = {p_R:k_int} #0003 #0006
								#
							#
							# delete item from flat copy dictionary #0004
							print("\t\tDELETING:", k +' > '+ x)
							del self.p_f_copy[k][x]
							#
							if len(_g_items) > 0:
								#
								if x in _g_items:
									# delete item from group items list
									_g_items.remove(x)
								#
					#
					if _type == "GL":
						#
						p_R = False
						#
					#
				#
				#print(_g_items)
				#
				if len(_g_items) > 0:
					#
					for y in _g_items:
						#
						print("\t\tDELETING:", k +' > '+ y)
						#
						# delete group items list item from flat copy dictionary
						if y in self.p_f_copy[k]:
							#
							del self.p_f_copy[k][y] #0004
							#
						#
				#
				print("\tFLAT COPY LENGTH:", "Before:", len_before, "After:", len(self.p_f_copy[k]))
				#
			#
		#
	#
	def test_compress(self, flat, simex_groups):
		#
		#
		'''
		compress logic:

			get sim list
				sim list includes L and R sim groups
				
				Group to Group (GG): 
					permute L side with any R side from simex #0001
					for items in permut list
						get unique group items of simex L and R groups #0002
						gather int value from flat list provided L and R #0003
						remove the group contents from the flat list that are in L R simex unique group #0004
					# deleting from flat_copy in matches of permut list, the group items of both simex groups since they are covered by the both group contents

				Group to Letter (GL):
					list simex keys with L #0005
					for L simex keys
						gather values from flat kerning provided key L #0006
						remove values from flat kerning provided key L #0007
						remove group items included in flat groups
					# deleting from flat_copy in matches of permut list, the group items of L simex group since they are covered by Group to Group

				Letter to Group (LG):
					list simex keys with R #0008
					gather groups that include key R from flat kerning
					get keys from those groups
					permute flat keys on left side not in simex group keys and not in all simex group items with key R
					for items in permut list
						gather values from flat kerning
						remove the values gathered from flat list and values in simex R group items
					# deleting from flat_copy in matches of permut list, the group items of R simex group since they are covered by the R group contents


				Letter to Letter (LL):
					whatever key remains in flat list and is not key in simex
					# deleting all simex group items that are keys in flat_copy because they are covered in GG or GL #0009

		'''
		#
		#
		self.p_c = {"GG":{},"GL":{},"LG":{},"LL":{}}
		#
		p_f = plistlib.readPlist(flat)
		#
		self.p_f_copy = copy.deepcopy(p_f)
		#
		p_g = plistlib.readPlist(simex_groups)
		#
		all_group_items = []
		#
		#


		# \/ Group to Group (GG)
		#
		# #\/0001
		p_g_keys = list(p_g.keys())
		permute_directional= self.permute_direction(p_g_keys)
		# #/\0001
		#
		#
		# #\/0002
		for x in permute_directional:
			#
			group_items_for_pair = self.get_group_items_unique_keep_order(p_g,x)
			#
			all_group_items.extend(group_items_for_pair)
			#
			self.transfer_delete_kern_value(p_f, x, group_items_for_pair, "GG")
			#
		# #/\0002
		#
		# /\


		# \/ Group to Letter (GL)
		#
		#
		p_g_keys_L = [x for x in p_g_keys if x.startswith('@MMK_L_')] #0005
		#
		for y in p_g_keys_L:
			#
			group_items_for_L = self.get_group_items(p_g,y)
			#
			self.transfer_delete_kern_value(p_f, y, group_items_for_L, "GL")
			#
		#
		# /\


		# \/ Letter to Group (LG)
		#
		p_g_keys_R = [x for x in p_g_keys if x.startswith('@MMK_R_')] #0008
		#
		p_f_LG_permut = []
		#
		p_f_keys = list(p_f.keys())
		#
		for k,v in self.p_f_copy.items():
			#
			if "@MMK_L_"+k not in p_g_keys and "@MMK_R_"+k not in p_g_keys: # dealt with on GG
					
				for d in p_g_keys_R:
					#
					if k not in all_group_items: # dealt with on GG
						#
						p_f_LG_permut.append([k,d])
						#
					#
				#
			#
		#
		for z in p_f_LG_permut:
			#
			group_items_for_R = self.get_group_items(p_g,z)
			#
			self.transfer_delete_kern_value(p_f, z, group_items_for_R,"LG")
			#
		#
		# /\


		# \/ Letter to Letter (LL)
		#
		# #0009
		for q in all_group_items: 
			#
			if q in list(self.p_f_copy.keys()):
				#
				del self.p_f_copy[q]
				#
			#
		#
		# /\
		
		pprint.pprint(self.p_f_copy)
		#
		p_f_combine = []
		#
	#
	def do_class_kern_replacement(self):
		#
		dir_flat_ufo_file = self._temp_source
		dir_to_comp_ufo_file = self._temp_source_copy
		file_base_group = self._source_efo_similarity_kern_plist
		#
		dir_flat_ufo_file_kern=os.path.join(dir_flat_ufo_file,'kerning.plist')
		#
		#copyfile(file_base_group, os.path.join(dir_to_comp_ufo_file,'groups.plist'))
		#
		print('Compressing:', self._current_font_instance_weight)
		#
		#self.do_compress(file_base_group, dir_flat_ufo_file_kern, dir_to_comp_ufo_file)
		#
		self.test_compress(dir_flat_ufo_file_kern, file_base_group)
		#
	#