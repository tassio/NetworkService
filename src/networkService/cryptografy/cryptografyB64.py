'''
Created on 19/06/2011

@author: Tassio
'''
import base64
from networkService.cryptografy.cryptografy import Cryptografy
    
    
class CriptografyB64(Cryptografy):
    def encrypt(self, data):
        return base64.b64encode(data)
    def decrypt(self, data):
        return base64.b64decode(data)