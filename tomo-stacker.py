#!/usr/bin/env python

import subprocess
import sys
import os
import glob

vers = '0.2.1'

def init():
	'''check that the tilt axis and apix values are numbers - assign the tilt axis and apix variables'''
	print(':: Tomo stacker vers {0}::'.format(vers))
	try:
		tilt_axis = float(sys.argv[-2])
		apix = float(sys.argv[-1])
	except:
		sys.exit("USAGE: tomostacker.py <inputfiles search string> <tilt axis> <apix>")

	return(tilt_axis,apix)

def getkey(i):
	'''used for sorting a list of tuples by their 1st item'''
	return(i[0])
	
def parse_filename(infile):
	'''parse a filename written in the matt tomo rename script format - return a shortened file name (stripped of directory and tilt info/image no) and tilt angle
	deals with twonaming conventions where decimal in tilt is a _ or a p'''
	tilt = '.'.join(infile.split('/')[-1].split('_')[-3:-1])
	if len(tilt.split('p')) == 2:
		tilt = float(infile.split('/')[-1].split('_')[-2].replace('p','.'))
		shortname = '_'.join(infile.split('/')[-1].split('_')[:-3])
	else:
		tilt = float('.'.join(infile.split('/')[-1].split('_')[-3:-1]))
		shortname = '_'.join(infile.split('/')[-1].split('_')[:-4])
	return(shortname,tilt)

def update_header(infile,tilt,tilt_axis,apix):
	'''update the header of a single mrc file using imod alterheader. Add tilt angle, tilt axis, and update pixel size'''
	print('{0}\t{1}'.format(tilt,infile))
	subprocess.call(['alterheader','{0}'.format(infile),'-tlt','0,0,{0}'.format(tilt),'-del','{0},{0},{0}'.format(apix),'-title','Tilt axis rotation angle = {0}'.format(tilt_axis)],stdout=logout)

def put_in_dict(file,shortname,tilt):
	'''Put the files in a dictionary by short name (which is the name of the final tomogram). Returns dictionary: {tomo name:(tilt,full filename),(tilt 2,full filename 2)...(tilt n,full filename n)}'''
	try:
		filesdic[shortname].append((tilt,file))
	except:
		filesdic[shortname] = [(tilt,file)]
	
## program

subprocess.call(['touch','tomostacker.log'])			# touch the logfile
logout = open("tomostacker.log", "w")				# open the logfile for writing

(tilt_axis,apix) = init()					# start the program - get the tiltaxis and apix variable values
filesdic = {}							# intialize the dictionary to store all the files
print(':: updating headers ::')					# screen output
print('tilt\tfile name')					# screen output
for i in sys.argv[1:-2]:					# operate on all files 1 at a time
	shortname,tilt = parse_filename(i)				# get the name and tilt for the file
	update_header(i,tilt,tilt_axis,apix)				# update the file's header
	put_in_dict(i,shortname,tilt)					# put the file in the dictionary attached to the correct tomo
print(':: making stacks ::')					# screen output
print('#images\tname')						# screen output
for i in filesdic:						# operate on each tomogram
	print("{0}\t{1}/{1}.mrc".format(len(filesdic[i]),i))		# screen output
	if os.path.isdir(i) == False:					# check that the output directory exists
		subprocess.call(['mkdir',i])					# if it doesn't create it
	sortedlist = ['newstack']					# start building the command that will  go into newstack
	files_sorted = sorted(filesdic[i], key=getkey)			# make a list of the subfiles in the tomogram in order by tilt
	for j in files_sorted:						# for every file in that list
		sortedlist.append(j[1])						# add the filename to the newstack command 
	sortedlist.append('{0}/{0}.mrc'.format(i))			# add the output file name to the end of the newstack command
	subprocess.call(sortedlist,stdout=logout)			# run the newstack command, write newstack's output to the logfile
	subprocess.call(['cp','{0}/{0}.mrc'.format(i),'{0}/{0}.mrc.backup'.format(i)])	# add a backup of the stacked file
logout.close()							# close the logfile