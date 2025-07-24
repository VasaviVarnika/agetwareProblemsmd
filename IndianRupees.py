num= 1898345.67676 #float(input())
def indian(num):
    numstring=str(num)
    if '.' in numstring:
        int_part,dec_part=numstring.split(".")
        dec_part='.'+dec_part
    else:
        int_part=numstring
        dec_part=""
    
    intrev=int_part[::-1]
    grp=intrev[:3]
    
    for i in range(3,len(intrev),2):
        grp+=','+intrev[i:i+2]
    indian_format=grp[::-1]+dec_part
    return indian_format
print("indian format",indian(num))
