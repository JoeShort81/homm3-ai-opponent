#!/usr/bin/env python3
"""
Heroes of Might & Magic III AI Opponent
Ultra-simple version guaranteed to build as .exe
"""

import json
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class HoMM3AI:
    def __init__(self):
        self.name = "Heroes III AI"
        
    def make_decision(self, game_data):
        """Make AI decision based on game data"""
        turn = game_data.get("turn", 1)
        gold = game_data.get("resources", {}).get("gold", 0)
        
        if turn <= 10:
            if gold < 2000:
                return {"action": "explore", "reason": "Early game exploration"}
            else:
                return {"action": "build", "reason": "Early development"}
        else:
            return {"action": "attack", "reason": "Mid-late game aggression"}

class FileWatcher:
    def __init__(self, callback):
        self.callback = callback
        self.watching = False
        self.thread = None
        
    def start(self, state_file, action_file):
        self.state_file = state_file
        self.action_file = action_file
        self.watching = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        self.watching = False
        
    def _watch_loop(self):
        last_time = 0
        while self.watching:
            try:
                if os.path.exists(self.state_file):
                    current_time = os.path.getmtime(self.state_file)
                    if current_time > last_time:
                        last_time = current_time
                        with open(self.state_file, 'r') as f:
                            data = json.load(f)
                        self.callback(data)
                time.sleep(1)
            except:
                time.sleep(2)

class AIApp:
    def __init__(self):
        self.root = tk.Tk()
        self.ai = HoMM3AI()
        self.watcher = FileWatcher(self.on_game_update)
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Heroes III AI Opponent")
        self.root.geometry("400x300")
        
        # File inputs
        ttk.Label(self.root, text="Game State File:").pack(pady=5)
        self.state_var = tk.StringVar()
        frame1 = ttk.Frame(self.root)
        frame1.pack(fill="x", padx=10)
        ttk.Entry(frame1, textvariable=self.state_var).pack(side="left", fill="x", expand=True)
        ttk.Button(frame1, text="Browse", command=self.browse_state).pack(side="right")
        
        ttk.Label(self.root, text="Action File:").pack(pady=5)
        self.action_var = tk.StringVar()
        frame2 = ttk.Frame(self.root)
        frame2.pack(fill="x", padx=10)
        ttk.Entry(frame2, textvariable=self.action_var).pack(side="left", fill="x", expand=True)
        ttk.Button(frame2, text="Browse", command=self.browse_action).pack(side="right")
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        self.start_btn = ttk.Button(button_frame, text="Start AI", command=self.start_ai)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(button_frame, text="Stop AI", command=self.stop_ai, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        # Log
        ttk.Label(self.root, text="Status:").pack(pady=(20,0))
        self.log = tk.Text(self.root, height=8)
        self.log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_msg("AI ready! Select files and click Start AI.")
        
    def browse_state(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.state_var.set(file_path)
            
    def browse_action(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.action_var.set(file_path)
            
    def start_ai(self):
        if not self.state_var.get() or not self.action_var.get():
            messagebox.showerror("Error", "Please select both files")
            return
            
        self.watcher.start(self.state_var.get(), self.action_var.get())
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log_msg("AI started monitoring...")
        
    def stop_ai(self):
        self.watcher.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log_msg("AI stopped.")
        
    def on_game_update(self, game_data):
        decision = self.ai.make_decision(game_data)
        with open(self.action_var.get(), 'w') as f:
            json.dump(decision, f)
        self.log_msg(f"AI decision: {decision['action']} - {decision['reason']}")
        
    def log_msg(self, msg):
        self.log.insert("end", f"{msg}\n")
        self.log.see("end")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AIApp()
    app.run()