import random
from typing import List

# Gestione oggetti di gioco utilizzabili dai players

listaoggetti: List[str] = [
"Mela",
"Tacchino Arrosto",
"Pozione Mana",
"Pozione Stamina",
"Bomba",
"Pozione Scudo",
"Pozione Furia",
"Reliquia"
]

def random_item() -> str:
    return random.choice(listaoggetti)

def descrizione_oggetti(name: str) -> str:
    return {
        "Mela": "cura 15 punti vita",
        "Tacchino Arrosto": "cura 40 punti vita",
        "Pozione Mana": "+10 Mana (if Mago)",
        "Pozione Stamina": "+10 Stamina (if Guerriero)",
        "Bomba": "12 danni",
        "GigaBomba": "*debug item* 100 danni",                    #per testing e debugging, non presente in listaoggetti
        "Pozione Scudo": "dimezza i danni subiti per 2 turni",
        "Pozione Furia": "raddoppia i danni inflitti per 2 turni",
        "Reliquia": "+8 Fede (solo per Chierico)",
    }.get(name, name)