import customtkinter as ctk
import threading
import os
from datetime import datetime
from PIL import Image
from voice_assistant import VoiceAssistant

# Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VoiceAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("AI Voice Assistant")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # State
        self.assistant = None
        self.listener_thread = None
        self.is_listening = False

        # Initialize API Key
        self.api_key = os.getenv("OPENAI_API_KEY")

        # Layout
        self.create_header()
        self.create_chat_area()
        self.create_footer()

        # Initialize Assistant
        self.init_assistant()

    def create_header(self):
        """Create the header with status and title"""
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="AI Voice Assistant", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="Ready to start",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 10))

    def create_chat_area(self):
        """Create the scrollable chat area"""
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

    def create_footer(self):
        """Create the footer with controls"""
        self.footer_frame = ctk.CTkFrame(self, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="ew", pady=20)
        
        self.start_button = ctk.CTkButton(
            self.footer_frame,
            text="Start Listening",
            command=self.toggle_listening,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.start_button.pack(padx=20, pady=10)

    def init_assistant(self):
        """Initialize the backend voice assistant"""
        try:
            self.assistant = VoiceAssistant(
                api_key=self.api_key,
                status_callback=self.update_status_safe,
                chat_callback=self.add_message_safe
            )
        except Exception as e:
            self.update_status_safe(f"Error initializing: {e}")

    def toggle_listening(self):
        """Start or stop the voice assistant loop"""
        if not self.is_listening:
            # Start
            self.is_listening = True
            self.start_button.configure(text="Stop Listening", fg_color="#c0392b", hover_color="#e74c3c")
            
            # Start thread
            self.listener_thread = threading.Thread(target=self.run_assistant_thread, daemon=True)
            self.listener_thread.start()
        else:
            # Stop
            self.is_listening = False
            self.start_button.configure(text="Start Listening", fg_color="#1f6aa5", hover_color="#144870")
            if self.assistant:
                self.assistant.is_running = False
            self.update_status_safe("Stopped")

    def run_assistant_thread(self):
        """Thread worker to run the assistant loop"""
        if self.assistant:
            try:
                self.assistant.run()
            except Exception as e:
                self.update_status_safe(f"Error: {e}")
            finally:
                # Reset UI when thread ends (if it ends unexpectedly)
                if self.is_listening:
                    self.after(0, self.toggle_listening)

    def update_status_safe(self, text):
        """Thread-safe status update"""
        self.after(0, lambda: self.status_label.configure(text=text))

    def add_message_safe(self, sender, text):
        """Thread-safe message addition"""
        self.after(0, lambda: self._add_message(sender, text))

    def _add_message(self, sender, text):
        """Internal method to add message widget"""
        is_user = sender == "user"
        
        # Message container
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color="#2b2b2b" if is_user else "#3b3b3b",
            corner_radius=15
        )
        msg_frame.pack(fill="x", pady=5, padx=10, anchor="e" if is_user else "w")

        # Label
        sender_name = "You" if is_user else "Assistant"
        color = "#3498db" if is_user else "#2ecc71"
        
        name_label = ctk.CTkLabel(
            msg_frame, 
            text=sender_name, 
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color
        )
        name_label.pack(anchor="w", padx=10, pady=(5, 0))

        content_label = ctk.CTkLabel(
            msg_frame, 
            text=text, 
            wraplength=400, 
            justify="left",
            font=ctk.CTkFont(size=14)
        )
        content_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Scroll to bottom
        # self.chat_frame._parent_canvas.yview_moveto(1.0) # This can be tricky in ctk; usually auto-scroll works or needs update


if __name__ == "__main__":
    app = VoiceAssistantGUI()
    app.mainloop()
