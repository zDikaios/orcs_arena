from typing import List

def intervallonumerico(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def show_bar(nome: str, valore_attuale: int, valore_massimo: int):
    if valore_massimo <= 0:
        valore_massimo = 1
    larghezza_barra = 20
    parte_piena = int((valore_attuale / valore_massimo) * larghezza_barra)
    parte_piena = max(0, min(larghezza_barra, parte_piena))
    bar = "[" + ("X" * parte_piena) + ("-" * (larghezza_barra - parte_piena)) + "]"
    print(f"{nome} {bar} {valore_attuale}/{valore_massimo}")


def richiestanumeroscelta(prompt: str, valid: List[int]) -> int:
    while True:
        try:
            v = int(input(prompt))
            if v in valid:
                return v
        except ValueError:
            pass
        print(f"Scelta non valida. Opzioni: {valid}")


def si_o_no(prompt: str) -> bool:
    while True:
        s = input(prompt).lower()
        if s in ("s", "si", "y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Rispondi con s/n.")

titletext2 = r""" 
||====||====||   .----. .----.  .---.  .----.     .--.  .----. .----..-. .-.  .--.     ||====||====||
||====||====||  /  {}  \| {}  }/  ___}{ {__      / {} \ | {}  }| {_  |  `| | / {} \    ||====||====||
||====||====||  \      /| .-. \\     }.-._} }   /  /\  \| .-. \| {__ | |\  |/  /\  \   ||====||====||
||====||====||   `----' `-' `-' `---' `----'    `-'  `-'`-' `-'`----'`-' `-'`-'  `-'   ||====||====||"""

titletext = r"""                                                          
|-------|   _____ _____ _____ _____    _____ _____ _____ _____ _____   |-------|  
|-------|  |     | __  |     |   __|  |  _  | __  |   __|   | |  _  |  |-------|  
|-------|  |  |  |    -|   --|__   |  |     |    -|   __| | | |     |  |-------|  
|-------|  |_____|__|__|_____|_____|  |__|__|__|__|_____|_|___|__|__|  |-------|  """
ee = r"""
  __________
 / ___  ___ \
/ / @ \/ @ \ \
\ \___/\___/ /\  Hai trovato un gufetto magico!
 \____\/____/||    
 /     /\\\\\//   
 |     |\\\\\\    
  \      \\\\\\  
   \______/\\\\  
    _||_||_"""
ee2 = r"""
     _    _          _____     _______ _____   ______      __  _______ ____      _    _ _   _     ______           _____ _______ ______ _____      ______ _____  _____   _ 
    | |  | |   /\   |_   _|   |__   __|  __ \ / __ \ \    / /\|__   __/ __ \    | |  | | \ | |   |  ____|   /\    / ____|__   __|  ____|  __ \    |  ____/ ____|/ ____| | |
    | |__| |  /  \    | |        | |  | |__) | |  | \ \  / /  \  | | | |  | |   | |  | |  \| |   | |__     /  \  | (___    | |  | |__  | |__) |   | |__ | |  __| |  __  | |
    |  __  | / /\ \   | |        | |  |  _  /| |  | |\ \/ / /\ \ | | | |  | |   | |  | | . ` |   |  __|   / /\ \  \___ \   | |  |  __| |  _  /    |  __|| | |_ | | |_ | | |
    | |  | |/ ____ \ _| |_       | |  | | \ \| |__| | \  / ____ \| | | |__| |   | |__| | |\  |   | |____ / ____ \ ____) |  | |  | |____| | \ \    | |___| |__| | |__| | |_|
    |_|  |_/_/    \_\_____|      |_|  |_|  \_\\____/   \/_/    \_\_|  \____/     \____/|_| \_|   |______/_/    \_\_____/   |_|  |______|_|  \_\   |______\_____|\_____| (_)"""