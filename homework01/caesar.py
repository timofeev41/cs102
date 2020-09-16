import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for letter in plaintext:
        if (65 <= ord(letter) + 3 <= 90) or (97 <= ord(letter) + 3 <= 122):
            ciphertext += chr(ord(letter) + 3)
        elif (ord(letter) < 65) or (90 < ord(letter) < 97) or (ord(letter) > 122):
            ciphertext += letter
        else:
            ciphertext += chr(ord(letter) - 23)
            
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for letter in ciphertext:
        if (65 <= ord(letter) - 3 <= 90) or (97 <= ord(letter) - 3 <= 122):
            plaintext += chr(ord(letter) - 3)
        elif (ord(letter) < 65) or (90 < ord(letter) < 97) or (ord(letter) > 122):
            plaintext += letter
        else:
            plaintext += chr(ord(letter) + 23) ##- 26 + 3
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift