import os
import sys
import time
import datetime
import struct
from datetime import timedelta
from struct import *
import json
# Test program for reading Mainframe file
# File  conversion treats Big Endian to Little
# and ASCII to EBCDIC

# for test purpose data ar located
# in a windows directory " data"
# we only parse  a few bytes from the first blocksize.

os.chdir("D:/data")
# some conversion fonction
def BigEndianToLittle(data):

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


f = open("smftom.data", "rb")
try:
      octets = f.read(4);
      bdw = BigEndianToLittle(octets[0:2]);

      if bdw == 0:
         exit;
      startlogical = 0;
      while True:
          octets = f.read(bdw) # read first block : 32760 +4 bytes for length
          if octets == "":
        	  break;

          rdw = BigEndianToLittle(octets[0:2]);
          logicalRec = octets[startlogical:rdw-1]
          startlogical = startlogical + rdw;
          bdw = bdw - rdw # decrease blocsize with logical length
          Z07FILEN = logicalRec[16:16+8]
          Z07FILEN = Z07FILEN.decode('cp500',"replace")

          Z07DSNAM = logicalRec[24:24+44]
          Z07DSNAM = Z07DSNAM.decode('cp500',"replace")

          print ('Z07SMFLG %d' % rdw);
          smfseg = octets[6:8]
          print ('Z07SMFNS %02X' % smfseg[0]);
          Z07SMFRT = int.from_bytes(logicalRec[5:6],'big')
          Z07SMFTM = int.from_bytes(logicalRec[6:10],'big')
          print(Z07SMFTM)
          Z07SMFTM = SmfTimeToTime(Z07SMFTM)
          print (Z07SMFTM)
          Z07SMFDT = bytes(logicalRec[10:14])
          Z07SMFDT = str(smftodate(Z07SMFDT));
          #hexdisplay(Z07SMFDT)

          #smfrty = octets[9:10]
          #smfrty =bin(smfrty);
          print('%d' % Z07SMFRT)
          record =json.JSONEncoder().encode([{"name":"Z07SMFDT","value":Z07SMFDT},{"name":"Z07SMFTM","value":Z07SMFTM}
          ,{"name":"Z07FILEN","value":Z07FILEN},{"name":"Z07DSNAM","value":Z07DSNAM}])

          print(record);

          break;
except IOError:
    	# Your error handling here
    	# Nothing for this example
     	pass
finally:
        f.close()




