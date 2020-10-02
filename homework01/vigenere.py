def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    for number, letter in enumerate(plaintext):
        if ord("A") <= ord(keyword[number % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[number % len(keyword)]) - 65
        else:
            shift = ord(keyword[number % len(keyword)]) - 97

        if ord("A") <= ord(letter) <= ord("Z"):
            ciphertext += str(chr(ord("A") + ((ord(letter) - 65 + shift) % 26)))
        elif ord("a") <= ord(letter) <= ord("z"):
            ciphertext += str(chr(ord("a") + ((ord(letter) - 97 + shift) % 26)))
        else:
            ciphertext += str(letter)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    for number, letter in enumerate(ciphertext):
        if ord("A") <= ord(keyword[number % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[number % len(keyword)]) - 65
        else:
            shift = ord(keyword[number % len(keyword)]) - 97

        if ord("A") <= ord(letter) <= ord("Z"):
            plaintext += str(chr(ord("A") + ((ord(letter) - (65 - 26) - shift) % 26)))
        elif ord("a") <= ord(letter) <= ord("z"):
            plaintext += str(chr(ord("a") + ((ord(letter) - (97 - 26) - shift) % 26)))
        else:
            plaintext += str(letter)

    return plaintext
