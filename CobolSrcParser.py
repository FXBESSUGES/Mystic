#-------------------------------------------------------------------------------
# Name:        CobolSrcparser
# Purpose:
#
# Author:      X090670
#
# Created:     28/11/2018
# Copyright:   (c) X090670 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import argparse
import sys
import json
import binascii

from pathlib import Path

import argparse
import sys
import json
import binascii
import collections

def CobolSrcParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpycbl", help="Cobolfile to parse")
    parser.add_argument("--outfile", help="directory where to store results")

    args = parser.parse_args()
    if args.cpycbl:
        print("Cobol file is specified")
        in_cobol = Path(args.cpycbl)
        if in_cobol.is_file():
            print(args.cpycbl)

    if args.outfile:
        print("outputfile is specified")
        outfile = Path(args.outfile)
    json_file = []
    divisions = []
    sections = []
    variables= {}
    instructions =[]

    filename = args.cpycbl;
    #in_file = open(filename, "rt") # Open the Copy Book Cobol
    offset = 0;
    nbvars = 0;
    jsonstring = [];
    source = collections.Collection
    in_file = open("D:\\Python\\cobol\\testcobol.cob", "rt") # Open the Copy Book Cobol
    for line in  in_file.readlines():
        #cobol_line_array = line.split(" ");
        print(line)
        idex = line.find("PIC")
     # if idex is not negative  ==> PIC or Picture is found
     # that means we have to split data
        line_array = line.split();
        print(line_array)
        #json_pgm =json.JSONEncoder(line_array)
        jidx = 0
        if line.find("PROCEDURE DIVISION") > 0:
            #identification
            for word in line_array:
                divisions.append(word)
        if line.find("ENVIRONMENT") > 0:
            #identification
            for word in line_array:
                sections.append(word)
        if line.find("DATA DIVISION") > 0:
            #identification
            for word in line_array:
                sections.append(word)



    return None


if __name__ == '__main__':
    CobolSrcParser()

