import sys


def reverse_hash(string):
    string = string.rstrip()
    decrypted_str = ''.join([chr(character-offset) for offset, character in enumerate(string)])
    return decrypted_str


if __name__ == '__main__':
    with open(sys.argv[-1], 'rb') as token_file:
        print(reverse_hash(token_file.read()))
