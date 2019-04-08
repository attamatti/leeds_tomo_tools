#!/usr/bin/env python

# give tomography files from serialEM reasonable names

import os                      # for running UNIX commands
import glob                    # for getting file names



files = glob.glob('*.mrc')      # get all the mrcs put in list

commands = []                   # empty list to put the commands in

for i in files:                                             # iterate over the list
    chunk1 = i.split('[')                                   # split at [ into chunk1[0] and chunk1[1]
    
    first_half =  chunk1[0]                                 # 1st half of the file name
    
    chunk2 = chunk1[1].split(']')                           # split the 2nd half at ]
    
    tilt = chunk2[0]                                        # 1st half of that is the tilt
    if tilt == '-0.00':                                     # fix negative 0 tilt
        tilt = '0.00'
    tilt = tilt.replace('.','p')                            # replace the . with p
    
    rest_of_filename = chunk2[1].strip('-')                 # 2nd half is rest of filename, removing the -
    
    newfilename = '{0}_{1}_{2}'.format(first_half,tilt,rest_of_filename)    # make new filename
    command = 'mv {0} {1}'.format(i,newfilename)            # make the command
    commands.append(command)                                # add the command to the list of commands
    

for i in commands:                                          # iterate over the list of commands
    print(i)                                                # screen barf = remove this line if you want
    os.system(i)                                            # run each