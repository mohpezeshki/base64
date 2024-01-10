import string
import sys
import os


BASE64_TABLE = string.ascii_uppercase + string.ascii_lowercase + string.digits  + '+' + '/'

PADDING = "="

def get_string_bits(text):
    return  ''.join(format(ord(i), '08b') for i in text)
 

def encode_base64(b_str):
    base64_arr = []
    for i in range(len(b_str)//6):
        base64_arr.append(b_str[i*6:i*6+6])
    
    if len(b_str) % 6 != 0 :
        if len(b_str) % 6 == 4:
            _temp = b_str[-(len(b_str)%6):] + '00'
        else:
            _temp = b_str[-(len(b_str)%6):] + '0000'
        base64_arr.append(_temp)

    base64_arr = [int(item , base=2) for item in base64_arr]
    base64_str =  ''.join([BASE64_TABLE[item] for item in base64_arr])
    
    if len(b_str) % 6 ==  2:
        base64_str = base64_str + PADDING + PADDING
    if len(b_str) % 6 == 4:
        base64_str = base64_str + PADDING

    return base64_str

def decode_base64(text):
   
    bit_array = [format(BASE64_TABLE.find(i) , '08b') for i in text.replace(PADDING , "")]     
    
    for i in range(len(bit_array) - 1 ):
        bit_array[i] = bit_array[i][2:]

    if text[-2:] == PADDING + PADDING:
        bit_array[len(bit_array) -1 ] = bit_array[len(bit_array) - 1][6:]
    elif text[-1:] == PADDING:
        bit_array[len(bit_array) -1 ] = bit_array[len(bit_array) - 1][4:]
    else:
        bit_array[len(bit_array) -1 ] = bit_array[len(bit_array) - 1][2:]
    
    bit_str = ''.join(bit_array)
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(bit_str)]*8))

def get_file_bits(file_path):
    with open(file_path , 'rb') as f:
        contents = f.read()
    return ''.join([format(x, '08b') for x in contents])


if __name__ == "__main__":
    
    base64_txt = "INSERT encode OR decode COMMAND!"
    if len(sys.argv) < 3:
        print("Insert the text!")
    else:
        _typ = "string"
        if len(sys.argv) == 4 and sys.argv[2] == "file":
            _typ = "file"
            bit_string = get_file_bits(sys.argv[3])
        if sys.argv[1] == "encode":
            if _typ == "string": 
                base64_txt = encode_base64(get_string_bits(sys.argv[2]))
            else:
                base64_txt = encode_base64(bit_string)
        elif(sys.argv[1]) == "decode":
            base64_txt = decode_base64(sys.argv[2])
        
        print(base64_txt)
