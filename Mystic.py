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
parser = argparse.ArgumentParser()
parser.add_argument("--infile", help="input file to translate")
parser.add_argument("--outfile", help="outfile translated")
parser.add_argument("--format", help="json file which describes internal format")
args = parser.parse_args()
if args.infile:
    print("infile specified")
    in_file = Path(args.infile)
    if in_file.is_file():
        print(args.infile)
if args.outfile:
    print("outfile specified")
    print(args.outfile)
if args.format:
    print("json file which describe the files is located  below")
    cf_file = Path(args.format)
    if cf_file.is_file():


        print(args.format)
        # print file caracteristics upon console
        jsondata = ParseFormat(args.format);
        filename =jsondata['filedesc']['filename'];
        record_length =jsondata['filedesc']['lrecl'];

        # now compute each fields and call parsing functions
        #  open inputfile
        #        getrecord
        #extract data with json desciptor
        #
        for element in jsondata['fields']:
            print(element['order']);   # Order of the field
            print(element['offset']);  # offset from the beginning of record
            print(element['length']);  # length of the field
            print(element['from']);    # input format of the field
            print(element['to']);      # output format of the field
            print(element['namevar']); # variable  name in json outputfile
        # Create Json record with extracted data, other format can be checked there
        # Write data to output file
        # Close every files



