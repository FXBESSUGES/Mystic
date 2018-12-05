import argparse
import sys
import json
import os
import sys
import time
import logging
import datetime
import struct
from datetime import timedelta
from struct import *
import binascii
#--------------------Conversions fonctions starts here------
def packed_integer(field,sens):

    #fonction that returns integer  from a  packed decimal value
    # the data are 1rst transformed in hexadecimal value
    # which is a string starting with "0x"

    # the whole string is catenate except the last bytes containing
    #the sign  I.E: 'c' of 'f' for positive number, 'd' for negative

    if sens == "A":
        field =field.hex();
        ll =len(str(field));
        sign = field[ll-1:ll]
        value = int(field[0:ll-1])

        if sign == "D":
            value = value * -1


        return(value)


    #  Sens is from Big Data to Mainframe


    if sens == "B":


        if field < 0:
            sign = "D"
            #field = field * -1
        if field >= 0:
            sign = "C"

        hexvalue = int(str(field),16)
        hexvalue = hex(hexvalue) + sign
        realvalue =     len (str(hexvalue[2:len(hexvalue)]))
        if realvalue%2==0:
            hexvar =  str(hexvalue[2:len(hexvalue)])
        else:
            hexvar = "0" + str(hexvalue[2:len(hexvalue)])
        Vars =binascii.unhexlify(hexvar)

        ll = len(str(field))
        #BufferOut = struct.pack('1b',Vars)

        return(Vars)
#Ebcdic Ascii conversion routines
#
def ebcdic_ascii(field,sens):
    if sens =="A":
        field =bytes(field)

        field.decode('cp500',"replace")
        return(field)
    if sens=="B":
        champ = bytes(field)
        field = champ.decode('cp500',"replace")
        field = field.encode()

        return(field)
def extend_integer(field,sens):
    if sens == "A":
        field =bytes(field)
        field = field.hex()
        i = 0;valeur= " "
        while i <= len(field):
            check_val =field[i:i+1]
            if check_val =="f":
                i = i + 1
                sign = " "
            else :
                if check_val =="c":
                    sign = "+"
                    i = i + 1
                else:
                    if check_val == "d":
                        sign= "-"
                        i = i + 1
                    else:
                        valeur = valeur + check_val
                        i = i +1
        valeur = sign.strip() + valeur.strip()

    if sens == "B":
        if field >= 0 :
            sign = "C"
        if field < 0 :
            sign = "D"
        field = str(field)
        if sign == "C":
            field = "+".strip() + field
        i = 1;valeur = ""
        while i < len(field):
            valeur = valeur +"F" + field[i:i+1]
            i = i + 1
        valeur = valeur + sign

    return(valeur)

def BigEndian_LittleEndian(field,sens):
    if sens == "A":
        valeur = int.from_bytes(field,'big')
    if sens == "B":
        valeur = int.from_bytes(field,'little')
    return(valeur)
#--------------------Conversions fonctions stops here------

testfile = open("harry.bin","rb")

variable = testfile.read(11) # skip first characters
variable = testfile.read(4)  # read a full word (big endian)
variable = BigEndian_LittleEndian(variable,"A")
variable = -123456
variable = +234567
variable = extend_integer(variable,"B")



#variable =ebcdic_ascii(variable,"B")
#variable = packed_integer(variable,"A")
print(variable)
#variable = packed_integer(variable,"B")
#fileout = open("fileout.bin","wb");
#variable = bytearray(variable)
#fileout.write(variable)
#fileout.close()
#print(variable)

