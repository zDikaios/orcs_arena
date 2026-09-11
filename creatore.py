from characters import Mage, Warrior, personaggi

# Factory di creazione personaggio

class creatorepersonaggio:
    def create(classe: str, name: str) -> personaggi:
        classe = classe.lower()
        if classe == "mage":
            return Mage(name=name)
        if classe == "warrior":
            return Warrior(name=name)
        raise ValueError(f"Tipo personaggio non valido: {classe}")
