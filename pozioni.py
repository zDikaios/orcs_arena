from characters import personaggi
from nemici import Enemy

class ScudoMagico(personaggi):
    # decoratore strutturale che prende un personaggio base
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
        # dimezza il danno prima di passarlo al personaggio
        danno_ridotto = dmg // 2
        print(f"lo scudo magico assorbe il colpo danno ridotto a {danno_ridotto}")
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

    def attack(self, enemy: Enemy) -> str:
        return self.target.attack(enemy)

    def curarsi(self) -> str:
        return self.target.curarsi()

    def usaoggetto(self, item: str, enemy: Enemy) -> str:
        return self.target.usaoggetto(item, enemy)

    def scala_turno(self) -> bool:
        # scala un turno e dice se il buff e ancora attivo
        self.turni -= 1
        return self.turni > 0