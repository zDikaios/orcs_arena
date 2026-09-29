from typing import TYPE_CHECKING
from characters import personaggi

if TYPE_CHECKING:
    from nemici import Enemy


class ScudoMagico(personaggi):
    def __init__(self, target: personaggi, turni: int = 2):
        self.target = target
        self.turni = turni

    @property
    def name(self) -> str:
        return self.target.name

    @property
    def level(self) -> int:
        return self.target.level

    @property
    def hp(self) -> int:
        return self.target.hp

    @property
    def max_hp(self) -> int:
        return self.target.max_hp

    def ancoravivo(self) -> bool:
        return self.target.ancoravivo()

    def take_damage(self, dmg: int) -> None:
        danno_ridotto = dmg // 2
        print(f"[BUFF] Lo scudo magico assorbe il colpo: danno ridotto a {danno_ridotto}")
        self.target.take_damage(danno_ridotto)

    def heal(self, amount: int) -> None:
        self.target.heal(amount)

    def full_vita(self) -> None:
        self.target.full_vita()

    def levelup(self) -> None:
        self.target.levelup()

    def nome_risorsa(self) -> str:
        return self.target.nome_risorsa()

    def valore_risorsa(self) -> int:
        return self.target.valore_risorsa()

    def max_risorsa(self) -> int:
        return self.target.max_risorsa()

    def refilla_risorsa(self) -> None:
        self.target.refilla_risorsa()

    def attack(self, enemy: "Enemy", *args, **kwargs) -> str:
        return self.target.attack(enemy, *args, **kwargs)

    def seconda_azione(self) -> str:
        return self.target.seconda_azione()

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        return self.target.usaoggetto(item, enemy)

    def scala_turno(self) -> bool:
        self.turni -= 1
        return self.turni > 0


class Furia(personaggi):
    def __init__(self, target: personaggi, turni: int = 2):
        self.target = target
        self.turni = turni

    @property
    def name(self) -> str:
        return self.target.name

    @property
    def level(self) -> int:
        return self.target.level

    @property
    def hp(self) -> int:
        return self.target.hp

    @property
    def max_hp(self) -> int:
        return self.target.max_hp

    def ancoravivo(self) -> bool:
        return self.target.ancoravivo()

    def take_damage(self, dmg: int) -> None:
        self.target.take_damage(dmg)

    def heal(self, amount: int) -> None:
        self.target.heal(amount)

    def full_vita(self) -> None:
        self.target.full_vita()

    def levelup(self) -> None:
        self.target.levelup()

    def nome_risorsa(self) -> str:
        return self.target.nome_risorsa()

    def valore_risorsa(self) -> int:
        return self.target.valore_risorsa()

    def max_risorsa(self) -> int:
        return self.target.max_risorsa()

    def refilla_risorsa(self) -> None:
        self.target.refilla_risorsa()

    def attack(self, enemy: "Enemy", *args, **kwargs) -> str:
        hp_prima = enemy.hp
        messaggio = self.target.attack(enemy, *args, **kwargs)
        danno_base = hp_prima - enemy.hp
        if danno_base > 0:
            enemy.take_damage(danno_base)
            totale = danno_base * 2
            return f"{messaggio}\n[FURIA] Danno raddoppiato a {totale}!"
        return messaggio

    def seconda_azione(self) -> str:
        return self.target.seconda_azione()

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        return self.target.usaoggetto(item, enemy)

    def scala_turno(self) -> bool:
        self.turni -= 1
        return self.turni > 0