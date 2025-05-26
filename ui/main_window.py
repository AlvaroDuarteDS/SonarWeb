import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_app import VoiceWebAssistant


class MainWindow:
    def __init__(self, app: 'VoiceWebAssistant'):
        self.app = app
        self.cookies_button = None
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface"""
        self.root = tk.Tk()
        self.root.title("Voice Web Assistant - Enhanced")
        self.root.geometry("550x350")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)

        # Main title
        tk.Label(self.root, text="🎤 Voice Web Assistant",
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Instructions
        instructions = "Hold SPACE to record • Left Shift to stop speech/recording"
        tk.Label(self.root, text=instructions,
                 font=("Arial", 9)).pack(pady=5)

        # Status
        self.status_label = tk.Label(self.root, text="Ready",
                                     font=("Arial", 12), fg="green")
        self.status_label.pack(pady=10)

        # Current site
        self.current_site_label = tk.Label(self.root, text="No site loaded",
                                           font=("Arial", 10), fg="blue")
        self.current_site_label.pack(pady=5)

        # Auto-accept cookies button (toggleable)
        self.cookies_button = tk.Button(self.root, text="🍪 Enable Auto Cookies",
                                        command=self.app.auto_accept_cookies,
                                        bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                        relief="flat", padx=20, pady=5)
        self.cookies_button.pack(pady=10)

        # Quick actions frame
        actions_frame = tk.Frame(self.root)
        actions_frame.pack(pady=10)

        tk.Button(actions_frame, text="📸 Screenshot",
                  command=self.app.take_manual_screenshot,
                  bg="#27ae60", fg="white", relief="flat", padx=15).grid(row=0, column=0, padx=3)

        tk.Button(actions_frame, text="🔄 Refresh",
                  command=self.app.refresh_page,
                  bg="#f39c12", fg="white", relief="flat", padx=15).grid(row=0, column=1, padx=3)

        tk.Button(actions_frame, text="🗑️ Clear Cache",
                  command=self.app.clear_cache,
                  bg="#9b59b6", fg="white", relief="flat", padx=15).grid(row=0, column=2, padx=3)

        tk.Button(actions_frame, text="❌ Exit",
                  command=self.app.exit_program,
                  bg="#e74c3c", fg="white", relief="flat", padx=15).grid(row=0, column=3, padx=3)

        # Key bindings
        self.root.bind('<KeyPress-space>', self.app.start_recording)
        self.root.bind('<KeyRelease-space>', self.app.stop_recording)
        self.root.bind('<KeyPress-Shift_L>', self.app.force_stop_recording)  # Left Shift to stop
        self.root.bind('<Escape>', self.app.exit_program)

        # Make window focusable
        self.root.focus_set()

    def update_status(self, status):
        """Update status label safely"""
        try:
            self.status_label.config(text=status)
            self.root.update_idletasks()
        except:
            pass

    def update_current_site(self, site_text):
        """Update current site label"""
        try:
            self.current_site_label.config(text=site_text)
        except:
            pass

    def update_cookies_button(self, text):
        """Update cookies button text"""
        try:
            self.cookies_button.config(text=text)
        except:
            pass
