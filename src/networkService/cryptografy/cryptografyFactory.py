'''
Created on 12/06/2011

@author: Tassio
'''
from networkService.cryptografy.cryptografyB64 import CriptografyB64


class CryptografyFactory(object):
    @staticmethod
    def getDefaultInstance():
        return CriptografyB64()
