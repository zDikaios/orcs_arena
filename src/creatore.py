from characters import Warrior, Mage, Cleric

# Factory di creazione personaggio

class creatorepersonaggio:
    @staticmethod
    def create(classe: str, name: str):
        c = classe.strip().lower()
        if c in ("guerriero", "warrior"):
            return Warrior(name)
        elif c in ("mago", "mage"):
            return Mage(name)
        elif c in ("chierico", "cleric"):
            return Cleric(name)
        raise ValueError(f"ERRORE: Classe sconosciuta: {classe}")