import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_app import VoiceWebAssistant

if __name__ == "__main__":
    try:
        print("🚀 Starting Voice Web Assistant...")
        app = VoiceWebAssistant()
        app.run()
    except Exception as e:
        print(f"Critical error: {e}")
        input("Press Enter to exit...")