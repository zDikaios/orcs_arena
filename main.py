import pygame
from typing import List, Optional

from ui import UIManager, GuiButton, SCREEN_WIDTH
from items import random_item
from characters import personaggi, Cleric
from nemici import Enemy, summona_nemico
from creatore import creatorepersonaggio
from saveload import saveload
from pozioni import ScudoMagico, Furia
from hall_of_fame import HallOfFame


##
## Versione 5.0 - Gui Edition
## Introdotto pygame con il quale è stato aggiunta una finestra di gioco
## con sprites, suoni e menù grafici
##

class Game:
    def __init__(self):
        self.num_players: int = 1
        self.stage: int = 1
        self.players: List[personaggi] = []
        self.inventory: List[str] = []
        self.percorso_di_salvataggio = "salvataggio.txt"
        self.durata_partita = 10
        self.ui = UIManager()

    def esegui_attacco_giocatore(self, player: personaggi, enemy: Enemy, power_choice: Optional[int]) -> str:
        # Polimorfismo puro: se power_choice è valorizzato, viene passato come kwargs
        if power_choice is not None:
            return player.attack(enemy, power=power_choice)
        return player.attack(enemy)

    def nuovogioco(self) -> None:
        btn_party = [
            GuiButton((SCREEN_WIDTH // 2 - 210, 240, 190, 55), "1) Solo", 1),
            GuiButton((SCREEN_WIDTH // 2 + 20, 240, 190, 55), "2) Coppia", 2)
        ]
        self.num_players = self.ui.wait_for_choice("CONFIGURAZIONE PARTITA", "Seleziona il numero di giocatori (Premi 1 o 2)", btn_party)
        self.stage = 1
        self.inventory = []

        classi_disponibili = {1: "warrior", 2: "mage", 3: "cleric"}
        nomi_default = {1: "Guerriero", 2: "Mago", 3: "Chierico"}

        if self.num_players == 1:
            btn_classi = [
                GuiButton((170, 260, 220, 52), "1) Guerriero", 1),
                GuiButton((450, 260, 220, 52), "2) Mago", 2),
                GuiButton((730, 260, 220, 52), "3) Chierico", 3),
            ]
            kind = self.ui.wait_for_choice("SELEZIONE CLASSE", "Scegli la tua classe (Premi 1, 2 o 3)", btn_classi)
            name = self.ui.text_input_dialog(f"Nome per {nomi_default[kind]}:", nomi_default[kind])
            self.players = [creatorepersonaggio.create(classi_disponibili[kind], name)]
            print(f"[LOG] Creata nuova partita Solo: {name} ({nomi_default[kind]})")
        else:
            btn_c1 = [
                GuiButton((170, 260, 220, 52), "1) Guerriero", 1),
                GuiButton((450, 260, 220, 52), "2) Mago", 2),
                GuiButton((730, 260, 220, 52), "3) Chierico", 3),
            ]
            kind1 = self.ui.wait_for_choice("GIOCATORE 1", "Scegli la classe del Giocatore 1 (Premi 1, 2 o 3)", btn_c1)
            name1 = self.ui.text_input_dialog(f"Nome Giocatore 1 ({nomi_default[kind1]}):", nomi_default[kind1])

            rimaste = [k for k in [1, 2, 3] if k != kind1]
            btn_c2 = [
                GuiButton((SCREEN_WIDTH // 2 - 240, 260, 220, 52), f"{rimaste[0]}) {nomi_default[rimaste[0]]}", rimaste[0]),
                GuiButton((SCREEN_WIDTH // 2 + 20, 260, 220, 52), f"{rimaste[1]}) {nomi_default[rimaste[1]]}", rimaste[1]),
            ]
            kind2 = self.ui.wait_for_choice("GIOCATORE 2", f"Scegli la classe del Giocatore 2 (Premi {rimaste[0]} o {rimaste[1]})", btn_c2)
            name2 = self.ui.text_input_dialog(f"Nome Giocatore 2 ({nomi_default[kind2]}):", nomi_default[kind2])

            self.players = [
                creatorepersonaggio.create(classi_disponibili[kind1], name1),
                creatorepersonaggio.create(classi_disponibili[kind2], name2),
            ]
            print(f"[LOG] Creata nuova partita Coppia: {name1} ({nomi_default[kind1]}) & {name2} ({nomi_default[kind2]})")

    def caricagioco(self) -> bool:
        try:
            dati = saveload.load(self.percorso_di_salvataggio)
            self.num_players = int(dati["num_players"])
            self.stage = int(dati["stage"])
            self.players = dati["players"]
            self.inventory = dati["inventory"]
            print(f"[LOG] Salvataggio caricato: Stage {self.stage}/10 ({self.num_players} Giocatori)")
            return True
        except FileNotFoundError:
            print("[LOG] Nessun file di salvataggio trovato.")
            return False

    def salvagioco(self) -> None:
        saveload.save(
            path=self.percorso_di_salvataggio,
            num_players=self.num_players,
            stage=self.stage,
            players=self.players,
            inventory=self.inventory
        )
        print(f"[LOG] Partita salvata con successo in {self.percorso_di_salvataggio}")

    def totalpartykill(self) -> bool:
        return all(not p.ancoravivo() for p in self.players)

    def menu_combat(self) -> None:
        while self.stage <= self.durata_partita:
            enemy = summona_nemico(self.stage)
            banner = f"Inizio Stage {self.stage}: l'orco '{enemy.name}' è sceso in campo!"
            print(f"\n[COMBAT] {banner}")
            ultimo_messaggio = banner

            while enemy.ancoravivo() and not self.totalpartykill():
                for player in self.players:
                    if not player.ancoravivo() or not enemy.ancoravivo():
                        continue

                    while True:
                        action, power_choice, chosen_item = self.ui.get_battle_action(
                            self.players, enemy, player, ultimo_messaggio, self.inventory
                        )

                        if action == 1:
                            ultimo_messaggio = self.esegui_attacco_giocatore(player, enemy, power_choice)
                            print(f"[COMBAT] {ultimo_messaggio}")
                            break
                        elif action == 2:
                            ultimo_messaggio = player.seconda_azione()
                            print(f"[COMBAT] {ultimo_messaggio}")
                            break
                        elif action == 3:
                            item = chosen_item
                            esito = player.usaoggetto(item, enemy)
                            if esito.startswith("ERRORE:"):
                                self.inventory.append(item)
                                ultimo_messaggio = f"{esito} Turno non consumato."
                                print(f"[COMBAT] {esito}")
                                continue
                            elif esito == "APPLICA_SCUDO":
                                idx = self.players.index(player)
                                self.players[idx] = ScudoMagico(player, turni=2)
                                ultimo_messaggio = f"{player.name} beve la pozione scudo: difesa raddoppiata per 2 turni!"
                            elif esito == "APPLICA_FURIA":
                                idx = self.players.index(player)
                                self.players[idx] = Furia(player, turni=2)
                                ultimo_messaggio = f"{player.name} beve la pozione furia: danni raddoppiati per 2 turni!"
                            else:
                                ultimo_messaggio = esito

                            print(f"[COMBAT] {ultimo_messaggio}")
                            break
                        elif action == 4:
                            self.salvagioco()
                            print(f"[LOG] {player.name} ha salvato la partita.")
                            return
                        else:  # action == 5
                            btn_confirm = [
                                GuiButton((SCREEN_WIDTH // 2 - 180, 560, 160, 50), "Esci", 1),
                                GuiButton((SCREEN_WIDTH // 2 + 20, 560, 160, 50), "Resta", 2)
                            ]
                            confirm = self.ui.wait_for_choice("CONFERMA ABBANDONO",
                                                              "Vuoi davvero abbandonare la partita?", btn_confirm)
                            if confirm == 1:
                                print(f"[LOG] {player.name} ha abbandonato la partita senza salvare.")
                                return
                            ultimo_messaggio = f"{player.name} riprende a lottare!"
                            continue

                if enemy.ancoravivo() and not self.totalpartykill():
                    outputnemico = enemy.attack(self.players)
                    ultimo_messaggio = outputnemico
                    print(f"[COMBAT] {outputnemico}")

                for idx, p in enumerate(self.players):
                    if isinstance(p, (ScudoMagico, Furia)):
                        ancora_valido = p.scala_turno()
                        if not ancora_valido:
                            print(f"[BUFF] L'effetto di {p.name} si è esaurito.")
                            self.players[idx] = p.target

                for p in self.players:
                    personaggio_reale = getattr(p, "target", p)
                    if isinstance(personaggio_reale, Cleric) and personaggio_reale.ancoravivo():
                        msg_decadimento = personaggio_reale.decadimento_turno()
                        if msg_decadimento:
                            print(f"[BUFF] {msg_decadimento}")

            if self.totalpartykill():
                print(f"[RISULTATO] Disfatta allo Stage {self.stage}! Tutti i giocatori sono stati sconfitti.")
                HallOfFame.new_record(self.players, self.stage)
                btn_end = [GuiButton((SCREEN_WIDTH // 2 - 100, 340, 200, 52), "1) Continua", 1)]
                self.ui.wait_for_choice("GAME OVER", "Il party è caduto in battaglia... (Premi 1 o SPAZIO)", btn_end)
                return

            print(f"[RISULTATO] Nemico sconfitto! Stage {self.stage} completato.")
            for player in self.players:
                if player.ancoravivo():
                    player.levelup()
                    print(f"[LEVEL UP] {player.name} sale di livello!")
                else:
                    player.full_vita()
                    print(f"[REVIVE] {player.name} è tornato in piedi (nessun livello guadagnato).")

            reward = random_item()
            self.inventory.append(reward)
            print(f"[LOOT] Ottenuto: {reward}")
            self.stage += 1

        print("[TRIONFO] L'Arena è stata completata con successo!")
        HallOfFame.new_record(self.players, self.stage - 1)
        btn_win = [GuiButton((SCREEN_WIDTH // 2 - 100, 340, 200, 52), "1) Trionfo!", 1)]
        self.ui.wait_for_choice("VITTORIA", "Complimenti! Hai completato l'Arena! (Premi 1 o SPAZIO)", btn_win)

    def mostra_hall_of_fame(self) -> None:
        try:
            records = HallOfFame.leggi_classifica()
            lines = [
                f"{idx + 1}.  {r.get('nomi', 'Eroe')}   -   Stage: {r.get('stage', 1)}   -   Punti: {r.get('punti', 0)}"
                for
                idx, r in enumerate(records)]
            if not lines:
                lines = ["Nessun record presente."]
        except Exception:
            lines = ["Classifica vuota o non accessibile."]

        print(f"[LOG] Visualizzazione Hall of Fame ({len(lines)} record caricati dal file binario)")

        # Pulsante in basso a destra con immagine goback.png (e fallback a testo)
        btn_back = [
            GuiButton((860, 590, 200, 50), "Torna Indietro", 1, image=self.ui.goback_texture)
        ]

        self.ui.wait_for_choice("HALL OF FAME", "", btn_back, lines)
    def menu_principale(self) -> None:
        print("[SISTEMA] Avvio Orcs Arena 5.0")
        while True:
            # Pulsanti con le 4 immagini caricate (300 x 55 pixel)
            btn_main = [
                GuiButton((SCREEN_WIDTH // 2 - 150, 300, 300, 55), "1) Nuova partita", 1,
                          image=self.ui.menu_btn_textures.get(1)),
                GuiButton((SCREEN_WIDTH // 2 - 150, 375, 300, 55), "2) Carica salvataggio", 2,
                          image=self.ui.menu_btn_textures.get(2)),
                GuiButton((SCREEN_WIDTH // 2 - 150, 450, 300, 55), "3) Hall of Fame", 3,
                          image=self.ui.menu_btn_textures.get(3)),
                GuiButton((SCREEN_WIDTH // 2 - 150, 525, 300, 55), "4) Esci dal gioco", 4,
                          image=self.ui.menu_btn_textures.get(4)),
            ]

            # is_main_menu=True nasconde titolo e scritte nel menu principale
            choice = self.ui.wait_for_choice("", "", btn_main, is_main_menu=True)

            if choice == 1:
                self.nuovogioco()
                self.menu_combat()
            elif choice == 2:
                if self.caricagioco():
                    self.menu_combat()
            elif choice == 3:
                self.mostra_hall_of_fame()
            elif choice == 4:
                print("[SISTEMA] Uscita dal gioco.")
                pygame.quit()
                return

if __name__ == "__main__":
    Game().menu_principale()