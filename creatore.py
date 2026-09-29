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

    ##
    ## Versione 5.0 - Gui Edition
    ## Introdotto pygame con il quale è stato aggiunta una finestra di gioco
    ## con sprites, suoni e menù grafici
    ##