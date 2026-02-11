import random
from abc import ABC, abstractmethod
from typing import List
from characters import personaggi


def prendi_hp(personaggi):
    return personaggi.hp

class Strategia(ABC):
    @abstractmethod
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        raise NotImplementedError

class attaccarandom(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivo = [b for b in bersaglio if b.ancoravivo()]
        return random.choice(vivo)

class conmenovita(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivo = [b for b in bersaglio if b.ancoravivo()]
        return min(vivo, key=prendi_hp)

class conpiuvita(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivo = [b for b in bersaglio if b.ancoravivo()]
        return max(vivo, key=prendi_hp)