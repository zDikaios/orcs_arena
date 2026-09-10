import random
from abc import ABC
from utilities import intervallonumerico, show_bar, richiestanumeroscelta

class personaggi(ABC):
    def __init__(self, name: str, level: int = 1):
        self._name = name
        self._level = level
        self._max_hp = 50
        self._hp = self._max_hp

    @property
    def name(self) -> str:
        return self._name

    @property
    def level(self) -> int:
        return self._level

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._max_hp

    def ancoravivo(self) -> bool:
        return self._hp > 0

    def take_damage(self, dmg: int) -> None:
        self._hp = intervallonumerico(self._hp - max(0, dmg), 0, self._max_hp)

    def heal(self, amount: int) -> None:
        self._hp = intervallonumerico(self._hp + max(0, amount), 0, self._max_hp)

    def full_vita(self) -> None:
        self._hp = self._max_hp
        self.refilla_risorsa()

    def levelup(self) -> None:
        self._level += 1
        self._max_hp += 5
        self._hp = self._max_hp
        self.refilla_risorsa()

    # Metodi astratti

    def nome_risorsa(self) -> str:
        raise NotImplementedError


    def valore_risorsa(self) -> int:
        raise NotImplementedError


    def max_risorsa(self) -> int:
        raise NotImplementedError


    def refilla_risorsa(self) -> None:
        raise NotImplementedError


    def attack(self, enemy: "Enemy") -> str:
        raise NotImplementedError


    def curarsi(self) -> str:
        raise NotImplementedError

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        raise NotImplementedError

    def status(self):
        print(f"\n{self.name} (Lv {self.level})")
        show_bar("Salute ", self.hp, self.max_hp)
        show_bar(self.nome_risorsa(), self.valore_risorsa(), self.max_risorsa())


class Mage(personaggi):
    def __init__(self, name: str, level: int = 1, mana: int = 30, max_mana: int = 30):
        super().__init__(name, level)
        self._max_mana = max_mana
        self._mana = mana

    def nome_risorsa(self) -> str:
        return "Mana"

    def valore_risorsa(self) -> int:
        return self._mana

    def max_risorsa(self) -> int:
        return self._max_mana

    def refilla_risorsa(self) -> None:
        self._mana = self._max_mana

    def attack(self, enemy: "Enemy") -> str:
        costo = 3
        if self._mana < costo:
            return f"{self.name} non ha abbastanza mana ({costo}) per attaccare!"
        self._mana -= costo
        danno = random.randint(1, 6) + self.level
        enemy.take_damage(danno)
        return f"{self.name} lancia una magia e infligge {danno} danni (costo {costo} Mana)."

    def curarsi(self) -> str:
        costo = 4
        if self._mana < costo:
            return f"{self.name} non ha abbastanza mana ({costo}) per curarsi!"
        self._mana -= costo
        amount = 12 + self.level
        self.heal(amount)
        return f"{self.name} si cura di {amount} HP (costo {costo} Mana)."

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Pozione Vita":
            self.heal(15)                                       #buffare pozione salute, magari 20% maxhp anzichè 155hp ***FIXARE
            return f"{self.name} usa una Pozione: +15 HP."
        if item == "Pozione Mana":
            before = self._mana
            self._mana = intervallonumerico(self._mana + 10, 0, self._max_mana)
            return f"{self.name} usa Mana Potion: Mana {before}->{self._mana}."
        if item == "Bomba":
            enemy.take_damage(12)                           # buffare danno bomba ***FIXARE
            return f"{self.name} lancia una Bomba: 12 danni al nemico."
        if item == "Pozione Stamina":
            return f"{self.name} non può usare la pozione della stamina (solo per Guerriero)."
        if item == "Pozione Scudo":
            return "APPLICA_SCUDO"
        return f"Oggetto sconosciuto: {item}"


class Warrior(personaggi):
    def __init__(self, name: str, level: int = 1, stamina: int = 30, max_stamina: int = 30):
        super().__init__(name, level)
        self._max_stamina = max_stamina
        self._stamina = stamina

    def nome_risorsa(self) -> str:
        return "Stamina "

    def valore_risorsa(self) -> int:
        return self._stamina

    def max_risorsa(self) -> int:
        return self._max_stamina

    def refilla_risorsa(self) -> None:
        self._stamina = self._max_stamina

    def attack(self, enemy: "Enemy") -> str:
        print("Scegli potenza attacco: 1 (leggero), 2 (medio), 3 (forte)")
        power = richiestanumeroscelta("> ", [1, 2, 3])
        costo = 2 * power
        if self._stamina < costo:
            return f"{self.name} non ha abbastanza stamina ({costo}) per attaccare!"
        self._stamina -= costo
        danno = (4 * power) + self.level
        enemy.take_damage(danno)
        return f"\n\n\n{self.name} colpisce (potenza {power}) e infligge {danno} danni (costo {costo} Stamina)."

    def curarsi(self) -> str:
        costo = 4
        if self._stamina < costo:
            return f"{self.name} non ha abbastanza stamina ({costo}) per curarsi!"
        self._stamina -= costo
        amount = 10 + self.level
        self.heal(amount)
        return f"{self.name} si fascia: +{amount} HP (costo {costo} Stamina)."

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Pozione Vita":
            self.heal(15)
            return f"{self.name} usa una Pozione: +15 HP."
        if item == "Pozione Stamina":
            before = self._stamina
            self._stamina = intervallonumerico(self._stamina + 10, 0, self._max_stamina)
            return f"{self.name} usa Stamina Potion: ST {before}->{self._stamina}."
        if item == "Bomba":
            enemy.take_damage(12)
            return f"{self.name} lancia una Bomba: 12 danni al nemico."
        if item == "Pozione Mana":
            return f"{self.name} non può usare la pozione per mana, (solo per Mago)."
        if item == "Pozione Scudo":
            return "APPLICA_SCUDO"
        return f"Oggetto sconosciuto: {item}"
