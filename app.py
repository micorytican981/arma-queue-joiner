"""
Arma Reforger Queue Joiner
Automatically clicks on a server until you get into the queue.
"""

import threading
import time
import tkinter as tk
from tkinter import ttk

import keyboard
import numpy as np
import pyautogui
from PIL import ImageGrab


class QueueJoiner:
    """Core logic: click server, detect screen state, retry or stop."""

    def __init__(self, on_log, on_state_change):
        self.on_log = on_log
        self.on_state_change = on_state_change
        self.running = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.attempt = 0

        # Configurable timings (seconds)
        self.wait_after_click = 2.0
        self.escape_hold = 1.5
        self.pause_before_retry = 0.5

    def detect_state(self):
        """
        Take a screenshot and look for colored text in the center dialog.
        Yellow text = in queue (success).
        Red text = server full (retry).
        """
        screenshot = ImageGrab.grab()
        width, height = screenshot.size

        left = int(width * 0.25)
        right = int(width * 0.75)
        top = int(height * 0.25)
        bottom = int(height * 0.55)

        region = screenshot.crop((left, top, right, bottom))
        arr = np.array(region)

        # Yellow pixels (queue confirmation text)
        yellow = int(
            ((arr[:, :, 0] > 180) & (arr[:, :, 1] > 130) & (arr[:, :, 2] < 80)).sum()
        )

        # Red pixels (server full text)
        red = int(
            ((arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)).sum()
        )

        threshold = 50

        if yellow > threshold and yellow > red:
            return "in_queue", yellow, red
        elif red > threshold:
            return "server_full", yellow, red
        return "unknown", yellow, red

    def hold_escape(self, duration):
        pyautogui.keyDown("escape")
        time.sleep(duration)
        pyautogui.keyUp("escape")

    def start(self, mouse_x, mouse_y):
        self.running = True
        self.attempt = 0
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.on_log(f"Mouse position: ({self.mouse_x}, {self.mouse_y})")
        self.on_state_change("running")

        # Small delay so the hotkey itself doesn't interfere
        time.sleep(0.3)

        # Main loop
        while self.running:
            self.attempt += 1
            self.on_log(f"Attempt {self.attempt} - clicking server...")

            pyautogui.click(self.mouse_x, self.mouse_y)
            time.sleep(0.3)
            pyautogui.click(self.mouse_x, self.mouse_y)
            time.sleep(self.wait_after_click)

            if not self.running:
                break

            state, yellow, red = self.detect_state()

            if state == "in_queue":
                self.on_log(
                    f"SUCCESS - You are in the queue! (y={yellow}, r={red})"
                )
                self.on_state_change("success")
                self.running = False
                self._play_alert()
                return

            elif state == "server_full":
                self.on_log(f"Queue full (y={yellow}, r={red}) - retrying...")
                time.sleep(0.5)
                self.hold_escape(self.escape_hold)
                time.sleep(self.pause_before_retry)

            else:
                self.on_log(f"Unknown state (y={yellow}, r={red}) - waiting...")
                time.sleep(1.0)

                if not self.running:
                    break

                state2, y2, r2 = self.detect_state()
                if state2 == "in_queue":
                    self.on_log(f"SUCCESS - You are in the queue! (y={y2}, r={r2})")
                    self.on_state_change("success")
                    self.running = False
                    self._play_alert()
                    return
                else:
                    self.on_log("Still unclear - pressing ESC and retrying...")
                    time.sleep(0.5)
                    self.hold_escape(self.escape_hold)
                    time.sleep(self.pause_before_retry)

        self.on_log("Stopped.")
        self.on_state_change("idle")

    def stop(self):
        self.running = False

    def _play_alert(self):
        try:
            import winsound
            for _ in range(3):
                winsound.Beep(1000, 300)
                time.sleep(0.1)
        except Exception:
            pass


class App(tk.Tk):
    """Main application window."""

    WINDOW_WIDTH = 520
    WINDOW_HEIGHT = 520

    HOTKEY_OPTIONS = ["F5", "F6", "F7", "F8", "F9", "F10"]
    STOP_HOTKEY = "F4"

    def __init__(self):
        super().__init__()
        self.title("Arma Reforger Queue Joiner")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.joiner = QueueJoiner(
            on_log=self._append_log,
            on_state_change=self._update_state,
        )
        self.worker_thread = None
        self.current_hotkey = None
        self.current_stop_hotkey = None

        self._build_ui()
        self._register_hotkeys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---- UI ----

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure(
            "TLabel", background="#1e1e1e", foreground="#cccccc", font=("Segoe UI", 10)
        )
        style.configure(
            "Header.TLabel",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background="#1e1e1e",
            foreground="#888888",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Hotkey.TLabel",
            background="#1e1e1e",
            foreground="#e8a832",
            font=("Segoe UI", 12, "bold"),
        )

        # Header
        header = ttk.Label(self, text="Arma Reforger Queue Joiner", style="Header.TLabel")
        header.pack(pady=(15, 5))

        # Instructions
        instructions = ttk.Label(
            self,
            text="1. Open the game, go to server browser\n"
                 "2. Hover your mouse over the server you want to join\n"
                 "3. Press the Start hotkey (see below)\n"
                 "4. The tool will click and retry until you are in the queue",
            style="TLabel",
            justify="left",
        )
        instructions.pack(padx=20, pady=(0, 10))

        # Hotkey frame
        hotkey_frame = ttk.Frame(self)
        hotkey_frame.pack(padx=20, fill="x", pady=(0, 5))

        ttk.Label(hotkey_frame, text="Start hotkey:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.hotkey_var = tk.StringVar(value="F6")
        hotkey_combo = ttk.Combobox(
            hotkey_frame,
            textvariable=self.hotkey_var,
            values=self.HOTKEY_OPTIONS,
            state="readonly",
            width=6,
        )
        hotkey_combo.grid(row=0, column=1, padx=(10, 20), pady=2)
        hotkey_combo.bind("<<ComboboxSelected>>", lambda e: self._register_hotkeys())

        ttk.Label(hotkey_frame, text="Stop hotkey:").grid(
            row=0, column=2, sticky="w", pady=2
        )
        ttk.Label(hotkey_frame, text="F4", style="Hotkey.TLabel").grid(
            row=0, column=3, padx=(10, 0), pady=2
        )

        # Big hotkey display
        self.hotkey_display = ttk.Label(
            self,
            text="Hover over server, press F6 to start",
            style="Hotkey.TLabel",
        )
        self.hotkey_display.pack(pady=(5, 5))

        # Settings frame
        settings_frame = ttk.Frame(self)
        settings_frame.pack(padx=20, fill="x")

        ttk.Label(settings_frame, text="Wait after click (sec):").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.wait_var = tk.StringVar(value="2.0")
        ttk.Entry(settings_frame, textvariable=self.wait_var, width=8).grid(
            row=0, column=1, padx=(10, 0), pady=2
        )

        ttk.Label(settings_frame, text="ESC hold time (sec):").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.esc_var = tk.StringVar(value="1.5")
        ttk.Entry(settings_frame, textvariable=self.esc_var, width=8).grid(
            row=1, column=1, padx=(10, 0), pady=2
        )

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)

        self.stop_btn = tk.Button(
            btn_frame,
            text="Stop",
            command=self._on_stop,
            bg="#8a2d2d",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=14,
            relief="flat",
            cursor="hand2",
            state="disabled",
        )
        self.stop_btn.pack()

        # Status
        self.status_label = ttk.Label(self, text="Status: Idle", style="Status.TLabel")
        self.status_label.pack(pady=(0, 5))

        # Log area
        log_frame = tk.Frame(self, bg="#1e1e1e")
        log_frame.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            bg="#111111",
            fg="#aaaaaa",
            font=("Consolas", 9),
            relief="flat",
            state="disabled",
            wrap="word",
        )
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

    # ---- Hotkeys ----

    def _register_hotkeys(self):
        # Unregister old hotkeys
        if self.current_hotkey is not None:
            try:
                keyboard.unhook_key(self.current_hotkey)
            except (KeyError, ValueError):
                pass
        if self.current_stop_hotkey is not None:
            try:
                keyboard.unhook_key(self.current_stop_hotkey)
            except (KeyError, ValueError):
                pass

        start_key = self.hotkey_var.get()

        self.current_hotkey = keyboard.on_press_key(
            start_key, lambda e: self._on_hotkey_start(), suppress=False
        )
        self.current_stop_hotkey = keyboard.on_press_key(
            self.STOP_HOTKEY, lambda e: self._on_stop(), suppress=False
        )

        self.hotkey_display.configure(
            text=f"Hover over server, press {start_key} to start  |  {self.STOP_HOTKEY} to stop"
        )

    def _on_hotkey_start(self):
        if self.joiner.running:
            return

        # Capture mouse position RIGHT NOW (while hovering over server)
        mx, my = pyautogui.position()

        try:
            self.joiner.wait_after_click = float(self.wait_var.get())
            self.joiner.escape_hold = float(self.esc_var.get())
        except ValueError:
            self._append_log("ERROR: Invalid settings values.")
            return

        self.after(0, lambda: self.stop_btn.configure(state="normal"))
        self._clear_log()

        self.worker_thread = threading.Thread(
            target=self.joiner.start, args=(mx, my), daemon=True
        )
        self.worker_thread.start()

    # ---- Actions ----

    def _on_stop(self):
        self.joiner.stop()
        self.after(0, lambda: self.stop_btn.configure(state="disabled"))

    def _on_close(self):
        self.joiner.stop()
        keyboard.unhook_all()
        self.destroy()

    # ---- Logging ----

    def _append_log(self, message):
        def _update():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self.after(0, _update)

    def _clear_log(self):
        def _update():
            self.log_text.configure(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.configure(state="disabled")

        self.after(0, _update)

    def _update_state(self, state):
        def _update():
            if state == "running":
                self.status_label.configure(text="Status: Running...", foreground="#e8a832")
            elif state == "success":
                self.status_label.configure(text="Status: IN QUEUE!", foreground="#2dcc5e")
                self.stop_btn.configure(state="disabled")
            else:
                self.status_label.configure(text="Status: Idle", foreground="#888888")
                self.stop_btn.configure(state="disabled")

        self.after(0, _update)


if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    app = App()
    app.mainloop()