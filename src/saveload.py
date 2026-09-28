from typing import List, Dict
from creatore import creatorepersonaggio


# Gestione salvataggio e caricamento del savefile

class saveload:

    @staticmethod
    def save(path: str, num_players: int, stage: int, players: List[object], inventory: List[str]) -> None:
        lines: List[str] = []
        lines.append(f"numero_giocatori={num_players}")

        # Serializza dinamicamente qualunque classe e numero di giocatori
        for i, player in enumerate(players, start=1):
            # Se il personaggio ha un Decorator attivo, estraiamo l'oggetto reale sottostante
            pg_reale = getattr(player, "target", player)

            # Ricava dinamicamente il nome della classe ('warrior', 'mage', 'cleric', ecc.) -> scalabilità
            classe_nome = pg_reale.__class__.__name__.lower()
            nome_giocatore = getattr(pg_reale, "name", f"Giocatore{i}")

            lines.append(f"classe_giocatore{i}={classe_nome}")
            lines.append(f"nome_giocatore{i}={nome_giocatore}")

        lines.append(f"stage={stage}")
        lines.append("oggetti=" + (",".join(inventory) if inventory else ""))

        with open(path, "w") as f:
            f.write("\n".join(lines))

    @staticmethod
    def load(path: str) -> Dict[str, object]:
        with open(path, "r") as f:
            raw = [line.rstrip("\n") for line in f.readlines()]

        dati_salvataggio: Dict[str, str] = {}
        for line in raw:
            if not line:
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                dati_salvataggio[k] = v

        num_players = int(dati_salvataggio.get("numero_giocatori", "1"))
        stage = int(dati_salvataggio.get("stage", "1"))
        listaoggetti = dati_salvataggio.get("oggetti", "")
        inventory = [x for x in listaoggetti.split(",") if x] if listaoggetti else []

        players: List[object] = []
        for i in range(1, num_players + 1):
            # Compatibilità: legge classe_giocatore1 (o fallback classe_giocatore per vecchi save a 1 player)
            classe = dati_salvataggio.get(f"classe_giocatore{i}")
            if not classe and i == 1:
                classe = dati_salvataggio.get("classe_giocatore", "warrior")

            name = dati_salvataggio.get(f"nome_giocatore{i}")
            if not name and i == 1:
                name = dati_salvataggio.get("nome_giocatore", "Player")

            # La Factory istanzia dinamicamente qualsiasi classe passata
            player = creatorepersonaggio.create(classe.strip().lower(), name)

            # I giocatori livellano tante volte quanti sono gli stage superati
            for _ in range(stage - 1):
                player.levelup()

            players.append(player)

        return {
            "num_players": num_players,
            "stage": stage,
            "players": players,
            "inventory": inventory
        }