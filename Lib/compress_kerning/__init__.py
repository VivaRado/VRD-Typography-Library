#
import os
import re
import io
import sys
#import os
import sys
import json
# import io
import copy
#import json
import random
import string
#import atexit
import pprint
import difflib
import datetime
import plistlib
#import datetime
import itertools
#import readline 
import collections
import rlcompleter 
from sys import argv
from shutil import copyfile
from collections import Counter
#from Lib.efo import efo_fontinfo
from math import sqrt, ceil, floor
from argparse import ArgumentParser
from Lib.generic import generic_tools
from os.path import dirname, join, abspath
#
ignore_glyphs = []
#
fea_pos_line = '''    pos {0} {1} {2};'''
#
#flc_file_header = '''%%FONTLAB CLASSES\n\n'''
#
#flc_content = '''%%CLASS _{0}
#%%GLYPHS  {1}' {2}
#%%KERNING {3} 0
#%%END\n\n'''
#
fea_class_content = '''@{0} = [{1} {2}];\n'''
#
fea_prefix = '''# Languagesystems Start
# Prefix: Languagesystems
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem grek dflt;
# Languagesystems End\n\n'''
#
kern_script_lang = '''
    script grek; # Greek
    script latn; # Latin
    script DFLT; # Default
'''
#
kern_header = '''# Kerning Start \n\nfeature kern { # Kerning\n'''
kern_footer = '''\n} kern;\n# Kerning End'''
#
kern_feature_header = '''\n    # ------
    # {0}
    # ------

    lookup kern_{1} useExtension {{\n'''
#
kern_feature_footer = '''
    }} kern_{0};
'''
#
features_display_style = "@" # @ or MMK : only @ style compiles on variable
#
do_patch = True
#
class COMPRESS(object):
	#
	def __init__(self, EFO,_f_name, _temp_source, _temp_source_copy, _source_efo_similarity_kern_plist, _compress_pattern = False):
		#
		self._in_efo = EFO._in
		self._current_font_instance_weight = _f_name
		self._temp_source = _temp_source
		self._temp_source_copy = _temp_source_copy
		self._source_efo_similarity_kern_plist = _source_efo_similarity_kern_plist
		#
		self._compress_pattern = _compress_pattern
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
	def join_lookups(self, _lu):
		#
		return '{0}{1}{2}'.format('    lookup kern_', ';\n    lookup kern_'.join(_lu), ';')
		#
	#
	def make_kern_fea_lines(self, patch_list):
		#
		#
		p_uni_calues = []
		fea_kerning_lines = []
		#
		all_kern_fea_str = kern_header
		#
		j = 0
		#
		kerning_lookups = []
		#
		for k,v in self.p_c.items():
			#
			type_long = self.get_long_type(k,True)
			#
			kerning_lookups.append(type_long)
			#
			z = 0
			#
			fea_lines = []
			#
			for _k, _v in self.p_c[k].items():
				#
				
				#
				if z == 0:
					#
					all_kern_fea_str = all_kern_fea_str + kern_feature_header.format(k,type_long)
					#
				#
				#
				y = 0
				#
				for __k, __v in self.p_c[k][_k].items():
					#
					self.stats[k] = self.stats[k]+1
					#
					L_pair = _k
					R_pair = __k
					#
					let_a = L_pair
					let_b = R_pair
					#
					if features_display_style == "@":
						#
						if "MMK_" in L_pair:
							#
							ltkd_a = self.get_kern_name_and_dir(L_pair)
							let_a = '@_'+ltkd_a[0]
							#
						#
						if "MMK_" in R_pair:
							#
							ltkd_b = self.get_kern_name_and_dir(R_pair)
							#
							add_one = ''
							#
							if R_pair in list(self.p_g.keys()):
								#
								add_one = '1'
								#
							let_b = '@_'+ltkd_b[0]+add_one
							#
						#
					#
					fea_line = fea_pos_line.format(let_a, let_b, str(__v))
					#
					fea_lines.append(fea_line)
					#
					y = y + 1
					#
					#
				#
				z = z + 1
				#
				#
				if z == len(self.p_c[k].items()):
					#
					sorted_fea = sorted(fea_lines, key=lambda x: x.count('@_'))
					#
					if do_patch == True and k == "LL":
						#
						for x in patch_list:
							#
							if x[3] == self._current_font_instance_weight:
								#
								_cL = x[0]
								_cR = x[1]
								_v = x[2]
								#
								if "@" in _cL or "@" in _cR: # pass only Letter to Letter
									#
									pass
									#
								else:
									#	
									print("ADJUSTING LETTER to LETTER FIX: ", _cL,_cR,_v)
									#
									fea_line = fea_pos_line.format(_cL, _cR, str(_v))
									#
									sorted_fea.append(fea_line)
									#
									self.stats['LL'] = self.stats['LL']+1
									#
								#
							#
						#
					#
					type_kern_fea_lines = self.fea_kern_list_to_strings(sorted_fea)
					#
					all_kern_fea_str = all_kern_fea_str + type_kern_fea_lines + kern_feature_footer.format(type_long)
					#
			#
			j = j + 1
			#
			if j == len(self.p_c.items()):
				#
				all_kern_fea_str = all_kern_fea_str + kern_script_lang + self.join_lookups(kerning_lookups) + kern_footer
				#
			#

		#
		fea_classes = self.make_classes_fea()
		#
		generic_tools.save_file(self._temp_source_copy, 'features'+'.fea', fea_prefix+fea_classes+all_kern_fea_str)
		#
	#
	def fea_kern_list_to_strings(self, kern_fea_list):
		#
		kern_strings = ''
		#
		x = 0
		#
		for y in kern_fea_list:
			#
			kern_strings = kern_strings + '    '+y+'\n'
			#
			x = x + 1
		#
		return kern_strings
		#
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
		print("Directional Permutation Result Size:", len(directional_permute))
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
	def get_long_type(self, _type, sanitize=False):
		#
		if _type == "GG":
			op_long = "GROUP TO GROUP"
		elif _type == "GL":
			op_long = "GROUP TO LETTER"
		elif _type == "LG":
			op_long = "LETTER TO GROUP"
		elif _type == "LL":
			op_long = "LETTER TO LETTER"
		#
		if sanitize:
			#
			op_long = re.sub(' ','_',op_long).title()
			#
		#
		return op_long
		#
	#
	def transfer_delete_kern_value(self, _p_f, _input, _g_items, _type):
		#
		log = False
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
			op_long = self.get_long_type(_type)
			#
			if log:
				
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
			if log:
				
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
				if _type == "GG":
					# Add class to itself #0011
					t_glyph = self.get_kern_name_and_dir(p_L)[0]
					mirror = '@MMK_R_'+t_glyph
					#
					if p_L in self.p_c[_type]:
						#
						if mirror not in self.p_c[_type][p_L]:
							#
							self.p_c[_type][p_L].update({mirror:_p_f[t_glyph][t_glyph]})
							#
						#
					#
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
							#
							k_int = int(self.p_f_copy[k][x])
							#
							if log:
								print('===')
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
							if log:
								print("\t\tDELETING:", k +' > '+ x)
							#
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
						if log:
							print("\t\tDELETING:", k +' > '+ y)
						#
						# delete group items list item from flat copy dictionary
						if y in self.p_f_copy[k]:
							#
							del self.p_f_copy[k][y] #0004
							#
						#
				#
				if log:
					print("\tFLAT COPY LENGTH:", "Before:", len_before, "After:", len(self.p_f_copy[k]))
				#
			#
		#
	#
	def round_to_nearest(self, n, m):
		r = n % m
		return n + m - r if r + r >= m else n - r
	#
	def make_kern_plist(self):
		#
		self.p_uni_c = collections.OrderedDict()
		# combining all GG,GL,LG,LL to one PLIST
		#
		for k,v in self.p_c.items():
			#
			for _k,_v in self.p_c[k].items():
				#
				if _k not in self.p_uni_c:
					#
					self.p_uni_c.update({_k: {}})
					#
				#
				for __k,__v in self.p_c[k][_k].items():
					#
					#__v = self.round_to_nearest(__v, 15)
					#
					#if __v != 0:
					#
					self.p_uni_c[_k].update({__k:__v})
					#
					#
				#
			#
		#
		# save kern plist
		k_c_temp = 'kerning'+'.plist'
		dstFile = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(self._temp_source_copy,k_c_temp)))
		#
		plistlib.writePlist(self.p_uni_c, dstFile)
		#
		
	#
	def make_classes_fea(self):
		#
		all_kern_flc = ''
		#
		for k,v in self.p_g.items():
			#
			k_spl = self.get_kern_name_and_dir(k)
			kern_name = k_spl[0]
			kern_dir = k_spl[1]
			#
			#v.sort()
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
			if features_display_style == "@":
				#
				num_dir = ''
				#
				if kern_dir == 'R':
					#
					num_dir = '1'
					#
				#
				new_fea_line = fea_class_content.format(kern_name+num_dir, kern_name, ' '.join(v), kern_dir)
				#
			else:
				#
				num_dir = 'L'
				#
				if kern_dir == 'R':
					#
					num_dir = 'R'
					#
				#
				new_fea_line = fea_class_content.format("MMK_"+num_dir+'_'+kern_name, kern_name, ' '.join(v), kern_dir)
				#
			#
			all_kern_flc = all_kern_flc + new_fea_line
		#
		#
		fea_classes = '# Classes Start\n'+all_kern_flc+'# Classes End\n\n'
		# #
		return fea_classes
		# new_data = fea_prefix+fea_classes+self.fea_kern_list_to_file(sorted(self.final_class_kerning, key=lambda x: x.count('@_')))
		# generic_tools.save_file(dir_to_comp_ufo_file, 'features'+'.fea', new_data)
		# #
		#
		#
	#
	def kern_adjustments(self, adustments_json):
		# 
		adjustments = []
		#
		for k,v in adustments_json.items():
			#
			if (k == self._current_font_instance_weight):
				#
				for _k,_v in v.items():
					#
					_sp = _k.split(" ")
					#
					_cL = _sp[0]
					_cR = _sp[1]
					#
					add_c_L = ""
					add_c_R = ""
					#
					if "@_" in _cL:
						#
						_cL = _cL.replace("@_","")
						add_c_L = "@MMK_L_"
						#
					#
					if "@_" in _cR:
						#
						_cR = _cR.replace("@_","")
						add_c_R = "@MMK_R_"
						#
					#
					#if "@_" in _cL or "@_" in _cR: # pass only Group to Group, Letter to Group, Group to Letter # leave Letter to Letter for final Adjustment Tuning
					#
					adjustments.append([add_c_L+_cL, add_c_R+_cR, int(_v), k])
					#
					#
				#
			#
		#
		return adjustments
		#
	#
	def test_compress(self, flat, simex_groups):
		#
		self.stats = {"GG":0,"GL":0,"LG":0,"LL":0}
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
						add class to itself #0011
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
					# deleting all simex group items that are items in flat_copy because they are covered in GG or GL #0010
				
				Rounding has been also applied.

		'''
		#
		ka_dir = os.path.join(self._in_efo,"kerning","adjustments.json")
		#
		
		#
		self.adustments_json = json.load(open(ka_dir, "r"))
		#
		#
		self.p_c = collections.OrderedDict()
		self.p_c.update({"GG":{},"GL":{},"LG":{},"LL":{}})
		#self.p_c.update({"GG":{}})
		#
		p_f = plistlib.readPlist(flat)
		#
		self.p_f_copy = copy.deepcopy(p_f)
		#
		self.p_g = plistlib.readPlist(simex_groups)
		#
		all_group_items = []
		#
		#
		

		# \/ Group to Group (GG)
		#
		# #\/0001
		p_g_keys = list(self.p_g.keys())
		permute_directional= self.permute_direction(p_g_keys)
		# #/\0001
		#
		#
		# #\/0002
		#
		for x in permute_directional:
			#
			got_both = 0
			#
			group_items_for_pair = self.get_group_items_unique_keep_order(self.p_g,x)
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
		y = 0
		#
		p_g_keys_L = [x for x in p_g_keys if x.startswith('@MMK_L_')] #0005
		#
		for y in p_g_keys_L:
			#
			group_items_for_L = self.get_group_items(self.p_g,y)
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
			group_items_for_R = self.get_group_items(self.p_g,z)
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
		# #0010
		for k,v in p_f.items():
			#
			if k in self.p_f_copy:
				#
				for x in v:
					#
					if x in all_group_items:
						#
						if x in self.p_f_copy[k]:
							#
							del self.p_f_copy[k][x]
							#
						#
					#
				#
			#
		#
		self.p_c["LL"].update(self.p_f_copy)
		# 
		

		# /\
		#
		# Patch Fix Pair Kerning : 
		# More precise adjustments than those, 
		# meaning bigger numbers, 
		# break kerning on other letters
		kerning_patch_list = self.kern_adjustments(self.adustments_json)
		#pprint.pprint(kerning_patch_list)
		#
		#print(self.adustments_json)
		#print(kerning_patch_list)
		#
		if do_patch == True:
			#
			for k,v in self.p_c.items():
				#
				for _k,_v in self.p_c[k].items():
					#
					for __k,__v in self.p_c[k][_k].items():
						#
						for x in kerning_patch_list:
							#
							if x[3] == self._current_font_instance_weight:
								#
								if [_k,__k] == [x[0], x[1]]:
									#
									print("ADJUSTING: ", _k,__k, self.p_c[k][_k][__k], " to ", self.p_c[k][_k][__k] + x[2])
									#
									self.p_c[k][_k].update({__k:self.p_c[k][_k][__k] + x[2]})
									#
								#
							# 
						#
					#
				#
			#
		#
		if self._compress_pattern:
			#
			self.p_c_copy = copy.deepcopy(self.p_c)
			#
			'''
			Keep kerning file structure exactly the same as the pattern, just change the values, for kerning interpolation
			'''
			#
			self.p_p = collections.OrderedDict()
			self.p_p.update( plistlib.readPlist(self._compress_pattern))
			self.p_p_copy = copy.deepcopy(self.p_p)
			#
			for k,v in self.p_c.items():
				#
				for _k,_v in self.p_c[k].items():
					#
					for __k,__v in self.p_c[k][_k].items():
						#
						if __k not in self.p_p[_k]:
							#
							self.p_c[k][_k][__k] = 0
							#
						#
					self.p_c[k][_k].update(self.p_p[_k])
					#
			
			self.p_c = self.p_c_copy
			#
		#
		self.make_kern_plist()
		#
		self.make_kern_fea_lines(kerning_patch_list) # pass patch list Letter to Letter to fea
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
		print('Compressing:', self._current_font_instance_weight)
		#
		self.test_compress(dir_flat_ufo_file_kern, file_base_group)
		#
		#
		total_pairs = 0
		#
		for x in self.stats:
			#
			total_pairs = total_pairs + self.stats[x]
			#
		#
		print("=======================================")
		print("RESULTS:")
		#
		pprint.pprint(self.stats)
		#
		print("Total Pairs",total_pairs)
		print("=======================================")
		#
	#
#
'''IGNORE'''
#if self._compress_pattern:
# 	#
# 	self.p_c_copy = copy.deepcopy(self.p_c)
# 	#
# 	'''
# 	Keep kerning file structure exactly the same as the pattern, just change the values
# 	'''
# 	#
# 	self.p_p = plistlib.readPlist(self._compress_pattern)
# 	#
# 	for k,v in self.p_c.items():
# 		#
# 		for _k,_v in self.p_c[k].items():
# 			#
# 			#
# 			for __k,__v in self.p_c[k][_k].items():
# 				#
# 				if __k in self.p_p[_k]:
# 					#
# 					pass
# 				# 	#
# 				else:
# 					#
# 					if __k in self.p_c[k][_k]:
# 						#
# 						self.p_c_copy[k][_k][__k] = 0
# 						#
# 					else:
# 						#
# 						pass
# 						#
# 					#
# 				#
# 			#
# 		#
# 	#
# 	self.p_c = copy.deepcopy(self.p_c_copy)
# 	#
# #
#