import sys
import argparse

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

keys = [chr(0x50) + chr(0x2f) + chr(0x08) + chr(0x7c) + chr(0x5f) + chr(0x30) + chr(0x00)]

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
    possibleKeyMatrix = []
    possiblePlaintextMatrix = []
    for line in text:
        for byte in line:
            ch, cl = splitByte(byte)
            ch_indices = findIndices2dArray(hashMap, ch)
            cl_indices = findIndices2dArray(hashMap, cl)
            possibleKeyCharacterVector = []
            possiblePlaintextVector = []
            for pl, kh in cl_indices:
                for ph, kl in ch_indices:
                    plain_char = chr(ph << 4 | pl)
                    key_char = chr(kh << 4 | kl)
                    if isPrintableAscii(key_char):
                        possiblePlaintextVector.append(plain_char)
                        possibleKeyCharacterVector.append(key_char)
            possibleKeyMatrix.append(possibleKeyCharacterVector)
            possiblePlaintextMatrix.append(possiblePlaintextVector)
    return possiblePlaintextMatrix, possibleKeyMatrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt ciphertext given from stdin/file using a specified key, following the encryption scheme specified in CMPUT 333 Assigment 1")
    parser.add_argument('-k', '--key', help='Specify a key to use to decrypt the ciphertext passed from stdin.')
    parser.add_argument('-knum', '--key-number', help='Use an already found key [1, 2, 3] corresponding to the keys for Ciphertext1, Ciphertext2, and Ciphertext3 respectively.')
    parser.add_argument('-f', '--file', help='A file name to be used as input instead of stdin.')
    parser.add_argument('-a', '--analyze', action='store_true', help='Run on file input in analysis mode (for part 2).')
    args = parser.parse_args()

    if args.file:
        f = open(args.file, 'r+')
    else:
        f = sys.stdin

    text = ""
    for line in f:
        text += line

    if args.analyze:
        possiblePlaintextMatrix, possibleKeyMatrix = createPossiblePlaintextAndKeyMatrices(text)

    else:

        if args.key:
            print decryptTextUsingKey(text, args.key)
        elif args.key_number:
            print decryptTextUsingKey(text, keys[int(args.key_number) - 1])
        else:
            print decryptTextUsingKey(text, keys[0])
