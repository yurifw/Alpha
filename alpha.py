#!/usr/bin/python
import random
import os


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


def s_box(byte):
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
    t = [None]*64
    t[0] = ((e[5] >> 2) ^ (e[5] >> 4) ^ (e[1] >> 6) ^ (e[0] >> 5) ^ (e[6] >> 7) ^ (e[3] >> 5) ^ (e[4] >> 6)) & 1
    t[1] = ((e[7] >> 2) ^ (e[4] >> 2) ^ (e[2] >> 2) ^ (e[1] >> 5) ^ (e[6] >> 1) ^ (e[5] >> 6) ^ (e[3] >> 6)) & 1
    t[2] = ((e[3] >> 1) ^ (e[2] >> 1) ^ (e[3] >> 3) ^ (e[0] >> 4) ^ (e[1] >> 2) ^ (e[7] >> 7) ^ (e[5] >> 5)) & 1
    t[3] = ((e[1] >> 4) ^ (e[0] >> 1) ^ (e[7] >> 6) ^ (e[6] >> 4) ^ (e[1] >> 2) ^ (e[4] >> 5) ^ (e[5] >> 4)) & 1
    t[4] = ((e[2] >> 3) ^ (e[5] >> 7) ^ (e[0]) ^ (e[4] >> 7) ^ (e[3] >> 7) ^ (e[1] >> 7) ^ (e[3])) & 1
    t[5] = ((e[6] >> 3) ^ (e[2]) ^ (e[4] >> 6) ^ (e[6] >> 6) ^ (e[7] >> 5) ^ (e[0]) ^ (e[3] >> 5)) & 1
    t[6] = ((e[3] >> 2) ^ (e[2] >> 2) ^ (e[5] >> 6) ^ (e[0]) ^ (e[7] >> 6) ^ (e[6] >> 4) ^ (e[4] >> 7)) & 1
    t[7] = ((e[0] >> 3) ^ (e[6] >> 2) ^ (e[3] >> 6) ^ (e[4] >> 1) ^ (e[2]) ^ (e[1] >> 1) ^ (e[0] >> 6)) & 1

    t[8] = ((e[0] >> 3) ^ (e[4] >> 3) ^ (e[0] >> 2) ^ (e[2] >> 7) ^ (e[7] >> 4) ^ (e[1] >> 5) ^ (e[2] >> 6)) & 1
    t[9] = ((e[3] >> 1) ^ (e[3] >> 5) ^ (e[0] >> 2) ^ (e[6] >> 7) ^ (e[4] >> 1) ^ (e[6] >> 6) ^ (e[1] >> 3)) & 1
    t[10] = ((e[1] >> 4) ^ (e[7] >> 4) ^ (e[1] >> 3) ^ (e[4] >> 1) ^ (e[6]) ^ (e[0] >> 6) ^ (e[2])) & 1
    t[11] = ((e[2] >> 3) ^ (e[1] >> 5) ^ (e[7] >> 4) ^ (e[0] >> 4) ^ (e[2] >> 7) ^ (e[7] >> 6) ^ (e[6] >> 4)) & 1
    t[12] = ((e[3] >> 2) ^ (e[6] >> 7) ^ (e[0] >> 7 >> 7) ^ (e[3]) ^ (e[5] >> 1) ^ (e[2] >> 1) ^ (e[7] >> 7)) & 1
    t[13] = ((e[5] >> 2) ^ (e[1] >> 1) ^ (e[3] >> 7) ^ (e[4] >> 7) ^ (e[5] >> 7) ^ (e[6] >> 1) ^ (e[2] >> 2)) & 1
    t[14] = ((e[4] >> 4) ^ (e[0] >> 6) ^ (e[1] >> 3) ^ (e[5] >> 4) ^ (e[1] >> 7) ^ (e[7] >> 4) ^ (e[5] >> 7)) & 1
    t[15] = ((e[6] >> 3) ^ (e[5] >> 1) ^ (e[4]) ^ (e[2] >> 5) ^ (e[6]) ^ (e[0] >> 1) ^ (e[1] >> 7)) & 1

    t[16] = ((e[1] >> 4) ^ (e[0]) ^ (e[4] >> 3) ^ (e[2] >> 6) ^ (e[3] >> 7) ^ (e[7] >> 5) ^ (e[6] >> 1)) & 1
    t[17] = ((e[5] >> 2) ^ (e[1]) ^ (e[0] >> 4) ^ (e[7] >> 7) ^ (e[2] >> 5) ^ (e[5] >> 1) ^ (e[0] >> 2)) & 1
    t[18] = ((e[5]) ^ (e[6]) ^ (e[5] >> 5) ^ (e[7] >> 1) ^ (e[4] >> 2) ^ (e[0] >> 2) ^ (e[6] >> 2)) & 1
    t[19] = ((e[6] >> 3) ^ (e[6] >> 5) ^ (e[0] >> 5) ^ (e[7]) ^ (e[4] >> 2) ^ (e[1] >> 2) ^ (e[5] >> 4)) & 1
    t[20] = ((e[7] >> 1) ^ (e[5]) ^ (e[1] >> 4) ^ (e[0] >> 3) ^ (e[3] >> 1) ^ (e[7] >> 2) ^ (e[6] >> 3)) & 1
    t[21] = ((e[4] >> 4) ^ (e[7] >> 7) ^ (e[2] >> 5) ^ (e[4]) ^ (e[7] >> 6) ^ (e[6] >> 2) ^ (e[3] >> 7)) & 1
    t[22] = ((e[3] >> 1) ^ (e[5] >> 3) ^ (e[2] >> 4) ^ (e[4] >> 5) ^ (e[0]) ^ (e[1] >> 7) ^ (e[7] >> 6)) & 1
    t[23] = ((e[3] >> 2) ^ (e[1] >> 1) ^ (e[6]) ^ (e[4] >> 3) ^ (e[6] >> 2) ^ (e[0] >> 1) ^ (e[1] >> 6)) & 1

    t[24] = ((e[0] >> 3) ^ (e[1]) ^ (e[2] >> 2) ^ (e[5] >> 6) ^ (e[3] >> 3) ^ (e[6] >> 5) ^ (e[5] >> 3)) & 1
    t[25] = ((e[6] >> 3) ^ (e[2] >> 1) ^ (e[3] >> 3) ^ (e[6] >> 2) ^ (e[1] >> 6) ^ (e[7] >> 4) ^ (e[3])) & 1
    t[26] = ((e[3] >> 2) ^ (e[2] >> 4) ^ (e[4] >> 2) ^ (e[7] >> 5) ^ (e[3] >> 7) ^ (e[5] >> 3) ^ (e[3] >> 6)) & 1
    t[27] = ((e[5] >> 2) ^ (e[1] >> 2) ^ (e[5] >> 3) ^ (e[4] >> 3) ^ (e[2] >> 1) ^ (e[4] >> 1) ^ (e[7] >> 3)) & 1
    t[28] = ((e[4] >> 4) ^ (e[4] >> 5) ^ (e[3]) ^ (e[0] >> 4) ^ (e[6] >> 7) ^ (e[1] >> 5) ^ (e[5] >> 1)) & 1
    t[29] = ((e[5]) ^ (e[7] >> 5) ^ (e[4]) ^ (e[1] >> 3) ^ (e[2]) ^ (e[3] >> 5) ^ (e[0] >> 1)) & 1
    t[30] = ((e[2] >> 3) ^ (e[2] >> 1) ^ (e[4] >> 2) ^ (e[1] >> 6) ^ (e[6] >> 1) ^ (e[0] >> 5) ^ (e[5] >> 3)) & 1
    t[31] = ((e[0] >> 3) ^ (e[3] >> 6) ^ (e[7] >> 5) ^ (e[4] >> 2) ^ (e[6] >> 7) ^ (e[0] >> 7) ^ (e[1] >> 2)) & 1

    t[32] = ((e[0] >> 3) ^ (e[5] >> 1) ^ (e[7] >> 7) ^ (e[3] >> 4) ^ (e[0] >> 1) ^ (e[4]) ^ (e[6] >> 4)) & 1
    t[33] = ((e[5] >> 2) ^ (e[0] >> 1) ^ (e[6]) ^ (e[2] >> 4) ^ (e[3] >> 3) ^ (e[5] >> 6) ^ (e[7])) & 1
    t[34] = ((e[5]) ^ (e[1] >> 7) ^ (e[1] >> 1) ^ (e[0] >> 4) ^ (e[7]) ^ (e[6] >> 5) ^ (e[4] >> 7)) & 1
    t[35] = ((e[5]) ^ (e[3] >> 3) ^ (e[4] >> 3) ^ (e[2] >> 2) ^ (e[1] >> 1) ^ (e[6] >> 7) ^ (e[5] >> 6)) & 1
    t[36] = ((e[4] >> 4) ^ (e[0] >> 2) ^ (e[6] >> 5) ^ (e[4] >> 1) ^ (e[1]) ^ (e[3] >> 5) ^ (e[2] >> 6)) & 1
    t[37] = ((e[3] >> 1) ^ (e[5] >> 7) ^ (e[6] >> 1) ^ (e[3] >> 4) ^ (e[5] >> 6) ^ (e[1] >> 6) ^ (e[7] >> 3)) & 1
    t[38] = ((e[7] >> 2) ^ (e[0] >> 5) ^ (e[7] >> 6) ^ (e[4] >> 5) ^ (e[0]) ^ (e[1]) ^ (e[6] >> 4)) & 1
    t[39] = ((e[3] >> 2) ^ (e[5] >> 5) ^ (e[2] >> 6) ^ (e[0] >> 4) ^ (e[7] >> 4) ^ (e[3] >> 5) ^ (e[4] >> 6)) & 1

    t[40] = ((e[0] >> 3) ^ (e[4] >> 6) ^ (e[6] >> 6) ^ (e[2] >> 7) ^ (e[7] >> 3) ^ (e[0] >> 4) ^ (e[7] >> 1)) & 1
    t[41] = ((e[4] >> 4) ^ (e[1] >> 5) ^ (e[0] >> 7) ^ (e[6] >> 4) ^ (e[3] >> 6) ^ (e[4] >> 5) ^ (e[2] >> 7)) & 1
    t[42] = ((e[2] >> 5) ^ (e[5] >> 4) ^ (e[2] >> 7) ^ (e[6] >> 5) ^ (e[2]) ^ (e[6] >> 1) ^ (e[0] >> 6)) & 1
    t[43] = ((e[6] >> 3) ^ (e[5] >> 3) ^ (e[6] >> 4) ^ (e[1] >> 3) ^ (e[5] >> 5) ^ (e[7] >> 1) ^ (e[2] >> 2)) & 1
    t[44] = ((e[3] >> 1) ^ (e[4] >> 3) ^ (e[6] >> 2) ^ (e[2] >> 7) ^ (e[7]) ^ (e[5] >> 4) ^ (e[1] >> 1)) & 1
    t[45] = ((e[5]) ^ (e[6] >> 6) ^ (e[3] >> 4) ^ (e[0] >> 7) ^ (e[4] >> 6) ^ (e[1] >> 2) ^ (e[2] >> 6)) & 1
    t[46] = ((e[7] >> 2) ^ (e[3] >> 4) ^ (e[5] >> 3) ^ (e[2]) ^ (e[4]) ^ (e[5] >> 5) ^ (e[2] >> 1)) & 1
    t[47] = ((e[2] >> 3) ^ (e[4] >> 4) ^ (e[5] >> 2) ^ (e[3] >> 2) ^ (e[2] >> 5) ^ (e[4] >> 5) ^ (e[6] >> 2)) & 1

    t[48] = ((e[4] >> 4) ^ (e[3] >> 3) ^ (e[0]) ^ (e[2]) ^ (e[6] >> 6) ^ (e[4] >> 2) ^ (e[5] >> 5)) & 1
    t[49] = ((e[5] >> 2) ^ (e[7] >> 1) ^ (e[2] >> 6) ^ (e[0] >> 2) ^ (e[6] >> 5) ^ (e[3]) ^ (e[7] >> 5)) & 1
    t[50] = ((e[7] >> 2) ^ (e[3] >> 7) ^ (e[0] >> 1) ^ (e[7] >> 4) ^ (e[1] >> 7) ^ (e[4] >> 7) ^ (e[1] >> 1)) & 1
    t[51] = ((e[1] >> 4) ^ (e[6]) ^ (e[1] >> 3) ^ (e[0] >> 5) ^ (e[5] >> 7) ^ (e[3] >> 5) ^ (e[1] >> 6)) & 1
    t[52] = ((e[2] >> 3) ^ (e[2] >> 4) ^ (e[3] >> 6) ^ (e[1]) ^ (e[0] >> 2) ^ (e[7] >> 7) ^ (e[5] >> 4)) & 1
    t[53] = ((e[5]) ^ (e[1]) ^ (e[6] >> 7) ^ (e[7] >> 3) ^ (e[0] >> 5) ^ (e[4] >> 6) ^ (e[2] >> 1)) & 1
    t[54] = ((e[3] >> 1) ^ (e[7] >> 5) ^ (e[0] >> 6) ^ (e[4] >> 6) ^ (e[2] >> 6) ^ (e[3]) ^ (e[5] >> 1)) & 1
    t[55] = ((e[2] >> 5) ^ (e[1] >> 3) ^ (e[7] >> 1) ^ (e[3] >> 4) ^ (e[4] >> 1) ^ (e[1] >> 5) ^ (e[0] >> 5)) & 1

    t[56] = ((e[6] >> 3) ^ (e[5] >> 6) ^ (e[0] >> 6) ^ (e[7] >> 6) ^ (e[3] >> 4) ^ (e[4] >> 3) ^ (e[2] >> 4)) & 1
    t[57] = ((e[1] >> 4) ^ (e[1] >> 5) ^ (e[3]) ^ (e[4] >> 7) ^ (e[5] >> 5) ^ (e[2] >> 2) ^ (e[7])) & 1
    t[58] = ((e[3] >> 2) ^ (e[7] >> 3) ^ (e[3] >> 4) ^ (e[1] >> 2) ^ (e[4] >> 5) ^ (e[6] >> 6) ^ (e[1])) & 1
    t[59] = ((e[1] >> 4) ^ (e[7] >> 7) ^ (e[0] >> 7) ^ (e[6] >> 6) ^ (e[1] >> 6) ^ (e[4]) ^ (e[2] >> 4)) & 1
    t[60] = ((e[7] >> 2) ^ (e[2] >> 4) ^ (e[6]) ^ (e[4] >> 7) ^ (e[3] >> 7) ^ (e[0] >> 7) ^ (e[7] >> 1)) & 1
    t[61] = ((e[2] >> 3) ^ (e[7] >> 3) ^ (e[0] >> 6) ^ (e[4] >> 1) ^ (e[5] >> 1) ^ (e[6] >> 5) ^ (e[7])) & 1
    t[62] = ((e[2] >> 5) ^ (e[2] >> 3) ^ (e[5] >> 7) ^ (e[3] >> 3) ^ (e[7]) ^ (e[4]) ^ (e[1] >> 7)) & 1
    t[63] = ((e[7] >> 2) ^ (e[7] >> 3) ^ (e[5] >> 7) ^ (e[2] >> 7) ^ (e[3] >> 6) ^ (e[0] >> 7) ^ (e[6] >> 1)) & 1

    s = [None]*8
    s[0] = (t[0] << 7) | (t[1] << 6) | (t[2] << 5) | (t[3] << 4) | (t[4] << 3) | (t[5] << 2) | (t[6] << 1) | (t[7])
    s[1] = (t[8] << 7) | (t[9] << 6) | (t[10] << 5) | (t[11] << 4) | (t[12] << 3) | (t[13] << 2) | (t[14] << 1) | (t[15])
    s[2] = (t[16] << 7) | (t[17] << 6) | (t[18] << 5) | (t[19] << 4) | (t[20] << 3) | (t[21] << 2) | (t[22] << 1) | (t[23])
    s[3] = (t[24] << 7) | (t[25] << 6) | (t[26] << 5) | (t[27] << 4) | (t[28] << 3) | (t[29] << 2) | (t[30] << 1) | (t[31])
    s[4] = (t[32] << 7) | (t[33] << 6) | (t[34] << 5) | (t[35] << 4) | (t[36] << 3) | (t[37] << 2) | (t[38] << 1) | (t[39])
    s[5] = (t[40] << 7) | (t[41] << 6) | (t[42] << 5) | (t[43] << 4) | (t[44] << 3) | (t[45] << 2) | (t[46] << 1) | (t[47])
    s[6] = (t[48] << 7) | (t[49] << 6) | (t[50] << 5) | (t[51] << 4) | (t[52] << 3) | (t[53] << 2) | (t[54] << 1) | (t[55])
    s[7] = (t[56] << 7) | (t[57] << 6) | (t[58] << 5) | (t[59] << 4) | (t[60] << 3) | (t[61] << 2) | (t[62] << 1) | (t[63])
    return s


def encipher_block(text, key, rounds, block_size, encipher):
    """encipher or decipher the given text (True to encipher and False to decipher), using the given key(not expanded)
    the algorithm will do nr rounds. For now, the only block_size ssupported is 16, and the rounds should also be 16
    """
    #adicionar parametro block_size e trocar as ocorrencias de 16 por este parametro e 8 por este parametro/2

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

    if enciphering:  # storing name and extension in first and second blocks
        file_name = input_file[input_file.rfind(os.sep)+1:]
        extension = file_name[file_name.find(".")+1:]
        name_only = file_name.replace("."+extension, "")

        bytes = bytearray(name_only)
        pad(bytes, block_size)

        bytes.extend(bytearray(extension))
        pad(bytes, block_size)

    bytes.extend(read_file(input_file))
    pad(bytes, block_size)

    result = bytearray()
    for i in range(len(bytes)/block_size):
        result.extend(encipher_block(get_block(bytes, i, block_size), key, rounds, block_size, enciphering))
    if not enciphering:  # retrieving original name and extension from first and second block
        output_file = output_file + os.sep

        name_bytes = get_block(result, 0, block_size)
        unpad(name_bytes)
        name = ""
        for b in name_bytes:
            name += chr(b)
        extension_bytes = get_block(result, 1, block_size)
        unpad(extension_bytes)
        extension=""
        for b in extension_bytes:
            extension += chr(b)
        output_file = output_file + name + "." + extension
        result = result[block_size*2:]
    unpad(result)

    f = open(output_file, "w+")
    f.write(result)
    f.close()


