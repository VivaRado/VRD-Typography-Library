Compress Kerning
===================

Compress Flat Kerning to Component Based Kerning

compress logic:

	sim list includes L and R sim groups
	
	 - Group to Group (GG): 
		permute L side with any R side from simex #0001
		for items in permut list
			get unique group items of simex L and R groups #0002
			gather int value from flat list provided L and R #0003
			remove the group contents from the flat list that are in L R simex unique group #0004
		# deleting from flat_copy in matches of permut list, the group items of both simex groups since they are covered by the both group contents

	 - Group to Letter (GL):
		list simex keys with L #0005
		for L simex keys
			gather values from flat kerning provided key L #0006
			remove values from flat kerning provided key L #0007
			remove group items included in flat groups
		# deleting from flat_copy in matches of permut list, the group items of L simex group since they are covered by Group to Group

	 - Letter to Group (LG):
		list simex keys with R #0008
		gather groups that include key R from flat kerning
		get keys from those groups
		permute flat keys on left side not in simex group keys and not in all simex group items with key R
		for items in permut list
			gather values from flat kerning
			remove the values gathered from flat list and values in simex R group items
		# deleting from flat_copy in matches of permut list, the group items of R simex group since they are covered by the R group contents


	 - Letter to Letter (LL):
		whatever key remains in flat list and is not key in simex
		# deleting all simex group items that are keys in flat_copy because they are covered in GG or GL #0009


[By VivaRado](https://www.vivarado.com)
