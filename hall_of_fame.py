import os
from typing import List, Dict, Any

#Una Hall of Fame che mostra i 10 migliori punteggi dei giocatori (Punteggio = Stage*100 + Vita residua)

class HallOfFame:
    percorso_hof = "hall_of_fame.bin"
    dim_nome = 16
    dim_record = 20
    limite_record = 10  # memorizza solo i migliori dieci

    @staticmethod
    def aggiungi_punteggio(nomi: str, stage: int, punti: int):
        records = HallOfFame.leggi_classifica()
        records.append({"nomi": nomi, "stage": stage, "punti": punti})

        # ordina decrescente per punteggio e tiene i primi dieci
        records.sort(key=lambda x: x["punti"], reverse=True)
        records = records[:HallOfFame.limite_record]

        # scrittura binaria
        with open(HallOfFame.percorso_hof, "wb") as file:
            for r in records:
                nome_bytes = r["nomi"].encode("utf-8")[:HallOfFame.dim_nome]
                nome_bytes = nome_bytes.ljust(HallOfFame.dim_nome, b"\x00")

                stage_bytes = r["stage"].to_bytes(2, byteorder="big")
                punti_bytes = r["punti"].to_bytes(2, byteorder="big")

                file.write(nome_bytes)
                file.write(stage_bytes)
                file.write(punti_bytes)


    @staticmethod
    def leggi_classifica() -> List[Dict[str, Any]]:
        if not os.path.exists(HallOfFame.percorso_hof):
            return []

        records = []
        with open(HallOfFame.percorso_hof, "rb") as file:
            while True:
                blocco = file.read(HallOfFame.dim_record)
                if len(blocco) < HallOfFame.dim_record:
                    break
                nome_raw = blocco[0:16]
                nomi = nome_raw.decode("utf-8", errors="ignore").rstrip("\x00")
                stage = int.from_bytes(blocco[16:18], byteorder="big")
                punti = int.from_bytes(blocco[18:20], byteorder="big")
                records.append({"nomi": nomi, "stage": stage, "punti": punti})
        return records


    @staticmethod
    def mostra():
        dati = HallOfFame.leggi_classifica()
        print("\nx=x=x=x= Hall of fame =x=x=x=x")
        if not dati:
            print("Nessun record presente, gioca una partita!")
        else:
            for i, r in enumerate(dati, start=1):
                print(f"{i}) {r['nomi']} - Stage {r['stage']} - {r['punti']} punti")
        print("x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x\n")