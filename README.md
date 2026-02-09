# Arma Reforger Queue Joiner

A simple tool that automatically retries joining a full server in Arma Reforger until you get into the queue.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## How it works

1. You hover your mouse over a server in the server browser
2. The tool clicks the server repeatedly
3. If the queue is full (red text) — it presses ESC and retries
4. If you get into the queue (yellow text) — it stops and plays a sound alert

Detection is based on pixel color analysis in the center of the screen — no OCR needed.

## Download

Go to [Releases](../../releases) and download `ArmaQueueJoiner.exe` — no Python installation required.

## Run from source

If you prefer running from source:

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

## Settings

| Setting | Default | Description |
|---|---|---|
| Countdown | 5 sec | Time to switch to the game after pressing Start |
| Wait after click | 2.0 sec | Delay after clicking to let the dialog appear |
| ESC hold time | 1.5 sec | How long to hold ESC to leave the dialog |

## Safety

- **Failsafe**: Move your mouse to the top-left corner of the screen to force-stop
- **Stop button**: Click Stop in the app window at any time
- **Ctrl+C**: If running from terminal

## License

MIT