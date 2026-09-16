from typing import List, Dict, Optional
from utilities import richiestanumeroscelta, si_o_no, ee2, titletext2
from items import random_item, descrizione_oggetti
from characters import personaggi, Cleric
from nemici import Enemy, summona_nemico
from creatore import creatorepersonaggio
from saveload import saveload
from pozioni import ScudoMagico, Furia
from hall_of_fame import HallOfFame


class Game:
    def __init__(self):
        self.num_players: int = 1
        self.stage: int = 1
        self.players: List[personaggi] = []
        self.inventory: List[str] = []
        self.percorso_di_salvataggio = "salvataggio.txt"
        self.durata_partita = 10

    def nuovogioco(self) -> None:
        print("Nuova partita:")
        self.num_players = richiestanumeroscelta("1) Solo  2) Coppia  > ", [1, 2])
        self.stage = 1
        self.inventory = []

        # Aggiornare per garantire la scalabilità delle classi                    ***FIXARE

        classi_disponibili = {1: "warrior", 2: "mage", 3: "cleric"}
        nomi_default = {1: "Guerriero", 2: "Mago", 3: "Chierico"}

        if self.num_players == 1:
            kind = richiestanumeroscelta("Scegli classe: 1) Guerriero  2) Mago  3) Chierico  > ", [1, 2, 3])
            name = input("Nome giocatore: ").strip() or nomi_default[kind]
            self.players = [creatorepersonaggio.create(classi_disponibili[kind], name)]
        else:
            # Scelta Giocatore 1
            print("\n--- Giocatore 1 ---")
            kind1 = richiestanumeroscelta("Scegli classe: 1) Guerriero  2) Mago  3) Chierico  > ", [1, 2, 3])
            name1 = input("Nome primo giocatore: ").strip() or nomi_default[kind1]

            # Scelta Giocatore 2 tra le sole classi rimaste libere
            print("\n--- Giocatore 2 ---")
            rimaste = [k for k in [1, 2, 3] if k != kind1]
            prompt = f"Scegli classe: {rimaste[0]}) {nomi_default[rimaste[0]]}  {rimaste[1]}) {nomi_default[rimaste[1]]}  > "
            kind2 = richiestanumeroscelta(prompt, rimaste)
            name2 = input("Nome secondo giocatore: ").strip() or nomi_default[kind2]

            self.players = [
                creatorepersonaggio.create(classi_disponibili[kind1], name1),
                creatorepersonaggio.create(classi_disponibili[kind2], name2),
            ]

    def caricagioco(self) -> bool:
        try:
            dati_di_salvataggio = saveload.load(self.percorso_di_salvataggio)
            self.num_players = int(dati_di_salvataggio["num_players"])
            self.stage = int(dati_di_salvataggio["stage"])
            self.players = dati_di_salvataggio["players"]
            self.inventory = dati_di_salvataggio["inventory"]
            print(f"Salvataggio caricato: Stage {self.stage}/10, Giocatori={self.num_players}")
            return True
        except FileNotFoundError:
            print("Nessun salvataggio trovato")
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
            inv_str = ", ".join([f"{k} x{v}" for k, v in conta.items()])
            print(f"Inventario: {inv_str}")
        else:
            print("Inventario: (vuoto)")
        print()

    def choose_item(self) -> Optional[str]:
        if not self.inventory:
            print("L'inventario è vuoto.")
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
        while self.stage <= self.durata_partita:
            enemy = summona_nemico(self.stage)
            print(f"\n***** Squillano le trombe, l'orco '{enemy.name}' è sceso in campo *****")

            while enemy.ancoravivo() and not self.totalpartykill():
                self.mostra_stato(enemy)

                for player in self.players:
                    if not player.ancoravivo() or not enemy.ancoravivo():
                        continue

                    # Ciclo per ripetere l'azione in caso di input non valido o annullamento
                    while True:
                        # Estrazione sicura del nome azione anche se il pg è decorato da Scudo/Furia
                        pg_effettivo = getattr(player, "target", player)
                        nome_azione = getattr(pg_effettivo, "nome_seconda_azione", "Cura")

                        print(f"Tocca a {player.name} |1) Attacca  |2) {nome_azione}  |3) Oggetti  |4) Salva ed Esci  |5) Abbandona senza salvare")
                        action = richiestanumeroscelta("> ", [1, 2, 3, 4, 5])

                        if action == 1:
                            messaggio_scelta = player.attack(enemy)
                            print(messaggio_scelta)
                            break
                        elif action == 2:
                            messaggio_scelta = player.seconda_azione()
                            print(messaggio_scelta)
                            break
                        elif action == 3:
                            item = self.choose_item()
                            if item is None:
                                print(f"{player.name} ci ripensa.")
                                continue

                            esito = player.usaoggetto(item, enemy)
                            if esito.startswith("ERRORE:"):
                                print(esito)
                                self.inventory.append(item)
                                print("Turno non consumato, riprova.")
                                continue
                            elif esito == "APPLICA_SCUDO":
                                idx = self.players.index(player)
                                self.players[idx] = ScudoMagico(player, turni=2)
                                messaggio_scelta = f"{player.name} beve la pozione scudo, difesa raddoppiata per 2 turni"
                            elif esito == "APPLICA_FURIA":
                                idx = self.players.index(player)
                                self.players[idx] = Furia(player, turni=2)
                                messaggio_scelta = f"{player.name} beve la pozione furia, danni raddoppiati per 2 turni"
                            else:
                                messaggio_scelta = esito

                            print(messaggio_scelta)
                            break
                        elif action == 4:
                            self.salvagioco()
                            print(f"{player.name} ha deciso di prendersi una pausa")
                            return
                        else:  # action == 5
                            confirm = si_o_no("Sei sicuro di abbandonare senza salvare? (s/n) ")
                            if confirm:
                                print("Hai abbandonato la partita.")
                                return
                            print(f"{player.name} non ha perso la speranza")
                            continue

                # Turno del nemico
                if enemy.ancoravivo() and not self.totalpartykill():
                    outputnemico = enemy.attack(self.players)
                    print(outputnemico)

                # Gestione scadenza decoratori a fine round
                for idx, p in enumerate(self.players):
                    if isinstance(p, (ScudoMagico, Furia)):
                        ancora_valido = p.scala_turno()
                        if not ancora_valido:
                            print(f"L'effetto di {p.name} si è esaurito")
                            self.players[idx] = p.target

                # Decadimento passivo Fede del Chierico
                for p in self.players:
                    personaggio_reale = getattr(p, "target", p)
                    if isinstance(personaggio_reale, Cleric) and personaggio_reale.ancoravivo():
                        msg_decadimento = personaggio_reale.decadimento_turno()
                        if msg_decadimento:
                            print(msg_decadimento)

            if self.totalpartykill():
                print("\nDisfatta! Tutti i giocatori sono stati sconfitti!")
                HallOfFame.new_record(self.players, self.stage)
                return

            print(f"\nNemico sconfitto! Stage {self.stage} completato.")

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
        HallOfFame.new_record(self.players, self.stage - 1)

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