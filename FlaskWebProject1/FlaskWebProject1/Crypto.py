from os import urandom 
from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode

class Crypto:
    
    def __init__(self, saltSize, keySize, rounds):
        
        self.SaltSize=saltSize

        self.PBKDF2SubkeyLength=keySize

        self.PBKDF2IterCount=rounds
    
    @staticmethod
    def CreateWithRfc2898DeriveBytes():

        return Crypto(16, 32, 1000)
    
    def HashPassword(self, password):

        saltbytes=bytearray(urandom(self.SaltSize))

        res=pbkdf2_hmac('sha1', password, saltbytes, self.PBKDF2IterCount, dklen=self.PBKDF2SubkeyLength)

        keybytes=list(bytearray(res)[:self.PBKDF2SubkeyLength])

        data=[0]

        data[1:]=saltbytes

        data[17:]=keybytes

        return b64encode(bytearray(data))
    
    
    def VerifyHashedPassword(self, hashedPassword, password):

        if hashedPassword is None:
            return False
        if password is None:
            raise AssertionError("password")

        bytesArray=list(bytearray(b64decode(hashedPassword)))

        if len(bytesArray) != 49 or bytesArray[0] != 0:
            return False

        saltbytes=bytearray(bytesArray[1:1+self.SaltSize:1])

        keybytes=bytearray(bytesArray[17:17+self.PBKDF2SubkeyLength:1])

        res=pbkdf2_hmac('sha1', password, saltbytes, self.PBKDF2IterCount, dklen=self.PBKDF2SubkeyLength)

        bytes=bytearray(res)[:self.PBKDF2SubkeyLength]

        return keybytes==bytes


