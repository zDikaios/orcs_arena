from typing import List, Dict, Optional
from utilities import richiestanumeroscelta, si_o_no, ee2, titletext2
from items import random_item, descrizione_oggetti
from characters import personaggi
from nemici import Enemy, summona_nemico
from creatore import creatorepersonaggio
from saveload import saveload
from pozioni import ScudoMagico
from hall_of_fame import HallOfFame


class Game:
    def __init__(self):
        self.num_players: int = 1
        self.stage: int = 1
        self.players: List[personaggi] = []
        self.inventory: List[str] = []
        self.percorso_di_salvataggio = "salvataggio.txt"

    def nuovogioco(self) -> None:
        print("Nuova partita:")
        self.num_players = richiestanumeroscelta("1) Solo  2) Coppia  > ", [1, 2])
        self.stage = 1
        self.inventory = []

        if self.num_players == 1:
            kind = richiestanumeroscelta("Scegli classe: 1) Guerriero  2) Mago  > ", [1, 2])
            name = input("Nome giocatore: ") or "Player"
            if kind == 1:
                self.players = [creatorepersonaggio.create("warrior", name)]
            else:
                self.players = [creatorepersonaggio.create("mage", name)]
        else:
            #il primo giocatore sceglie la classe il secondo ottiene automaticamente l'altra
            kind1 = richiestanumeroscelta("Scegli classe per il primo giocatore: 1) Guerriero  2) Mago  > ", [1, 2])
            name1 = input("Nome primo giocatore: ") or ("Guerriero" if kind1 == 1 else "Mago")
            name2 = input("Nome secondo giocatore: ") or ("Mago" if kind1 == 1 else "Guerriero")
            if kind1 == 1:
                self.players = [
                    creatorepersonaggio.create("warrior", name1),
                    creatorepersonaggio.create("mage", name2),
                ]
            else:
                self.players = [
                    creatorepersonaggio.create("mage", name1),
                    creatorepersonaggio.create("warrior", name2),
                ]

    def caricagioco(self) -> bool:
        try:
            dati_di_salvataggio = saveload.load(self.percorso_di_salvataggio)     # prende i dati dal file
            self.num_players = int(dati_di_salvataggio["num_players"])            # legge il numero di giocatori
            self.stage = int(dati_di_salvataggio["stage"])                        # legge lo stage
            self.players = dati_di_salvataggio["players"]                         # legge i personaggi
            self.inventory = dati_di_salvataggio["inventory"]                     # legge l'inventario
            print(f"Salvataggio caricato: Stage {self.stage}/10, Giocatori={self.num_players}")
            return True
        except FileNotFoundError:
            print(f"Nessun salvataggio trovato")
            return False

    def salvagioco(self) -> None:
        saveload.save(
            path=self.percorso_di_salvataggio,
            num_players=self.num_players,
            stage=self.stage,
            players=self.players,
            inventory=self.inventory
        )
        print(f"Partita salvata in {self.percorso_di_salvataggio}")

    def mostra_stato(self, enemy: Enemy) -> None:
        print("\n" + "=" * 40)
        for p in self.players:
            p.status()
        enemy.barre_di_stato()
        print("=" * 40)

        if self.inventory:
            conta: Dict[str, int] = {}
            for it in self.inventory:
                conta[it] = conta.get(it, 0) + 1
            inv_str = ", ".join([f"{k}x{v}" for k, v in conta.items()])
            print(f"Inventario: {inv_str}")
        else:
            print("Inventario: (vuoto)")
        print()

    def choose_item(self) -> Optional[str]:
        if not self.inventory:
            print("Inventario vuoto.")
            return None
        print("Scegli oggetto:")
        for i, it in enumerate(self.inventory, start=1):
            print(f"{i}) {it} - {descrizione_oggetti(it)}")
        print("0) Annulla")
        while True:
            try:
                oggetto_scelto = int(input("> "))
                if oggetto_scelto == 0:
                    return None
                if 1 <= oggetto_scelto <= len(self.inventory):
                    return self.inventory.pop(oggetto_scelto - 1)
            except ValueError:
                pass
            print("Scelta non valida.")

    def totalpartykill(self) -> bool:
        return all(not p.ancoravivo() for p in self.players)

    def menu_combat(self) -> None:
        while self.stage <= 10:
            enemy = summona_nemico(self.stage)
            print(f"\n***** Squillano le trombe, l'orco '{enemy.name}' è sceso in campo *****")

            # loop combattimento
            while enemy.ancoravivo() and not self.totalpartykill():
                self.mostra_stato(enemy)

                # Turno giocatori (ognuno vivo)
                for player in self.players:
                    if not player.ancoravivo() or not enemy.ancoravivo():
                        continue

                    print(f"Tocca a {player.name} |1) Attacca  |2) Cura  |3) Oggetti  |4) Salva ed Esci  |5) Abbandona senza salvare")
                    action = richiestanumeroscelta("> ", [1, 2, 3, 4, 5])

                    if action == 1:
                        messaggio_scelta = player.attack(enemy)
                    elif action == 2:
                        messaggio_scelta = player.curarsi()
                    elif action == 3:
                        item = self.choose_item()
                        if item is None:
                            messaggio_scelta = f"{player.name}: 'Non c'è niente di utile in questa borsa...'"
                        else:
                            esito = player.usaoggetto(item, enemy)
                            if esito == "APPLICA_SCUDO":
                                # sostituisce il pg col decorator scudo
                                idx = self.players.index(player)
                                self.players[idx] = ScudoMagico(player, turni=2)
                                messaggio_scelta = f"{player.name} beve la pozione scudo, difesa raddoppiata per 2 turni"
                            else:
                                messaggio_scelta = esito
                    elif action == 4:
                        self.salvagioco()
                        print(f"{player.name} ha deciso di prendersi una pausa")
                        return # si ritorna al menu principale
                    else:  # action == 5 cioè abbandona senza salvare
                        confirm = si_o_no("Sei sicuro di abbandonare senza salvare? (s/n) ")
                        if confirm:
                            print("Hai abbandonato la partita.")
                            return # si ritorna al menu principale
                        messaggio_scelta = f"{player.name} non ha perso la speranza"

                    print(messaggio_scelta)

                # il turno dei nemici (da rendere più interessante)
                if enemy.ancoravivo() and not self.totalpartykill():
                    outputnemico = enemy.attack(self.players)
                    print(outputnemico)

                # riduce il contatore dei turni del decoratore a fine round
                for idx, p in enumerate(self.players):
                    if isinstance(p, ScudoMagico):
                        ancora_valido = p.scala_turno()
                        if not ancora_valido:
                            print(f"lo scudo magico di {p.name} si e esaurito")
                            # si toglie il decoratore tornando al personaggio base
                            self.players[idx] = p.target


            # calcolo nomi e punteggio per hall of fame
            nomi = " e ".join([p.name for p in self.players])
            punti = (self.stage * 100) + sum([p.hp for p in self.players])

            # sconfitta
            if self.totalpartykill():
                print("\nDisfatta! Tutti i giocatori sono stati sconfitti!")
                # salvataggio binario al game over
                HallOfFame.aggiungi_punteggio(nomi, self.stage, punti)
                HallOfFame.mostra()
                return

            # vittoria stage
            print(f"\nNemico sconfitto! Stage {self.stage} completato.")

            # Level up + restore + ricompensa
            for player in self.players:
                if player.ancoravivo():
                    player.levelup()
                else:
                    player.full_vita()
                    print(f"{player.name} è tornato in piedi, ma non ha guadagnato esperienza!")

            reward = random_item()
            self.inventory.append(reward)
            print(f"{enemy.name} aveva con se {reward} ({descrizione_oggetti(reward)})")

            self.stage += 1

        print("\nL'ARENA HA UN NUOVO CAMPIONE!")

        # salvataggio nella hall of fame e print
        nomi = " e ".join([p.name for p in self.players])
        punti = (self.stage * 100) + sum([p.hp for p in self.players])
        HallOfFame.aggiungi_punteggio(nomi, self.stage - 1, punti)
        HallOfFame.mostra()

    def menu_principale(self) -> None:
        while True:
            print(titletext2)
            print("\n             |1) Nuova partita")
            print("             |2) Carica salvataggio")
            print("             |3) Hall of Fame")
            print("             |4) Exit")
            choice = richiestanumeroscelta("             > ", [1, 2, 3, 4, 42, 69, 404, 420, 502])

            if choice == 1:
                self.nuovogioco()
                self.menu_combat()
            elif choice == 2:
                if self.caricagioco():
                    self.menu_combat()
            elif choice == 3:
                HallOfFame.mostra()
            elif choice == 4:
                print("Uscita dal gioco...")
                return
            else:
                print(ee2)



if __name__ == "__main__":
    Game().menu_principale()
