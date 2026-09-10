from typing import List
import random
from strategianemica import conpiuvita, conmenovita, attaccarandom
from utilities import intervallonumerico, show_bar
from characters import personaggi


class Enemy:
    def __init__(self, name: str, level: int, max_hp: int, hp: int, base_damage: int, strategia):
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.hp = hp
        self.base_damage = base_damage
        self.strategia = strategia

    def ancoravivo(self) -> bool:
        return self.hp > 0

    def take_damage(self, dmg: int) -> None:
        self.hp = intervallonumerico(self.hp - max(0, dmg), 0, self.max_hp)

    def attack(self, targets: List[personaggi]) -> str:
        alive = [t for t in targets if t.ancoravivo()]
        if not alive:
            return f"{self.name} non ha bersagli."

        target = self.strategia.scegli_bersaglio(targets)  # oppure alive

        dmg = self.base_damage + random.randint(0, 2)
        target.take_damage(dmg)
        return f"{self.name} attacca {target.name} e infligge {dmg} danni."

    def barre_di_stato(self):
        print(f"\n{self.name} (Lv {self.level})")
        show_bar("Salute ", self.hp, self.max_hp)


def summona_nemico(stage: int) -> Enemy:
    lvl = stage
    nomi_nemici = ["Grak", "Mug", "Zog", "Thrum", "Karg", "Gianluca", "Blud", "Gnash", "Urk", "Drog", "Skab", "Pugg", "Gruk", "Lok", "Brak"]
    max_hp = 30 + stage * 8
    base_damage = 4 + stage
    if stage <= 3:
        strat = attaccarandom()         #sotto lo stage 3 attacca a caso
    elif stage <= 7:
        strat = conpiuvita()            #tra lo stage 3 e 7 attacca chi ha più vita
    else:
        strat = conmenovita()           #sopra al 7imo stage attacca chi ha meno vita

    return Enemy(
        name=random.choice(nomi_nemici),  #così facendo però ogni volta che si carica un salvataggio il nemico cambia nome ***FIXARE
        level=lvl,
        max_hp=max_hp,
        hp=max_hp,
        base_damage=base_damage,
        strategia=strat
        )

