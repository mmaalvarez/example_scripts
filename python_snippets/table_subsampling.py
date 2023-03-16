import random
import itertools
import numpy as np
import sys

def extract_subtype(dict_table, cancer, pop, list_subtypes):
	# Extracting smallest subtype from dict_table[cancer][pop] 
	dict_counts = {key: len(dict_table[cancer][pop][key]) for key in dict_table[cancer][pop].keys() & set(list_subtypes)}
	smallest_subtype = min(list_subtypes, key=dict_counts.__getitem__)
	return smallest_subtype

def get_index_random_cline(dict_table, cancer, pop, subtype):
	# pick one random cell line
	clines = dict_table[cancer][pop][subtype]
	random_cline = random.choice(clines)
	index_random_cline = dict_table[cancer][pop][subtype].index(random_cline)
	return index_random_cline

def get_num_clines(dict_table, cancer, pop):
	# update number cell lines
	num_cls_pop = len(list(itertools.chain(*list(dict_table[cancer][pop].values()))))
	return num_cls_pop


## file names
input_file = "ANOVA_DepMap_ID.cancer_type_presubsample.subtype.supergroup.20Q4.tsv"
output_file = "ANOVA_DepMap_ID.cancer_type_subsampled.subtype.supergroup.tsv"


## convert input file into a dictionary
with open(input_file, "r+") as presubsample:
	dict_table = dict()
	for i, line in enumerate(presubsample):
		if i == 0:
			header = "\t".join(line.strip().split('\t')[0:4])
		else:
			split_line = line.strip().split("\t")
			DepMap_ID = split_line[0]
			cancer_type = split_line[1]
			cancer_subtype = split_line[2]
			supergroup = split_line[3]

			## update dict_table
			try:
				dict_table[cancer_type]
			except KeyError:
				# add new cancer type
				dict_table[cancer_type] = {'0':{}, '1':{}}
			try:
				dict_table[cancer_type][supergroup][cancer_subtype]
			except KeyError:
				# new subtype
				# dict_table[cancer_type][supergroup][cancer_subtype] = [[],0]
				dict_table[cancer_type][supergroup][cancer_subtype] = []

			# dict_table[cancer_type][supergroup][cancer_subtype][0].append(DepMap_ID)
			dict_table[cancer_type][supergroup][cancer_subtype].append(DepMap_ID)


## subsample unbalanced cancer types
for cancer in dict_table:

	## number cell lines per population
	num_cls_EUR = len(list(itertools.chain(*list(dict_table[cancer]['0'].values()))))
	num_cls_EAS = len(list(itertools.chain(*list(dict_table[cancer]['1'].values()))))

	# if any of both populations has 0 cell lines for this cancer type, remove the cancer type altogether
	if num_cls_EUR == 0 | num_cls_EAS == 0:
		dict_table[cancer]['0'].pop(cancer)
		dict_table[cancer]['1'].pop(cancer)
		print(f'cancer type {cancer} removed, it has 0 cell lines in at least one supergroup\n')

	# which is the population with more cell lines for this cancer type?
	elif num_cls_EUR == num_cls_EAS:
		# equal sizes
		pass

	else: 
		# one pop has more cell lines than the other
		if num_cls_EUR > num_cls_EAS:
			# EUR more cell lines

			large_pop = '0'
			small_pop = '1'

			num_cls_large_pop = num_cls_EUR
			num_cls_small_pop = num_cls_EAS

		elif num_cls_EUR < num_cls_EAS:
			# EAS more cell lines

			large_pop = '1'
			small_pop = '0'

			num_cls_large_pop = num_cls_EAS
			num_cls_small_pop = num_cls_EUR

		else:
			sys.exit("Something went wrong, check lines ~80-100 from script\n")

		## subtypes small_pop
		subtypes_small_pop = list(dict_table[cancer][small_pop].keys())

		while num_cls_large_pop > num_cls_small_pop:
			## loop, removing one cell line from large_pop in each iteration, until equal

			# subtypes large_pop (update in each loop)
			subtypes_large_pop = list(dict_table[cancer][large_pop].keys())

			# common subtypes (update in each loop, not remove cell lines from them unless necessary)
			common_subtypes = list(set(subtypes_large_pop).intersection(subtypes_small_pop))

			## reduce samples from large_pop
			# first use only non common subtypes, starting by the smallest one
			if len(common_subtypes) != 0:

				# yield large_pop subtypes that are not among the common_subtypes
				noncommons = np.setdiff1d(subtypes_large_pop, common_subtypes)

				if len(noncommons) != 0:
					# Extracting noncommon subtypes from dict_table[cancer][large_pop] 
					smallest_noncommon = extract_subtype(dict_table, cancer, large_pop, noncommons)

					# pick one random cell line from smallest_noncommon in large_pop
					index_random_cline = get_index_random_cline(dict_table, cancer, large_pop, smallest_noncommon)
					# remove it
					dict_table[cancer][large_pop][smallest_noncommon].pop(index_random_cline)

					## update number cell lines large_pop
					num_cls_large_pop = get_num_clines(dict_table, cancer, large_pop)

					## remove the smallest_noncommon subtype IF it is now empty of cell lines
					if len(dict_table[cancer][large_pop][smallest_noncommon]) == 0:
						dict_table[cancer][large_pop].pop(smallest_noncommon)

				else:
					## large_pop only has subtypes that are also present in small_pop, so remove from the subtype that contains the least cell lines in small_pop
					# find out which is the smallest subtype in small_pop, out of the common ones
					smallest_small_pop = extract_subtype(dict_table, cancer, small_pop, common_subtypes)

					## check whether large_pop has equal or less number of cell lines for that subtype and, if, so, remove from the next smaller one
					num_clines_large_pop_this_subtype = len(dict_table[cancer][large_pop][smallest_small_pop])
					num_clines_small_pop_this_subtype = len(dict_table[cancer][small_pop][smallest_small_pop])

					if num_clines_large_pop_this_subtype <= num_clines_small_pop_this_subtype:
						while (num_clines_large_pop_this_subtype <= num_clines_small_pop_this_subtype) & (len(common_subtypes) >= 1) :
							common_subtypes.remove(smallest_small_pop)
							smallest_small_pop = extract_subtype(dict_table, cancer, small_pop, common_subtypes)
							num_clines_large_pop_this_subtype = len(dict_table[cancer][large_pop][smallest_small_pop])
							num_clines_small_pop_this_subtype = len(dict_table[cancer][small_pop][smallest_small_pop])
						if num_clines_large_pop_this_subtype <= num_clines_small_pop_this_subtype & len(common_subtypes) == 1:
							break  

					# pick one random cell line from that subtype in large_pop
					index_random_cline = get_index_random_cline(dict_table, cancer, large_pop, smallest_small_pop)
					# remove it
					dict_table[cancer][large_pop][smallest_small_pop].pop(index_random_cline)

					## update number cell lines large_pop
					num_cls_large_pop = get_num_clines(dict_table, cancer, large_pop)

					## remove the smallest_small_pop subtype IF it is now empty of cell lines in large_pop
					if len(dict_table[cancer][large_pop][smallest_small_pop]) == 0:
						dict_table[cancer][large_pop].pop(smallest_small_pop)

			else:
				## no subtype matching between populations, just remove any cell line from the large_pop
				# pick one random cell line from any subtype in large_pop
				random_subtype_large_pop = random.choice(subtypes_large_pop)
				index_random_cline = get_index_random_cline(dict_table, cancer, large_pop, random_subtype_large_pop)
				# remove it
				dict_table[cancer][large_pop][random_subtype_large_pop].pop(index_random_cline)

				## update number cell lines large_pop
				num_cls_large_pop = get_num_clines(dict_table, cancer, large_pop)

				## remove the random_subtype_large_pop subtype IF it is now empty of cell lines in large_pop
				if len(dict_table[cancer][large_pop][random_subtype_large_pop]) == 0:
					dict_table[cancer][large_pop].pop(random_subtype_large_pop)


## write subsampled table
with open(output_file, "w") as out:
	out.write(header + "\n")

	for cancer_type in dict_table:
		for pop in ['0', '1']:
			for subtype in dict_table[cancer_type][pop]:
				for cline in dict_table[cancer_type][pop][subtype]:
					out.write(f'{cline}	{cancer_type}	{subtype}	{pop}\n')

'''
# print input dictionary to stdout (use ' > data_summary.txt')
print(f'cancer types: {len(dict_table.keys())}\n')
samples = 0
for cancer in list(dict_table.keys()):
	print(f'cancer type: {cancer}\n')
	for pop in ['0','1']:
		print(f'pop: {pop}\n')
		print(f'n subtypes: {len(list(dict_table[cancer][pop].keys()))}\n')
		for subtype in list(dict_table[cancer][pop].keys()):
			n_samples = len(dict_table[cancer][pop][subtype])
			print(f'{subtype}: {n_samples}\n')
			samples += n_samples
print(f'total samples: {samples}\n')
'''
