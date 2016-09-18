import sys

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

# For a given vector of indices of appearence for a letter in the ciphertext,
# this should return possible repetition distances

intervals = {}

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

        if not fail:
            if test_distance in intervals:
                intervals[test_distance] += 1
            else:
                intervals[test_distance] = 1
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
    invalid_indexes = []
    valid_indexes = []
    while len(repeated_key) < len(text):
        repeated_key += key

    slicedKey = repeated_key[0 : len(text)]
    decryption = ""
    for i in range(len(text)):
        decrypted_char = decrypt(text[i], slicedKey[i])
        if not isPrintableAscii(decrypted_char):
            invalid_indexes.append(i)
        else:
            valid_indexes.append(i)
        decryption += decrypt(text[i], slicedKey[i])
    return decryption, valid_indexes, invalid_indexes

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

def main():
    text = ""
    possibleKeyMatrix = []
    possiblePlaintextMatrix = []
    for line in sys.stdin:
        text += line
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
                    if isPrintableAscii(plain_char) and isValidAscii(key_char):
                        possiblePlaintextVector.append(plain_char)
                        possibleKeyCharacterVector.append(key_char)
            possibleKeyMatrix.append(possibleKeyCharacterVector)
            possiblePlaintextMatrix.append(possiblePlaintextVector)

main()
