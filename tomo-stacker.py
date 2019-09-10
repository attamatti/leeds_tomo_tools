#!/usr/bin/env python

import subprocess
import sys
import os
import glob

vers = '0.3.0'

#-----------------------------------------------------------------------------------#
errormsg = ""
class Arg(object):
    _registry = []
    def __init__(self, flag, value, req):
        self._registry.append(self)
        self.flag = flag
        self.value = value
        self.req = req

def make_arg(flag, value, req):
    Argument = Arg(flag, value, req)
    errormsg = """
USAGE: tomostacker.py <arguments> <inputfiles search string>

::required arguments::

--tilt_axis  <tilt axis>	In degrees
--apix 	     <apix>		angstroms per pixel

::optional arguments::

--serialEM			add this flag if the data are from serial EM and use its naming convention

"""

    if Argument.req == True:
        if Argument.flag not in sys.argv:
            print(errormsg)
            sys.exit("ERROR: required argument '{0}' is missing".format(Argument.flag))
    if Argument.value == True:
        try:
            test = sys.argv[sys.argv.index(Argument.flag)+1]
        except ValueError:
            if Argument.req == True:
                print(errormsg)
                sys.exit("ERROR: required argument '{0}' is missing".format(Argument.flag))
            elif Argument.req == False:
                return False
        except IndexError:
                print(errormsg)
                sys.exit("ERROR: argument '{0}' requires a value".format(Argument.flag))
        else:
            if Argument.value == True:
                Argument.value = sys.argv[sys.argv.index(Argument.flag)+1]
        
    if Argument.value == False:
        if Argument.flag in sys.argv:
            Argument.value = True
        else:
            Argument.value = False
    return Argument.value
#-----------------------------------------------------------------------------------#

def init():
	'''check that the tilt axis and apix values are numbers - assign the tilt axis and apix variables'''
	print(':: Tomo stacker vers {0}::'.format(vers))
	tilt_axis = make_arg('--tilt_axis',True,True)
	apix = make_arg('--apix',True,True)
	serialEM = make_arg('--serialEM',False,False)
	if serialEM== False:
		print('NonserialEM data')
		nargs= 5
	elif serialEM==True:
		print('SerialEM data')
		nargs=6
	return(tilt_axis,apix,serialEM,nargs)

def getkey(i):
	'''used for sorting a list of tuples by their 1st item could be replaced with a sort(lambda) function'''
	return(float(i[0]))
	
def parse_filename(infile,serialEM):
	'''parse a filename written in the matt tomo rename script format - return a shortened file name (stripped of directory and tilt info/image no) and tilt angle'''
	tilt = '.'.join(infile.split('/')[-1].split('_')[-3:-1])
	if serialEM == True:
		tilt = '.'.join('.'.join(infile.split('/')[-1].split('_')[-2:]).split('.')[0:2])
		shortname = '_'.join(infile.split('/')[-1].split('_')[:-3])
		return(shortname,tilt)
	else:
		tilt = '.'.join(infile.split('/')[-1].split('_')[-3:-1])
		shortname = '_'.join(infile.split('/')[-1].split('_')[:-4])
		return(shortname,tilt)

def update_header(infile,tilt,tilt_axis,apix):
	'''update the header of a single mrc file using imod alterheader. Add tilt angle, tilt axis, and update pixel size'''
	print('{0}\t{1}'.format(tilt,infile))
	subprocess.call(['alterheader','{0}'.format(infile),'-del','{0},{0},{0}'.format(apix),'-title','Tilt axis rotation angle = {0}'.format(tilt_axis)],stdout=logout)

def put_in_dict(file,shortname):
	'''Put the files in a dictionary by short name (which is the name of the final tomogram). Returns dictionary: {tomo name:(tilt,full filename),(tilt 2,full filename 2)...(tilt n,full filename n)}'''
	try:
		filesdic[shortname].append((tilt,file))
	except:
		filesdic[shortname] = [(tilt,file)]
	
## program

proc = subprocess.Popen('module list', stderr=subprocess.PIPE, shell=True)	# run the module list command 
mods = proc.stderr.read()							# capture its output
if 'imod' not in mods:								# if imod isn't loaded
	sys.exit('ERROR: imod not loaded - load an imod module and try again')	# error out and inform user

subprocess.call(['touch','tomostacker.log'])			# touch the logfile
logout = open("tomostacker.log", "w")				# open the logfile for writing

(tilt_axis,apix,serialEM,nargs) = init()			# start the program - get the tiltaxis and apix variable values
filesdic = {}							# intialize the dictionary to store all the files
print(':: updating headers ::')					# screen output
print('tilt\tfile name')					# screen output

for i in sys.argv[nargs:]:					# operate on all files 1 at a time
	try:								# try loop to exclude files that don't fit the naming convention
		shortname,tilt = parse_filename(i,serialEM)				# get the name and tilt for the file
		update_header(i,tilt,tilt_axis,apix)				# update the file's header
		put_in_dict(i,shortname)					# put the file in the dictionary attached to the correct tomo
	except:								#exception if the filename can't be read properly
		print("skipping file {0}: couldn't parse name".format(i))		# error message then move on to the next file
print(':: making stacks ::')					# screen output
print('#images\tname')						# screen output
finished_files = []						# make a list of finished files **
for i in filesdic:						# operate on each tomogram
	print("{0}\t{1}/{1}.mrc".format(len(filesdic[i]),i))		# screen output
	if os.path.isdir(i) == False:					# check that the output directory exists
		subprocess.call(['mkdir',i])				# if it doesn't create it
	files_sorted = sorted(filesdic[i], key=getkey)			# make a list of the subfiles in the tomogram in order by tilt
	tiltsfile = open('{0}/{0}.rawtlt'.format(i),'w')			# open a file to write the tilts to
	for j in files_sorted:						# for every file in that list
		tiltsfile.write('{0}\n'.format(j[0]))			# add the tilt to the tilt file			
	tiltsfile.close()						# close the tilts file
	sortedlist = ['newstack','-tilt','{0}/{0}.rawtlt'.format(i)]					# start building the command that will  go into newstack
	for j in files_sorted:						# for every file in that list
		sortedlist.append(j[1])					# add the filename to the newstack command 
	sortedlist.append('{0}/{0}.mrc'.format(i))			# add the output file name to the end of the newstack command
	subprocess.call(sortedlist,stdout=logout)			# run the newstack command, write newstack's output to the logfile
	finished_files.append('{0}/{0}.mrc'.format(i))			# add the file to the finished list **
logout.close()							# close the logfile
print(':: making backups ::')					# screen output
for i in finished_files:					# iteratre over the list of finished files **
	subprocess.call(['cp',i,'{0}.backup'.format(i)])		# make a copy of each
								# ** did this because there seemed to be a lag between newstack writing the file and
								# ** it actually appearing causing missed files errors if writing the backups immediately 
