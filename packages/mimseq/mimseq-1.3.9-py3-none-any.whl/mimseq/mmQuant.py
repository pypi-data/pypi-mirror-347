#! /usr/bin/env python3

###########################################################################
# Analysis of modifications/misincorporations and stops per tRNA position #
#    also includes counting of CCA vs CC ends required for CCA analysis   #
###########################################################################

from __future__ import absolute_import
import os, logging
import re
import gzip
import pysam
from itertools import groupby, combinations as comb
from operator import itemgetter, le
from .tRNAtools import countsAnticodon, newModsParser
from .getCoverage import getBamList, filterCoverage
from multiprocessing import Pool, Value
import multiprocessing.pool
from functools import partial
import pandas as pd
import numpy as np
from collections import defaultdict
import subprocess
from .ssAlign import getAnticodon, clusterAnticodon, tRNAclassifier, tRNAclassifier_nogaps

log = logging.getLogger(__name__)

mods = {'9':(['G', 'A'],[]), 
            '20':(['C', 'T'],[]), 
            '20a':(['T'],[]), 
            '20b':(['T'],[]), 
            '26':(['G'],[]), 
            '32':(['C'],[]), 
            '37':(['G', 'A'],[]), 
            '58':(['A'],[]),
            'e9':(['C'],['Leu-CAG','Ser-AGA','Ser-CGA','Ser-GCT','Ser-TGA'])}

# custom classes to allow non-demonic processes allowing children processes to spawn more children sub-processes (i.e. multiprocessing within multiprocessing)
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

def unknownMods(inputs, knownTable, cluster_dict, modTable, misinc_thresh, cov_table, min_cov, tRNA_dict, remap):
# find unknown modifications with a total misincorporation threshold >= misinc_thresh

	log.info('Finding potential unannotated mods for {}'.format(inputs))
	new_mods_isodecoder = defaultdict(list)
	new_inosines_isodecoder = defaultdict(list)
	new_mods_cluster =  defaultdict(list)
	new_inosines_cluster = defaultdict(list)
	cons_anticodon = getAnticodon()

	# if this is round 2, read in previously predicted mods and subtract from knownTable so that they can be re-predicted and written to predictedMods
	predRound1 = defaultdict(list)
	try:
		with open(inputs + "_predictedModstemp.csv", "r") as predFile:
			for line in predFile:
				line = line.strip()
				isodecoder, pos = line.split("\t")[0:2]
				predRound1[isodecoder].append(int(pos))
		knownTable = {cluster:[pos for pos in knownTable[cluster] if pos not in predRound1[cluster]] for cluster, pos in knownTable.items()} # subtraction
		knownTable = defaultdict(list, knownTable)
	except:
		next

	for isodecoder, data in modTable.items():
		if cluster_dict:
			cluster = [parent for parent, child in cluster_dict.items() if isodecoder in child][0]
			short_isodecoder = "-".join(isodecoder.split("-")[:-1]) if not "chr" in isodecoder else isodecoder
		# if cluster_dict is empty, then clustering is disabled and in this case isodecoder in modTable is the "cluster"
		else:
			cluster = isodecoder
			short_isodecoder = isodecoder
		anticodon = clusterAnticodon(cons_anticodon, short_isodecoder)
		for pos in data.keys():
			cov = cov_table.loc[(cov_table.isodecoder == isodecoder) & (cov_table.pos == pos), 'cov']
			if (sum(modTable[isodecoder][pos].values()) >= misinc_thresh and (any(cov >= min_cov) or 'mito' in isodecoder) and pos-1 not in knownTable[isodecoder]): # misinc above threshold, cov above threshold and not previously known
				# if one nucleotide dominates misinc. pattern (i.e. >= 0.97 of all misinc, likely a true SNP or misalignment)
				if (max(modTable[isodecoder][pos].values()) / sum(modTable[isodecoder][pos].values()) > 0.97):
					# if mod seems to be an inosine (i.e. A with G misinc at 34) add to list and modification SNPs file (see tRNAtools.ModsParser())
					if (tRNA_dict[isodecoder]['sequence'][pos-1] == 'A' and list(modTable[isodecoder][pos].keys())[list(modTable[isodecoder][pos].values()).index(max(modTable[isodecoder][pos].values()))] == 'G' and pos-1 == min(anticodon)):
						new_inosines_cluster[cluster].append(pos-1)
						new_inosines_isodecoder[isodecoder].append(pos-1)
				elif (max(modTable[isodecoder][pos].values()) / sum(modTable[isodecoder][pos].values()) <= 0.97 and not (pos-1 == min(anticodon))):
					new_mods_cluster[cluster].append(pos-1) #modTable has 1 based values - convert back to 0 based for mod_lists
					new_mods_isodecoder[isodecoder].append(pos-1)

	with open(inputs + "_predictedModstemp.csv", "w") as predMods:
		#predMods.write("isodecoder\tpos\tidentity\tbam\n")
		for isodecoder, data in new_mods_isodecoder.items():
			for pos in data:
				predMods.write(isodecoder + "\t" + \
					str(pos) + "\t" + \
					str(tRNA_dict[isodecoder]['sequence'][int(pos)]) + "\t" + \
					inputs.split("/")[-1] + "\n")
		
		if not remap:	
			for isodecoder, data in new_inosines_isodecoder.items():
				for pos in data:
					predMods.write(isodecoder + "\t" + \
						str(pos) + "\t" + \
						"A" + "\t" + \
						inputs.split("/")[-1] + "\n")

	return(new_mods_cluster, new_inosines_cluster)

def bamMods_mp(out_dir, min_cov, info, mismatch_dict, insert_dict, del_dict, cluster_dict, cca, tRNA_struct, tRNA_ungap2canon,remap, misinc_thresh, knownTable, tRNA_dict, unique_isodecoderMMs, splitBool, isodecoder_sizes, crosstalks, threads, inputs):
# modification counting and table generation, and CCA analysis

	# output structures
	modTable = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
	stopTable = defaultdict(lambda: defaultdict(int))
	counts = defaultdict(lambda: defaultdict(int))
	cov = defaultdict(lambda: defaultdict(int))
	readRef_match_dict = defaultdict(lambda: defaultdict(int)) # boolean counts of reads assigned to parent by default that match (True) or do not match (False) parent sequence
	geneCov = defaultdict(int)
	condition = info[inputs][0]

	# initialise structures if CCA analysis in on
	if cca:
		aln_count = 0
		cca_dict = defaultdict(lambda: defaultdict(int))
		dinuc_dict = defaultdict(int)

	# Open files for single read analysis
	if crosstalks and not remap:
		sample_name = inputs.split("/")[-1].split(".")[0]
		if not os.path.exists(out_dir + "single_read_data/" + sample_name):
			os.mkdir(out_dir + "single_read_data/" + sample_name)
		srfiles = dict()
		for r in isodecoder_sizes.keys():
			shortname = r.split("/")[0] if "/" in r else "-".join(r.split("-")[:-1]) if not "chr" in r else r
			srfiles[shortname] = gzip.open(out_dir + "single_read_data/" + sample_name +"/"+ r.replace("/",".") +".tsv.gz", "wt")
			if cca:
				cols = ["READ"]+[str(s) for s in  tRNA_struct.loc[shortname].index]+["Charged"]
			else:
				cols = ["READ"]+[str(s) for s in  tRNA_struct.loc[shortname].index]
			srfiles[shortname].write("\t".join(cols)+"\n")

	# process mods by looping through alignments in bam file
	bam_file = pysam.AlignmentFile(inputs, "rb")
	log.info('Analysing {}...'.format(inputs))
	for read in bam_file.fetch(until_eof=True):
		reference = read.reference_name

		#########################
		# Modification analysis #
		#########################

		# get MD tags for mismatches, split into list of integers and characters
		md_tag = read.get_tag('MD')
		md_list = re.split('(.*?)([A-Za-z]|[\^][A-Za-z]+)', md_tag)
		md_list = list(filter(None, md_list))

		# get cigar string, split as above
		cigar = read.cigarstring
		cigar_list = re.split('(.*?)([A-Za-z]|[\^][A-Za-z]+)', cigar)
		cigar_list = list(filter(None, cigar_list))

		# check cigar for softclipping at 5' and 3' of read (usually because of terminal transferase of RT) - if so remove soft-clipped bases from sequence
		if cigar_list[1].upper() == "S".upper():
			soft_clip = int(cigar_list[0])
			read_seq = read.query_sequence[soft_clip:]
			del cigar_list[0:2]
		else:
			read_seq = read.query_sequence 

		if cigar_list[-1].upper() == "S".upper():
			soft_clip = int(cigar_list[-2])
			read_seq = read_seq[:-soft_clip]
			del cigar_list[-3:-1]

		# remove insertions in read from the sequence (MD tags do not account for deletions and effect misinc. identity matching)
		# record ref_deletions (insertions in read) for matching later to unique differences between ref and read for isodecoder splitting - note use read_pos here so that deletions in read_seq are not subtracted from insert positions
		read_ins_pos = 0
		read_pos = 0
		ref_deletions = list()
		for index, i in enumerate(cigar_list):
			if i.isdigit():
				read_ins_pos += int(i)
				read_pos += int(i)
			elif i.isalpha() and i.upper() == 'D':
				del_size = int(cigar_list[index-1])
				read_ins_pos -= del_size
				read_pos -= del_size
			elif i.isalpha() and i.upper() == 'I':
				ins_size = int(cigar_list[index-1])
				ref_deletions.append(read_pos-ins_size)
				read_seq = read_seq[0:read_ins_pos-ins_size] + read_seq[read_ins_pos:]
				read_ins_pos -= ins_size

		# get offset of read mapping position to reference start in order to adjust mismatch position, and end of alignment for coverage calculation
		# (offset is simply start position of read alignment realtive to reference)
		offset = read.reference_start
		aln_end = read.reference_end
		
		# count mods and find new reference
		ref_pos = 0
		read_pos = 0
		adjust = 0
		temp = defaultdict()
		temp, ref_pos, read_pos, readRef_dif, insertions = countMods(temp, reference, ref_pos, read_pos, read_seq, offset, md_list, ref_deletions, tRNA_dict, mismatch_dict, insert_dict, del_dict, remap)
		# remove duplictae entries from readRed_dif (usually insertions! Not sure the caue...)
		readRef_dif = tuple(set(readRef_dif))
		readRef_match = True
		if readRef_dif: # only assign new reference if readRef_dif is recorded which only happens when remap = False (i.e. after 2nd alignment or if remap is never activated)
			reference, temp, adjust, readRef_match = findNewReference(unique_isodecoderMMs, tRNA_ungap2canon, readRef_dif, reference, temp, insertions, insert_dict, del_dict, ref_deletions, adjust, splitBool)
		readRef_match_dict[read.reference_name][readRef_match] += 1
		# read counts, stops and coverage
		counts[inputs][reference] += 1
		geneCov[reference] += 1
		
		# offset + 1 (0 to 1 based) is start of alignment - i.e. any start > 1 indicates a stop to RT at this position
		# correct for members that are shorter than parents at 5' end using adjust variable (see countMods)
		
		# only for reads that start at the 0 position of memebers they are assigned to
		# there are weird cases where a read is longer at 5' end than its new assigned member (probably incorrect assignment) and this would generate negative values for stop
		if offset - adjust >= 0:
			stopTable[reference][offset+1] += 1
			for i in range(offset+1, aln_end+1):
				cov[reference][i] += 1
		# if it is a weird case as described above, then just assume the read is full-length and add to stop at position 1
		else:
			stopTable[reference][1] += 1
			for i in range(0, aln_end+1):
				cov[reference][i] += 1

		for pos, identity in temp.items():
			modTable[reference][pos][identity] += 1

		################
		# CCA analysis #
		################

		if cca:
			aln_count += 1
			dinuc = read.query_sequence[-2:]
			dinuc_dict[dinuc] += 1

			mapped_ref = read.reference_name

			ref_length = bam_file.get_reference_length(mapped_ref)
			if ref_pos in [ref_length, ref_length - 1]:
				cca_dict[reference][dinuc] += 1
			elif ref_pos == ref_length - 2:
				dinuc = read.query_sequence[-1:]
				cca_dict[reference][dinuc] += 1
			elif ref_pos <= ref_length - 3:
				dinuc = "Absent"
				cca_dict[reference][dinuc] += 1
			
		############################
		# Single-read mods and CCA #
		############################
			
		if crosstalks and not remap:
			# Modifications
			shortname = "-".join(reference.split("-")[:-1]) if not "chr" in reference else reference
			seqtemp = []
			for n in tRNA_struct.loc[shortname].index:
				if (n<(offset+1)) or (n>(aln_end)):
					seqtemp.append("NA")
				elif n not in temp.keys():
					seqtemp.append("0")
				else:
					b = temp[n]
					if b!="N":
						seqtemp.append(b)
					else:
						seqtemp.append("NA")
			if cca:
				# Record charging status
				if aln_end==ref_length:
					chrg = "1"
				elif aln_end==(ref_length-1):
					chrg = "0"
				else:
					chrg = "NA"
				add = [read.query_name]+seqtemp+[chrg]
			else:
				add = [read.query_name]+seqtemp
			
			# Add line
			srfiles[shortname].write("\t".join(add)+"\n")


	# filter readRef_match_dict to those clusters with more than 10% false reads (i.e. do not match parent) or those with no True reads (usually low count clusters)
	readRef_match_dict = {k:v for k, v in readRef_match_dict.items() if ((v[True]) and (v[False]/v[True] >= 0.1)) or (not v[True])}
	# filter for --min-cov
	mapped_reads = sum(counts[inputs].values())
	if min_cov < 1:
		readRef_match_dict = {k:v for k, v in readRef_match_dict.items() if counts[inputs][k]/mapped_reads >= min_cov}
	else:
		readRef_match_dict = {k:v for k, v in readRef_match_dict.items() if counts[inputs][k] >= min_cov}
	## Edit misincorportation and stop data before writing

	# build dictionaries for mismatches and stops, normalizing to total coverage per nucleotide
	# readthroughTable is similar to stops but normalised by coverage at each base
	# This reflects the proportion of reads at a given site that stop at this site, as opposed to the proportion of all reads for the reference that stop here

	modTable_prop = {isodecoder: {pos: {
				group: count / (cov[isodecoder][pos]) if cov[isodecoder][pos] != 0 else 0
				  for group, count in data.items() if group in ['A','C','G','T']
								}
			for pos, data in values.items()
							}
		for isodecoder, values in modTable.items()
					}

	stopTable_prop = {isodecoder: {
			pos: (count / geneCov[isodecoder]) if geneCov[isodecoder] != 0 else 0
			for pos, count in values.items()
						}
		for isodecoder, values in stopTable.items()
				}

	readthroughTable = {isodecoder: {
			pos: (1 - (count / cov[isodecoder][pos])) if cov[isodecoder][pos] != 0 else 0 # 1 - stops gives readthrough
			for pos, count in values.items()
						}
		for isodecoder, values in stopTable.items()
				}

	# reformat cov_table and save
	cov_table = pd.DataFrame.from_dict(cov)
	cov_table['pos'] = cov_table.index
	cov_table['pos'] = cov_table['pos'].astype(int)
	cov_table_melt = cov_table.melt(id_vars='pos', var_name='isodecoder', value_name='cov')
	cov_table_melt.dropna(inplace = True)
	cov_table_melt['bam'] = inputs
	cov_table_melt = cov_table_melt[['isodecoder', 'pos', 'bam', 'cov']]
	cov_table_melt.to_csv(out_dir + inputs.split("/")[-1] + "_coverage.txt", sep = "\t", index = False)

	# convert coverages to proprtion mapped reads if it is a fraction
	cov_table_newMods = cov_table_melt.copy()
	if min_cov < 1:
		cov_table_newMods['cov'] = cov_table_newMods['cov'].div(mapped_reads)
				
	# find unknown mod sites
	new_mods, new_Inosines = unknownMods(inputs, knownTable, cluster_dict, modTable_prop, misinc_thresh, cov_table_newMods, min_cov, tRNA_dict, remap)
	# format and output mods and stops if remap is disabled (i.e. also occurs after round 2 of mapping)
	if not remap:
	#	new_mods = {}
	#	new_Inosines = {}

		log.info('Building modification, stop and count data tables for {}'.format(inputs))

		# reformat modTable and add gaps
		reform = {(outerKey, innerKey): values for outerKey, innerDict in modTable_prop.items() for innerKey, values in innerDict.items()}
		modTable_prop_df = pd.DataFrame.from_dict(reform)
		modTable_prop_df['type'] = modTable_prop_df.index
		modTable_prop_melt = modTable_prop_df.melt(id_vars=['type'], var_name=['isodecoder','pos'], value_name='proportion')
		modTable_prop_melt['condition'] = condition
		modTable_prop_melt['bam'] = inputs
		modTable_prop_melt.pos = pd.to_numeric(modTable_prop_melt.pos)

		# split and parallelize addNA
		names, dfs = splitTable(modTable_prop_melt)
		pool = Pool(threads)
		func = partial(addNA, tRNA_struct, "mods", cluster_dict)
		modTable_prop_melt = pd.concat(pool.starmap(func, zip(names, dfs)))
		pool.close()
		pool.join()

		# copy and add NAs for correct merging with modTable
		cov_table_na = cov_table_melt.copy()
		names, dfs = splitTable(cov_table_na)
		pool = Pool(threads)
		func = partial(addNA, tRNA_struct, "cov", cluster_dict)
		cov_table_na = pd.concat(pool.starmap(func, zip(names, dfs)))
		pool.close()
		pool.join()

		# add coverage per nucelotide from cov
		modTable_prop_melt = pd.merge(modTable_prop_melt, cov_table_na, on = ['isodecoder', 'pos', 'bam'], how = 'left')
		#modTable_prop_melt = addNA(modTable_prop_melt, tRNA_struct, cluster_dict, "mods")
		modTable_prop_melt = modTable_prop_melt[['isodecoder','pos', 'type','proportion','condition', 'bam', 'cov']]

		# reformat stopTable and add gaps 
		stopTable_prop_df = pd.DataFrame.from_dict(stopTable_prop)
		stopTable_prop_df['pos'] = stopTable_prop_df.index
		stopTable_prop_melt = stopTable_prop_df.melt(id_vars='pos', var_name='isodecoder', value_name='proportion')
		stopTable_prop_melt['condition'] = condition
		stopTable_prop_melt['bam'] = inputs
		stopTable_prop_melt.pos = pd.to_numeric(stopTable_prop_melt.pos)

		# split and parallelize addNA
		stopTable_prop_melt.dropna(inplace = True)
		names, dfs = splitTable(stopTable_prop_melt)
		pool = Pool(threads)
		func = partial(addNA, tRNA_struct, "stops", cluster_dict)
		stopTable_prop_melt = pd.concat(pool.starmap(func, zip(names, dfs)))
		pool.close()
		pool.join()
		# add coverage per nucelotide from cov
		stopTable_prop_melt = pd.merge(stopTable_prop_melt, cov_table_na, on = ['isodecoder', 'pos', 'bam'], how = 'left')
		#stopTable_prop_melt = addNA(stopTable_prop_melt, tRNA_struct, cluster_dict, "stops")
		stopTable_prop_melt = stopTable_prop_melt[['isodecoder', 'pos', 'proportion', 'cov', 'condition', 'bam']]

		# reformat readthroughTable
		readthroughTable = pd.DataFrame.from_dict(readthroughTable)
		readthroughTable['pos'] = readthroughTable.index
		readthroughTable_melt = readthroughTable.melt(id_vars='pos', var_name='isodecoder', value_name='proportion')
		readthroughTable_melt['condition'] = condition
		readthroughTable_melt['bam'] = inputs
		readthroughTable_melt.pos = pd.to_numeric(readthroughTable_melt.pos)

		# split and parallelize addNA
		readthroughTable_melt.dropna(inplace = True)
		names, dfs = splitTable(readthroughTable_melt)
		pool = Pool(threads)
		func = partial(addNA, tRNA_struct, "stops", cluster_dict)
		readthroughTable_melt = pd.concat(pool.starmap(func, zip(names, dfs)))
		pool.close()
		pool.join()

		# add coverage per nucelotide from cov
		readthroughTable_melt = pd.merge(readthroughTable_melt, cov_table_na, on = ['isodecoder', 'pos', 'bam'], how = 'left')
		readthroughTable_melt = readthroughTable_melt[['isodecoder', 'pos', 'proportion', 'cov', 'condition', 'bam']]

		# build temp counts DataFrame
		counts_table = pd.DataFrame.from_dict(counts)
		counts_table['isodecoder'] = counts_table.index
		counts_table = counts_table[['isodecoder', inputs]]
		# add 0 count isodecoders to table
		temp_add = pd.DataFrame(columns = ['isodecoder', inputs])
		for isodecoder in isodecoder_sizes.keys():
			if "/" in isodecoder:
				temp = isodecoder.split("/")[0]
				isodecoder = [key for key in splitBool.keys() if key.startswith(temp)][0]
			if not isodecoder in counts_table['isodecoder']:
				temp_add = temp_add.append({'isodecoder':isodecoder, inputs:0}, ignore_index = True)
		counts_table = counts_table.append(temp_add)

		# save tables to temp files per sample
		counts_table.to_csv(inputs + "countTable.csv", sep = "\t", index = False, na_rep = "0")
		modTable_prop_melt.to_csv(inputs + "mismatchTable.csv", sep = "\t", index = False, na_rep = 'NA')
		stopTable_prop_melt.to_csv(inputs + "RTstopTable.csv", sep = "\t", index = False, na_rep = 'NA')
		readthroughTable_melt.to_csv(inputs + "readthroughTable.csv", sep = "\t", index = False, na_rep = 'NA')

		if cca:
			with open(inputs + "_dinuc.csv", "w") as dinuc_prop, open(inputs + "_CCAcounts.csv", "w") as CCAvsCC_counts:
			# write dinuc proportions for current bam
				for dinuc, count in dinuc_dict.items():
					dinuc_prop.write(dinuc + "\t" + str(count/aln_count) + "\t" + inputs.split("/")[-1] + "\n")

				# add missing ends to dict to prevent issues with plotting in R
				for end in ["CA", "CC", "C", "Absent"]:
					for cluster, data in cca_dict.items():
						if not end in data.keys():
							cca_dict[cluster][end] = 0

				# write CCA outputs for current bam
				for cluster, data in cca_dict.items():
						for dinuc, count in data.items():
							if dinuc.upper() in ["CA", "CC", "C", "ABSENT"]:
								CCAvsCC_counts.write(cluster + "\t" + dinuc + "\t" + inputs + "\t" + condition + "\t" + str(count) + "\n")
		if crosstalks:
			# Close single-read analysis files
			for r in srfiles.keys():
				srfiles[r].close()

	log.info('Analysis complete for {}...'.format(inputs))

	return(new_mods, new_Inosines, readRef_match_dict)

def splitTable(table):
# splits various tables so that addNA can be run in parallel on groupby objects

	split_table = table.groupby('isodecoder')
	dfs = [group for name, group in split_table]
	names = [name for name, group in split_table]

	return(names, dfs)

def countMods(temp, reference, ref_pos, read_pos, read_seq, offset, md_list, ref_deletions, tRNA_dict, mismatch_dict, insert_dict, del_dict, remap):
# Loop though mismatches in read, assign to new deconvoluted reference (if possible) and count mods
	
	insertions = list()
	#deletions = list()
	readRef_dif = tuple() # mismatches, insertions and deleteion in read relative to reference used to assign to isodecoders
	for index, interval in enumerate(md_list):
		if not index == 0:
			new_offset = 0
		else:
			new_offset = offset
		if not interval.startswith('^'): 
			if interval.isdigit(): # stretch of matches
				read_pos += int(interval)
				interval = int(interval) + new_offset
				ref_pos += interval
			elif interval.isalpha(): # is a mismatch
				identity = read_seq[read_pos]
				ref_pos += new_offset 
				# check if current mismatch is in cluster mismatches and add to tuple of differences for deconvolution
				# if cluster_id not 1 and remap is disabed or this is round 2 of alignment (avoid errors in adding new mods for clusters)
				if (ref_pos in mismatch_dict[reference]) and (not remap) and (not ref_pos in tRNA_dict[reference]['modified']):
					toAdd = str(ref_pos) + identity
					readRef_dif = readRef_dif + (toAdd,)
				# only include these positions if they aren't registered mismatches between clusters
				elif (ref_pos not in mismatch_dict[reference]):
					temp[ref_pos+1] = identity
				# move forward
				read_pos += 1
				ref_pos += 1
		elif interval.startswith('^'):
			identity = 'Ins'
			insert_length = len(interval) - 1
			# register all insertions (including consecutive insertions) to be checked later against cluster parent
			current_inserts = [x for x in range(ref_pos,ref_pos+insert_length)]
			insertions.extend(current_inserts)
			for ins in current_inserts:
				if (ins in insert_dict[reference].keys()) and (not remap): # only add position to tuple to deconvolute if it exists as a known difference in the cluster
					toAdd = str(ref_pos) + identity
					readRef_dif = readRef_dif + (toAdd,)
			ref_pos += insert_length

	# add applicable deletions after cycling through MD list
	identity = "Del"
	for deletion in ref_deletions:
		if deletion in del_dict[reference].keys() and (not remap):
			toAdd = str(deletion) + identity
			readRef_dif = readRef_dif + (toAdd,)

	return(temp, ref_pos, read_pos, readRef_dif, insertions)

def findNewReference(unique_isodecoderMMs, tRNA_ungap2canon, readRef_dif, reference, temp, insertions, insert_dict, del_dict, ref_deletions, adjust, splitBool):
# function to find new reference for read based on mismatches to cluster parent

	old_reference = reference
	# Check sorted readRef_dif in unique_isodecoderMMs to update reference
	readRef_dif = tuple(sorted(readRef_dif))
	readRef_match = True
	new_readRef_dif = tuple()
	if readRef_dif:
		if readRef_dif in unique_isodecoderMMs[old_reference].keys():
			# set new reference only if it is not in splitBool - these are unsplit isodecoders because of significant cov difference between 3' end and mismatch used for splitting
			reference = unique_isodecoderMMs[old_reference][readRef_dif][0]
		# if it is not found, it may be some shorter combination as unique_isodecoderMMs contains shortest possible combination set
		else:
			# find which key(s) in unique_isodecoderMMs is a subset of readRef_diff
			isSubset = list()
			for uss in unique_isodecoderMMs[old_reference].keys():
				if set(uss).issubset(readRef_dif):
					isSubset.append(uss)
				# if it is not a subset, then the differences in the read relative to reference are not recorded as mismatches between cluster member's sequences
				# this can occur due to faulty alignment by GSNAP - e.g. iMet-CAT-1 (parent; ID 0.95) and -2 in human: m1A58 introduces deletions in reads, faulty alignment 
				# and inability to distinguish member from parent at mismatch position (55)

			# however, if isSubset is empty then the isodecoder was not deconvoluted
			# possibly from distinguishing mismatches at canonical mod sites (see splitClusters:findUniqueSubset)
			# only if there isSubset then find best match
			if isSubset:
				if len(isSubset) == 1:
					reference = unique_isodecoderMMs[old_reference][isSubset[0]][0]
				# if there are more than 1 uss which are subsets of readRef_dif
				elif len(isSubset) > 1:
					# get full sets of transcript differences to ref
					full_ss ={uss:set(unique_isodecoderMMs[old_reference][uss][1]) for uss in isSubset}
					# store the length of differences between readRef_dif and each full set
					difference_ss = {k:len(set(readRef_dif).difference(v)) for k, v in full_ss.items()}
					# new reference belongs to the set with least differences
					####!!! Potential future error if there is not only one minuss !!!###
					minuss = min(difference_ss, key=difference_ss.get)
					reference = unique_isodecoderMMs[old_reference][minuss][0]

	# handle insertions and deletions between cluster parent and members present in read (different from insertions or deletions in read only)
	# i.e. once new ref is found above and this member has an insertion or deletion relative to parent, subtract (ins) or add (del) 1 from all misinc positions after the insertion
	# corrects for difference in length between member and parent. 
	# Note that 1 bp up and down from the insertion/deletion are checked to account for differences in insertion/deletion position due to GSNAP alignment variation and usearch clustering
	if (not reference == old_reference):
		for i in insertions:
			if reference in (insert_dict[old_reference][i] or insert_dict[old_reference][i+1] or insert_dict[old_reference][i-1]):
				temp = {(k - 1 if k > i else k):v for k,v in temp.items()}
		for d in ref_deletions:
			if reference in (del_dict[old_reference][d] or del_dict[old_reference][d+1] or del_dict[old_reference][d-1]):
				temp = {(k + 1 if k > d else k):v for k, v in temp.items()}
			
		# special case for members that are shorter than parents at the 5' end or 3'
		# need to subtract the number of bases from recorded mismatches in temp to correct the position info
		cluster_inserts = [ins for ins in insert_dict[old_reference].keys() if reference in insert_dict[old_reference][ins]] # get all inserts in parent for the new reference (child)
		consec_inserts_5 = list()
		if cluster_inserts:
			for k, g in groupby(enumerate(cluster_inserts), lambda ix: ix[0] - ix[1]): # this gets lists of consecutive inserts - non-consecutive inserts could just be normal inserts in the body
				l = list(map(itemgetter(1), g))
				if 0 in l: # checks consecutive inserts for those starting at the 5' end of the parent
					consec_inserts_5 = l
					adjust = max(consec_inserts_5) #+ 1 # add one to adjustment variable because an insert at (for e.g.) pos 0 of the parent indicates that the member starts at position 1 of the parent
		temp = {(k - adjust):v for k,v in temp.items() if k >= adjust}

	elif (reference == old_reference) and (readRef_dif) and not (reference in splitBool.keys()):
		global mods
		ref_short = "-".join(reference.split("-")[:-1])
		modsFilter = {i:v[0] for i, v in mods.items() if (i in tRNA_ungap2canon[ref_short].values()) and (any([re.search(x, ref_short) for x in v[1]] if v[1] else ['empty']))}
		clusterMods_pos = {list(tRNA_ungap2canon[ref_short].keys())[list(tRNA_ungap2canon[ref_short].values()).index(i)]:v for i, v in modsFilter.items()}
		clusterMods_list = [str(i) for i in clusterMods_pos.keys()]
		new_readRef_dif = tuple([x for x in readRef_dif if not (re.search("([0-9]*)[A-Z]?", x).group(1) in clusterMods_list or re.search("Ins", x))])
		if new_readRef_dif:
			readRef_match = False

	return(reference, temp, adjust, readRef_match)

def addNA(tRNA_struct, data_type, cluster_dict, name, table):
# fill mods and stops tables with 'NA' for gapped alignment
	
	# edit cluster name to find in tRNA_struct; if --no-cluster then the name does not need to be edited
	if cluster_dict:
		shortname = "-".join(name.split("-")[:-1]) if not "chr" in name else name
	else:
		shortname = name
	new = pd.DataFrame()
	for pos in tRNA_struct.loc[shortname].index:
		if not any(table.loc[table.isodecoder == name].pos == pos): #and not (data_type == "readthrough"):
			if data_type == 'mods':
				#new = pd.DataFrame({'isodecoder':name, 'pos':pos, 'type':pd.Categorical(['A','C','G','T']), 'proportion':'NA', 'condition':table.condition.iloc[1], 'bam':table.bam.iloc[1], 'cov':'NA'})
				new = pd.DataFrame({'isodecoder':name, 'pos':pos, 'type':pd.Categorical(['A','C','G','T']), 'proportion':'NA', 'condition':table.condition.iloc[1], 'bam':table.bam.iloc[1]})
			elif data_type == 'stops':
				new = pd.DataFrame({'isodecoder':name, 'pos':pos, 'proportion':'NA', 'condition':table.condition.iloc[0], 'bam':table.bam.iloc[0]}, index=[0])
			elif data_type == 'cov':
				new = pd.DataFrame({'isodecoder':name, 'pos':pos, 'bam':table.bam.iloc[0], 'cov':'NA'}, index=[0])
			
			table = table.append(new)

	return(table)

def generateModsTable(sampleGroups, out_dir, name, threads, min_cov, mismatch_dict, insert_dict, del_dict, cluster_dict, cca, remap, misinc_thresh, knownTable, Inosine_lists, tRNA_dict, Inosine_clusters, unique_isodecoderMMs, splitBool, isodecoder_sizes, unsplitCluster_lookup, clustering, crosstalks):
# Wrapper function to call countMods_mp with multiprocessing

	if cca:
	
		log.info("\n+--------------------------------------------------------------------+\
		\n| Analysing misincorporations and stops to RT, and analysing 3' ends |\
		\n+--------------------------------------------------------------------+")

		try:
			os.mkdir(out_dir + "CCAanalysis")
			os.mkdir(out_dir + "mods")
			if crosstalks: os.mkdir(out_dir + "single_read_data")
		except FileExistsError:
			log.warning("Rewriting over old mods and CCA files...")

	else:

		log.info("\n+---------------------------------------------+\
		\n| Analysing misincorporations and stops to RT |\
		\n+---------------------------------------------+")

		try:
			os.mkdir(out_dir + "mods")
			if crosstalks: os.mkdir(out_dir + "single_read_data")
		except FileExistsError:
			log.warning("Rewriting over old mods files...")

	if remap:
		log.info("** Discovering unannotated modifications for realignment **")

	# Get bam info using function in getCoverage
	baminfo, bamlist = getBamList(sampleGroups)

	if len(baminfo) > threads:
		multi = threads
	else:
		multi = len(baminfo)

	# get tRNA struct info from ssAlign
	tRNA_ungap2canon = tRNAclassifier()[1]
	tRNA_struct = tRNAclassifier_nogaps(oneBased=True)

	tRNA_struct_df = pd.DataFrame(tRNA_struct).unstack().rename_axis(('cluster', 'pos')).rename('struct')
	tRNA_struct_df = pd.DataFrame(tRNA_struct_df)
	tRNA_struct_df = tRNA_struct_df.loc[~pd.isna(tRNA_struct_df.struct)]

	# format canonical position dictionary for merging with various tables below
	tRNA_ungap2canon_table = pd.DataFrame.from_dict(tRNA_ungap2canon, orient = "index")
	tRNA_ungap2canon_table = tRNA_ungap2canon_table.reset_index()
	tRNA_ungap2canon_table = tRNA_ungap2canon_table.melt(var_name='pos', value_name='canon_pos', id_vars='index')
	tRNA_ungap2canon_table.columns = ['isodecoder', 'pos', 'canon_pos']
	tRNA_ungap2canon_table['pos'] = tRNA_ungap2canon_table['pos'].astype(int) 
	tRNA_ungap2canon_table = tRNA_ungap2canon_table[~pd.isna(tRNA_ungap2canon_table.canon_pos)]

	# initiate custom non-daemonic multiprocessing pool and run with bam names
	pool = MyPool(multi)
	# to avoid assigning too many threads, divide available threads by number of processes
	threadsForMP = int(threads/multi)
	func = partial(bamMods_mp, out_dir, min_cov, baminfo, mismatch_dict, insert_dict, del_dict, cluster_dict, cca, tRNA_struct_df, tRNA_ungap2canon, remap, misinc_thresh, knownTable, tRNA_dict, unique_isodecoderMMs, splitBool, isodecoder_sizes, crosstalks, threadsForMP)
	new_mods, new_Inosines, readRef_match_dict = zip(*pool.map(func, bamlist))
	pool.close()
	pool.join()

	filtered = list()
	filter_warning = False
	readRef_unsplit_newNames = list()

	if not remap:

		# update splitBool and unsplitCluster_lookup with further unsplit clusters resulting from parent-assigned reads with mismatches
		# see readRef_match_dict
		# first, combine all items in readRef_match_dict resulting from multiprocessing
		readRef_match_set = {cluster for proc in readRef_match_dict for cluster in proc.keys()}
		# save new names of these unsplit clusters (due to mismatches between reads and parent) to variable for data aggregation later
		# for each new unsplit cluster get unique set of member isodecoders and update splitBool
		readRef_unsplit_count = 0
		for cluster in readRef_match_set:
			shortClusterName = "-".join(cluster.split("-")[:-1])
			members = [member for member in cluster_dict[cluster] if not member.split("-")[3] == cluster.split("-")[3]]
			iso_set = set()
			filtMembers = list()
			for member in members:
				if "-".join(member.split("-")[0:4]) not in iso_set:
					filtMembers.append(member)
					iso_set.add("-".join(member.split("-")[0:4]))
			splitBool[cluster].update(set(filtMembers))
			
			# generate new unsplit cluster names and add to the lookup dictionary (keep tRX naming for these isodecoders)
			if "tRNA" in cluster:
				member_IsoNums = tuple(int(iso.split("-")[-2]) if "tRNA" in iso else "tRX" + iso.split("-")[-2] for iso in filtMembers)
			elif "tRX" in cluster:
				member_IsoNums = tuple(int(iso.split("-")[-2]) if "tRX" in iso else "tRNA" + iso.split("-")[-2] for iso in filtMembers)
			member_IsoNums = sorted(tuple(x for x in member_IsoNums if isinstance(x, int))) + [x for x in member_IsoNums if isinstance(x, str)]
			member_IsoString = "/" + "/".join([str(iso) for iso in member_IsoNums])
			newClusterName = "-".join(cluster.split("-")[:-1]) + member_IsoString
			readRef_unsplit_newNames.append(newClusterName)
			unsplitCluster_lookup[shortClusterName] = newClusterName
			# for these unsplit clusters, the associated transcripts are also still in the table
			# need to add these to lookup as well so they are renamed with new cluster name, and later can be aggregated with others sharing the name
			filtMembers_short = ["-".join(iso.split("-")[:-1]) for iso in filtMembers]
			for iso in filtMembers_short:
				unsplitCluster_lookup[iso] = newClusterName
			readRef_unsplit_count += len(filtMembers)

		# Redo newModsParser here so that knownTable is updated with new mods from second round and written to allModsTable
		Inosine_clusters, snp_tolerance, newtRNA_dict, newknownTable, newInosineTable = newModsParser(out_dir, name, new_mods, new_Inosines, knownTable, Inosine_lists, tRNA_dict, clustering, remap, snp_tolerance = True)
		# convert newknownTable to DataFrame
		newknownTable_df = pd.DataFrame.from_dict(newknownTable, orient = "index").melt(ignore_index=False).dropna()[['value']].reset_index()
		newknownTable_df.columns = ['isodecoder', 'pos']
		if clustering:
			newknownTable_df.loc[~newknownTable_df['isodecoder'].str.contains("chr"), 'isodecoder'] = newknownTable_df['isodecoder'].str.split("-").str[:-1].str.join("-")
		# convert newInosineTable to DataFrame 
		newInosineTable_df = pd.DataFrame.from_dict(newInosineTable, orient = "index").melt(ignore_index=False).dropna()[['value']].reset_index()
		newInosineTable_df.columns = ['isodecoder', 'pos']
		if clustering:
			newInosineTable_df.loc[~newInosineTable_df['isodecoder'].str.contains("chr"), 'isodecoder'] = newInosineTable_df['isodecoder'].str.split("-").str[:-1].str.join("-")
		
		# combine new mods and new inosine tables
		allnewKnownTable_df = pd.concat([newknownTable_df, newInosineTable_df])

		allnewKnownTable_df = pd.merge(allnewKnownTable_df, tRNA_ungap2canon_table, on = ['isodecoder', 'pos'], how = "left")
		# replace isodecoder names for unsplit clusters with new names
		allnewKnownTable_df['isodecoder'] = allnewKnownTable_df['isodecoder'].replace(unsplitCluster_lookup)
		allnewKnownTable_df.to_csv(out_dir + "mods/allModsTable.csv", sep = "\t", index = False, na_rep = 'NA')

		modTable_total = pd.DataFrame()
		countsTable_total = pd.DataFrame()
		stopTable_total = pd.DataFrame()
		readthroughTable_total = pd.DataFrame()
		newMods_total = pd.DataFrame()

		dinuc_table = pd.DataFrame()
		CCAvsCC_table = pd.DataFrame()

		# generate counts table to select tRNAs to filter
		for bam in bamlist:
			countsTable = pd.read_csv(bam + "countTable.csv", header = 0, sep = "\t")
			os.remove(bam + "countTable.csv")
			if countsTable_total.empty:
				countsTable_total = pd.concat([countsTable_total, countsTable], ignore_index = True)
			else:
				countsTable_total = pd.merge(countsTable_total, countsTable, on = "isodecoder", how = "left")

		# get isodecoders to filter
		countsTable_total.index = countsTable_total.isodecoder
		countsTable_total.drop(columns = ['isodecoder'], inplace = True)
		filtered, filter_warning = filterCoverage(countsTable_total, min_cov)
 
		for bam in bamlist:
			# read in temp files and then delete
			modTable = pd.read_csv(bam + "mismatchTable.csv", header = 0, sep = "\t")
			modTable = modTable[~modTable.isodecoder.isin(filtered)]
			if clustering:
				modTable.loc[~modTable['isodecoder'].str.contains("chr"), 'isodecoder'] = modTable['isodecoder'].str.split("-").str[:-1].str.join("-")
			modTable['pos'] = modTable['pos'] - 1 # subtract 1 for 0-based numbering to get canon_pos
			modTable = pd.merge(modTable, tRNA_ungap2canon_table, on = ['isodecoder', 'pos'], how = "left")
			modTable['pos'] = modTable['pos'] + 1 # return to 1-based
			# edit misinc. propoportions of inosines to reflect true level of Gs, set As to NA
			for cluster in Inosine_clusters:
				if clustering:
					for isodecoder in cluster_dict[cluster]:
						iso_short = "-".join(isodecoder.split("-")[:-1])
						if any(modTable.isodecoder.str.contains(iso_short)):
							modTable.at[(modTable.canon_pos == '34') & (modTable['type'] == 'G') & (modTable.isodecoder == iso_short), 'proportion'] = 1 - sum(modTable[(modTable.canon_pos == '34') & (modTable['type'] != 'G') & (modTable.isodecoder == iso_short)]['proportion'].dropna())
							modTable.at[(modTable.canon_pos == '34') & (modTable['type'] == 'A') & (modTable.isodecoder == iso_short), 'proportion'] = np.nan
				else:
					modTable.at[(modTable.canon_pos == '34') & (modTable['type'] == 'G') & (modTable.isodecoder == cluster), 'proportion'] = 1 - sum(modTable[(modTable.canon_pos == '34') & (modTable['type'] != 'G') & (modTable.isodecoder == cluster)]['proportion'].dropna())
					modTable.at[(modTable.canon_pos == '34') & (modTable['type'] == 'A') & (modTable.isodecoder == cluster), 'proportion'] = np.nan
	
			# replace isodecoder names for unsplit clusters with new names
			modTable['isodecoder'] = modTable['isodecoder'].replace(unsplitCluster_lookup)
			# set NA props to 0 to avoid errors with aggregation for new unsplit clusters due to mismatches to reference
			modTable['proportion'] = modTable['proportion'].fillna(0)
			# get weighted average proportion (by cov)
			wm = lambda x: np.average(x, weights=modTable.loc[x.index, "cov"])
			newProps = modTable.loc[(modTable.isodecoder.isin(readRef_unsplit_newNames))].groupby(["isodecoder","canon_pos","pos","type","condition","bam"]).agg(cov=("cov", "sum"), proportion=("proportion", wm)).reset_index()[["isodecoder", "canon_pos", "pos", "type", "proportion", "cov", "condition", "bam"]]
			# filter old rows matching these clusters
			modTable = modTable.loc[~(modTable.isodecoder.isin(readRef_unsplit_newNames))]
			# add new aggregated rows back
			modTable = pd.concat([modTable, newProps])
			os.remove(bam + "mismatchTable.csv")

			stopTable = pd.read_csv(bam + "RTstopTable.csv", header = 0, sep = "\t")
			stopTable = stopTable[~stopTable.isodecoder.isin(filtered)]
			if clustering:
				stopTable.loc[~stopTable['isodecoder'].str.contains("chr"), 'isodecoder'] = stopTable['isodecoder'].str.split("-").str[:-1].str.join("-")
			stopTable['pos'] = stopTable['pos'] - 1
			stopTable = pd.merge(stopTable, tRNA_ungap2canon_table, on = ['isodecoder', 'pos'], how = "left")
			stopTable['pos'] = stopTable['pos'] + 1
			# replace isodecoder names for unsplit clusters with new names
			stopTable['isodecoder'] = stopTable['isodecoder'].replace(unsplitCluster_lookup)
			# set NA props to 0 to avoid errors with aggregation for new unsplit clusters due to mismatches to reference
			stopTable['proportion'] = stopTable['proportion'].fillna(0)
			# get weighted average proportion (by cov)
			wm = lambda x: np.average(x, weights=stopTable.loc[x.index, "cov"])
			newProps = stopTable.loc[(stopTable.isodecoder.isin(readRef_unsplit_newNames))].groupby(["isodecoder","canon_pos","pos","condition","bam"]).agg(cov=("cov", "sum"), proportion=("proportion", wm)).reset_index()[["isodecoder", "canon_pos", "pos", "proportion", "cov", "condition", "bam"]]
			# filter old rows matching these clusters
			stopTable = stopTable.loc[~(stopTable.isodecoder.isin(readRef_unsplit_newNames))]
			# add new aggregated rows back
			stopTable = pd.concat([stopTable, newProps])
			os.remove(bam + "RTstopTable.csv")

			readthroughTable = pd.read_csv(bam + "readthroughTable.csv", header = 0, sep = "\t")
			readthroughTable = readthroughTable[~readthroughTable.isodecoder.isin(filtered)]
			if clustering:
				readthroughTable.loc[~readthroughTable['isodecoder'].str.contains("chr"), 'isodecoder'] = readthroughTable['isodecoder'].str.split("-").str[:-1].str.join("-")
			readthroughTable['pos'] = readthroughTable['pos'] - 1
			readthroughTable = pd.merge(readthroughTable, tRNA_ungap2canon_table, on = ['isodecoder', 'pos'], how = "left")
			readthroughTable['pos'] = readthroughTable['pos'] + 1
			# replace isodecoder names for unsplit clusters with new names
			readthroughTable['isodecoder'] = readthroughTable['isodecoder'].replace(unsplitCluster_lookup)
			# set NA props to 0 to avoid errors with aggregation for new unsplit clusters due to mismatches to reference
			readthroughTable['proportion'] = readthroughTable['proportion'].fillna(0)
			# get weighted average proportion (by cov)
			wm = lambda x: np.average(x, weights=readthroughTable.loc[x.index, "cov"])
			newProps = readthroughTable.loc[(readthroughTable.isodecoder.isin(readRef_unsplit_newNames))].groupby(["isodecoder","canon_pos","pos", "condition","bam"]).agg(cov=("cov", "sum"), proportion=("proportion", wm)).reset_index()[["isodecoder", "canon_pos", "pos", "proportion", "cov", "condition", "bam"]]
			# filter old rows matching these clusters
			readthroughTable = readthroughTable.loc[~(readthroughTable.isodecoder.isin(readRef_unsplit_newNames))]
			# add new aggregated rows back
			readthroughTable = pd.concat([readthroughTable, newProps])
			os.remove(bam + "readthroughTable.csv")

			newModsTable = pd.read_csv(bam + "_predictedModstemp.csv", header = None, names = ['isodecoder', 'pos', 'identity', 'bam'], sep = "\t")
			os.remove(bam + "_predictedModstemp.csv")

			# add individual temp files to main concatenated table
			modTable_total = pd.concat([modTable_total,modTable], ignore_index = True)
			stopTable_total = pd.concat([stopTable_total, stopTable], ignore_index = True)
			readthroughTable_total = pd.concat([readthroughTable_total, readthroughTable], ignore_index = True)
			newMods_total = pd.concat([newMods_total, newModsTable], ignore_index = True)

			if cca:
				# same for CCA analysis files
				dinuc = pd.read_csv(bam + "_dinuc.csv", header = None, keep_default_na=False, sep = "\t")
				os.remove(bam + "_dinuc.csv")
				CCA = pd.read_table(bam + "_CCAcounts.csv", header = None)
				CCA = CCA[~CCA[0].isin(filtered)]
				os.remove(bam + "_CCAcounts.csv")

				dinuc_table = pd.concat([dinuc_table, dinuc], ignore_index = True)
				CCAvsCC_table = pd.concat([CCAvsCC_table, CCA], ignore_index = True)

		# edit splitBool isodecoder names for filtering from tables and adding to Single_isodecoder in counts files
		# convert to list
		tempSplitBool = list()
		newSplitBool = list() # with short names
		for cluster, isos in splitBool.items():
			tempSplitBool.append("-".join(cluster.split("-")[:-1]))
			tempSplitBool.append(["-".join(x.split("-")[:-1]) for x in isos])
		for sublist in tempSplitBool:
			if not isinstance(sublist, list):
				newSplitBool.append(sublist)
			else:
				for item in sublist:
					newSplitBool.append(item)

		# output tables
		log.info("Output final tables, counts and new mods...")
		modTable_total.drop_duplicates(inplace = True)
		modTable_total.sort_values(by=['isodecoder', 'pos'], inplace = True)
		modTable_total = modTable_total[['isodecoder', 'canon_pos', 'pos', 'type', 'proportion', 'cov', 'condition', 'bam']]
		modTable_total.to_csv(out_dir + "mods/mismatchTable.csv", sep = "\t", index = False, na_rep = 'NA')
		
		stopTable_total.drop_duplicates(inplace = True)
		stopTable_total.sort_values(by=['isodecoder', 'pos'], inplace = True)
		stopTable_total = stopTable_total[['isodecoder', 'canon_pos', 'pos', 'proportion', 'cov', 'condition', 'bam']]
		stopTable_total.to_csv(out_dir + "mods/RTstopTable.csv", sep = "\t", index = False, na_rep = 'NA')

		readthroughTable_total.drop_duplicates(inplace = True)
		readthroughTable_total.sort_values(by=['isodecoder', 'pos'], inplace = True)
		readthroughTable_total = readthroughTable_total[['isodecoder', 'canon_pos', 'pos', 'proportion', 'cov', 'condition', 'bam']]
		readthroughTable_total.to_csv(out_dir + "mods/readthroughTable.csv", sep = "\t", index = False, na_rep = 'NA')	
		
		# add column to counts to indicate complete isodecoder split or not, sizes, and parent
		countsTable_total['isodecoder'] = countsTable_total.index
		if clustering:
			countsTable_total.loc[~countsTable_total.isodecoder.str.contains("chr"), "isodecoder"] = countsTable_total.isodecoder.str.split("-").str[:-1].str.join("-")
		countsTable_total.set_index("isodecoder", inplace=True)
		countsTable_total['isodecoder'] = countsTable_total.index
		countsTable_total['Single_isodecoder'] = "NA"
		for iso, size in isodecoder_sizes.items():
			if clustering:
				short = "-".join(iso.split("-")[:-1]) if not re.search("chr|/", iso) else iso.split("/")[0]
			else:
				short = iso
			countsTable_total.at[short, 'size'] = size
		for isodecoder in countsTable_total.index:
			countsTable_total.at[isodecoder, 'Single_isodecoder'] = "False" if isodecoder in newSplitBool else "True"
		if clustering:
			clusterInfo = pd.read_csv(out_dir + "/" + name + "clusterInfo.txt", sep = "\t")
			clusterInfo = clusterInfo[['tRNA','parent']]
			clusterInfo.columns = ['isodecoder','parent']
			clusterInfo.loc[~clusterInfo['isodecoder'].str.contains("chr"), 'isodecoder'] = clusterInfo['isodecoder'].str.split("-").str[:-1].str.join("-")
			clusterInfo.loc[~clusterInfo['parent'].str.contains("chr"), 'parent'] = clusterInfo['parent'].str.split("-").str[:-1].str.join("-")
			clusterInfo.drop_duplicates(inplace=True)
			clusterInfo.index = clusterInfo.isodecoder
			clusterInfo.drop(columns = ['isodecoder'], inplace = True)
		else:
			clusterInfo = pd.DataFrame({'parent':list(tRNA_dict.keys())}, index = list(tRNA_dict.keys()))
		countsTable_total = countsTable_total.join(clusterInfo)
		# replace isodecoder names for unsplit clusters with new names
		countsTable_total['isodecoder'] = countsTable_total['isodecoder'].replace(unsplitCluster_lookup)
		countsTable_total.set_index("isodecoder", inplace = True)
		countsTable_total.sort_values(by=["isodecoder"], inplace = True)
		# aggregate duplicate isodeocders due to new unsplit clusters
		countsTable_total = countsTable_total.groupby([countsTable_total.index, "parent", "Single_isodecoder"]).agg(sum).reset_index()
		# reorder columns
		newCols = [col for col in countsTable_total.columns if col != "parent"] + ["parent"]
		countsTable_total = countsTable_total[newCols]
		countsTable_total.to_csv(out_dir + "Isodecoder_counts_raw.txt", sep = "\t", index = False, na_rep = "0")

		# map canon_pos for each isodecoder ungapped pos to newMods
		newMods_total = newMods_total[~newMods_total.isodecoder.isin(filtered)]
		if clustering:
			newMods_total.loc[~newMods_total['isodecoder'].str.contains("chr"), 'isodecoder'] = newMods_total['isodecoder'].str.split("-").str[:-1].str.join("-")
		newMods_total = pd.merge(newMods_total, tRNA_ungap2canon_table, on = ['isodecoder', 'pos'], how = "left")
		# replace isodecoder names for unsplit clusters with new names
		newMods_total['isodecoder'] = newMods_total['isodecoder'].replace(unsplitCluster_lookup)
		# make pivot table from mods and add A, C, G, T misinc. proportions for new mods
		pivot = modTable_total.pivot_table(index = ['isodecoder', 'bam', 'canon_pos'], columns = 'type', values = 'proportion')
		pivot = pivot.reset_index()
		pivot['bam'].replace(out_dir, "", regex = True, inplace = True)
		newMods_total = pd.merge(newMods_total, pivot, on = ['isodecoder', 'canon_pos', 'bam'], how = "left")
		newMods_total.drop(columns = ['pos'], inplace = True)
		newMods_total.drop_duplicates(inplace = True)
		newMods_total.to_csv(out_dir + 'mods/predictedMods.csv', sep = "\t", index = False, na_rep = "NA")

		if cca:
			dinuc_table.columns = ['dinuc', 'proportion', 'sample']
			dinuc_table.to_csv(out_dir + "CCAanalysis/AlignedDinucProportions.csv", sep = "\t", index = False, na_rep = 'NA')
			CCAvsCC_table.columns = ['gene', 'end', 'sample', 'condition', 'count']
			if clustering:
				CCAvsCC_table.loc[~CCAvsCC_table['gene'].str.contains("chr"), 'gene'] = CCAvsCC_table['gene'].str.split("-").str[:-1].str.join("-")
			# replace isodecoder names for unsplit clusters with new names
			CCAvsCC_table['gene'] = CCAvsCC_table['gene'].replace(unsplitCluster_lookup)
			CCAvsCC_table = CCAvsCC_table.groupby(["gene","end","sample","condition"]).agg(sum).reset_index()
			CCAvsCC_table.drop_duplicates(inplace = True)
			CCAvsCC_table.to_csv(out_dir + "CCAanalysis/CCAcounts.csv", sep = "\t", index = False)

		# Anticodon and/or isodecoder counts counts
		countsAnticodon(countsTable_total, out_dir)

		log.info("** Read counts per isodecoder saved to " + out_dir + "counts/Isodecoder_counts_raw.txt **")
		log.info("{} sequences could not be deconvoluted as >10% parent assigned-reads do not match parent sequence!".format(readRef_unsplit_count + len(readRef_match_set)))
		if len(readRef_match_set) > 0:
			log.info("Reasons for this include misaligment of reads to an incorrect cluster, or inaccurate aligment by GSNAP (e.g. at indels in reads) prohibiting correct devonvolution.")
		log.info("{} total unique sequences not deconvoluted due to mismatches at modified sites, insufficient coverage or read mismatches to parent".format(len(splitBool) + sum([len(data) for data in splitBool.values()])))


	return(new_mods, new_Inosines, filtered, filter_warning, unsplitCluster_lookup, readRef_unsplit_newNames)

def plotCCA(out_dir, double_cca):

	log.info("\n+-----------------+\
		\n| 3'-CCA analysis |\
		\n+-----------------+")

	out = out_dir + "CCAanalysis/"
	script_path = os.path.dirname(os.path.realpath(__file__))
	command = ["Rscript", script_path + "/ccaPlots.R", out + "AlignedDinucProportions.csv", out + "/CCAcounts.csv", out, str(double_cca)]
	subprocess.check_call(command)

	log.info("CCA analysis done and plots created. Located in {}".format(out))
