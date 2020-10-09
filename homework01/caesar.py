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
        if not letter.isalpha():
            ciphertext += str(letter)
            continue
        if letter.isupper():
            ciphertext += str(chr((ord(letter) + shift - ord("A")) % 26 + ord("A")))
        else:
            ciphertext += str(chr((ord(letter) + shift - ord("a")) % 26 + ord("a")))
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
        if not letter.isalpha():
            plaintext += str(letter)
            continue
        if letter.isupper():
            plaintext += str(chr((ord(letter) - shift - ord("A")) % 26 + ord("A")))
        else:
            plaintext += str(chr((ord(letter) - shift - ord("a")) % 26 + ord("a")))
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
            raise Exception("Can't find anything to compare (Different word lengths)")
        if ciphertext == word:
            return 0
        for shift in range(1, 26):
            new_word = decrypt_caesar(word, shift)
            if new_word == ciphertext:
                return shift
    return shift
