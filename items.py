import random
from typing import List

listaoggetti: List[str] = ["Pozione Vita", "Pozione Mana", "Pozione Stamina", "Bomba"]


def random_item() -> str:
    return random.choice(listaoggetti)


def descrizione_oggetti(name: str) -> str:
    return {
        "Pozione Vita": "cura 15 punti vita",
        "Pozione Mana": "+10 Mana (if Mago)",
        "Pozione Stamina": "+10 Stamina (if Guerriero)",
        "Bomba": "12 danni",
    }.get(name, name)
