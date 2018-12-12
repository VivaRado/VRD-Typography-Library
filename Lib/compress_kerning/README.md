Compress Kerning
===================

Compress Flat Kerning to Component Based Kerning

Logic:
------
 - #### Group to Group (GG): 
	 - permute L side with any R side from simex.
	 - for items in permut list:
		 - get unique group items of simex L and R groups.
		 - gather int value from flat list provided L and R.
		 - remove the group contents from the flat list that are in L R simex unique group.
	> deleting from flat_copy in matches of permut list, the group items of both simex groups since they are covered by the both group contents.
------
 - #### Group to Letter (GL):
	 - list simex keys with L.
	 - for L simex keys:
		 - gather values from flat kerning provided key L.
		 - remove values from flat kerning provided key L.
		 - remove group items included in flat groups.
	> deleting from flat_copy in matches of permut list, the group items of L simex group since they are covered by Group to Group.
------
 - #### Letter to Group (LG):
	 - list simex keys with R.
	 - gather groups that include key R from flat kerning.
	 - get keys from those groups.
	 - permute flat keys on left side not in simex group keys and not in all simex group items with key R.
	 - for items in permut list:
		 - gather values from flat kerning.
		 - remove the values gathered from flat list and values in simex R group items.
	> deleting from flat_copy in matches of permut list, the group items of R simex group since they are covered by the R group contents.
------
 - #### Letter to Letter (LL):
    > deleting all simex group items that are keys in flat_copy because they are covered in GG or GL.

    whatever key remains in flat list and is not key in simex.

------

[By VivaRado](https://www.vivarado.com)