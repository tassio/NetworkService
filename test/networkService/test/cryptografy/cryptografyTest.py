'''
Created on 12/06/2011

@author: Tassio
'''
import unittest
from networkService.cryptografy.cryptografyB64 import CriptografyB64

class CryptografyTest(unittest.TestCase):
    def test_cryptografyB64(self):
        cryptografy = CriptografyB64()
        
        data = b"Testando criptografia"
        crypt = cryptografy.encrypt(data)
        
        self.assertEqual(data, cryptografy.decrypt(crypt))
        
if __name__ == "__main__":
    unittest.main()