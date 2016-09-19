To run the code on a given machine, using python2, pass the ciphertext into stdin to the program, or specify a file to be opened using -f.

Example:

cat ciphertext1 | python assignment1.py

or

python assignment1.py -f=ciphertext1

The keys are hardcoded into the program, to use a ciphertexts corresponding key, use the -knum or --key-number command line argument. The first key will be used by default.

Example:

cat ciphertext2 | python assignment1.py -knum=2

or python assignment1.py --file=ciphertext3 --key-number=3

etc.

To use a key that is not hardcoded into the program, pass the desired key (as a string) to the -k or --key command line argument.

Example:

cat ciphertext1 | python assignment1.py -k=test123
