from typing import List, Dict
from characters import Mage, Warrior

# Gestione salvataggio e caricamento del savefile

class saveload:

        #Salvataggio
    def save(path: str, num_players: int, stage: int, players: List[object], inventory: List[str]) -> None:
        lines: List[str] = []
        lines.append(f"numero_giocatori={num_players}")

        if num_players == 1 and players:
            player = players[0]
            if isinstance(player, Mage):
                lines.append("classe_giocatore=mage")
            elif isinstance(player, Warrior):
                lines.append("classe_giocatore=warrior")
            else:
                lines.append("classe_giocatore=warrior")
            try:
                lines.append(f"nome_giocatore={player.name}")
            except Exception:
                pass

        elif num_players == 2 and players and len(players) >= 2:
            player1 = players[0]
            player2 = players[1]
            classe1 = "warrior" if isinstance(player1, Warrior) else "mage"
            classe2 = "warrior" if isinstance(player2, Warrior) else "mage"
            lines.append(f"classe_giocatore1={classe1}")
            lines.append(f"classe_giocatore2={classe2}")

            try:
                lines.append(f"nome_giocatore1={player1.name}")
                lines.append(f"nome_giocatore2={player2.name}")
            except Exception:
                pass

        lines.append(f"stage={stage}")
        lines.append("oggetti=" + ",".join(inventory) if inventory else "oggetti=")
        with open(path, "w") as f:
            f.write("\n".join(lines))

        # Caricamento
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
        if num_players == 1:
            classe = dati_salvataggio.get("classe_giocatore", "warrior").lower()
            name = dati_salvataggio.get("nome_giocatore", "Player")

            if classe == "mage":
                player = Mage(name=name)
            else:
                player = Warrior(name=name)

            for _ in range(stage - 1):  #i giocatori livellano tante volte quanti stage son stati superati
                player.levelup()
            players.append(player)


        else:
            classe1 = dati_salvataggio.get("classe_giocatore1", "warrior").lower()
            classe2 = dati_salvataggio.get("classe_giocatore2", "mage").lower()

            name1 = dati_salvataggio.get("nome_giocatore1", "Warrior")
            name2 = dati_salvataggio.get("nome_giocatore2", "Mage")
            if classe1 == "mage":
                p1 = Mage(name=name1)
            else:
                p1 = Warrior(name=name1)
            if classe2 == "mage":
                p2 = Mage(name=name2)
            else:
                p2 = Warrior(name=name2)
            for _ in range(stage - 1):
                p1.levelup()
                p2.levelup()
            players.extend([p1, p2])

        return {"num_players": num_players, "stage": stage, "players": players, "inventory": inventory}

