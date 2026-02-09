# Arma Reforger Queue Joiner

A simple tool that automatically retries joining a full server in Arma Reforger until you get into the queue.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## How it works

1. Open the tool and minimize it
2. In the game, hover your mouse over the server you want to join
3. Press **F6** — the tool saves your mouse position and starts clicking
4. If the queue is full (red text) — it presses ESC and retries
5. If you get into the queue (yellow text) — it stops and plays a sound alert
6. Press **F4** to stop at any time

Detection is based on pixel color analysis in the center of the screen — no OCR needed.

## Download

Go to [Releases](../../releases) and download `ArmaQueueJoiner.exe` — no Python installation required.

## Run from source

```bash
git clone https://github.com/YOUR_USERNAME/arma-queue-joiner.git
cd arma-queue-joiner
pip install -r requirements.txt
python app.py
```

## Build .exe yourself

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name "ArmaQueueJoiner" app.py
```

The executable will be in the `dist/` folder.

## Hotkeys

| Key | Action |
|---|---|
| **F6** | Start (saves mouse position and begins clicking) |
| **F4** | Stop |

The start hotkey can be changed in the app (F5-F10).

## Settings

| Setting | Default | Description |
|---|---|---|
| Wait after click | 2.0 sec | Delay after clicking to let the dialog appear |
| ESC hold time | 1.5 sec | How long to hold ESC to leave the dialog |

## Safety

- **F4**: Stop hotkey, works from anywhere
- **Failsafe**: Move your mouse to the top-left corner of the screen to force-stop
- **Stop button**: Click Stop in the app window

## License

MIT