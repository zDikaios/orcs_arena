from characters import personaggi
from nemici import Enemy

# Le pozioni inseriscono buff o debuff temporanei al giocatore

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


class Furia(personaggi):
    # raddoppia i danni inflitti per un tot di turni
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

    def attack(self, enemy: Enemy) -> str:
        # calcola gli hp del nemico prima dell'attacco
        hp_prima = enemy.hp
        # esegue l'attacco normale
        messaggio = self.target.attack(enemy)
        # se il nemico ha subito danni significa che l'attacco e andato a segno
        # (rispettando una possibile futura implementazione di "attacco fallito")
        danno_base = hp_prima - enemy.hp
        if danno_base > 0:
            # infligge di nuovo lo stesso danno raddoppiando l'effetto
            enemy.take_damage(danno_base)
            totale = danno_base * 2
            return f"{messaggio}\n[furia] il colpo e potenziato danno raddoppiato a {totale}"
        return messaggio

    def curarsi(self) -> str:
        return self.target.curarsi()

    def usaoggetto(self, item: str, enemy: Enemy) -> str:
        return self.target.usaoggetto(item, enemy)

    def scala_turno(self) -> bool:
        self.turni -= 1
        return self.turni > 0