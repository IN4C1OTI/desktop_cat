"""
Desktop Cat - Green Edition
"""

import tkinter as tk
import random
import os
import sys
import math
import time
import ctypes
import webbrowser

try:
    from PIL import Image, ImageTk, ImageChops
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Audio: tenta pygame primeiro, cai para MCI do Windows (sem dependencias extras)
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
    SOUND_BACKEND = "pygame"
except Exception:
    SOUND_AVAILABLE = True   # MCI sempre disponivel no Windows
    SOUND_BACKEND = "mci"

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DIST_DIR = os.path.join(BASE_DIR, "dist")

GREEN_NEON  = "#00FF41"
GREEN_MID   = "#00CC33"
GREEN_DARK  = "#003300"
DARK        = "#000A00"
GLITCH_RED  = "#FF0044"
GLITCH_CYAN = "#00FFFF"
TRANSP      = "#010203"

MESSAGES = [
    "MIAU!",
    "MIAR, Gatinho gaucho.",
    "Olha o gatinho passando.",
    "Eu apertei algo... boa sorte ai!",
    "Esse mouse sera meu!",
    "Deletei o sistema. Brincadeira... ou nao.",
    "Cade o botao de comida?",
    "Atencao: 110% de preguica ativada.",
    "Seu foco foi pro ralo?!",
    "Acho que quebrei alguma coisa...",
    "CTRL+ALT+MIAU!",
    "Oi, eu existo.",
    "Nao me ignora.",
    "Pspspsps...",
    "Olha so que gatinho bonito.",
    "Tava dormindo, mas acordei.",
    "Ronron...",
    "Miau? MIAU.",
    "Voce ta me vendo, ne?",
    "Fui eu. Nao foi.",
    "Tô de olho em voce.",
    "Precisa de ajuda? Nao vou dar.",
    "Ja salvou o arquivo? Perguntando por nada...",
    "Aquele arquivo era importante?",
    "Sete vidas. Usei seis.",
    "Nao fui eu que fechei. Juro.",
    "O teclado tem gosto de atum?",
    "Passei por cima do Wi-Fi. De nada.",
    "Hora do cafe. Pra mim, nao pra voce.",
    "Dormir e minha religiao.",
    "Por que voce ta acordado? Vai dormir.",
    "Vim verificar se voce ainda existe.",
    "Fiz nada. Prometo. Talvez.",
    "Bom, isso foi interessante.",
    "Posso sentar no teclado? Vou sentar.",
    "Acho que derrubei algo. Nao sei o que.",
    "Sistema operando em modo gatinho.",
    "Nao clique nisso... tarde demais.",
    "Vim so dar uma olhada. Mentira.",
    # Referencias a filmes
    "Eu sou seu pai. Miau.",
    "Voce nao pode lidar com a verdade! (mas eu posso)",
    "Que a Forca esteja com voce. Ou nao.",
    "Houston, temos um gatinho.",
    "Por que tao serio? Vou sentar no seu teclado.",
    "Nao e um sonho. Eu sou real. Infelizmente.",
    "Faca uma oferta que eu nao possa recusar... tipo atum.",
    "Sera que esse e o melhor que voce tem? Triste.",
    "Voce nao passa! (do meu territorio)",
    "Com grandes poderes vem grandes responsabilidades de me alimentar.",
    "E.T. vai pra casa. Eu fico aqui.",
    "Voce vai precisar de um barco maior. Pra escapar de mim.",
    "Nao me faca usar meu segundo par de garras.",
    "Hakuna Matata. Mas voce ainda vai me dar comida.",
    "Eu vejo pessoas mortas... que nao me deram atum.",
    "Minha vida por... nao, guarda isso. Nao vou me sacrificar.",
    "Hasta la vista, teclado.",
    "Eles vivem entre nos. Eu sou um deles.",
    "Eu estou pronto! (disse o gato, ignorando tudo)",
    "Nao e pessoal. E negocio. O negocio e atum.",
    "Voce nao pode me ver. Eu sou o mestre do stealth.",
    "Abra os pods, HAL. Digo, a latinha.",
    "Nao olhe pra cima. Olhe pra mim.",
    "Eu voltarei. Ja estou aqui, na verdade.",
    "A vida e como uma caixa de chocolates... prefiro atum.",
]

GLITCH_CHARS = list("##%%&&@@$$!!??01ABCDEF::::////||||")

def random_glitch_text(length=12):
    return "".join(random.choices(GLITCH_CHARS, k=length))


# ============================================================
#  SPRITES
# ============================================================
def load_sprites():
    frames = []
    for i in range(1, 17):
        wd2  = os.path.join(DIST_DIR, f"cat{i}_wd2.png")
        orig = os.path.join(DIST_DIR, f"cat{i}.png")
        path = wd2 if os.path.exists(wd2) else orig
        if not os.path.exists(path) or not PIL_AVAILABLE:
            continue
        img = Image.open(path).convert("RGBA")
        half = (img.width // 2, img.height // 2)
        img = img.resize(half, Image.NEAREST)
        frames.append(img)
    return frames


def make_glitch_variant(img):
    if not PIL_AVAILABLE:
        return img
    w, h = img.size
    out = img.copy()
    r, g, b, a = img.split()
    r_shifted = ImageChops.offset(r, random.randint(3, 7), 0)
    aberrated = Image.merge("RGBA", (r_shifted, g, b, a))
    for _ in range(random.randint(2, 6)):
        row = random.randint(0, h - 1)
        dx  = random.randint(-8, 8)
        row_px = [aberrated.getpixel((x, row)) for x in range(w)]
        for x in range(w):
            out.putpixel((x, row), row_px[(x - dx) % w])
    return out


def make_inverted_sprite(img):
    if not PIL_AVAILABLE:
        return img
    r, g, b, a = img.split()
    return Image.merge("RGBA", (
        ImageChops.invert(r),
        ImageChops.invert(g),
        ImageChops.invert(b),
        a
    ))


# ============================================================
#  SHADOW  — oval escura sob o gato
# ============================================================
class Shadow:
    def __init__(self, master, sprite_w):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", False)
        self.root.attributes("-alpha", 0.35)
        self.root.configure(bg="black")
        self.root.attributes("-transparentcolor", TRANSP)
        w = sprite_w
        self.canvas = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                                width=w, height=10)
        self.canvas.pack()
        self.canvas.create_oval(w // 6, 1, w - w // 6, 9,
                                fill="#002200", outline="")
        self.root.geometry(f"{w}x10+0+0")

    def update(self, x, y, sprite_h):
        if self.root.winfo_exists():
            self.root.geometry(f"+{int(x)}+{int(y + sprite_h - 4)}")

    def destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  ZZZ BUBBLE — balao de sono
# ============================================================
class ZzzBubble:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSP)
        self.root.attributes("-transparentcolor", TRANSP)
        self.canvas = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                                width=60, height=60)
        self.canvas.pack()
        self.root.geometry("+0+0")
        self._alive = True
        self._items = []
        self._step  = 0
        self._tick()

    def _tick(self):
        if not self._alive or not self.root.winfo_exists():
            return
        sizes = [13, 10, 7]
        sz = sizes[self._step % 3]
        xi = 8 + (self._step % 3) * 12
        yi = 48 - (self._step % 3) * 14
        item = self.canvas.create_text(xi, yi, text="z", fill=GREEN_NEON,
                                       font=("Courier New", sz, "bold"))
        self._items.append((item, 0))
        aged = []
        for it, age in self._items:
            if age >= 8:
                self.canvas.delete(it)
            else:
                aged.append((it, age + 1))
        self._items = aged
        self._step = (self._step + 1) % 9
        self.root.after(350, self._tick)

    def update(self, x, y, sprite_w):
        if self.root.winfo_exists():
            self.root.geometry(f"+{int(x + sprite_w // 2)}+{int(y - 30)}")

    def destroy(self):
        self._alive = False
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  GHOST CAT — copia fantasma durante glitch
# ============================================================
class GhostCat:
    def __init__(self, master, x, y, sprites, sw, sh, sprite_w, sprite_h):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.28)
        self.root.configure(bg=TRANSP)
        self.root.attributes("-transparentcolor", TRANSP)
        c = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                      width=sprite_w, height=sprite_h)
        c.pack()
        img = random.choice(sprites)
        self._ref = img
        c.create_image(0, 0, anchor="nw", image=img)
        ox = x + random.randint(-100, 100)
        oy = y + random.randint(-60, 60)
        ox = max(0, min(sw - sprite_w, ox))
        oy = max(0, min(sh - sprite_h, oy))
        self.root.geometry(f"+{ox}+{oy}")
        self.root.after(random.randint(1200, 2800), self._destroy)

    def _destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  GLITCH FLASH
# ============================================================
class GlitchFlash:
    def __init__(self, master, sw, sh):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.12)
        color = random.choice([GLITCH_RED, GLITCH_CYAN, GREEN_NEON])
        self.root.configure(bg=color)
        c = tk.Canvas(self.root, bg=color, highlightthickness=0, width=sw, height=sh)
        c.pack()
        for y in range(0, sh, 4):
            c.create_line(0, y, sw, y, fill="black", width=1)
        for _ in range(random.randint(4, 10)):
            gy  = random.randint(0, sh)
            gh  = random.randint(2, 24)
            col = random.choice([GLITCH_RED, GLITCH_CYAN, GREEN_NEON, "#FFFFFF"])
            c.create_rectangle(0, gy, sw, gy + gh, fill=col, outline="")
        self.root.geometry(f"{sw}x{sh}+0+0")
        self.root.after(random.randint(800, 2500), self._destroy)

    def _destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  SPEECH BUBBLE
# ============================================================
class SpeechBubble:
    def __init__(self, master, x, y, message):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSP)
        self.root.attributes("-transparentcolor", TRANSP)
        self.canvas = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                                width=300, height=90)
        self.canvas.pack()
        self._msg = message
        self._draw(message)
        self.root.geometry(f"+{x}+{y}")
        self._glitch_count = 0
        self._schedule_glitch()
        self.root.after(4200, self._destroy)

    def _draw(self, text, color=GREEN_NEON):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(8, 8, 292, 72, fill=DARK, outline=GREEN_NEON, width=2)
        c.create_text(16, 18, text="> CAT", fill=GREEN_MID,
                      font=("Courier New", 7, "bold"), anchor="w")
        c.create_line(9, 27, 291, 27, fill=GREEN_NEON, width=1)
        self._tid = c.create_text(16, 50, text=text, fill=color,
                                   font=("Courier New", 9, "bold"),
                                   anchor="w", width=268)
        c.create_polygon(18, 72, 32, 72, 25, 84, fill=DARK, outline=GREEN_NEON)

    def _schedule_glitch(self):
        if not self.root.winfo_exists():
            return
        self.root.after(random.randint(500, 1200), self._do_glitch)

    def _do_glitch(self):
        if not self.root.winfo_exists():
            return
        self._glitch_count += 1
        if self._glitch_count <= 4:
            self.canvas.itemconfig(self._tid,
                                   text=random_glitch_text(random.randint(8, 16)),
                                   fill=random.choice([GLITCH_RED, GLITCH_CYAN, GREEN_NEON]))
            self.root.after(70, self._restore)
        self._schedule_glitch()

    def _restore(self):
        if not self.root.winfo_exists():
            return
        self.canvas.itemconfig(self._tid, text=self._msg, fill=GREEN_NEON)

    def destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def _destroy(self):
        self.destroy()


# ============================================================
#  GLITCH POPUP
# ============================================================
class GlitchPopup:
    def __init__(self, master, x, y):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=DARK)
        outer = tk.Frame(self.root, bg=GREEN_NEON, bd=1)
        outer.pack()
        inner = tk.Frame(outer, bg=DARK, padx=10, pady=6)
        inner.pack(padx=1, pady=1)
        hdr = tk.Frame(inner, bg=DARK)
        hdr.pack(fill="x", pady=(0, 3))
        tk.Label(hdr, text="> CAT", fg=GREEN_NEON, bg=DARK,
                 font=("Courier New", 8, "bold")).pack(side="left")
        tk.Label(hdr, text="[ALERTA]", fg=GREEN_MID, bg=DARK,
                 font=("Courier New", 7)).pack(side="right")
        tk.Frame(inner, bg=GREEN_NEON, height=1).pack(fill="x", pady=2)
        tk.Label(inner, text=random.choice(MESSAGES), fg=GREEN_NEON, bg=DARK,
                 font=("Courier New", 9, "bold"),
                 wraplength=260, justify="left").pack(pady=4)
        pf = tk.Frame(inner, bg=DARK)
        pf.pack(fill="x")
        tk.Label(pf, text="STATUS:", fg=GREEN_MID, bg=DARK,
                 font=("Courier New", 7)).pack(side="left")
        self._bar = tk.Label(pf, text="", fg=GREEN_NEON, bg=DARK,
                             font=("Courier New", 7))
        self._bar.pack(side="left", padx=4)
        self.root.geometry(f"+{x}+{y}")
        self._progress = 0
        self._tick()
        self.root.after(random.randint(3500, 6000), self._destroy)

    def _tick(self):
        if not self.root.winfo_exists():
            return
        self._progress = min(100, self._progress + random.randint(4, 14))
        filled = self._progress // 5
        self._bar.config(text="|" * filled + "." * (20 - filled) + f" {self._progress}%")
        if self._progress < 100:
            self.root.after(110, self._tick)

    def _destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass



# ============================================================
#  SHUTDOWN WARNING — aviso falso de desligamento
# ============================================================
class ShutdownWarning:
    def __init__(self, master, on_x, on_timeout):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=DARK)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w, h = 680, 290
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Borda vermelha para dar susto
        outer = tk.Frame(self.root, bg=GLITCH_RED, bd=2)
        outer.pack(fill="both", expand=True)
        inner = tk.Frame(outer, bg=DARK, padx=30, pady=18)
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        tk.Label(inner, text="!! AVISO DO SISTEMA !!", fg=GLITCH_RED, bg=DARK,
                 font=("Courier New", 13, "bold")).pack(pady=(0, 8))

        tk.Label(inner,
                 text="Vou desligar o PC,\nse nao quiser aperte no X.",
                 fg=GREEN_NEON, bg=DARK,
                 font=("Courier New", 22, "bold"),
                 justify="center").pack(pady=6)

        self._cvar = tk.StringVar(value="Desligando em 5s...")
        tk.Label(inner, textvariable=self._cvar, fg=GLITCH_RED, bg=DARK,
                 font=("Courier New", 11, "bold")).pack(pady=4)

        tk.Button(inner, text="  X  ", fg=DARK, bg=GREEN_NEON,
                  activebackground=GREEN_MID, activeforeground=DARK,
                  font=("Courier New", 18, "bold"),
                  relief="flat", cursor="hand2", bd=0,
                  command=lambda: self._click_x(on_x)).pack(pady=8)

        self._countdown = 5
        self._alive = True
        self._on_timeout = on_timeout
        self.root.after(1000, self._tick)

    def _tick(self):
        if not self._alive or not self.root.winfo_exists():
            return
        self._countdown -= 1
        if self._countdown <= 0:
            self._alive = False
            try:
                self.root.destroy()
            except Exception:
                pass
            self._on_timeout()
            return
        self._cvar.set(f"Desligando em {self._countdown}s...")
        self.root.after(1000, self._tick)

    def _click_x(self, callback):
        self._alive = False
        try:
            self.root.destroy()
        except Exception:
            pass
        callback()


# ============================================================
#  BLACKOUT — tela preta total por 3 segundos
# ============================================================
class BlackoutScreen:
    def __init__(self, master, on_done):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}+0+0")
        self.root.after(3000, lambda: self._done(on_done))

    def _done(self, callback):
        try:
            self.root.destroy()
        except Exception:
            pass
        try:
            callback()
        except Exception:
            pass


# ============================================================
#  MEME WINDOW — meme desliza da borda e fica visivel
# ============================================================
class MemeWindow:
    """Janela que desliza da borda da tela mostrando um meme."""
    def __init__(self, master, image_path, sw, sh):
        if not PIL_AVAILABLE:
            return
        try:
            img = Image.open(image_path).convert("RGBA")
        except Exception:
            return

        # Redimensiona para no maximo 320x320 mantendo proporcao
        max_side = 320
        ratio = min(max_side / img.width, max_side / img.height, 1.0)
        nw = max(1, int(img.width * ratio))
        nh = max(1, int(img.height * ratio))
        img = img.resize((nw, nh), Image.LANCZOS)

        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=TRANSP)
        self.root.attributes("-transparentcolor", TRANSP)
        self.root.attributes("-alpha", 0.0)

        self._ref = ImageTk.PhotoImage(img)
        c = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                      width=nw, height=nh)
        c.pack()
        c.create_image(0, 0, anchor="nw", image=self._ref)

        # Escolhe borda aleatoria: top, bottom, left, right
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self._tx = random.randint(0, max(0, sw - nw))
            self._ty = 40
            self._sx, self._sy = self._tx, -nh
        elif side == "bottom":
            self._tx = random.randint(0, max(0, sw - nw))
            self._ty = sh - nh - 40
            self._sx, self._sy = self._tx, sh
        elif side == "left":
            self._tx = 40
            self._ty = random.randint(0, max(0, sh - nh))
            self._sx, self._sy = -nw, self._ty
        else:
            self._tx = sw - nw - 40
            self._ty = random.randint(0, max(0, sh - nh))
            self._sx, self._sy = sw, self._ty

        self._cx = float(self._sx)
        self._cy = float(self._sy)
        self.root.geometry(f"{nw}x{nh}+{self._sx}+{self._sy}")
        self._alive = True
        self._slide_in()

    def _slide_in(self):
        if not self._alive or not self.root.winfo_exists():
            return
        dx = self._tx - self._cx
        dy = self._ty - self._cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 3:
            self._cx, self._cy = float(self._tx), float(self._ty)
            self.root.geometry(f"+{self._tx}+{self._ty}")
            self.root.attributes("-alpha", 0.92)
            self.root.after(4500, self._slide_out)
            return
        step = min(dist, 22)
        self._cx += (dx / dist) * step
        self._cy += (dy / dist) * step
        self.root.geometry(f"+{int(self._cx)}+{int(self._cy)}")
        alpha = min(0.92, max(0.1, 1.0 - dist / 600))
        self.root.attributes("-alpha", alpha)
        self.root.after(16, self._slide_in)

    def _slide_out(self):
        if not self._alive or not self.root.winfo_exists():
            return
        dx = self._sx - self._cx
        dy = self._sy - self._cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 5:
            self._destroy()
            return
        step = min(dist, 26)
        self._cx += (dx / dist) * step
        self._cy += (dy / dist) * step
        alpha = max(0.0, min(0.92, dist / 500))
        try:
            self.root.geometry(f"+{int(self._cx)}+{int(self._cy)}")
            self.root.attributes("-alpha", alpha)
        except Exception:
            pass
        self.root.after(16, self._slide_out)

    def _destroy(self):
        self._alive = False
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  CAT CLONE — clone para jutsu das sombras
# ============================================================
class CatClone:
    """Clone semi-transparente do gato para o jutsu das sombras."""
    def __init__(self, master, x, y, sprites, sprite_w, sprite_h, alpha=0.55):
        self.root = tk.Toplevel(master)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", alpha)
        self.root.configure(bg=TRANSP)
        self.root.attributes("-transparentcolor", TRANSP)
        c = tk.Canvas(self.root, bg=TRANSP, highlightthickness=0,
                      width=sprite_w, height=sprite_h)
        c.pack()
        img = random.choice(sprites)
        self._ref = img
        c.create_image(0, 0, anchor="nw", image=img)
        self.root.geometry(f"{sprite_w}x{sprite_h}+{x}+{y}")
        self._alive = True

    def destroy(self):
        self._alive = False
        try:
            self.root.destroy()
        except Exception:
            pass


# ============================================================
#  MAIN DESKTOP CAT
# ============================================================
class DesktopCat:
    # Apenas cat2_wd2 (idx 1) e cat6_wd2 (idx 5)
    WALK_FRAMES  = [1, 5]
    IDLE_FRAMES  = list(range(8, 16))
    FRAME_DELAY  = 100
    SPEED        = 5.5
    GRAVITY      = 0.65
    BOUNCE_DAMP  = 0.52

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desktop Cat")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", TRANSP)
        self.root.configure(bg=TRANSP)
        self.root.resizable(False, False)

        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        self.raw_sprites = load_sprites()
        if not self.raw_sprites:
            print("ERRO: sprites nao encontrados em", DIST_DIR)
            self.root.destroy()
            return

        self.sprites         = [ImageTk.PhotoImage(s) for s in self.raw_sprites]
        self.sprite_w        = self.raw_sprites[0].width
        self.sprite_h        = self.raw_sprites[0].height
        self.glitch_sprites  = [ImageTk.PhotoImage(make_glitch_variant(s))
                                 for s in self.raw_sprites]
        self.inverted_sprites= [ImageTk.PhotoImage(make_inverted_sprite(s))
                                 for s in self.raw_sprites]

        # Posicao e direcao
        self.x  = float(self.sw // 2)
        self.y  = float(self.sh // 2)
        self._new_direction()

        # Estado
        # Estados: walk | idle | sleep | follow | flee | falling | edge_pause
        self.state        = "walk"
        self._active_bubble = None
        self.frame_idx    = 0
        self.glitch_mode  = False
        self.glitch_ttl   = 0
        self.idle_ttl     = 0
        self.edge_ttl     = 0
        self._gravity_vy  = 0.0
        self._zzz         = None
        self._hunt_target = None   # (x, y) do botao minimizar alvo

        # Controle de cliques rapidos para caos do mouse
        self._click_times    = []
        self._mouse_chaos    = False

        # Canvas principal
        self.canvas = tk.Canvas(self.root,
                                width=self.sprite_w, height=self.sprite_h,
                                bg=TRANSP, highlightthickness=0)
        self.canvas.pack()
        self._img_item = self.canvas.create_image(0, 0, anchor="nw",
                                                  image=self.sprites[0])

        # Auxiliares
        self.shadow = Shadow(self.root, self.sprite_w)

        # Drag
        self.canvas.bind("<Button-1>",          self._on_click)
        self.canvas.bind("<B1-Motion>",          self._on_drag)
        self.canvas.bind("<ButtonRelease-1>",    self._on_release)
        self.canvas.bind("<Button-3>",           self._on_right_click)
        self._drag_hist = []

        self.sounds = self._load_sounds()

        self._update_pos()
        self._animate()
        self._schedule_behavior()
        self._schedule_glitch_event()
        self._schedule_minimize_hunt()
        self._schedule_shutdown_prank()
        self._schedule_youtube_prank()
        self._schedule_clone_jutsu()
        self._load_memes()
        self._schedule_random_sound()
        self._schedule_random_meme()

        self.root.mainloop()

    # ── Direcao aleatoria ─────────────────────────────────────────────────────
    def _new_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.SPEED
        self.dy = math.sin(angle) * self.SPEED

    # ── Sons ──────────────────────────────────────────────────────────────────
    def _schedule_random_sound(self):
        self.root.after(30_000, self._play_random_sound)  # 30 segundos

    def _play_random_sound(self):
        self._play_sound()
        self._schedule_random_sound()


    def _load_sounds(self):
        """Retorna lista de caminhos de arquivos de audio."""
        paths = []
        if not SOUND_AVAILABLE:
            return paths
        d = os.path.join(DIST_DIR, "sounds")
        if not os.path.exists(d):
            return paths
        for f in os.listdir(d):
            if f.lower().endswith((".mp3", ".wav", ".ogg")):
                paths.append(os.path.join(d, f))
        return paths

    def _play_sound(self):
        if not SOUND_AVAILABLE or not self.sounds:
            return
        import threading
        path = random.choice(self.sounds)
        threading.Thread(target=self._play_audio, args=(path,), daemon=True).start()

    def _play_audio(self, path):
        """Toca audio usando pygame ou MCI do Windows (sem dependencias extras)."""
        try:
            if SOUND_BACKEND == "pygame":
                if path.lower().endswith(".wav"):
                    snd = pygame.mixer.Sound(path)
                    snd.set_volume(0.7)
                    snd.play()
                else:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
            else:
                # MCI — API nativa do Windows, suporta MP3/WAV sem instalacao
                mci = ctypes.windll.winmm.mciSendStringW
                alias = "desktopcat_snd"
                mci(f'close {alias}', None, 0, None)
                mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, None)
                mci(f'setaudio {alias} volume to 700', None, 0, None)
                mci(f'play {alias}', None, 0, None)
                time.sleep(5)
                mci(f'close {alias}', None, 0, None)
        except Exception:
            pass

    # ── Posicao ───────────────────────────────────────────────────────────────
    def _update_pos(self):
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.shadow.update(self.x, self.y, self.sprite_h)

    # ── Drag / launch ─────────────────────────────────────────────────────────
    def _on_click(self, e):
        self._drag_hist = [(time.time(), self.x, self.y)]
        self._drag_ex, self._drag_ey = e.x, e.y

        # Acorda se dormindo
        if self.state == "sleep":
            self._wake()

        # Detecta cliques rapidos (3+ cliques em 1.2s)
        now = time.time()
        self._click_times.append(now)
        self._click_times = [t for t in self._click_times if now - t < 1.2]
        if len(self._click_times) >= 3 and not self._mouse_chaos:
            self._start_mouse_chaos()

    def _on_drag(self, e):
        nx = self.x + e.x - self._drag_ex
        ny = self.y + e.y - self._drag_ey
        self.x = max(0, min(self.sw - self.sprite_w, nx))
        self.y = max(0, min(self.sh - self.sprite_h, ny))
        self._drag_ex, self._drag_ey = e.x, e.y
        self._drag_hist.append((time.time(), self.x, self.y))
        if len(self._drag_hist) > 6:
            self._drag_hist.pop(0)
        self.state = "idle"
        self._update_pos()

    def _on_release(self, e):
        if len(self._drag_hist) >= 2:
            t0, x0, y0 = self._drag_hist[0]
            t1, x1, y1 = self._drag_hist[-1]
            dt = max(t1 - t0, 0.016)
            scale = 0.018
            vx = (x1 - x0) / dt * scale
            vy = (y1 - y0) / dt * scale
            self.dx = max(-14, min(14, vx))
            self._gravity_vy = max(-18, min(8, vy))
        else:
            self.dx = 0
            self._gravity_vy = 0
        self.state = "falling"

    # ── Caos do mouse ─────────────────────────────────────────────────────────
    CHAOS_MESSAGES = [
        "ESSE MOUSE E MEU AGORA.",
        "Nao fica clicando em mim!",
        "Achei que era o dono do mouse?",
        "CAPTURADO. >:3",
        "Clicou demais. Consequencias.",
        "O mouse obedece a mim agora.",
        "Para de me cutucar!",
        "Voce pediu. MIAU.",
    ]

    def _start_mouse_chaos(self):
        self._mouse_chaos = True
        self._click_times = []
        # Aviso
        bx = int(self.x)
        by = max(0, int(self.y) - 100)
        self._speak(random.choice(self.CHAOS_MESSAGES))
        # Ativa glitch junto
        self.glitch_mode = True
        self.glitch_ttl  = 30
        try:
            GlitchFlash(self.root, self.sw, self.sh)
        except Exception:
            pass
        # Duracao do caos: 5-9 segundos
        duration = random.randint(5000, 9000)
        self.root.after(duration, self._stop_mouse_chaos)
        self._teleport_mouse()

    def _teleport_mouse(self):
        if not self._mouse_chaos or not self.root.winfo_exists():
            return
        # Teleporta para posicao aleatoria na tela
        tx = random.randint(50, self.sw - 50)
        ty = random.randint(50, self.sh - 50)
        try:
            ctypes.windll.user32.SetCursorPos(tx, ty)
        except Exception:
            pass
        # Intervalo aleatorio entre teleportes (80-300ms)
        self.root.after(random.randint(80, 300), self._teleport_mouse)

    def _stop_mouse_chaos(self):
        self._mouse_chaos = False
        bx = int(self.x)
        by = max(0, int(self.y) - 100)
        self._speak("Tudo bem. Pode ter o mouse de volta.")

    # ── Menu de contexto (botao direito) ──────────────────────────────────────
    def _on_right_click(self, e):
        menu = tk.Menu(self.root, tearoff=0,
                       bg=DARK, fg=GREEN_NEON,
                       activebackground=GREEN_DARK,
                       activeforeground=GREEN_NEON,
                       font=("Courier New", 9))
        menu.add_command(label=">> Dar comida",    command=self._feed)
        menu.add_command(label=">> Dormir",        command=self._force_sleep)
        menu.add_separator()
        menu.add_command(label=">> Seguir mouse",  command=lambda: self._set_mode("follow"))
        menu.add_command(label=">> Fugir do mouse",command=lambda: self._set_mode("flee"))
        menu.add_command(label=">> Modo normal",   command=lambda: self._set_mode("walk"))
        menu.add_separator()
        menu.add_command(label=">> Sair",          command=self.root.destroy)
        gx = self.root.winfo_rootx() + e.x
        gy = self.root.winfo_rooty() + e.y
        menu.tk_popup(gx, gy)

    def _feed(self):
        self._speak("Nomnom... obrigado!")
        self._play_sound()

    def _force_sleep(self):
        self._go_sleep()

    def _set_mode(self, mode):
        if self.state == "sleep":
            self._wake()
        self.state = mode
        if mode == "walk":
            self._new_direction()

    # ── Sono ──────────────────────────────────────────────────────────────────
    def _go_sleep(self):
        self.state = "sleep"
        if self._zzz is None:
            self._zzz = ZzzBubble(self.root)
        self._zzz.update(self.x, self.y, self.sprite_w)
        # Acorda sozinho depois de um tempo
        self.root.after(random.randint(8000, 18000), self._wake)

    def _wake(self):
        if self._zzz:
            self._zzz.destroy()
            self._zzz = None
        if self.state == "sleep":
            self.state = "walk"
            self._new_direction()
            self._speak("Tava dormindo, mas acordei.")

    # ── Animacao principal ────────────────────────────────────────────────────
    def _animate(self):
        if not self.root.winfo_exists():
            return

        pool = self.IDLE_FRAMES if self.state in ("idle", "sleep") else self.WALK_FRAMES
        self.frame_idx = (self.frame_idx + 1) % len(pool)
        idx = pool[self.frame_idx]

        # Escolha de sprite
        if self.glitch_mode and random.random() < 0.45:
            img = self.glitch_sprites[idx] if idx < len(self.glitch_sprites) \
                  else self.sprites[idx]
        elif self.glitch_mode and random.random() < 0.15:
            img = self.inverted_sprites[idx] if idx < len(self.inverted_sprites) \
                  else self.sprites[idx]
        else:
            img = self.sprites[idx] if idx < len(self.sprites) else self.sprites[0]

        self.canvas.itemconfig(self._img_item, image=img)

        # Movimento por estado
        if self.state == "walk":
            self._move_walk()
        elif self.state == "follow":
            self._move_follow(toward=True)
        elif self.state == "flee":
            self._move_follow(toward=False)
        elif self.state == "falling":
            self._move_falling()
        elif self.state == "hunting":
            self._move_hunting()
        elif self.state == "edge_pause":
            self.edge_ttl -= 1
            if self.edge_ttl <= 0:
                self.state = "walk"
        elif self.state == "sleep":
            if self._zzz:
                self._zzz.update(self.x, self.y, self.sprite_w)
        elif self.state == "idle":
            self.idle_ttl -= 1
            if self.idle_ttl <= 0:
                # Chance de adormecer ao fim do idle
                if random.random() < 0.25:
                    self._go_sleep()
                else:
                    self.state = "walk"
                    self._new_direction()

        self.root.after(self.FRAME_DELAY, self._animate)

    def _move_walk(self):
        jx = jy = 0
        if self.glitch_mode:
            jx = random.randint(-5, 5)
            jy = random.randint(-4, 4)
            self.glitch_ttl -= 1
            if self.glitch_ttl <= 0:
                self.glitch_mode = False

        nx = self.x + self.dx + jx
        ny = self.y + self.dy + jy

        hit_wall = False
        if nx < 0 or nx > self.sw - self.sprite_w:
            self.dx *= -1
            nx = max(0, min(self.sw - self.sprite_w, nx))
            hit_wall = True
        if ny < 0 or ny > self.sh - self.sprite_h:
            self.dy *= -1
            ny = max(0, min(self.sh - self.sprite_h, ny))
            hit_wall = True

        # Pausa na borda antes de virar
        if hit_wall and random.random() < 0.3:
            self.state    = "edge_pause"
            self.edge_ttl = random.randint(3, 7)

        self.x, self.y = nx, ny
        self._update_pos()

    def _move_follow(self, toward=True):
        mx = self.root.winfo_pointerx()
        my = self.root.winfo_pointery()
        cx = self.x + self.sprite_w / 2
        cy = self.y + self.sprite_h / 2
        ddx = mx - cx
        ddy = my - cy
        dist = math.hypot(ddx, ddy)
        if dist < 1:
            return
        speed = self.SPEED * (1 if toward else -1)
        nx = self.x + (ddx / dist) * speed
        ny = self.y + (ddy / dist) * speed
        self.x = max(0, min(self.sw - self.sprite_w, nx))
        self.y = max(0, min(self.sh - self.sprite_h, ny))
        self._update_pos()

    def _move_falling(self):
        self._gravity_vy += self.GRAVITY
        nx = self.x + self.dx
        ny = self.y + self._gravity_vy

        if nx < 0 or nx > self.sw - self.sprite_w:
            self.dx *= -0.7
            nx = max(0, min(self.sw - self.sprite_w, nx))

        floor = float(self.sh - self.sprite_h)
        if ny >= floor:
            ny = floor
            self._gravity_vy *= -self.BOUNCE_DAMP
            self.dx *= 0.82
            if abs(self._gravity_vy) < 1.2:
                self.state = "walk"
                self._new_direction()

        self.x, self.y = nx, ny
        self._update_pos()

    # ── Comportamentos aleatorios ─────────────────────────────────────────────
    def _schedule_behavior(self):
        self.root.after(random.randint(5000, 12000), self._random_behavior)

    def _random_behavior(self):
        if not self.root.winfo_exists():
            return
        # So muda se nao estiver em modo manual (follow/flee)
        if self.state not in ("follow", "flee", "falling", "sleep"):
            action = random.choices(
                ["walk", "idle", "speak", "popup"],
                weights=[15, 20, 40, 25]
            )[0]
            if action == "walk":
                self.state = "walk"
                self._new_direction()
            elif action == "idle":
                self.state    = "idle"
                self.idle_ttl = random.randint(18, 50)
            elif action == "speak":
                bx = int(self.x)
                by = max(0, int(self.y) - 100)
                try:
                    self._speak(random.choice(MESSAGES))
                    self._play_sound()
                except Exception:
                    pass
            elif action == "popup":
                px = random.randint(50, max(51, self.sw - 320))
                py = random.randint(50, max(51, self.sh - 160))
                try:
                    GlitchPopup(self.root, px, py)
                except Exception:
                    pass
        self._schedule_behavior()

    # ── Cacada ao botao minimizar ─────────────────────────────────────────────
    MINIMIZE_MSGS = [
        "Minimizei! Hehe.",
        "Ops... foi mal.",
        "Nao precisava disso aberto.",
        "MIAU! Menos janelas.",
        "Limpeza de tela. De nada.",
        "Essa janela tava no meu caminho.",
        "Cliquei. Nao foi querer.",
        "Organizando o desktop pra voce. :3",
    ]

    def _schedule_minimize_hunt(self):
        delay = random.randint(25000, 55000)
        self.root.after(delay, self._start_minimize_hunt)

    def _start_minimize_hunt(self):
        if not self.root.winfo_exists():
            return
        # Nao interrompe estados criticos
        if self._mouse_chaos or self.state in ("sleep", "falling", "hunting"):
            self._schedule_minimize_hunt()
            return

        windows = self._get_visible_windows()
        if not windows:
            self._schedule_minimize_hunt()
            return

        hwnd, title, rect = random.choice(windows)
        bx, by = self._get_minimize_button_pos(rect)

        # Verificar se o botao esta dentro da tela
        if 20 <= bx <= self.sw - 20 and 5 <= by <= self.sh - 20:
            self._hunt_target = (bx, by)
            self.state = "hunting"
        else:
            self._schedule_minimize_hunt()

    def _move_hunting(self):
        if self._hunt_target is None:
            self.state = "walk"
            self._new_direction()
            return

        tx, ty = self._hunt_target
        cat_tx = tx - self.sprite_w // 2
        cat_ty = ty + 5
        ddx = cat_tx - self.x
        ddy = cat_ty - self.y
        dist = math.hypot(ddx, ddy)

        if dist < 6:
            self._do_minimize_click(tx, ty)
            self._hunt_target = None
            self.state = "walk"
            self._new_direction()
            self._schedule_minimize_hunt()
        else:
            speed = min(self.SPEED * 1.8, dist)
            self.x += (ddx / dist) * speed
            self.y += (ddy / dist) * speed
            self.x = max(0, min(self.sw - self.sprite_w, self.x))
            self.y = max(0, min(self.sh - self.sprite_h, self.y))
            self._update_pos()

    def _do_minimize_click(self, x, y):
        try:
            u32 = ctypes.windll.user32
            u32.SetCursorPos(int(x), int(y))
            time.sleep(0.08)
            u32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.05)
            u32.mouse_event(0x0004, 0, 0, 0, 0)
        except Exception:
            pass
        try:
            self._speak(random.choice(self.MINIMIZE_MSGS))
            self._play_sound()
        except Exception:
            pass

    def _get_visible_windows(self):
        from ctypes import wintypes
        u32 = ctypes.windll.user32
        windows = []

        def _cb(hwnd, _):
            if not u32.IsWindowVisible(hwnd):
                return True
            n = u32.GetWindowTextLengthW(hwnd)
            if n == 0:
                return True
            buf = ctypes.create_unicode_buffer(n + 1)
            u32.GetWindowTextW(hwnd, buf, n + 1)
            title = buf.value
            rect = wintypes.RECT()
            u32.GetWindowRect(hwnd, ctypes.byref(rect))
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            if w > 250 and h > 120 and title.strip():
                windows.append((hwnd, title, rect))
            return True

        PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        u32.EnumWindows(PROC(_cb), 0)
        return windows

    def _get_minimize_button_pos(self, rect):
        # Calcula posicao do botao minimizar levando em conta DPI
        try:
            dpi = ctypes.windll.user32.GetDpiForSystem()
        except Exception:
            dpi = 96
        # Cada botao tem ~46px em 96dpi; escala com DPI
        btn_w = int(46 * dpi / 96)
        # Minimize e o 3o botao da direita; centro em right - (btn_w * 2.5)
        x = rect.right - int(btn_w * 2.5)
        y = rect.top + max(12, int(15 * dpi / 96))
        return x, y

    # ── Glitch ────────────────────────────────────────────────────────────────
    def _schedule_glitch_event(self):
        self.root.after(random.randint(10000, 30000), self._trigger_glitch)

    def _trigger_glitch(self):
        if not self.root.winfo_exists():
            return

        self.glitch_mode = True
        self.glitch_ttl  = random.randint(10, 22)

        try:
            GlitchFlash(self.root, self.sw, self.sh)
        except Exception:
            pass

        if random.random() < 0.5:
            self.root.after(300, self._try_flash)

        n_ghosts = random.randint(1, 2)
        for i in range(n_ghosts):
            self.root.after(100 + i * 200, self._spawn_ghost)

        if random.random() < 0.65:
            self.root.after(400, self._speak_glitch)

        self._schedule_glitch_event()

    def _try_flash(self):
        try:
            GlitchFlash(self.root, self.sw, self.sh)
        except Exception:
            pass

    def _spawn_ghost(self):
        try:
            GhostCat(self.root, int(self.x), int(self.y),
                     self.sprites, self.sw, self.sh,
                     self.sprite_w, self.sprite_h)
        except Exception:
            pass

    def _speak(self, message):
        """Mostra um balao de fala, destruindo o anterior se existir."""
        if self._active_bubble is not None:
            try:
                self._active_bubble.destroy()
            except Exception:
                pass
            self._active_bubble = None
        try:
            bx = int(self.x)
            by = max(0, int(self.y) - 100)
            self._active_bubble = SpeechBubble(self.root, bx, by, message)
        except Exception:
            pass


    def _speak_glitch(self):
        self._speak(random.choice(MESSAGES))


    # ── Fake shutdown prank ───────────────────────────────────────────────────

    def _schedule_shutdown_prank(self):
        delay = random.randint(90_000, 210_000)  # 1.5 – 3.5 min
        self.root.after(delay, self._show_shutdown_warning)

    def _show_shutdown_warning(self):
        try:
            ShutdownWarning(
                self.root,
                on_x=self._start_blackout,
                on_timeout=self._schedule_shutdown_prank,
            )
        except Exception:
            self._schedule_shutdown_prank()

    def _start_blackout(self):
        try:
            BlackoutScreen(self.root, on_done=self._fake_shutdown_recovery)
        except Exception:
            self._schedule_shutdown_prank()

    def _fake_shutdown_recovery(self):
        try:
            self._speak("Era zoeira! Nao ia desligar nao. :3")
        except Exception:
            pass
        self._schedule_shutdown_prank()


    # ── YouTube prank ─────────────────────────────────────────────────────────

    YOUTUBE_URLS = [
        "https://www.youtube.com/watch?v=IxX_QHay02M",
        "https://www.youtube.com/watch?v=4SHgbM4LY48",
    ]

    def _schedule_youtube_prank(self):
        delay = random.randint(120_000, 300_000)  # 2 – 5 min
        self.root.after(delay, self._do_youtube_prank)

    def _do_youtube_prank(self):
        try:
            url = random.choice(self.YOUTUBE_URLS)
            webbrowser.open(url)
            msgs = [
                "Essa e a musica que eu gosto! >:3",
                "Ouvi isso aqui... e a minha favorita!",
                "Coloquei a minha playlist. De nada. ;3",
                "Toca essa ai, e boa demais!",
            ]
            self._speak(random.choice(msgs))
        except Exception:
            pass
        self._schedule_youtube_prank()

    # ── Clone Jutsu ───────────────────────────────────────────────────────────

    def _schedule_clone_jutsu(self):
        delay = random.randint(150_000, 360_000)  # 2.5 – 6 min
        self.root.after(delay, self._do_clone_jutsu)

    def _do_clone_jutsu(self):
        try:
            bx = int(self.x)
            by = max(0, int(self.y) - 90)
            self._speak("Kage Bunshin no Jutsu! >:3")
        except Exception:
            pass
        # Spawn clones progressivamente para encher a tela
        self._clones = []
        self._spawn_clones_wave(0)

    def _spawn_clones_wave(self, wave):
        if wave >= 12:
            # Depois de 4s destroi tudo
            self.root.after(4000, self._destroy_clones)
            return
        count = min(4 + wave, 8)
        for _ in range(count):
            x = random.randint(0, max(0, self.sw - self.sprite_w))
            y = random.randint(0, max(0, self.sh - self.sprite_h))
            alpha = random.uniform(0.35, 0.75)
            try:
                clone = CatClone(self.root, x, y, self.sprites,
                                 self.sprite_w, self.sprite_h, alpha=alpha)
                self._clones.append(clone)
            except Exception:
                pass
        self.root.after(350, lambda: self._spawn_clones_wave(wave + 1))

    def _destroy_clones(self):
        for c in getattr(self, "_clones", []):
            c.destroy()
        self._clones = []
        try:
            self._speak("Viu? Sou um ninja. Nhac.")
        except Exception:
            pass
        self._schedule_clone_jutsu()


    # ── Memes aleatorios ──────────────────────────────────────────────────────

    def _load_memes(self):
        self._meme_files = []
        memes_dir = os.path.join(DIST_DIR, "memes")
        if not os.path.isdir(memes_dir):
            return
        for f in os.listdir(memes_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                self._meme_files.append(os.path.join(memes_dir, f))

    def _schedule_random_meme(self):
        delay = random.randint(90_000, 240_000)  # 1.5 – 4 min
        self.root.after(delay, self._show_random_meme)

    def _show_random_meme(self):
        if self._meme_files and PIL_AVAILABLE:
            try:
                path = random.choice(self._meme_files)
                MemeWindow(self.root, path, self.sw, self.sh)
                msgs = [
                    "Olha esse meme que achei!",
                    "Encontrei isso na internet... hehe.",
                    "Isso descreve voce. Nao sou eu. ;3",
                    "Pera, nao ri nao!",
                ]
                self._speak(random.choice(msgs))
            except Exception:
                pass
        self._schedule_random_meme()


if __name__ == "__main__":
    DesktopCat()
