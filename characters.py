import random
from abc import ABC
from utilities import intervallonumerico, show_bar, richiestanumeroscelta

# Gestione Classi dei giocatori con le loro proprietà

class personaggi(ABC):
    # Attributo di classe predefinito per il menu
    nome_seconda_azione: str = "Cura"

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

    def seconda_azione(self) -> str:
        cura = 10 + (self._level * 2)
        self.heal(cura)
        return f"{self.name} si fascia le ferite: +{cura} HP."

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

    # Metodi astratti da implementare nelle sottoclassi
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

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Mela":
            self.heal(15)
            return f"{self.name} mangia una mela: +15 HP."
        if item == "Tacchino Arrosto":
            self.heal(40)
            return f"{self.name} mangia un tacchino arrosto: +40 HP."
        if item == "Bomba":
            enemy.take_damage(12)
            return f"{self.name} lancia una Bomba: 12 danni al nemico."
        if item == "GigaBomba":
            enemy.take_damage(100)
            return f"{self.name} lancia una GigaBomba: 100 danni al nemico."
        if item == "Pozione Scudo":
            return "APPLICA_SCUDO"
        if item == "Pozione Furia":
            return "APPLICA_FURIA"

        return f"Oggetto sconosciuto: {item}"

    def status(self):
        print(f"\n{self.name} (Lv {self.level})")
        show_bar("Salute ", self.hp, self.max_hp)
        show_bar(self.nome_risorsa(), self.valore_risorsa(), self.max_risorsa())


class Mage(personaggi):
    nome_seconda_azione: str = "Cura"

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

    # Sostituisce curarsi(): consuma mana ed esegue l'azione corretta
    def seconda_azione(self) -> str:
        costo = 4
        if self._mana < costo:
            return f"{self.name} non ha abbastanza mana ({costo}) per curarsi!"
        self._mana -= costo
        amount = 12 + self.level
        self.heal(amount)
        return f"{self.name} si cura di {amount} HP (costo {costo} Mana)."

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Pozione Mana":
            before = self._mana
            self._mana = intervallonumerico(self._mana + 10, 0, self._max_mana)
            return f"{self.name} usa Mana Potion: Mana {before}->{self._mana}."
        if item == "Pozione Stamina":
            return f"ERRORE: {self.name} non può usare la pozione della stamina (solo per Guerriero)."
        if item == "Reliquia":
            return f"ERRORE: Solo il Chierico può trarre potere dalla Reliquia!"

        return super().usaoggetto(item, enemy)


class Warrior(personaggi):
    nome_seconda_azione: str = "Cura"

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

    # Sostituisce curarsi(): consuma stamina ed esegue la fasciatura corretta
    def seconda_azione(self) -> str:
        costo = 4
        if self._stamina < costo:
            return f"{self.name} non ha abbastanza stamina ({costo}) per curarsi!"
        self._stamina -= costo
        amount = 10 + self.level
        self.heal(amount)
        return f"{self.name} si fascia: +{amount} HP (costo {costo} Stamina)."

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Pozione Stamina":
            before = self._stamina
            self._stamina = intervallonumerico(self._stamina + 10, 0, self._max_stamina)
            return f"{self.name} usa Stamina Potion: ST {before}->{self._stamina}."
        if item == "Pozione Mana":
            return f"ERRORE: {self.name} non può usare la pozione per mana, (solo per Mago)."
        if item == "Reliquia":
            return f"ERRORE: Solo il Chierico può trarre potere dalla Reliquia!"

        return super().usaoggetto(item, enemy)


class Cleric(personaggi):
    nome_seconda_azione: str = "Prega"

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self._max_fede = 20
        self._fede = 0

    def nome_risorsa(self) -> str:
        return "Fede"

    def valore_risorsa(self) -> int:
        return self._fede

    def max_risorsa(self) -> int:
        return self._max_fede

    def refilla_risorsa(self) -> None:
        self._fede = 0

    def seconda_azione(self) -> str:
        cura = 2 + (self.level * 2)
        self.heal(cura)
        prima = self._fede
        self._fede = min(self._max_fede, self._fede + 6)
        return f"{self.name} prega devotamente: +{cura} HP, Fede {prima} -> {self._fede}/{self._max_fede}."

    def attack(self, enemy: "Enemy") -> str:
        bonus = self._fede // 2
        danno = 6 + self.level + bonus
        enemy.take_damage(danno)

        prima = self._fede
        self._fede = max(0, self._fede - 3)
        return f"{self.name} scaglia punizione divina: {danno} danni (bonus fede +{bonus})! Fede {prima} -> {self._fede}/{self._max_fede}."

    def decadimento_turno(self) -> str:
        if self._fede > 0:
            self._fede -= 1
            return f"La fede di {self.name} cala a {self._fede}/{self._max_fede}."
        return ""

    def usaoggetto(self, item: str, enemy: "Enemy") -> str:
        if item == "Reliquia":
            prima = self._fede
            self._fede = min(self._max_fede, self._fede + 8)
            return f"{self.name} usa la Reliquia: Fede {prima} -> {self._fede}/{self._max_fede}."
        if item in ("Pozione Mana", "Pozione Stamina"):
            return f"ERRORE: {self.name} non può usare {item} (utilizza Fede)!"

        return super().usaoggetto(item, enemy)