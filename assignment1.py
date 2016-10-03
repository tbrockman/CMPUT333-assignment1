import sys
import argparse
import itertools
import os
import math
from cStringIO import StringIO
from PIL import Image

hashMap = [
   [0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe],
   [0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0],
   [0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7],
   [0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa],
   [0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4],
   [0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3],
   [0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1],
   [0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf],
   [0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2],
   [0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5],
   [0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb],
   [0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6],
   [0x9, 0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8],
   [0xd, 0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9],
   [0xc, 0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd],
   [0xe, 0xf, 0x7, 0x6, 0x4, 0x5, 0x1, 0x0, 0x2, 0x3, 0xb, 0xa, 0x8, 0x9, 0xd, 0xc]
];

keys = [chr(0x50) + chr(0x2f) + chr(0x08) + chr(0x7c) + chr(0x5f) + chr(0x30) + chr(0x00), "53.503563N,-113.528894W"]

def findRepititionIntervalsForLetter(text, letter_vector):
    distances = []
    first = letter_vector[0]
    for i in range(1, len(letter_vector) - 1):
        compare1 = letter_vector[i]
        test_distance = compare1 - first
        fail = False
        if test_distance > len(text) / 3:
            break

        for j in range(i+1, len(letter_vector)):
            compare2 = letter_vector[j]
            if compare2 - compare1 > test_distance:
                fail = True
                break

            elif compare2 - compare1 == test_distance:
                compare1 = compare2

            distances.append(test_distance)

    return distances


def findPossiblePositionsForCharacter(matrix, character):
    char_positions = []
    for i in range(len(matrix)):
        if character in matrix[i]:
            char_positions.append(i)
    return char_positions

def splitByte(byte):
    upperMask = 0xF0
    lowerMask = 0x0F
    ch = (ord(byte) & upperMask) >> 4
    cl = ord(byte) & lowerMask
    return ch, cl

def encrypt(character, key_character):
    ph, pl = splitByte(character)
    kh, kl = splitByte(key_character)
    mapped = hashMap[ph][kl] << 4 | hashMap[pl][kh]
    return mapped

def decryptTextAtIndicesUsingCharacter(text, key_character, indices):
    decryptedText = []
    for index in indices:
        decrypted = decrypt(text[index], key_character)
        if isPrintableAscii(decrypted):
            decryptedText.append((index, decrypted))
    return decryptedText

def decryptTextUsingKey(text, key):
    repeated_key = ""
    while len(repeated_key) < len(text):
        repeated_key += key

    slicedKey = repeated_key[0 : len(text)]
    decryption = ""
    for i in range(len(text)):
        decryption += decrypt(text[i], slicedKey[i])
    return decryption

def decrypt(ciphertext_char, key_char):
    ch, cl = splitByte(ciphertext_char)
    kh, kl = splitByte(key_char)
    ph = findIndiceKnowingColumn(hashMap, kl, ch)
    pl = findIndiceKnowingColumn(hashMap, kh, cl)
    return chr(ph << 4 | pl)

def findKeyCharKnowingPlaintext(plaintext_char, ciphertext_char):
    ch, cl = splitByte(ciphertext_char)
    ph, pl = splitByte(plaintext_char)
    kh = findIndiceKnowingRow(hashMap, pl, cl)
    kl = findIndiceKnowingRow(hashMap, ph, ch)
    return chr(kh << 4 | kl)

def check_image_valid(image, index):
    try:
        test = Image.open(image)
        test.save('decrypted_' + str(index) + '.jpeg')

    except IOError:
        return False
    return True

def tryToMatchFileFormats(text, file_formats, possible_key_matrix):
    key_format_tuples = []
    for i in range(len(file_formats)):
        key = matchFileFormatToCiphertext(file_formats[i], text, possible_key_matrix)
        if (key):
            key_format_tuples.append((key, file_formats[i]))
    return key_format_tuples

def matchFileFormatToCiphertext(file_format, text, possible_key_matrix):
    key = ""
    for i in range(len(file_format)):
        if (file_format[i] == 'n'):
            key += 'n'
        else:
            key_character_vector = possible_key_matrix[i]
            key_char = findKeyCharKnowingPlaintext(file_format[i], text[i])
            if isPrintableAscii(key_char): #and key_char in key_character_vector:
                key += key_char
            else:
                return None
    return key

def filterToGeographicCoordinate(index, possible_key_vector, key):
    return filter(lambda x: x.isdigit(), possible_key_vector)

def generateCombinationsOfLists(list1, list2):
    combinations = []
    for word in list1:
        for letter in list2:
            combinations.append(word + letter)
    return combinations

def testAndGenerateKeyCombinations(key, possible_key_matrix):
    list_key = list(key)
    for i in range(len(key)):
        if (key[i] == 'n'):
            list_key[i] = filterToGeographicCoordinate(i, possible_key_matrix[i], key)

    current_combinations = list_key[0]
    for j in range(1, len(list_key)):
        current_combinations = generateCombinationsOfLists(current_combinations, list_key[j])

    return current_combinations

def findIndiceKnowingRow(arr, row, item):
    for k in range(len(arr[0])):
        if arr[row][k] == item:
            return k

def findIndiceKnowingColumn(arr, col, item):
    for p in range(len(arr)):
        if arr[p][col] == item:
            return p

def findIndices2dArray(arr, item):
    matching = []
    for p in range(len(arr)):
        for k in range(len(arr[0])):
            if (arr[p][k] == item):
                matching.append((p, k))
    return matching

def isPrintableAscii(char):
    return ord(char) >= 32 and ord(char) < 127

def isValidAscii(char):
    return ord(char) >= 0 and ord(char) <= 127

def createPossiblePlaintextAndKeyMatrices(text):
    possible_key_matrix = []
    possible_plaintext_matrix = []
    for line in text:
        for byte in line:
            ch, cl = splitByte(byte)
            ch_indices = findIndices2dArray(hashMap, ch)
            cl_indices = findIndices2dArray(hashMap, cl)
            possible_key_vector = []
            possible_plaintext_vector = []
            for pl, kh in cl_indices:
                for ph, kl in ch_indices:
                    plain_char = chr(ph << 4 | pl)
                    key_char = chr(kh << 4 | kl)
                    if isPrintableAscii(key_char):
                        possible_plaintext_vector.append(plain_char)
                        possible_key_vector.append(key_char)
            possible_key_matrix.append(possible_key_vector)
            possible_plaintext_matrix.append(possible_plaintext_vector)
    return possible_plaintext_matrix, possible_key_matrix

def convertFormatsToChars(formats):
    formatted = []
    for format in formats:
        string = ''
        for j in xrange(0,len(format)-1, 2):
            if (format[j] != 'n'):
                str_byte = '0x' + format[j] + format[j+1]
                char = chr(int(str_byte, 16))
                string += char
            else:
                string += 'n'
        formatted.append(string)
    return formatted

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt ciphertext given from stdin/file using a specified key, following the encryption scheme specified in CMPUT 333 Assigment 1")
    parser.add_argument('-k', '--key', help='Specify a key to use to decrypt the ciphertext passed from stdin.')
    parser.add_argument('-knum', '--key-number', help='Use an already found key [1, 2, 3] corresponding to the keys for Ciphertext1, Ciphertext2, and Ciphertext3 respectively.')
    parser.add_argument('-f', '--file', help='A file name to be used as input instead of stdin.')
    parser.add_argument('-a', '--analyze', action='store_true', help='Run on file input in analysis mode (for part 2).')
    args = parser.parse_args()

    if args.file:
        f = open(args.file, 'rb')
    else:
        f = sys.stdin

    text = ""
    for line in f:
        text += line

    if args.analyze:
        # Only need to parse amount of text equal to the length of the longest key#
        #test_formats = ['00', 'nnnnnnnnnnn000000000000000000000000000000000000000000000000', 'BEBAFECA', '00014244', '00014454', '00010000', '00000100', 'nnnn667479703367', '1F9D', '1FA0', '4241434B4D494B454449534B', '425A68', '474946383761', '474946383961', '49492A00', '4D4D002A', '49492A00100000004352', '802A5FD7', '524E4301', '524E4302', '53445058', '58504453', '762F3101', '425047FB', 'FFD8FFDB', 'FFD8FFE0nnnn4A4649460001', 'FFD8FFE1nnnn457869660000', '464F524Dnnnnnnnn494C424D', '464F524Dnnnnnnnn38535658', '464F524Dnnnnnnnn4143424D', '464F524Dnnnnnnnn414E424D', '464F524Dnnnnnnnn414E494D', '464F524Dnnnnnnnn46415858', '464F524Dnnnnnnnn46545854', '464F524Dnnnnnnnn534D5553', '464F524Dnnnnnnnn434D5553', '464F524Dnnnnnnnn5955564E', '464F524Dnnnnnnnn46414E54', '464F524Dnnnnnnnn41494646', '494E4458', '4C5A4950', '4D5A', '504B0304', '504B0506', '504B0708', '526172211A0700', '526172211A070100', '7F454C46', '89504E470D0A1A0A', 'CAFEBABE', 'EFBBBF', 'FEEDFACE', 'FEEDFACF', 'CEFAEDFE', 'CFFAEDFE', 'FFFE', 'FFFE0000', '25215053', '25504446', '3026B2758E66CF11A6D900AA0062CE6C', '2453444930303031', '4F676753', '38425053', '52494646nnnnnnnn57415645', '52494646nnnnnnnn41564920', 'FFFB', '494433', '424D', '53494D504C452020', '3D202020202020202020202020202020202020202054', '664C6143', '4D546864', 'D0CF11E0A1B11AE1', '6465780A30333500', '4B444D', '43723234', '41474433', '05070000424F424F0507000000000000000000000001', '0607E100424F424F0607E10000000000000000000001', '455202000000', '8B455202000000', '7801730D626260', '78617221', '504D4F43434D4F43', '4E45531A', '7573746172003030', '7573746172202000', '746F7833', '4D4C5649', '44434D0150413330', '377ABCAF271C', '1F8B', '04224D18', '4D534346', '464C4946', '1A45DFA3', '4D494C20', '41542654464F524Dnnnnnnnn444A56', '3082', '774F4646', '774F4632', '3c3f786d6c20']
        #file_formats = convertFormatsToChars(test_formats)
        file_formats = ['53.503563N,-113.528894W']
        max_necessary_slice = max(file_formats, key=len)
        sliced_text = text[0:len(max_necessary_slice)]
        poss_plaintxt_matrix, poss_key_matrix = createPossiblePlaintextAndKeyMatrices(sliced_text)
        #valid_formats = tryToMatchFileFormats(sliced_text, file_formats, poss_key_matrix)
        keys = testAndGenerateKeyCombinations('53.503563N,-113.528894W', poss_key_matrix)

        for i in range(len(keys)):
            file_like_stream = StringIO(buff)

            if check_image_valid(file_like_stream, i):
                print 'Success!!!!!'
                print keys[i]

        #print valid_formats

    else:

        if args.key:
            print decryptTextUsingKey(text, args.key)
        elif args.key_number:
            if (int(args.key_number) == 2):
                decrypted = decryptTextUsingKey(text, keys[1])
                file_like_stream = StringIO(decrypted)
                img = Image.open(file_like_stream)
                img.show()

            print decryptTextUsingKey(text, keys[int(args.key_number) - 1])
        else:
            print decryptTextUsingKey(text, keys[0])
