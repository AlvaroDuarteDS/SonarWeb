import tkinter as tk
from typing import Callable, Optional


class StatusBar:
    def __init__(self, parent):
        self.label = tk.Label(parent, text="Ready", font=("Arial", 12), fg="green")
        self.label.pack(pady=10)

    def update(self, text: str, color: str = "black"):
        self.label.config(text=text, fg=color)


class ActionButtons:
    def __init__(self, parent, callbacks: dict):
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10)

        buttons = [
            ("🍪 Auto Accept Cookies", callbacks.get('cookies'), "#3498db"),
            ("📸 Screenshot", callbacks.get('screenshot'), "#27ae60"),
            ("🔄 Refresh", callbacks.get('refresh'), "#f39c12"),
            ("❌ Exit", callbacks.get('exit'), "#e74c3c")
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                self.frame, text=text, command=command,
                bg=color, fg="white", relief="flat", padx=15
            )
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=2)