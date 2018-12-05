def packedinteger(field):
    #fonction that returns integer  from a  packed decimal value
    # the data are 1rst transformed in hexadecimal value
    # which is a string starting with "0x"

    # the whole string is catenate except the last bytes containing
    #the sign  I.E: 'c' of 'f' for positive number, 'd' for negative

    field =hex(field);
    ll =len(str(field));
    #now the value contains a string  in the form of 0x12345F
    i=2;
    catnumber='';
    while i< ll - 1:
        catnumber = catnumber + field[i:i+1]
        i = i + 1
    sign = field[i:i+1]
    catnumber = int(catnumber)
    test = int(catnumber);
    if sign == 'd':
        catnumber = catnumber * - 1;

    return(catnumber)

field = 1193055;
field = 5805693; #12589D
print(packedinteger(field));
