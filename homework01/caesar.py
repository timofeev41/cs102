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
            (ord(letter) < ord("A"))
            or (ord("Z") < ord(letter) < ord("a"))
            or (ord(letter) > ord("z"))
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
            (ord(letter) < ord("A"))
            or (ord("Z") < ord(letter) < ord("a"))
            or (ord(letter) > ord("z"))
        ):
            plaintext += letter
        else:
            plaintext += chr(ord(letter) + (26 - shift))
    return plaintext


def caesar_breaker(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    for word in dictionary:
        if ciphertext == word:
            return 0
        if len(ciphertext) not in [len(_) for _ in dictionary]:
            raise ValueError("Can't find anything to compare (Different word lengths)")
        new_word = ""
        if ciphertext == word:
            return 0
        for shift in range(1, 26):
            for letter in word:
                if (ord("A") <= ord(letter) + shift <= ord("Z")) or (
                    ord("a") <= ord(letter) + shift <= ord("z")
                ):
                    new_word += chr(ord(letter) + shift)
                elif (
                    (ord(letter) < ord("A"))
                    or (ord("Z") < ord(letter) < ord("a"))
                    or (ord(letter) > ord("z"))
                ):
                    new_word += letter
                else:

                    new_word += chr(ord(letter) - (26 + shift))
                if len(new_word) == len(word):
                    if new_word == ciphertext:
                        return shift
                    new_word = ""

    return shift
