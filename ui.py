import os
import sys
import random
import pygame
import ctypes
from typing import List, Optional, Tuple

from items import descrizione_oggetti
from characters import personaggi

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 680

COLOR_BG = (20, 22, 28)
COLOR_PANEL = (32, 36, 46)
COLOR_WHITE = (240, 240, 240)
COLOR_GRAY = (110, 115, 125)
COLOR_GREEN = (46, 204, 113)
COLOR_RED = (231, 76, 60)
COLOR_BLUE = (52, 152, 219)
COLOR_GOLD = (241, 196, 15)
COLOR_PURPLE = (155, 89, 182)
COLOR_ORANGE = (230, 126, 34)
COLOR_BTN = (46, 58, 74)
COLOR_BTN_HOVER = (65, 102, 145)
COLOR_BTN_ACTIVE = (180, 140, 20)

KEY_TO_NUM = {
    pygame.K_0: 0, pygame.K_KP0: 0,
    pygame.K_1: 1, pygame.K_KP1: 1,
    pygame.K_2: 2, pygame.K_KP2: 2,
    pygame.K_3: 3, pygame.K_KP3: 3,
    pygame.K_4: 4, pygame.K_KP4: 4,
    pygame.K_5: 5, pygame.K_KP5: 5,
    pygame.K_6: 6, pygame.K_KP6: 6,
    pygame.K_7: 7, pygame.K_KP7: 7,
    pygame.K_8: 8, pygame.K_KP8: 8,
    pygame.K_9: 9, pygame.K_KP9: 9,
}


class GuiButton:
    """Pulsante interattivo renderizzato a schermo (supporta testo o texture PNG)."""

    def __init__(self, rect: Tuple[int, int, int, int], text: str, action_val,
                 active: bool = False, image: Optional[pygame.Surface] = None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action_val = action_val
        self.active = active
        self.image = image
        self.hovered = False  # Tiene traccia dello stato per l'effetto sonoro

    def check_hover(self, mouse_pos: Tuple[int, int], ui_manager=None) -> bool:
        is_hover = self.rect.collidepoint(mouse_pos)
        # Riproduce il suono solo al momento dell'ingresso del puntatore
        if is_hover and not self.hovered:
            if ui_manager:
                ui_manager.play_sound("hover")
        self.hovered = is_hover
        return is_hover

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        if self.image:
            img_to_draw = self.image.copy()
            if is_hover or self.active:
                # Scurisce la texture applicando un moltiplicatore d'ombra
                dark_overlay = pygame.Surface(img_to_draw.get_size(), flags=pygame.SRCALPHA)
                dark_overlay.fill((160, 160, 160, 255))
                img_to_draw.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(img_to_draw, self.rect)
        else:
            if self.active:
                color = COLOR_BTN_ACTIVE
            elif is_hover:
                color = COLOR_BTN_HOVER
            else:
                color = COLOR_BTN

            pygame.draw.rect(surface, color, self.rect, border_radius=6)
            pygame.draw.rect(surface, COLOR_WHITE, self.rect, width=2, border_radius=6)

            txt_surf = font.render(self.text, True, COLOR_WHITE)
            txt_rect = txt_surf.get_rect(center=self.rect.center)
            surface.blit(txt_surf, txt_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class UIManager:
    def __init__(self):
        # 1. Individua il percorso della cartella 'assets'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if os.path.exists(os.path.join(parent_dir, "assets")):
            assets_dir = os.path.join(parent_dir, "assets")
        elif os.path.exists(os.path.join(os.getcwd(), "assets")):
            assets_dir = os.path.join(os.getcwd(), "assets")
        else:
            assets_dir = os.path.join(current_dir, "assets")

        icon_path = os.path.join(assets_dir, "icon.png")

        # 2. SEPARE IL PROCESSO DA PYTHON.EXE (PRIMA DI CREARE LA FINESTRA!)
        if sys.platform == "win32":
            try:
                myappid = "lum.orcsarena.game.5.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                print(f"[ICON] Errore AppUserModelID: {e}")

        # 3. IMPOSTA L'ICONA DI PYGAME PRIMA DI SET_MODE
        if os.path.exists(icon_path):
            try:
                icon_surf = pygame.image.load(icon_path)
                pygame.display.set_icon(icon_surf)
            except Exception as e:
                print(f"[ICON] Errore caricamento icona: {e}")

        # 4. CREA LA FINESTRA DEL GIOCO
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Orcs Arena 5.0")

        # 5. FORZA L'ICONA DIRETTAMENTE SULL'HWND DELLA FINESTRA DI WINDOWS
        if sys.platform == "win32" and os.path.exists(icon_path):
            try:
                # Recupera l'handle nativo della finestra Pygame (SDL)
                hwnd = pygame.display.get_wm_info().get("window")
                if hwnd:
                    # Carica l'immagine a livello di sistema Windows
                    IMAGE_ICON = 1
                    LR_LOADFROMFILE = 0x00000010
                    WM_SETICON = 0x0080
                    ICON_SMALL = 0
                    ICON_BIG = 1

                    # Carica l'icona e invia il messaggio di cambio icona a Windows
                    hicon = ctypes.windll.user32.LoadImageW(
                        None, os.path.abspath(icon_path), IMAGE_ICON, 0, 0, LR_LOADFROMFILE
                    )
                    if hicon:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
                        print("[ICON] Icona agganciata alla barra delle applicazioni di Windows.")
            except Exception as e:
                print(f"[ICON] Forzatura HWND fallita: {e}")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_big = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 32, bold=True)

        # --- SUONI ---
        self.sounds = {"slash": [], "heal": [], "hover": None, "select": None}
        for i in range(1, 5):
            p = os.path.join(assets_dir, f"slash{i}.wav")
            if os.path.exists(p):
                try:
                    self.sounds["slash"].append(pygame.mixer.Sound(p))
                except Exception:
                    pass

        if not self.sounds["slash"]:
            p = os.path.join(assets_dir, "slash.wav")
            if os.path.exists(p):
                try:
                    self.sounds["slash"].append(pygame.mixer.Sound(p))
                except Exception:
                    pass

        for s_key, s_file in [("heal", "heal.wav"), ("hover", "hover.wav"), ("select", "select.wav")]:
            p = os.path.join(assets_dir, s_file)
            if os.path.exists(p):
                try:
                    snd = pygame.mixer.Sound(p)
                    if s_key == "heal":
                        self.sounds["heal"].append(snd)
                    else:
                        self.sounds[s_key] = snd
                except Exception:
                    pass

        # --- SFONDI ---
        self.backgrounds = {}
        for key, fname in [("menu", "bg_menu.png"), ("combat", "bg_combat.png"), ("hof", "bg_hof.png")]:
            p = os.path.join(assets_dir, fname)
            if not os.path.exists(p):
                p_jpg = os.path.join(assets_dir, fname.replace(".png", ".jpg"))
                if os.path.exists(p_jpg):
                    p = p_jpg
            if os.path.exists(p):
                try:
                    img = pygame.image.load(p).convert()
                    self.backgrounds[key] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                except Exception:
                    self.backgrounds[key] = None

        # --- SPRITE ---
        self.sprites = {}
        for key, fname in [("warrior", "warrior.png"), ("mage", "mage.png"), ("cleric", "cleric.png"),
                           ("enemy", "enemy.png")]:
            p = os.path.join(assets_dir, fname)
            if os.path.exists(p):
                try:
                    img = pygame.image.load(p).convert_alpha()
                    size = (160, 160) if key == "enemy" else (135, 135)
                    self.sprites[key] = pygame.transform.scale(img, size)
                except Exception:
                    self.sprites[key] = None

        # Texture pulsante Torna Indietro
        self.goback_texture = None
        p_goback = os.path.join(assets_dir, "goback.png")
        if os.path.exists(p_goback):
            try:
                img = pygame.image.load(p_goback).convert_alpha()
                self.goback_texture = pygame.transform.scale(img, (200, 50))
            except Exception:
                self.goback_texture = None

        # --- TEXTURE PULSANTI MENU (300 x 55 px) ---
        self.menu_btn_textures = {}
        btn_files = {
            1: "newgame_button.png",
            2: "load_button.png",
            3: "halloffame_button.png",
            4: "exit.png"
        }
        for act_id, fname in btn_files.items():
            p = os.path.join(assets_dir, fname)
            if os.path.exists(p):
                try:
                    t_img = pygame.image.load(p).convert_alpha()
                    self.menu_btn_textures[act_id] = pygame.transform.scale(t_img, (300, 55))
                except Exception:
                    self.menu_btn_textures[act_id] = None
            else:
                self.menu_btn_textures[act_id] = None

    def play_sound(self, sound_key: str):
        if sound_key in ("attack", "slash"):
            if self.sounds.get("slash"):
                random.choice(self.sounds["slash"]).play()
        elif sound_key == "heal":
            if self.sounds.get("heal"):
                random.choice(self.sounds["heal"]).play()
        elif sound_key in ("hover", "select"):
            if self.sounds.get(sound_key):
                self.sounds[sound_key].play()

    def draw_background(self, bg_key: str):
        bg = self.backgrounds.get(bg_key)
        if bg:
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill(COLOR_BG)

    def get_character_sprite_key(self, char_obj: personaggi) -> str:
        real = char_obj
        while hasattr(real, "target"):
            real = real.target
        c_name = real.__class__.__name__.lower()
        if "warrior" in c_name or "guerriero" in c_name:
            return "warrior"
        elif "mage" in c_name or "mago" in c_name:
            return "mage"
        elif "cleric" in c_name or "chierico" in c_name:
            return "cleric"
        return "warrior"

    def draw_bar(self, x: int, y: int, w: int, h: int, cur: int, mx: int, color: Tuple[int, int, int], label: str):
        ratio = max(0.0, min(1.0, cur / max(1, mx)))
        pygame.draw.rect(self.screen, (40, 40, 40), (x, y, w, h), border_radius=4)
        pygame.draw.rect(self.screen, color, (x, y, int(w * ratio), h), border_radius=4)
        pygame.draw.rect(self.screen, COLOR_WHITE, (x, y, w, h), width=1, border_radius=4)
        t = self.font.render(f"{label}: {cur}/{mx}", True, COLOR_WHITE)
        self.screen.blit(t, (x, y - 20))

    def render_generic_menu(self, title: str, subtitle: str, buttons: List[GuiButton],
                            lines: Optional[List[str]] = None, is_main_menu: bool = False):
        is_hof = ("HALL OF FAME" in title.upper())
        current_bg = "hof" if is_hof else "menu"
        self.draw_background(current_bg)

        # Se non è il menu principale e non è la Hall of Fame, mostra il titolo con il banner
        if not is_main_menu and not is_hof:
            title_banner = pygame.Surface((SCREEN_WIDTH, 110), pygame.SRCALPHA)
            title_banner.fill((15, 18, 24, 190))
            self.screen.blit(title_banner, (0, 10))

            t_surf = self.font_title.render(title, True, COLOR_GOLD)
            self.screen.blit(t_surf, t_surf.get_rect(center=(SCREEN_WIDTH // 2, 50)))

            if subtitle:
                sub_surf = self.font_big.render(subtitle, True, COLOR_WHITE)
                self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 95)))

        # Disegno delle righe dei record
        if lines:
            if is_hof:
                # Nessun box grigio: testi renderizzati direttamente sullo sfondo, spostati 100px a destra
                y_offset = 135
                for line in lines:
                    l_surf = self.font_big.render(line, True, COLOR_GOLD)
                    self.screen.blit(l_surf, (230, y_offset))
                    y_offset += 42
            else:
                panel_rect = pygame.Rect(100, 130, SCREEN_WIDTH - 200, 410)
                pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=8)
                pygame.draw.rect(self.screen, COLOR_WHITE, panel_rect, width=1, border_radius=8)
                y_offset = 150
                for line in lines:
                    l_surf = self.font.render(line, True, COLOR_WHITE)
                    self.screen.blit(l_surf, (130, y_offset))
                    y_offset += 34

        for b in buttons:
            b.draw(self.screen, self.font)

        pygame.display.flip()

    def wait_for_choice(self, title: str, subtitle: str, buttons: List[GuiButton],
                        lines: Optional[List[str]] = None, is_main_menu: bool = False):
        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            # Controllo hover per ogni bottone
            for b in buttons:
                b.check_hover(mouse_pos, self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for b in buttons:
                    if b.is_clicked(event):
                        self.play_sound("select")
                        return b.action_val

                if event.type == pygame.KEYDOWN:
                    if event.key in KEY_TO_NUM:
                        num = KEY_TO_NUM[event.key]
                        for b in buttons:
                            if b.action_val == num:
                                self.play_sound("select")
                                return b.action_val
                        if 1 <= num <= len(buttons):
                            self.play_sound("select")
                            return buttons[num - 1].action_val

                    if event.key in (pygame.K_RETURN, pygame.K_SPACE) and len(buttons) == 1:
                        self.play_sound("select")
                        return buttons[0].action_val

            self.render_generic_menu(title, subtitle, buttons, lines, is_main_menu=is_main_menu)

    def text_input_dialog(self, prompt: str, default_val: str) -> str:
        input_text = ""
        box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 270, 400, 50)
        confirm_btn = GuiButton((SCREEN_WIDTH // 2 - 90, 360, 180, 46), "Conferma", True)

        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            confirm_btn.check_hover(mouse_pos, self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.play_sound("select")
                        return input_text.strip() or default_val
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 16 and event.unicode.isprintable():
                        input_text += event.unicode
                if confirm_btn.is_clicked(event):
                    self.play_sound("select")
                    return input_text.strip() or default_val

            self.draw_background("menu")

            banner = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
            banner.fill((15, 18, 24, 200))
            self.screen.blit(banner, (0, 160))

            p_surf = self.font_big.render(prompt, True, COLOR_GOLD)
            self.screen.blit(p_surf, p_surf.get_rect(center=(SCREEN_WIDTH // 2, 200)))

            pygame.draw.rect(self.screen, COLOR_PANEL, box, border_radius=6)
            pygame.draw.rect(self.screen, COLOR_WHITE, box, width=2, border_radius=6)

            display_txt = input_text if input_text else f"({default_val})"
            txt_surf = self.font_big.render(display_txt, True, COLOR_WHITE if input_text else COLOR_GRAY)
            self.screen.blit(txt_surf, (box.x + 15, box.y + 12))

            confirm_btn.draw(self.screen, self.font)
            pygame.display.flip()

    def render_battle(self, players: list, enemy, current_player, message: str,
                      buttons: List[GuiButton], sub_buttons: Optional[List[GuiButton]] = None,
                      sub_title: str = "", font_btn: Optional[pygame.font.Font] = None):
        active_font = font_btn if font_btn else self.font
        self.draw_background("combat")

        # --- RENDERING GIOCATORI: NOME E BARRE IN ALTO, SPRITE IN BASSO ---
        for i, p in enumerate(players):
            px = 80 + (i * 240)

            # 1. Nome e Livello (in alto)
            p_title = f"{p.name} (Lv {p.level})"
            txt_color = COLOR_GOLD if p == current_player else COLOR_WHITE
            lbl_surf = self.font.render(p_title, True, txt_color)

            # Badge semitrasparente dietro al nome
            bg_tag = pygame.Rect(px - 5, 48, lbl_surf.get_width() + 10, lbl_surf.get_height() + 4)
            pygame.draw.rect(self.screen, (20, 22, 28, 180), bg_tag, border_radius=4)
            self.screen.blit(lbl_surf, (px, 50))

            # 2. Barre di stato subito sotto al nome
            self.draw_bar(px, 85, 170, 14, p.hp, p.max_hp, COLOR_GREEN, "HP")
            self.draw_bar(px, 125, 170, 11, p.valore_risorsa(), p.max_risorsa(), COLOR_GOLD,
                          p.nome_risorsa().strip())

            # 3. Sprite del personaggio posizionato sotto le barre
            sp_key = self.get_character_sprite_key(p)
            sprite = self.sprites.get(sp_key)
            sprite_y = 200

            if sprite:
                self.screen.blit(sprite, (px+50, sprite_y))
            else:
                fallback_colors = {"warrior": COLOR_ORANGE, "mage": COLOR_BLUE, "cleric": COLOR_PURPLE}
                col = fallback_colors.get(sp_key, COLOR_BLUE)
                pygame.draw.rect(self.screen, col, (px, sprite_y, 135, 135), border_radius=8)

        # --- RENDERING BOSS NEMICO (allineato specularmente: Nome/Barra sopra, Sprite sotto) ---
        ex = 860
        e_title_surf = self.font_big.render(f"{enemy.name} (Lv {enemy.level})", True, COLOR_RED)
        bg_etag = pygame.Rect(ex - 5, 48, e_title_surf.get_width() + 10, e_title_surf.get_height() + 4)
        pygame.draw.rect(self.screen, (20, 22, 28, 180), bg_etag, border_radius=4)
        self.screen.blit(e_title_surf, (ex, 50))

        self.draw_bar(ex, 95, 200, 15, enemy.hp, enemy.max_hp, COLOR_RED, "Boss HP")

        e_sprite = self.sprites.get("enemy")
        e_sprite_y = 190
        if e_sprite:
            self.screen.blit(e_sprite, (ex, e_sprite_y))
        else:
            pygame.draw.rect(self.screen, COLOR_RED, (ex, e_sprite_y, 160, 160), border_radius=8)

        # --- PANNELLO INFERIORE COMANDI E LOG ---
        panel = pygame.Rect(40, 360, SCREEN_WIDTH - 80, 290)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_WHITE, panel, width=1, border_radius=10)

        self.screen.blit(self.font.render(message[:140], True, COLOR_WHITE), (60, 380))

        for btn in buttons:
            btn.draw(self.screen, active_font)

        if sub_buttons:
            sub_panel = pygame.Rect(55, 495, SCREEN_WIDTH - 110, 140)
            pygame.draw.rect(self.screen, (22, 26, 34), sub_panel, border_radius=6)
            pygame.draw.rect(self.screen, COLOR_GOLD, sub_panel, width=1, border_radius=6)

            if sub_title:
                lbl = self.font_small.render(sub_title, True, COLOR_GOLD)
                self.screen.blit(lbl, (70, 503))

            for s_btn in sub_buttons:
                s_btn.draw(self.screen, self.font_small)

        pygame.display.flip()

    def get_battle_action(self, players: list, enemy, current_player, message: str, inventory: List[str]):
        pg_effettivo = getattr(current_player, "target", current_player)
        nome_azione = getattr(pg_effettivo, "nome_seconda_azione", "Cura")

        sp_key = self.get_character_sprite_key(current_player)
        is_warrior = (sp_key == "warrior")

        sub_mode = None
        prev_sub_mode = None
        inv_page = 0
        prev_inv_page = 0
        ITEMS_PER_PAGE = 4

        font_btn = pygame.font.SysFont("Arial", 14, bold=True)

        btn_w = 180
        btn_h = 46
        spacing = 16
        start_x = 78
        btn_y = 425

        # 1. ISTANZIAMO I PULSANTI PRINCIPALI UNA SOLA VOLTA FUORI DAL LOOP
        buttons = [
            GuiButton((start_x, btn_y, btn_w, btn_h), "1) Attacca", 1),
            GuiButton((start_x + (btn_w + spacing), btn_y, btn_w, btn_h), f"2) {nome_azione}", 2),
            GuiButton((start_x + (btn_w + spacing) * 2, btn_y, btn_w, btn_h), "3) Oggetti", 3),
            GuiButton((start_x + (btn_w + spacing) * 3, btn_y, btn_w, btn_h), "4) Salva ed Esci", 4),
            GuiButton((start_x + (btn_w + spacing) * 4, btn_y, btn_w, btn_h), "5) Abbandona", 5),
        ]

        sub_buttons = []
        sub_title = ""

        def rebuild_sub_buttons():
            nonlocal sub_buttons, sub_title
            sub_buttons = []
            if sub_mode == "power":
                sub_title = f"Potenza Colpo ({current_player.name}) - [Premi 1, 2, 3 o ESC per annullare]:"
                sub_buttons = [
                    GuiButton((78, 540, 160, 42), "1) Leggero (ST 2)", ("power", 1)),
                    GuiButton((250, 540, 160, 42), "2) Medio (ST 4)", ("power", 2)),
                    GuiButton((422, 540, 160, 42), "3) Forte (ST 6)", ("power", 3)),
                    GuiButton((910, 540, 130, 42), "0) Annulla", ("cancel", None)),
                ]
            elif sub_mode == "items":
                total_items = len(inventory)
                start_idx = inv_page * ITEMS_PER_PAGE
                page_items = inventory[start_idx:start_idx + ITEMS_PER_PAGE]

                if not inventory:
                    sub_title = "Zaino del Party (Vuoto!) - [Premi 0 o ESC per chiudere]:"
                    sub_buttons = [GuiButton((910, 540, 130, 42), "0) Chiudi", ("cancel", None))]
                else:
                    sub_title = "Zaino del Party - [Premi 1-4 per usare, 0 o ESC per annullare]:"
                    for idx_item, item_name in enumerate(page_items):
                        real_idx = start_idx + idx_item
                        bx = 78 + (idx_item % 2) * 410
                        by = 530 + (idx_item // 2) * 46
                        desc = descrizione_oggetti(item_name)
                        label = f"{idx_item + 1}) {item_name} ({desc})"[:44]
                        sub_buttons.append(GuiButton((bx, by, 395, 40), label, ("item", real_idx)))

                    if inv_page > 0:
                        sub_buttons.append(GuiButton((910, 530, 130, 30), "< Prec.", ("page", inv_page - 1)))
                    if start_idx + ITEMS_PER_PAGE < total_items:
                        sub_buttons.append(GuiButton((910, 565, 130, 30), "Succ. >", ("page", inv_page + 1)))

                    sub_buttons.append(GuiButton((910, 600, 130, 30), "0) Annulla", ("cancel", None)))

        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            # Rigenera i sotto-pulsanti solo se cambia la modalità o la pagina
            if sub_mode != prev_sub_mode or inv_page != prev_inv_page:
                buttons[0].active = (sub_mode == "power")
                buttons[2].active = (sub_mode == "items")
                rebuild_sub_buttons()
                prev_sub_mode = sub_mode
                prev_inv_page = inv_page

            # Controllo hover preservando lo stato per non ripetere il suono
            for b in buttons:
                b.check_hover(mouse_pos, self)
            for sb in sub_buttons:
                sb.check_hover(mouse_pos, self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Click sotto-pulsanti
                if sub_buttons:
                    for s_btn in sub_buttons:
                        if s_btn.is_clicked(event):
                            cmd_type, cmd_val = s_btn.action_val
                            if cmd_type == "cancel":
                                sub_mode = None
                            elif cmd_type == "page":
                                inv_page = cmd_val
                            elif cmd_type == "power":
                                self.play_sound("slash")
                                return 1, cmd_val, None
                            elif cmd_type == "item":
                                chosen_item = inventory.pop(cmd_val)
                                return 3, None, chosen_item

                # Click pulsanti principali
                for b in buttons:
                    if b.is_clicked(event):
                        if b.action_val == 1:
                            if is_warrior:
                                sub_mode = "power" if sub_mode != "power" else None
                            else:
                                self.play_sound("slash")
                                return 1, None, None
                        elif b.action_val == 2:
                            self.play_sound("heal")
                            return 2, None, None
                        elif b.action_val == 3:
                            sub_mode = "items" if sub_mode != "items" else None
                            inv_page = 0
                        else:
                            return b.action_val, None, None

                # Input da tastiera
                if event.type == pygame.KEYDOWN:
                    num = KEY_TO_NUM.get(event.key, None)

                    if event.key == pygame.K_ESCAPE and sub_mode is not None:
                        sub_mode = None
                        continue

                    if sub_mode == "power":
                        if num in (1, 2, 3):
                            self.play_sound("slash")
                            return 1, num, None
                        elif num == 0:
                            sub_mode = None

                    elif sub_mode == "items":
                        if num == 0:
                            sub_mode = None
                        elif num in (1, 2, 3, 4):
                            item_offset = num - 1
                            total_items = len(inventory)
                            start_idx = inv_page * ITEMS_PER_PAGE
                            chosen_real_idx = start_idx + item_offset
                            if chosen_real_idx < total_items:
                                chosen_item = inventory.pop(chosen_real_idx)
                                return 3, None, chosen_item

                    else:
                        if num == 1:
                            if is_warrior:
                                sub_mode = "power"
                            else:
                                self.play_sound("slash")
                                return 1, None, None
                        elif num == 2:
                            self.play_sound("heal")
                            return 2, None, None
                        elif num == 3:
                            sub_mode = "items"
                            inv_page = 0
                        elif num == 4:
                            return 4, None, None
                        elif num == 5:
                            return 5, None, None

            self.render_battle(players, enemy, current_player, message, buttons,
                               sub_buttons if sub_buttons else None, sub_title, font_btn=font_btn)