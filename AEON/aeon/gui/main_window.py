import sys
import os
import threading
import customtkinter as ctk
import pyttsx3
import speech_recognition as sr
from PIL import Image

# Ensure project root is in path
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(path))))

from aeon.core.engine import Engine
from aeon.config import check_config

# Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AeonApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AEON Intelligence System")
        self.geometry("1100x700")

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Chat area
        self.grid_rowconfigure(1, weight=0) # Input area

        # 1. Chat Display Area
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="#0a0a10", corner_radius=10)
        self.chat_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # 2. Input Area Container
        self.input_container = ctk.CTkFrame(self, fg_color="transparent")
        self.input_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_container.grid_columnconfigure(1, weight=1)

        # Voice Button
        self.voice_btn = ctk.CTkButton(
            self.input_container, 
            text="🎙️", 
            width=50, 
            height=50, 
            corner_radius=25,
            fg_color="#333",
            hover_color="#555",
            command=self.toggle_voice_input
        )
        self.voice_btn.grid(row=0, column=0, padx=(0, 10))

        # Text Input
        self.msg_entry = ctk.CTkEntry(
            self.input_container, 
            placeholder_text="Enter command...", 
            height=50, 
            border_color="#00f3ff", # Cyan accent
            fg_color="#14141e"
        )
        self.msg_entry.grid(row=0, column=1, sticky="ew")
        self.msg_entry.bind("<Return>", self.send_message_event)

        # Send Button
        self.send_btn = ctk.CTkButton(
            self.input_container, 
            text="SEND", 
            width=100, 
            height=50, 
            fg_color="#bc13fe", # Purple accent
            hover_color="#9c0ce6",
            command=self.send_message_event
        )
        self.send_btn.grid(row=0, column=2, padx=(10, 0))

        # Initialize System
        self.engine = None
        self.is_speaking = False
        self.voice_active = False
        
        # Voice Engines
        self.tts_engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        # Startup Thread
        threading.Thread(target=self.start_engine, daemon=True).start()

    def start_engine(self):
        self.add_message("System", "Initializing AEON Core...")
        try:
            # We pass a custom output handler that updates the UI
            self.engine = Engine(output_handler=self.engine_output)
            self.add_message("System", f"Online. Model: {self.engine.llm.model}")
        except Exception as e:
            self.add_message("Error", f"Startup Failed: {e}")

    def engine_output(self, text):
        # Callback from Engine to print text to UI
        # Must schedule on main thread if not already
        self.after(0, lambda: self.add_message("AEON", text))
        
        # Also speak it?
        # self.speak(text) # Simplistic approach, might block or overlap

    def add_message(self, sender, text):
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.grid(sticky="ew", pady=5)
        msg_frame.grid_columnconfigure(1, weight=1)

        if sender == "User":
            color = "#00f3ff"
            align = "e" # East
            bg = "#1a1a2e"
        elif sender == "System" or sender == "Error":
            color = "gray"
            align = "w"
            bg = "transparent"
        else: # AEON
            color = "#bc13fe"
            align = "w" # West
            bg = "#1a0b1e"

        bubble = ctk.CTkLabel(
            msg_frame, 
            text=text, 
            fg_color=bg, 
            corner_radius=8, 
            text_color="white",
            padx=15, 
            pady=10, 
            justify="left",
            wraplength=800
        )
        
        if align == "e":
            bubble.pack(side="right")
        else:
            bubble.pack(side="left")
            # Label
            label = ctk.CTkLabel(msg_frame, text=sender, text_color=color, font=("Arial", 10, "bold"))
            label.pack(side="left", padx=(0, 5))
            
        # TTS for AEON messages (automatically speak response)
        if sender == "AEON":
            threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    def send_message_event(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.msg_entry.delete(0, "end")
        self.add_message("User", msg)
        
        # Process in thread
        threading.Thread(target=self.process_chat, args=(msg,), daemon=True).start()

    def process_chat(self, msg):
        if self.engine:
            self.engine.chat(msg)
        else:
            self.add_message("Error", "Engine not ready.")

    def speak(self, text):
        # Filter markdown
        clean_text = text.replace("*", "").replace("`", "")
        self.tts_engine.say(clean_text)
        self.tts_engine.runAndWait()

    def toggle_voice_input(self):
        if self.voice_active:
            self.voice_active = False
            self.voice_btn.configure(fg_color="#333")
            return
        
        self.voice_active = True
        self.voice_btn.configure(fg_color="#ff0000") # Red indicating listening
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.voice_active:
                try:
                    # Short timeout to allow check of self.voice_active
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        self.after(0, lambda: self.handle_voice_entry(text))
                        # Stop listening after one command? Or continuous?
                        # For now, let's do continuous until toggled off
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Voice Error: {e}")
                    # Optionally notify UI
    
    def handle_voice_entry(self, text):
        self.msg_entry.delete(0, "end")
        self.msg_entry.insert(0, text)
        self.send_message_event()


if __name__ == "__main__":
    app = AeonApp()
    app.mainloop()
