Part 1
----------

Since the password was found mainly using online tools for frequency analysis and by hand, the only thing that the code was used for was for decryption. 
To print the decrypted file using the python program, in the programs directory type either (using python2):

python assignment1.py --file=cipertext1 --key-num=1

or

cat ciphertext1 | python assignment1.py --key-num=1


Part 2
----------

We quickly realized that the key to solving this part of the assignment was to take the given file signatures (or Known-Plaintext) and attempt to find a valid key that would allow those headers. 
This was done by formatting a list of file formats and iterating over them attempting to find a possible match (given possible key characters). 
This led to 4 possible matches, and knowing that the key length was longer than Part 1, indicated that the longest possible match would be our best bet, which was a key that produced a plaintext Exif header.
The format of the resulting key led to the realization that the key was actually a pair of coordinates, which helped narrow the search of possible keys to key characters that would follow the format of geographic data
From there, the strategy was to iterate over possible keys conforming to those rules that would produce a valid JPEG file containing Exif data. 
Comparing the file to a non-encrypted file with Exif data gave insight as to the format and metadata contained within, specifically date-time signature, which was used to verify the key without fully decrypting the file each time.

To print the decrypted file text to stdout and open a window with the decrypted image type using (using python2):

python assignment1.py --file=ciphertext2 --key-num=2