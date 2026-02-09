# Arma Reforger Queue Joiner

A tool that automatically retries joining a full server in Arma Reforger until you get into the queue.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## How it works

1. Open the tool and keep it running
2. In the game, hover your mouse over the server you want to join
3. Press **F6** — the tool saves your mouse position and starts clicking
4. If the queue is full — it presses ESC and retries automatically
5. If you get into the queue — it stops and plays a sound alert
6. Press **F4** to stop at any time

Detection is based on pixel color analysis — no OCR or external dependencies needed.

## Download

Go to [Releases](../../releases) and download **ArmaQueueJoiner.exe** — no Python required.

## Run from source

```bash
git clone https://github.com/lime98/arma-queue-joiner.git
cd arma-queue-joiner
pip install -r requirements.txt
python app.py
```

## Hotkeys

| Key | Action |
|---|---|
| **F6** | Start (configurable) |
| **F4** | Stop (configurable) |

Both hotkeys can be changed in the app.

## Notes

- Run as Administrator for best compatibility
- Works with multi-monitor setups
- Supports Borderless Windowed and Fullscreen modes

## License

MIT