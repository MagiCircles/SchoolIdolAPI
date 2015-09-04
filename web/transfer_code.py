from django.conf import settings
import base64
import md5
import itertools

def stringxor(message, key):
    """Symmetric xor-based cipher."""
    return [chr(ord(x) ^ ord(y)) for (x, y)
            in zip(message, itertools.cycle(key))]

def makekey(password):
    secret = settings.TRANSFER_CODE_SECRET_KEY
    assert(len(secret) == 16)
    m = md5.new()
    m.update(password)
    key = '%16s' % m.digest()
    key = stringxor(key, '%16s' % (secret[:16]))
    return key

def is_encrypted(text):
    return text.startswith('encrypted/')

def encrypt(cleartext, password):
    key = makekey(password)
    ciphertext = stringxor(cleartext, key)
    return 'encrypted/%s' % base64.b64encode(''.join(ciphertext))

def decrypt(ciphertext, password):
    assert is_encrypted(ciphertext)
    ciphertext = base64.b64decode('/'.join(ciphertext.split('/')[1:]))
    key = makekey(password)
    array = stringxor(ciphertext, key)
    return ' '.join(''.join(array[i:i+2]) for i in range(0, len(array), 2))
