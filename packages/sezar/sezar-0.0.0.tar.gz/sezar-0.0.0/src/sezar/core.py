alphabet = {
    'a': 'A', 'b': 'B', 'd': 'D',
    'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
    'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L',
    'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P',
    'q': 'Q', 'r': 'R', 's': 'S', 't': 'T',
    'u': 'U', 'v': 'V', 'x': 'X', 'y': 'Y',
    'z': 'Z', "o'": "O'", "g'": "G'", 'sh': 'SH',
    'ch': 'CH', 'ng': 'NG',
}

reverse_alphabet = {v: k for k, v in alphabet.items()}

letters = [
    'A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'X', 'Y', 'Z', "O'", "G'", 'SH', 'CH', 'NG'
]

lettersCount = len(letters)

def cipher(plaintext: str, key: int = 0) -> str:
    ciphertext = ""
    i = 0
    while i < len(plaintext):
        if i + 1 < len(plaintext):
            two_chars = plaintext[i:i+2].lower()
            if two_chars in alphabet:
                mapped = alphabet[two_chars]
                index = letters.index(mapped)
                ciphertext += letters[(index + key) % lettersCount]
                i += 2
                continue
        char = plaintext[i].lower()
        if char in alphabet:
            mapped = alphabet[char]
            index = letters.index(mapped)
            ciphertext += letters[(index + key) % lettersCount]
        else:
            ciphertext += plaintext[i]
        i += 1
    return ciphertext

def decipher(ciphertext: str, key: int = 0) -> str:
    plaintext = ""
    i = 0
    while i < len(ciphertext):
        found = False
        for l in sorted(letters, key=lambda x: -len(x)):
            if ciphertext[i:i+len(l)].upper() == l:
                index = letters.index(l)
                shifted = letters[(index - key) % lettersCount]
                plaintext += reverse_alphabet[shifted]
                i += len(l)
                found = True
                break
        if not found:
            plaintext += ciphertext[i]
            i += 1
    return plaintext