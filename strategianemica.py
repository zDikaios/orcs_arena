import random
from abc import ABC, abstractmethod
from typing import List
from characters import personaggi

# Gestione AI nemica, con l'implementazione di nemici più complessi sarà possibile
# far utilizzare determinati attacchi speciali in determinate situazioni


class Strategia(ABC):
    @abstractmethod
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        pass


class attaccarandom(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivi = [b for b in bersaglio if b.ancoravivo()]
        return random.choice(vivi)


class conmenovita(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivi = [b for b in bersaglio if b.ancoravivo()]
        return min(vivi, key=lambda p: p.hp)


class conpiuvita(Strategia):
    def scegli_bersaglio(self, bersaglio: List[personaggi]) -> personaggi:
        vivi = [b for b in bersaglio if b.ancoravivo()]
        return max(vivi, key=lambda p: p.hp)