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
    ciphertext = ""

    for letter in plaintext:
        if (ord("A") <= ord(letter) + shift <= ord("Z")) or (
            ord("a") <= ord(letter) + shift <= ord("z")
        ):
            ciphertext += chr(ord(letter) + shift)
        elif (
            (ord(letter) < ord("A")) or ("Z" < ord(letter) < "a") or (ord(letter) > "z")
        ):
            ciphertext += letter
        else:
            ciphertext += chr(ord(letter) - (26 - shift))

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
        if (ord("A") <= ord(letter) - shift <= ord("Z")) or (
            ord("a") <= ord(letter) - shift <= ord("z")
        ):
            plaintext += chr(ord(letter) - shift)
        elif (
            (ord(letter) < ord("A")) or ("Z" < ord(letter) < "a") or (ord(letter) > "z")
        ):
            plaintext += letter
        else:
            plaintext += chr(ord(letter) + (26 - shift))
    return plaintext


# def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
#     """
#     Brute force breaking a Caesar cipher.
#     """
#     best_shift = 0
#     # PUT YOUR CODE HERE
#     ##for letter in ciphertext:
#     ##
#     return best_shift
