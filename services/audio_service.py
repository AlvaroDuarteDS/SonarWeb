import wave
import pyaudio
import speech_recognition as sr
import tempfile
import os
import time
import threading
from gtts import gTTS
from pygame import mixer
import uuid


class AudioService:
    def __init__(self, speech_temp_dir):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.recording = False
        self.speaking = False
        self.speech_temp_dir = speech_temp_dir

        # Initialize PyAudio and mixer
        self.p = pyaudio.PyAudio()
        mixer.init()

        # Create temp directory
        if not os.path.exists(self.speech_temp_dir):
            os.makedirs(self.speech_temp_dir)

    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            return False

        # Stop any ongoing speech
        self.stop_speaking()

        self.recording = True
        return True

    def stop_recording(self):
        """Stop recording audio"""
        self.recording = False

    def stop_speaking(self):
        """Stop any ongoing speech"""
        try:
            if self.speaking:
                mixer.music.stop()
                self.speaking = False
        except:
            pass

    def record_audio(self):
        """Record audio and return file path"""
        temp_file = os.path.join(tempfile.gettempdir(), f"recording_{int(time.time())}.wav")

        try:
            stream = self.p.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK)

            frames = []
            while self.recording:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)

            stream.stop_stream()
            stream.close()

            if frames:
                wf = wave.open(temp_file, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                return temp_file

        except Exception as e:
            print(f"Error recording: {e}")

        return None

    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text"""
        try:
            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
        finally:
            try:
                os.remove(audio_file)
            except:
                pass

    def speak(self, text, status_callback=None):
        """Convert text to speech"""
        print(f"Assistant: {text}")

        def speak_thread():
            try:
                self.speaking = True

                if status_callback:
                    status_callback("Speaking...")

                if not mixer.get_init():
                    mixer.init()

                filename = os.path.join(self.speech_temp_dir, f"speech_{uuid.uuid4()}.mp3")

                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(filename)

                mixer.music.load(filename)
                mixer.music.play()

                while mixer.music.get_busy() and self.speaking:
                    time.sleep(0.1)

                try:
                    os.remove(filename)
                except:
                    pass

            except Exception as e:
                print(f"TTS error: {e}")
                print(f"Speech (fallback): {text}")
            finally:
                self.speaking = False
                if status_callback:
                    status_callback("Ready")

        threading.Thread(target=speak_thread, daemon=True).start()

    def cleanup(self):
        """Clean up audio resources"""
        try:
            self.stop_speaking()
            self.p.terminate()
            if mixer.get_init():
                mixer.quit()
        except:
            pass