string=input("string to be encoded/decoded")
shift_num=int(input("Enter shift number:"))
operation=input("enter operation").lower()
def encode(string,shift_num):
    encoded_str=""
    for char in string:
        if char.isalpha():
            shift_base=ord('A') if char.isupper() else ord('a')
            encoded_char=chr((ord(char)-shift_base+shift_num)% 26 +shift_base)
            encoded_str+=encoded_char
        else:
            encoded_str+=char
    return encoded_str
def decode(encoded_str,shift_num):
    return encode(encoded_str,-shift_num)
if operation==encode:
    encodedres=encode(string,shift_num)
    print("Encoded string is :",encodedres)
else:
    decodedres=decode(string,shift_num)
    print("Decoded string is :",decodedres)
