#-------------------------------------------------------------------------------
# Name:        Mystic Main Driver
# Purpose:
#
# Author:      FX BESSUGES
#
# Created:     25/09/2018
#
#
#-------------------------------------------------------------------------------
#Define constants used in this script

debug= True
version = 1.0
environnement = "windows"
python_version = 3.7
log_dir = "./log/"


import argparse
import sys
import json
import os
import sys
import time
import mystic

import struct
import logging
from datetime import datetime,date,time
#-----------------------------------------------------------*
# Put logging so we put some information into log
# if debug is set true
#-----------------------------------------------------------*
logfile = log_dir + datetime.now().strftime('mysticlog_%H_%M_%d_%m_%Y.log')


logging.basicConfig(filename=logfile,level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

from datetime import timedelta
from struct import *

from pathlib import Path

def ParseFormat(file):
    # parse json file into an array then process each fiels according
    # to their description
    with open(file) as f:
        data = json.load(f);
    return(data);
def ParseIndividualVar(record,offset,length,typein,typeoout):
    # for each record we extract fields described par
    # json format file
    print(record);

# prolog: parsing  parameters
parser = argparse.ArgumentParser()
parser.add_argument("--infile", help="input file to translate")
parser.add_argument("--outfile", help="outfile translated")
parser.add_argument("--format", help="json file which describes internal format")
args = parser.parse_args()


if debug:
    logging.debug('formatted message: %s', str(args.infile))
    logging.debug('formatted message: %s', str(args.outfile))
    logging.debug('formatted message: %s', str(args.format))
#------------------------------------------------------------
#
# Process input file // we identify mandatory file is specified
# and then we check if it's a true file
#
#------------------------------------------------------------
if args.infile :
    logging.info("The infile specified is : %s", args.infile)
    data = args.infile   # the data FileField will get  the file name
    in_file = Path(args.infile)
    if in_file.is_file():       # check if it's a real file
        data = args.infile
        logging.info("The infile specified : %s is a true file", args.infile)

else :          # No argument are specified
     logging.error('No input file was provided program aborted')
     #data = "D:\\Python\\Projets\\Mystic\\tests\\extrait.data"
     exit();
#------------------------------------------------------------
#
# Process outfile file // we identify mandatory parameter
# is specified, and if it's a true directory
#
#------------------------------------------------------------

if args.outfile:
    logging.info("the outfile specified is : %s ",args.outfile)
    ou_file = Path(args.outfile)
    if ou_file.is_file():
        logging.info("the outfile will be written to : %s ",args.outfile)
else :      # No arguments are specified for the output directory
    logging.error('No output file was provided program aborted')
    #file_output_name = "mystic"
    #print("outfile will be written to D:\Python\cobol\mystic.json")
    exit();
#------------------------------------------------------------
#
# Process format file // we identify mandatory parameter
# is specified, and if it's a true file
#
#------------------------------------------------------------

if args.format:
    logging.info("The format specified was : %s ",args.format)
    cf_file = Path(args.format)
    if cf_file.is_file():
        print(" the Json file wich describes the data is : ",cf_file)
else :
    logging.info("fie : %s ",args.format)
    logging.error('No config file was provided program aborted')
    #cf_file="D:\Python\cobol\Q801.json"
    exit()

#------------------------------------------------------------
#  Main part:
#  =========
#  Read sequentially each record from binary file  according
#  to caracteristics : LRECL, RECFM
#  1rst loop (while loop until end of file
#   2nd nested loop for each record (transformation for
#       each field parsed).
#------------------------------------------------------------

InputDataFile = open(data,"rb")
#
# format dictionary will get the description data
# we parse it first because we need to know how the file
# will be organized:
#   RECFM: (F,FB, V,VB)
#   LRECL: up to 32760 record length..
#
format = ParseFormat(cf_file)
lrecl = format['lrecl']
recfm = format['recfm']
buffer = InputDataFile.read(lrecl);
collection = {}

k = 0
collection['record'] = []
FileField_name=''
#while k < 5:
while buffer != b'':
    for element in format['fields']:

        FileField = buffer[element['offset']: element['offset']+ element['length']]


        #Parse  each data vars
        #----------------------
        # EBCDIC to ASCII=== > simply code Page.
        #
        if element['from'] == "EBCDIC" and element['to'] =="ASCII":
             FileField = Ebcdic_Ascii(FileField,"A")
             FileField =  FileField.decode('cp500',"replace")
             FileField_name = element['namevar']

        # EBCDIC to INTEGER  ( for instance   we got PIC 9 and we want to compute it
        #
        if element['from'] == "EBCDIC" and element['to'] =="INTEGER":
             FileField =  Ebcdic_Integer(FileField)
             FileField_name = element['namevar']

        # PACKED to INTEGER  ( ex '01235C'
        #
        if element['from'] == "PACKED" and element['to'] =="INTEGER":
             FileField =  Packed_Integer(FileField)
             FileField_name = element['namevar']

        # PACKED to ASCII  (decimal to an editable value
        #
        if element['from'] == "PACKED" and element['to'] =="ASCII":
             FileField =  Packed_Ascii(FileField)
             FileField_name = element['namevar']

        # BigEndian to little Endian  (integer from mainfame to open system
        #
        if element['from'] == "BIG" and element['to'] =="LITTLE":
             FileField =  Packed_Ascii(FileField)
             FileField_name = element['namevar']

        #Collection will get now the translated fields so we can append the
        # record to the Json stream
        #
        # we may be have to split into record the Json stream..

        collection['record'].append({
            'FileField_name':FileField_name,
            'value':FileField,
            'Formatsource':element['from']})

    k = k + 1
    buffer = InputDataFile.read(lrecl)
    logging.debug("buffer %s",buffer)
stringdata=str(json.dumps(collection, sort_keys=False, indent=4))
if debug:
    outfile = "D:\\Python\\cobol\\" + "test" + ".json"
else:
    outfile = args.outfile + file_output_name + ".json"



# End of the main  program we
# now close every files and go to beg
# for a long dreamful night



OutputDataFile = open(outfile,"w")
OutputDataFile.write(stringdata)
OutputDataFile.close()
InputDataFile.close()




