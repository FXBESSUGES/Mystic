#-------------------------------------------------------------------------------
# Name:       Cobol copybook parser
# Purpose:    transforms cobol files (associated to PIC) into json format
#             X to EBCDIC, 9 to EBCDIC or numbers (INT)
#             S9 COMP binary (big endian) to integer or double integer (little
#             Endian
# Author:      FX  BESSUGES
#
# Created:     15/10/2018
# version :   1.0
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

def parsetype(field):
    # check if there is any parenthesis
    left_par = field.find('(');

    # check if there is any left parenthesis in   the
    # field, because we have to compute  length

    if  left_par > 0 :
        right_par = field.find(')');
        bound_le = left_par + 1
        bound_ri = right_par
        data_size = field[bound_le:bound_ri ]
        type_cobol = field[0:left_par]
        # now data_size got the length
        # while type_cobol gets X or 9
    else:
        # Data are specified  X or XX or whatever but
        #no parenthesis...
        subfield  = field.split('.')
        data_size = len(subfield[0])
        type_cobol= field[0];

    parsed_type= [ data_size,type_cobol]
    #now we can leave this function
    # and give away array with values

    return(parsed_type)



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


filename = args.cpycbl;
in_file = open(filename, "rt") # Open the Copy Book Cobol
offset = 0;
nbvars = 0;
#in_file = open("D:\Python\cobol\cobol.src", "r") # Open the Copy Book Cobol
ou_file = open(outfile, "w")
offset = 0;
nbvars = 0;
filename = "****";
jsonstring = [];
z=0;
for line in  in_file.readlines():
    #cobol_line_array = line.split(" ");
    idex = line.find("PIC")
    # if idex is not negative  ==> PIC or Picture is found
    # that means we have to split data
    if idex > 0:
        z = z + 1;    # number of vars in the copybook file


        line_array = line.split();
        level = line_array[0]
        # each fields are parsed from the copy cobol
        #source file:
        # Varname ====> Variable name behind level (only if a PIC is present)
        # Variable_type_in  and variable_type_out according to array below
        #   EBCDIC  -->  ASCII or integer if data is PIC 9
        #   Packed  -->  Integer
        #

        varname = line_array[1]
        typevar  = line_array[3]
        vardef =parsetype(typevar)
        #first element of vardef contains the length
        #Second the type as specified in the copy book cobol
        # with comp-3 data the length must be calculated
        #because it's memory representation can be shorter

        if vardef[1] == "9" or vardef[1] == "X":
            variable_len = int(vardef[0])
            variable_type_in = "EBCDIC"
            variable_type_ou = "ASCII"

        if filename != varname[0:4]:
           if filename != "****":
                ou_file.write(stringdata)

           filename = varname[0:4]
           entetestring = {}
           entetestring["filedesc"] = "filedesc:"
           entetestring["filename"] = filename
           entetestring["lrecl"] = 0
           entetestring["recfm"] = "f"
           offset = 0
           jsonstring.append(entetestring)

        fieldstring = {}
        fieldstring["order"] = z
        fieldstring["offset"] = offset
        fieldstring["namevar"] = varname
        fieldstring["length"] = variable_len
        fieldstring["from"] = variable_type_in
        fieldstring["to"] = variable_type_ou


        jsonstring.append(fieldstring)
        stringdata=str(json.dumps(jsonstring, sort_keys=False, indent=4))
        offset = offset + variable_len

ou_file.write(stringdata)
ou_file.close()
in_file.close()



