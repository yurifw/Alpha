#!/usr/bin/python
import random
import os


def to_bit_array(array):
    def bitfield(n, min_size):
        return [1 if digit == '1' else 0 for digit in bin(n)[2:].zfill(min_size)] # [2:] to chop off the "0b" part
    result = []
    for i in range(len(array)):
        result.extend(bitfield(array[i], 8))
    return result

def bit_array_2_decimal(bitarray):
    array = [0] * (len(bitarray)/8)

    for i in range(0,len(bitarray),8):
        decimal = pow(2,7)*bitarray[i] + pow(2,6)*bitarray[i+1] + pow(2,5)*bitarray[i+2] + pow(2,4)*bitarray[i+3] + pow(2,3)*bitarray[i+4] + pow(2,2)*bitarray[i+5]  + pow(2,1)*bitarray[i+6] + pow(2,0)*bitarray[i+7]
        array[i/8] = decimal
    return array

def generate_random_key(size, path):
    """generates a random key with size = to size (in bytes) and save it to path (path should include file name)"""
    key = bytearray()
    for i in range(size):
        key.append(random.randrange(0, 255))
    f = open(path, 'w+')
    f.write(key)
    f.close()


def read_file(path):
    """reads the given file and returns a bytearray"""
    bytes = bytearray()
    f = open(path)
    for b in f.read():
        bytes.append(ord(b))
    return bytes

def s_box(byte, key, block_index):
    def s_box0(byte):
        """pass the given byte through the rijndael's s-box and return the resultant byte
        """
        s_box = ((0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76),
                (0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0),
                (0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15),
                (0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75),
                (0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84),
                (0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf),
                (0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8),
                (0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2),
                (0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73),
                (0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb),
                (0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79),
                (0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08),
                (0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a),
                (0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e),
                (0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf),
                (0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16))
        col = byte >> 4
        row = byte & 15
        return s_box[col][row]

    def s_box1(byte):
        """pass the given byte through the grey sbox and return the resultant byte
        """
        s_box = ((0x63 , 0x7c , 0x7b , 0x77 , 0x6f , 0xc5 , 0x6b , 0xf2 , 0xfe , 0xd7 , 0x76 , 0xab , 0x67 , 0x2b , 0x01 , 0x30 ),
                (0xad , 0xd4 , 0xaf , 0xa2 , 0x72 , 0xc0 , 0xa4 , 0x9c , 0xfa , 0x59 , 0xf0 , 0x47 , 0xc9 , 0x7d , 0x82 , 0xca ),
                (0x04 , 0xc7 , 0xc3 , 0x23 , 0x05 , 0x9a , 0x96 , 0x18 , 0xeb , 0x27 , 0x75 , 0xb2 , 0x80 , 0xe2 , 0x12 , 0x07 ),
                (0x34 , 0xa5 , 0xf1 , 0xe5 , 0x31 , 0x15 , 0xd8 , 0x71 , 0x36 , 0x3f , 0xcc , 0xf7 , 0x93 , 0x26 , 0xfd , 0xb7 ),
                (0xd0 , 0xef , 0xfb , 0xaa , 0x33 , 0x85 , 0x4d , 0x43 , 0x50 , 0x3c , 0xa8 , 0x9f , 0x02 , 0x7f , 0xf9 , 0x45 ),
                (0xbc , 0xb6 , 0x21 , 0xda , 0xf3 , 0xd2 , 0xff , 0x10 , 0x92 , 0x9d , 0xf5 , 0x38 , 0x40 , 0x8f , 0xa3 , 0x51 ),
                (0x53 , 0xd1 , 0xed , 0x00 , 0xb1 , 0x5b , 0xfc , 0x20 , 0x4a , 0x4c , 0xcf , 0x58 , 0xbe , 0x39 , 0xcb , 0x6a ),
                (0x52 , 0x3b , 0xb3 , 0xd6 , 0x2f , 0x84 , 0xe3 , 0x29 , 0x1b , 0x6e , 0xa0 , 0x5a , 0x2c , 0x1a , 0x83 , 0x09 ),
                (0xba , 0x78 , 0x2e , 0x25 , 0xb4 , 0xc6 , 0xa6 , 0x1c , 0x4b , 0xbd , 0x8a , 0x8b , 0x74 , 0x1f , 0xdd , 0xe8 ),
                (0x61 , 0x35 , 0xb9 , 0x57 , 0x1d , 0x9e , 0xc1 , 0x86 , 0x48 , 0x03 , 0x0e , 0xf6 , 0xb5 , 0x66 , 0x3e , 0x70 ),
                (0x8c , 0xa1 , 0x0d , 0x89 , 0x42 , 0x68 , 0xe6 , 0xbf , 0xb0 , 0x54 , 0x16 , 0xbb , 0x2d , 0x0f , 0x99 , 0x41 ),
                (0x9b , 0x1e , 0xe9 , 0x87 , 0x28 , 0xdf , 0x55 , 0xce , 0x69 , 0xd9 , 0x94 , 0x8e , 0x98 , 0x11 , 0xf8 , 0xe1 ),
                (0xe0 , 0x32 , 0x0a , 0x3a , 0x24 , 0x5c , 0x06 , 0x49 , 0x91 , 0x95 , 0x79 , 0xe4 , 0xac , 0x62 , 0xd3 , 0xc2 ),
                (0x6c , 0x56 , 0xea , 0xf4 , 0xae , 0x08 , 0x7a , 0x65 , 0x8d , 0xd5 , 0xa9 , 0x4e , 0x37 , 0x6d , 0xc8 , 0xe7 ),
                (0x60 , 0x81 , 0xdc , 0x4f , 0x90 , 0x88 , 0x2a , 0x22 , 0xde , 0x5e , 0xdb , 0x0b , 0xb8 , 0x14 , 0xee , 0x46 ),
                (0xc4 , 0xa7 , 0x3d , 0x7e , 0x19 , 0x73 , 0x5d , 0x64 , 0x5f , 0x97 , 0x17 , 0x44 , 0x13 , 0xec , 0x0c , 0xcd ))
        col = byte >> 4
        row = byte & 15
        return s_box[col][row]

    def s_box2(byte):
        """pass the given byte through the apa s-box and return the resultant byte
        """
        s_box = ((0x8c , 0x90 , 0xd9 , 0xc1 , 0x46 , 0x63 , 0x53 , 0xf1 , 0x61 , 0x32 , 0x15 , 0x3e , 0x26 , 0x9a , 0x97 , 0x2e),
                (0xd8 , 0xa0 , 0x99 , 0x9e , 0xc0 , 0x95 , 0x67 , 0xb7 , 0x6d , 0xe0 , 0xf3 , 0x28 , 0x20 , 0x86 , 0xb6 , 0xef),
                (0x4b , 0x31 , 0xb5 , 0xd2 , 0x13 , 0x39 , 0x6c , 0xa5 , 0x03 , 0x3f , 0x4d , 0x34 , 0xf9 , 0xec , 0x8e , 0x17),
                (0xc5 , 0x25 , 0x3c , 0x89 , 0xc9 , 0x2b , 0x3a , 0xc2 , 0x6e , 0xc6 , 0xaa , 0x91 , 0x49 , 0x18 , 0x93 , 0xde),
                (0x0d , 0x6f , 0x65 , 0xaf , 0x92 , 0xa7 , 0xf6 , 0xa6 , 0x40 , 0xb9 , 0xed , 0xb0 , 0xc3 , 0xd7 , 0x7d , 0x7c),
                (0x54 , 0x59 , 0xdf , 0x2f , 0xda , 0xa4 , 0x05 , 0x94 , 0x9b , 0x72 , 0x01 , 0x74 , 0xa9 , 0xf7 , 0x81 , 0xe9),
                (0x1f , 0xb3 , 0xeb , 0xcf , 0xe8 , 0x47 , 0x52 , 0x36 , 0xbc , 0x16 , 0x29 , 0x76 , 0x12 , 0xfa , 0x9c , 0x8a),
                (0x5b , 0xa8 , 0x43 , 0xd1 , 0x79 , 0x85 , 0x42 , 0x82 , 0xc7 , 0xa1 , 0x78 , 0x4f , 0xe2 , 0x35 , 0xea , 0xad),
                (0xdc , 0x0e , 0xd3 , 0x2d , 0x6a , 0x5a , 0x44 , 0xab , 0xc8 , 0xe5 , 0x37 , 0x0a , 0x6b , 0x51 , 0xe3 , 0x14),
                (0xcd , 0x56 , 0x4a , 0xd6 , 0x08 , 0x83 , 0xbb , 0x33 , 0xe1 , 0x30 , 0x4e , 0x24 , 0x5e , 0xb4 , 0x00 , 0x48),
                (0x5f , 0x22 , 0x0b , 0x50 , 0x3d , 0x80 , 0x1a , 0xbf , 0xcc , 0xff , 0x64 , 0x87 , 0x1b , 0xc4 , 0x07 , 0xf8),
                (0x0c , 0xd4 , 0xac , 0x02 , 0x10 , 0x84 , 0x7e , 0x69 , 0x70 , 0x60 , 0x55 , 0x2a , 0x21 , 0x57 , 0x23 , 0x66),
                (0x62 , 0x73 , 0xcb , 0x41 , 0x58 , 0x71 , 0x77 , 0x1c , 0x7b , 0x8f , 0x9f , 0x9d , 0xa3 , 0xb1 , 0x7f , 0x5d),
                (0xf4 , 0x06 , 0xae , 0xd5 , 0xe6 , 0x3b , 0xba , 0xFe , 0x96 , 0xe7 , 0x0f , 0x45 , 0x2c , 0xf0 , 0xfc , 0xbd),
                (0xe4 , 0x98 , 0xfb , 0xca , 0x11 , 0xf5 , 0xdd , 0x7a , 0x5c , 0xfd , 0xce , 0x88 , 0xd0 , 0x68 , 0x8d , 0x4c),
                (0xbe , 0x04 , 0x38 , 0x1d , 0x1e , 0xf2 , 0x27 , 0x19 , 0xb2 , 0x75 , 0xa2 , 0xee , 0xdb , 0xb8 , 0x09 , 0x8b))
        col = byte >> 4
        row = byte & 15
        return s_box[col][row]

    def s_box3(byte):
        """pass the given byte through the performance improved s-box and return the resultant byte
        """
        s_box = ((0x54 , 0xd7 , 0x04 , 0x34 , 0xed , 0x8b , 0x64 , 0xce , 0x19 , 0x22 , 0xbb , 0x75 , 0xdd , 0x86 , 0x88 , 0xff),
                (0xf2 , 0xd3 , 0xfe , 0x2c , 0x32 , 0xbc , 0xc4 , 0x1a , 0x90 , 0x8a , 0xac , 0x67 , 0xab , 0xb4 , 0x10 , 0xda),
                (0x07 , 0xd1 , 0x97 , 0xbe , 0x01 , 0x25 , 0xf9 , 0xea , 0xf6 , 0x4f , 0xb1 , 0xe1 , 0x1c , 0xba , 0xe2 , 0x72),
                (0x36 , 0x39 , 0xaa , 0xd6 , 0xb9 , 0x83 , 0xcd , 0xb3 , 0x3a , 0x91 , 0x24 , 0x52 , 0x76 , 0x45 , 0x13 , 0xf3),
                (0xfd , 0x28 , 0x96 , 0x4e , 0xb5 , 0x9f , 0xb0 , 0x5b , 0x6f , 0xca , 0x7d , 0xe8 , 0x82 , 0xa9 , 0x9a , 0xcb),
                (0x94 , 0x9e , 0xd9 , 0x6e , 0xa6 , 0x2a , 0x1f , 0x4b , 0x70 , 0x09 , 0x23 , 0x3d , 0x0f , 0x17 , 0x47 , 0xe6),
                (0x65 , 0x99 , 0x73 , 0xc9 , 0x2b , 0xec , 0x15 , 0x30 , 0x33 , 0x3e , 0x2e , 0xdb , 0x98 , 0x29 , 0xa7 , 0x84),
                (0x63 , 0x57 , 0x27 , 0x18 , 0x6c , 0x50 , 0xc6 , 0x0e , 0xd4 , 0xfc , 0x4d , 0x5d , 0x66 , 0x26 , 0x16 , 0x92),
                (0x11 , 0xe9 , 0x6a , 0x95 , 0xa4 , 0x78 , 0xc8 , 0x85 , 0x35 , 0xb8 , 0x20 , 0xd2 , 0xb7 , 0x53 , 0x42 , 0xeb),
                (0x58 , 0xdf , 0x1b , 0x55 , 0x51 , 0x8e , 0x9b , 0xfb , 0x3f , 0x62 , 0x3b , 0x89 , 0xa2 , 0x5f , 0x0a , 0xb6),
                (0xa5 , 0xee , 0x31 , 0xf1 , 0x03 , 0xc1 , 0x49 , 0xa8 , 0x2d , 0x69 , 0x6b , 0xaf , 0x60 , 0x8f , 0x4a , 0xc3),
                (0x46 , 0x05 , 0xfa , 0x93 , 0xef , 0x71 , 0xe0 , 0x7f , 0x68 , 0x80 , 0xf5 , 0x8d , 0x4c , 0xcf , 0x9c , 0x06),
                (0xcc , 0x38 , 0xb2 , 0x61 , 0x56 , 0x43 , 0x0b , 0xc2 , 0x7a , 0xae , 0x08 , 0x5a , 0xf4 , 0x2f , 0xf7 , 0x0c),
                (0xe7 , 0xde , 0xf0 , 0x40 , 0xf8 , 0xd5 , 0x02 , 0x1e , 0xa3 , 0x0d , 0x7b , 0xc0 , 0x3c , 0x21 , 0xad , 0x5c),
                (0x5e , 0xc5 , 0x44 , 0x9d , 0x7c , 0x41 , 0xe3 , 0x74 , 0x48 , 0xa1 , 0xc7 , 0x81 , 0x1d , 0x8c , 0x79 , 0x59),
                (0x14 , 0xa0 , 0x00 , 0x12 , 0xd8 , 0xbd , 0xd0 , 0x87 , 0xdc , 0xbf , 0x6d , 0xe5 , 0xe4 , 0x77 , 0x37 , 0x7e))
        col = byte >> 4
        row = byte & 15
        return s_box[col][row]

    key_bits = to_bit_array(key)
    maximum_blocks = len(key_bits)/2
    key_block = block_index % maximum_blocks

    s_box_index = get_block(key_bits, key_block , 2)
    if (s_box_index == [0,0]):
        return s_box0(byte)
    elif (s_box_index==[0,1]):
        return s_box1(byte)
    elif (s_box_index==[1,0]):
        return s_box2(byte)
    elif (s_box_index==[1,1]):
        return s_box3(byte)

def get_block(array, n, block_size):
    """returns the nth block of a block_size'd array (n starts at 0)"""
    return array[(n*block_size):(n*block_size+block_size)]


def key_expand(key, size):
    """expands the given key until it reaches the specified size (in bytes)"""
    rcon = bytearray()
    rcon.extend([0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
                0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
                0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
                0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
                0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
                0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
                0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b,
                0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
                0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
                0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
                0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
                0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
                0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
                0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
                0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd,
                0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d])
    rcon_index = 1
    initial_size = len(key)

    def schedule_core(temp, r):
        aux = temp[0]  # rotword
        temp[0] = temp[1]
        temp[1] = temp[2]
        temp[2] = temp[3]
        temp[3] = aux
        for i in range(4):
            temp[i] = s_box(temp[i])
        temp[0] = temp[0] ^ rcon[r]
        return temp
    t = [0]*4  # initializing temporary bytes
    while len(key) < size:
        t[0] = key[-4]
        t[1] = key[-3]
        t[2] = key[-2]
        t[3] = key[-1]

        if (len(key) % 16) == 0:
            t = schedule_core(t, rcon_index)
            rcon_index = rcon_index +1

        key.append(t[0] ^ key[len(key)-initial_size])
        key.append(t[1] ^ key[len(key)-initial_size])
        key.append(t[2] ^ key[len(key)-initial_size])
        key.append(t[3] ^ key[len(key)-initial_size])
    return key


def n_alpha(xy):
    """n_alpha transformation"""
    return s_box(xy)


def l_alpha(e):
    """l_alpha transformation, uses the matrix defined at Lambert's dissertation (appendix 12.8.1)"""
    def transform(seq):
        t = [None]*64
        t[0] = ((seq[5] >> 2) ^ (seq[5] >> 4) ^ (seq[1] >> 6) ^ (seq[0] >> 5) ^ (seq[6] >> 7) ^ (seq[3] >> 5) ^ (seq[4] >> 6)) & 1
        t[1] = ((seq[7] >> 2) ^ (seq[4] >> 2) ^ (seq[2] >> 2) ^ (seq[1] >> 5) ^ (seq[6] >> 1) ^ (seq[5] >> 6) ^ (seq[3] >> 6)) & 1
        t[2] = ((seq[3] >> 1) ^ (seq[2] >> 1) ^ (seq[3] >> 3) ^ (seq[0] >> 4) ^ (seq[1] >> 2) ^ (seq[7] >> 7) ^ (seq[5] >> 5)) & 1
        t[3] = ((seq[1] >> 4) ^ (seq[0] >> 1) ^ (seq[7] >> 6) ^ (seq[6] >> 4) ^ (seq[1] >> 2) ^ (seq[4] >> 5) ^ (seq[5] >> 4)) & 1
        t[4] = ((seq[2] >> 3) ^ (seq[5] >> 7) ^ (seq[0]) ^ (seq[4] >> 7) ^ (seq[3] >> 7) ^ (seq[1] >> 7) ^ (seq[3])) & 1
        t[5] = ((seq[6] >> 3) ^ (seq[2]) ^ (seq[4] >> 6) ^ (seq[6] >> 6) ^ (seq[7] >> 5) ^ (seq[0]) ^ (seq[3] >> 5)) & 1
        t[6] = ((seq[3] >> 2) ^ (seq[2] >> 2) ^ (seq[5] >> 6) ^ (seq[0]) ^ (seq[7] >> 6) ^ (seq[6] >> 4) ^ (seq[4] >> 7)) & 1
        t[7] = ((seq[0] >> 3) ^ (seq[6] >> 2) ^ (seq[3] >> 6) ^ (seq[4] >> 1) ^ (seq[2]) ^ (seq[1] >> 1) ^ (seq[0] >> 6)) & 1

        t[8] = ((seq[0] >> 3) ^ (seq[4] >> 3) ^ (seq[0] >> 2) ^ (seq[2] >> 7) ^ (seq[7] >> 4) ^ (seq[1] >> 5) ^ (seq[2] >> 6)) & 1
        t[9] = ((seq[3] >> 1) ^ (seq[3] >> 5) ^ (seq[0] >> 2) ^ (seq[6] >> 7) ^ (seq[4] >> 1) ^ (seq[6] >> 6) ^ (seq[1] >> 3)) & 1
        t[10] = ((seq[1] >> 4) ^ (seq[7] >> 4) ^ (seq[1] >> 3) ^ (seq[4] >> 1) ^ (seq[6]) ^ (seq[0] >> 6) ^ (seq[2])) & 1
        t[11] = ((seq[2] >> 3) ^ (seq[1] >> 5) ^ (seq[7] >> 4) ^ (seq[0] >> 4) ^ (seq[2] >> 7) ^ (seq[7] >> 6) ^ (seq[6] >> 4)) & 1
        t[12] = ((seq[3] >> 2) ^ (seq[6] >> 7) ^ (seq[0] >> 7 >> 7) ^ (seq[3]) ^ (seq[5] >> 1) ^ (seq[2] >> 1) ^ (seq[7] >> 7)) & 1
        t[13] = ((seq[5] >> 2) ^ (seq[1] >> 1) ^ (seq[3] >> 7) ^ (seq[4] >> 7) ^ (seq[5] >> 7) ^ (seq[6] >> 1) ^ (seq[2] >> 2)) & 1
        t[14] = ((seq[4] >> 4) ^ (seq[0] >> 6) ^ (seq[1] >> 3) ^ (seq[5] >> 4) ^ (seq[1] >> 7) ^ (seq[7] >> 4) ^ (seq[5] >> 7)) & 1
        t[15] = ((seq[6] >> 3) ^ (seq[5] >> 1) ^ (seq[4]) ^ (seq[2] >> 5) ^ (seq[6]) ^ (seq[0] >> 1) ^ (seq[1] >> 7)) & 1

        t[16] = ((seq[1] >> 4) ^ (seq[0]) ^ (seq[4] >> 3) ^ (seq[2] >> 6) ^ (seq[3] >> 7) ^ (seq[7] >> 5) ^ (seq[6] >> 1)) & 1
        t[17] = ((seq[5] >> 2) ^ (seq[1]) ^ (seq[0] >> 4) ^ (seq[7] >> 7) ^ (seq[2] >> 5) ^ (seq[5] >> 1) ^ (seq[0] >> 2)) & 1
        t[18] = ((seq[5]) ^ (seq[6]) ^ (seq[5] >> 5) ^ (seq[7] >> 1) ^ (seq[4] >> 2) ^ (seq[0] >> 2) ^ (seq[6] >> 2)) & 1
        t[19] = ((seq[6] >> 3) ^ (seq[6] >> 5) ^ (seq[0] >> 5) ^ (seq[7]) ^ (seq[4] >> 2) ^ (seq[1] >> 2) ^ (seq[5] >> 4)) & 1
        t[20] = ((seq[7] >> 1) ^ (seq[5]) ^ (seq[1] >> 4) ^ (seq[0] >> 3) ^ (seq[3] >> 1) ^ (seq[7] >> 2) ^ (seq[6] >> 3)) & 1
        t[21] = ((seq[4] >> 4) ^ (seq[7] >> 7) ^ (seq[2] >> 5) ^ (seq[4]) ^ (seq[7] >> 6) ^ (seq[6] >> 2) ^ (seq[3] >> 7)) & 1
        t[22] = ((seq[3] >> 1) ^ (seq[5] >> 3) ^ (seq[2] >> 4) ^ (seq[4] >> 5) ^ (seq[0]) ^ (seq[1] >> 7) ^ (seq[7] >> 6)) & 1
        t[23] = ((seq[3] >> 2) ^ (seq[1] >> 1) ^ (seq[6]) ^ (seq[4] >> 3) ^ (seq[6] >> 2) ^ (seq[0] >> 1) ^ (seq[1] >> 6)) & 1

        t[24] = ((seq[0] >> 3) ^ (seq[1]) ^ (seq[2] >> 2) ^ (seq[5] >> 6) ^ (seq[3] >> 3) ^ (seq[6] >> 5) ^ (seq[5] >> 3)) & 1
        t[25] = ((seq[6] >> 3) ^ (seq[2] >> 1) ^ (seq[3] >> 3) ^ (seq[6] >> 2) ^ (seq[1] >> 6) ^ (seq[7] >> 4) ^ (seq[3])) & 1
        t[26] = ((seq[3] >> 2) ^ (seq[2] >> 4) ^ (seq[4] >> 2) ^ (seq[7] >> 5) ^ (seq[3] >> 7) ^ (seq[5] >> 3) ^ (seq[3] >> 6)) & 1
        t[27] = ((seq[5] >> 2) ^ (seq[1] >> 2) ^ (seq[5] >> 3) ^ (seq[4] >> 3) ^ (seq[2] >> 1) ^ (seq[4] >> 1) ^ (seq[7] >> 3)) & 1
        t[28] = ((seq[4] >> 4) ^ (seq[4] >> 5) ^ (seq[3]) ^ (seq[0] >> 4) ^ (seq[6] >> 7) ^ (seq[1] >> 5) ^ (seq[5] >> 1)) & 1
        t[29] = ((seq[5]) ^ (seq[7] >> 5) ^ (seq[4]) ^ (seq[1] >> 3) ^ (seq[2]) ^ (seq[3] >> 5) ^ (seq[0] >> 1)) & 1
        t[30] = ((seq[2] >> 3) ^ (seq[2] >> 1) ^ (seq[4] >> 2) ^ (seq[1] >> 6) ^ (seq[6] >> 1) ^ (seq[0] >> 5) ^ (seq[5] >> 3)) & 1
        t[31] = ((seq[0] >> 3) ^ (seq[3] >> 6) ^ (seq[7] >> 5) ^ (seq[4] >> 2) ^ (seq[6] >> 7) ^ (seq[0] >> 7) ^ (seq[1] >> 2)) & 1

        t[32] = ((seq[0] >> 3) ^ (seq[5] >> 1) ^ (seq[7] >> 7) ^ (seq[3] >> 4) ^ (seq[0] >> 1) ^ (seq[4]) ^ (seq[6] >> 4)) & 1
        t[33] = ((seq[5] >> 2) ^ (seq[0] >> 1) ^ (seq[6]) ^ (seq[2] >> 4) ^ (seq[3] >> 3) ^ (seq[5] >> 6) ^ (seq[7])) & 1
        t[34] = ((seq[5]) ^ (seq[1] >> 7) ^ (seq[1] >> 1) ^ (seq[0] >> 4) ^ (seq[7]) ^ (seq[6] >> 5) ^ (seq[4] >> 7)) & 1
        t[35] = ((seq[5]) ^ (seq[3] >> 3) ^ (seq[4] >> 3) ^ (seq[2] >> 2) ^ (seq[1] >> 1) ^ (seq[6] >> 7) ^ (seq[5] >> 6)) & 1
        t[36] = ((seq[4] >> 4) ^ (seq[0] >> 2) ^ (seq[6] >> 5) ^ (seq[4] >> 1) ^ (seq[1]) ^ (seq[3] >> 5) ^ (seq[2] >> 6)) & 1
        t[37] = ((seq[3] >> 1) ^ (seq[5] >> 7) ^ (seq[6] >> 1) ^ (seq[3] >> 4) ^ (seq[5] >> 6) ^ (seq[1] >> 6) ^ (seq[7] >> 3)) & 1
        t[38] = ((seq[7] >> 2) ^ (seq[0] >> 5) ^ (seq[7] >> 6) ^ (seq[4] >> 5) ^ (seq[0]) ^ (seq[1]) ^ (seq[6] >> 4)) & 1
        t[39] = ((seq[3] >> 2) ^ (seq[5] >> 5) ^ (seq[2] >> 6) ^ (seq[0] >> 4) ^ (seq[7] >> 4) ^ (seq[3] >> 5) ^ (seq[4] >> 6)) & 1

        t[40] = ((seq[0] >> 3) ^ (seq[4] >> 6) ^ (seq[6] >> 6) ^ (seq[2] >> 7) ^ (seq[7] >> 3) ^ (seq[0] >> 4) ^ (seq[7] >> 1)) & 1
        t[41] = ((seq[4] >> 4) ^ (seq[1] >> 5) ^ (seq[0] >> 7) ^ (seq[6] >> 4) ^ (seq[3] >> 6) ^ (seq[4] >> 5) ^ (seq[2] >> 7)) & 1
        t[42] = ((seq[2] >> 5) ^ (seq[5] >> 4) ^ (seq[2] >> 7) ^ (seq[6] >> 5) ^ (seq[2]) ^ (seq[6] >> 1) ^ (seq[0] >> 6)) & 1
        t[43] = ((seq[6] >> 3) ^ (seq[5] >> 3) ^ (seq[6] >> 4) ^ (seq[1] >> 3) ^ (seq[5] >> 5) ^ (seq[7] >> 1) ^ (seq[2] >> 2)) & 1
        t[44] = ((seq[3] >> 1) ^ (seq[4] >> 3) ^ (seq[6] >> 2) ^ (seq[2] >> 7) ^ (seq[7]) ^ (seq[5] >> 4) ^ (seq[1] >> 1)) & 1
        t[45] = ((seq[5]) ^ (seq[6] >> 6) ^ (seq[3] >> 4) ^ (seq[0] >> 7) ^ (seq[4] >> 6) ^ (seq[1] >> 2) ^ (seq[2] >> 6)) & 1
        t[46] = ((seq[7] >> 2) ^ (seq[3] >> 4) ^ (seq[5] >> 3) ^ (seq[2]) ^ (seq[4]) ^ (seq[5] >> 5) ^ (seq[2] >> 1)) & 1
        t[47] = ((seq[2] >> 3) ^ (seq[4] >> 4) ^ (seq[5] >> 2) ^ (seq[3] >> 2) ^ (seq[2] >> 5) ^ (seq[4] >> 5) ^ (seq[6] >> 2)) & 1

        t[48] = ((seq[4] >> 4) ^ (seq[3] >> 3) ^ (seq[0]) ^ (seq[2]) ^ (seq[6] >> 6) ^ (seq[4] >> 2) ^ (seq[5] >> 5)) & 1
        t[49] = ((seq[5] >> 2) ^ (seq[7] >> 1) ^ (seq[2] >> 6) ^ (seq[0] >> 2) ^ (seq[6] >> 5) ^ (seq[3]) ^ (seq[7] >> 5)) & 1
        t[50] = ((seq[7] >> 2) ^ (seq[3] >> 7) ^ (seq[0] >> 1) ^ (seq[7] >> 4) ^ (seq[1] >> 7) ^ (seq[4] >> 7) ^ (seq[1] >> 1)) & 1
        t[51] = ((seq[1] >> 4) ^ (seq[6]) ^ (seq[1] >> 3) ^ (seq[0] >> 5) ^ (seq[5] >> 7) ^ (seq[3] >> 5) ^ (seq[1] >> 6)) & 1
        t[52] = ((seq[2] >> 3) ^ (seq[2] >> 4) ^ (seq[3] >> 6) ^ (seq[1]) ^ (seq[0] >> 2) ^ (seq[7] >> 7) ^ (seq[5] >> 4)) & 1
        t[53] = ((seq[5]) ^ (seq[1]) ^ (seq[6] >> 7) ^ (seq[7] >> 3) ^ (seq[0] >> 5) ^ (seq[4] >> 6) ^ (seq[2] >> 1)) & 1
        t[54] = ((seq[3] >> 1) ^ (seq[7] >> 5) ^ (seq[0] >> 6) ^ (seq[4] >> 6) ^ (seq[2] >> 6) ^ (seq[3]) ^ (seq[5] >> 1)) & 1
        t[55] = ((seq[2] >> 5) ^ (seq[1] >> 3) ^ (seq[7] >> 1) ^ (seq[3] >> 4) ^ (seq[4] >> 1) ^ (seq[1] >> 5) ^ (seq[0] >> 5)) & 1

        t[56] = ((seq[6] >> 3) ^ (seq[5] >> 6) ^ (seq[0] >> 6) ^ (seq[7] >> 6) ^ (seq[3] >> 4) ^ (seq[4] >> 3) ^ (seq[2] >> 4)) & 1
        t[57] = ((seq[1] >> 4) ^ (seq[1] >> 5) ^ (seq[3]) ^ (seq[4] >> 7) ^ (seq[5] >> 5) ^ (seq[2] >> 2) ^ (seq[7])) & 1
        t[58] = ((seq[3] >> 2) ^ (seq[7] >> 3) ^ (seq[3] >> 4) ^ (seq[1] >> 2) ^ (seq[4] >> 5) ^ (seq[6] >> 6) ^ (seq[1])) & 1
        t[59] = ((seq[1] >> 4) ^ (seq[7] >> 7) ^ (seq[0] >> 7) ^ (seq[6] >> 6) ^ (seq[1] >> 6) ^ (seq[4]) ^ (seq[2] >> 4)) & 1
        t[60] = ((seq[7] >> 2) ^ (seq[2] >> 4) ^ (seq[6]) ^ (seq[4] >> 7) ^ (seq[3] >> 7) ^ (seq[0] >> 7) ^ (seq[7] >> 1)) & 1
        t[61] = ((seq[2] >> 3) ^ (seq[7] >> 3) ^ (seq[0] >> 6) ^ (seq[4] >> 1) ^ (seq[5] >> 1) ^ (seq[6] >> 5) ^ (seq[7])) & 1
        t[62] = ((seq[2] >> 5) ^ (seq[2] >> 3) ^ (seq[5] >> 7) ^ (seq[3] >> 3) ^ (seq[7]) ^ (seq[4]) ^ (seq[1] >> 7)) & 1
        t[63] = ((seq[7] >> 2) ^ (seq[7] >> 3) ^ (seq[5] >> 7) ^ (seq[2] >> 7) ^ (seq[3] >> 6) ^ (seq[0] >> 7) ^ (seq[6] >> 1)) & 1

        s = [None]*8
        s[0] = (t[0] << 7) | (t[1] << 6) | (t[2] << 5) | (t[3] << 4) | (t[4] << 3) | (t[5] << 2) | (t[6] << 1) | (t[7])
        s[1] = (t[8] << 7) | (t[9] << 6) | (t[10] << 5) | (t[11] << 4) | (t[12] << 3) | (t[13] << 2) | (t[14] << 1) | (t[15])
        s[2] = (t[16] << 7) | (t[17] << 6) | (t[18] << 5) | (t[19] << 4) | (t[20] << 3) | (t[21] << 2) | (t[22] << 1) | (t[23])
        s[3] = (t[24] << 7) | (t[25] << 6) | (t[26] << 5) | (t[27] << 4) | (t[28] << 3) | (t[29] << 2) | (t[30] << 1) | (t[31])
        s[4] = (t[32] << 7) | (t[33] << 6) | (t[34] << 5) | (t[35] << 4) | (t[36] << 3) | (t[37] << 2) | (t[38] << 1) | (t[39])
        s[5] = (t[40] << 7) | (t[41] << 6) | (t[42] << 5) | (t[43] << 4) | (t[44] << 3) | (t[45] << 2) | (t[46] << 1) | (t[47])
        # noinspection PyInterpreter
        s[6] = (t[48] << 7) | (t[49] << 6) | (t[50] << 5) | (t[51] << 4) | (t[52] << 3) | (t[53] << 2) | (t[54] << 1) | (t[55])
        s[7] = (t[56] << 7) | (t[57] << 6) | (t[58] << 5) | (t[59] << 4) | (t[60] << 3) | (t[61] << 2) | (t[62] << 1) | (t[63])
        return s
    result=bytearray()
    for i in range(len(e)/8):  #8 is the amount of bits this functions transforms
        result.extend(transform(get_block(e,i,8)))
    return result

def encipher_block(text, key, rounds, block_size, encipher):
    """encipher or decipher the given text (True to encipher and False to decipher), using the given key(not expanded)
    the algorithm will do nr rounds. For now, the only block_size ssupported is 16, and the rounds should also be 16
    """
    expanded_key = key_expand(key, rounds * block_size)
    key = [[None]*block_size]*rounds
    for i in range(rounds):
        if encipher:
            key[i] = get_block(expanded_key, i, block_size)
        else:
            key[rounds-1-i] = get_block(expanded_key, i, block_size)

    half_block = block_size/2
    #intializing left[0] and right[0]
    left_prev = [0]*half_block
    left = [0]*half_block
    right_prev = [0]*half_block
    right = [0]*half_block

    temporary = [0]*half_block

    for j in range(half_block):
        left_prev[j] = text[j]  # left zero
        right_prev[j] = text[j + half_block]  # right zero

    #starting alpha iterations (rounds)
    for i in range(rounds):
        # left[i]
        for j in range(half_block):
            left[j] = right_prev[j] ^ key[i][j]  # key[j]=Ke[j]

        # right[i]
        for j in range(half_block):
            temporary[j] = right_prev[j]

        if not encipher:
            for j in range(half_block):
                temporary[j] = temporary[j] ^ key[i][j]  # if deciphering, do a xor with Ke

        right = l_alpha(temporary)

        for j in range(half_block):
            temporary[j] = (right[j] ^ key[i][j+half_block])  # Kd[j]== key[j+8]

        for j in range(half_block):
            byte = temporary[j]
            n_alpha(byte)
            temporary[j] = byte

        for j in range(half_block):
            right[j] = (left_prev[j] ^ temporary[j])
            left_prev[j] = left[j]
            right_prev[j] = right[j]

    for j in range(half_block):  # text = right | left (last permutation)
        text[j] = right[j]
        text[j+half_block] = left[j]
    return text


def pad(block, size):
    """add padding bytes to the block until it reaches the defined size,
    """
    if len(block) % size !=0:
        bytes_needed = size - (len(block) % size)
        for i in range(bytes_needed):
            block.append(bytes_needed)


def unpad(padded_block):
    """removes the bytes that were added with pad"""
    #note: if no byte was padded and by coincidence, the last byte is 1, it will be removed even if it shouldn't
    added_bytes = padded_block[-1]
    if padded_block[-2] == padded_block[-1]:
        for i in range(added_bytes):
            padded_block.pop()


def encipher(input_file, key, rounds, block_size, enciphering, output_file):
    """encipher or decipher a file, independent of the size. original name file is kept in first block, original
    extension is kept in the second block. input_file must be the whole absolute path to the file (including
    name and extension), when deciphering, output_file should be a path to a directory (name and file extensions should
    be in the first and second blocks)
    """
    bytes = bytearray()

    if enciphering:  # storing file extension in first block
        file_name = input_file[input_file.rfind(os.sep)+1:]
        extension = file_name[file_name.find(".")+1:]
        bytes = bytearray()

        for c in extension:
            bytes.append(ord(c))
        pad(bytes, block_size)

    bytes.extend(read_file(input_file))
    pad(bytes, block_size)

    result = bytearray()
    for i in range(len(bytes)/block_size):
        result.extend(encipher_block(get_block(bytes, i, block_size), key, rounds, block_size, enciphering))
    if not enciphering:  # retrieving original extension from first block
        extension_bytes = get_block(result, 0, block_size)
        unpad(extension_bytes)
        extension = ""
        for b in extension_bytes:
            extension += chr(b)
        output_file = output_file + "." + extension
        result = result[block_size:]  # ignoring first block because it just contained the extension, not relevant info
    unpad(result)

    f = open(output_file, "w+")
    f.write(result)
    f.close()


b = 0
block_ind=17
key=[27,27,27,27,27,27,27,27,27,27,27,27,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print s_box(b,key,block_ind)

"""
bs = 32 #block size
print "plain text: ",
plain_text=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
print plain_text

print "key: ",
key=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print key

print "cipher text: ",
cipher_text = encipher_block(plain_text, key, 16, bs, True)
print cipher_text

print "deciphered: ",
deciphered = encipher_block(cipher_text, key, 16, bs, False)
print deciphered
"""