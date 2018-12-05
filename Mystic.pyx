#-------------------------------------------------------------------------------
# Name:        Untitled2
# Purpose:
#
# Author:      X090670
#
# Created:     17/10/2018
# Copyright:   (c) X090670 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------
# Name:        Mystic Main Driver
# Purpose:
#
# Author:      X090670
#
# Created:     25/09/2018
# Copyright:   (c) X090670 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import argparse
import sys
import json
import os
import sys
import time
import datetime
import struct
import logging

logging.basicConfig(filename='Mystic.log',level=logging.DEBUG,\
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
#logging.debug('Debug error')
#logging.info('INFO ERROR')
#logging.warning('Warning Error %s: %s', '01234', 'Erreur Oracle')
#logging.error('error message')
#logging.critical('critical error')
print('***1***')
print (args.infile)
print('***1***')
if args.infile :
    logging.info("the infile specified: ")
    print(args.infile)
    data = args.infile
    in_file = Path(args.infile)
    if in_file.is_file():
        data = args.infile
        print(args.infile)
else : # for test without arguments
     data = "D:\\Python\\Projets\\Mystic\\tests\\extrait.data"
if args.outfile:
    logging.info("the outfile specified: ")
    ou_file = Path(args.outfile)
    print("outfile specified")
    print(args.outfile)
    if ou_file.is_file():
        print("Output will be written to ",args.outfile)
else :
    print("outfile will be written to D:\Python\cobol\mystic.json")
if args.format:
    print("json file which describe the files is located  below")
    cf_file = Path(args.format)
    if cf_file.is_file():
        print(" the Json file wich describes the data is : ",cf_file)
else :
    print(" the Json file wich describes the data is : D:\Python\cobol\Q801.json ")
    cf_file="D:\Python\cobol\Q801.json"

file = open(data,"rb")
format = ParseFormat(cf_file)
lrecl = format['lrecl']
buffer = file.read(lrecl);
collection = {}

k = 0
collection['record'] = []
variable_name=''
while k < 5:
#while buffer != "":
    for element in format['fields']:

        variable = buffer[element['offset']: element['offset']+ element['length']]



        if element['from'] == "EBCDIC" and element['to'] =="ASCII":
             variable =  variable.decode('cp500',"replace")
             variable_name = element['namevar']
            # variable_name = variable_name.replace("-","_")

        collection['record'].append({
            'variable_name':variable_name,
            'value':variable,
            'Formatsource':element['from']})

    k = k + 1
    buffer = file.read(lrecl)

stringdata=str(json.dumps(collection, sort_keys=False, indent=4))
filename="forhdfs"
oufile = "D:\\Python\\cobol\\" + filename + ".json"
ou_file = open(oufile,"w")
ou_file.write(stringdata)
ou_file.close()





