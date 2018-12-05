#-------------------------------------------------------------------------------
# Name:        Library
# Purpose:
#
# Author:      X090670
#
# Created:     14/09/2018
# Copyright:   (c) X090670 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
import struct
from datetime import timedelta
from struct import *
def packed_integer(field,sens):

    #fonction that returns integer  from a  packed decimal value
    # the data are 1rst transformed in hexadecimal value
    # which is a string starting with "0x"

    # the whole string is catenate except the last bytes containing
    #the sign  I.E: 'c' of 'f' for positive number, 'd' for negative

    if sens == "A":
        field =hex(field);
        ll =len(str(field));
        if ll > 10 or ll <= 18:
            scheme = bigint
        if ll > 4 or ll <= 9:
            scheme = fint
        if ll > 0 or ll <= 4:
            scheme = sint
        #now the value contains a string  in the form of 0x12345F
        i=2;
        catnumber='';
        while i< ll - 1:
            catnumber = catnumber + field[i:i+1]
            i = i + 1
        sign = field[i:i+1]
        catnumber = int(catnumber)
        #test = hex(catnumber);



        if sign == 'd':
            catnumber = catnumber * - 1;
        return(catnumber)


    #  Sens is from Big Data to Mainframe


    if sens == "B":


        if field < 0:
            sign = "D"
            #field = field * -1
        if field >= 0:
            sign = "C"

        hexvalue = int(str(field),16)
        hexvalue = hex(hexvalue) + sign
        hexvar = "0" + str(hexvalue[3:len(hexvalue)])
        Vars =binascii.unhexlify(hexvar)

        ll = len(str(field))
        #BufferOut = struct.pack('1b',Vars)

        return(Vars)

def BigEndianToLittle(data):
    #Funtion which transform Big Endian Data to little
    #Endian
    valeur = int.from_bytes(data,'big')
    return(valeur)
def SmfTimeToTime(hundredths):
    # convert Time in Hundredths of seconds since midnight
    #info printable format
    milli = hundredths % 100;
    seconds = round(hundredths / 100);
    realtime = str(datetime.timedelta(seconds=seconds)) + str(".") +str(milli)
    return(realtime);
def hexdisplay(field):
    variable =join (hex(ord(n)) for n in field)
    print(variable);
def smftodate(field):
    CC = hex(field[0]);
    print(CC)
    YY = hex(field[1]);
    YY = int(str(YY[2:4])) + 2000
    print (YY);
    #YY =int.to_bytes(1,YY)
    DD1 = hex(field[2]);
    DD2 = hex(field[3]);
    DD3 = field[3] >> 4

    StringData = str(DD1)
    xx = StringData[2:4];
    DDD = (int(xx) * 10) + DD3
    date_debut = datetime.date(YY,1,1)
    smfdate = date_debut + timedelta(days=DDD)
    print(smfdate)
    #smfdate = smfdate.strftime('%Y-%M-%D')

    return(smfdate)