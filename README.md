# 🐱 Desktop Cat — Green Hacker Edition

Um gato virtual travesso que vive na sua área de trabalho, inspirado no Desktop Goose e no visual hacker do Watch Dogs 2.

![Python](https://img.shields.io/badge/Feito%20em-Python%203-blue)
![Platform](https://img.shields.io/badge/Plataforma-Windows-red)
![Version](https://img.shields.io/badge/Vers%C3%A3o-1.0-brightgreen)

---

## 🎮 O que ele faz

- Anda por **toda a tela** em 2D com física de gravidade e quique
- **Efeitos de glitch** com aberração cromática, inversão de cores e cópias fantasma
- **Balões de fala** com frases engraçadas, referências de filmes e mensagens em PT-BR
- **Menu de contexto** (botão direito): dar comida, dormir, seguir/fugir do mouse
- **Caos do mouse**: clique rápido 3x e o gato sequestra o cursor por alguns segundos
- **Caçador de minimize**: periodicamente vai até a barra de título de uma janela aberta e minimiza
- **Falso desligamento**: aparece aviso "Vou desligar o PC" com contagem regressiva e tela preta
- **Kage Bunshin no Jutsu**: o gato se multiplica até cobrir a tela inteira
- **Abre vídeos no YouTube** dizendo que é a música favorita dele
- **Sons aleatórios** a cada 30 segundos (pasta `dist/sounds/`)
- **Memes** que deslizam da borda da tela (pasta `dist/memes/`)
- Modo sono com `zzz` flutuando, acorda com clique
- Sombra sob o gato
- Sprites em pixel-art com visual verde neon

---

## 🗂 Estrutura

```
desktop-cat-v1/
├── desktop_cat.py       # Código principal
├── build.bat            # Compila para .exe standalone
├── run.bat              # Roda direto com Python
├── .gitignore
└── dist/
    ├── cat1_wd2.png     # Sprites (cat1 a cat16)
    ├── ...
    ├── sounds/          # Sons .mp3 (adicione quantos quiser)
    ├── memes/           # Imagens de meme (adicione quantos quiser)
    └── texts/
        └── frases.txt
```

---

## 🚀 Como rodar

### Opção 1 — Direto com Python

Requer Python 3.10+ e Pillow instalados:

```bash
pip install pillow
python desktop_cat.py
```

### Opção 2 — Executável standalone (.exe)

1. Instale o [Python 3.12](https://www.python.org/downloads/release/python-3120/) (necessário para o build; o .exe final não precisa de Python)
2. Dê duplo clique em `build.bat`
3. O executável estará em `dist\DesktopCat.exe`

> O `.exe` gerado funciona em qualquer PC Windows sem instalar nada.

---

## ➕ Adicionando conteúdo

| Pasta | O que colocar |
|---|---|
| `dist/sounds/` | Qualquer `.mp3` ou `.wav` — tocado aleatoriamente a cada 30s |
| `dist/memes/` | Qualquer `.png` ou `.jpg` — aparece deslizando pela borda da tela |

---

## 🛠 Dependências

- `tkinter` (nativo do Python)
- `Pillow` — sprites e efeitos visuais
- `ctypes` (nativo) — controle do mouse e DPI
- `webbrowser` (nativo) — abrir YouTube

Não usa pygame nem pyautogui.

---

*Inspirado no [Desktop Goose](https://samperson.itch.io/desktop-goose)*
