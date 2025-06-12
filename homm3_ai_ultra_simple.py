#!/usr/bin/env python3
"""
Heroes of Might & Magic III AI Opponent
Ultra-minimal version for .exe building
"""

import json
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class SimpleAI:
    def decide(self, data):
        turn = data.get("turn", 1)
        if turn < 10:
            return {"action": "explore", "reason": "Early game"}
        else:
            return {"action": "attack", "reason": "Late game"}

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.ai = SimpleAI()
        self.watching = False
        self.setup()
        
    def setup(self):
        self.root.title("Heroes III AI")
        self.root.geometry("350x250")
        
        ttk.Label(self.root, text="State File:").pack(pady=5)
        self.state_var = tk.StringVar()
        f1 = ttk.Frame(self.root)
        f1.pack(fill="x", padx=10)
        ttk.Entry(f1, textvariable=self.state_var).pack(side="left", fill="x", expand=True)
        ttk.Button(f1, text="...", command=self.get_state).pack(side="right")
        
        ttk.Label(self.root, text="Action File:").pack(pady=5)
        self.action_var = tk.StringVar()
        f2 = ttk.Frame(self.root)
        f2.pack(fill="x", padx=10)
        ttk.Entry(f2, textvariable=self.action_var).pack(side="left", fill="x", expand=True)
        ttk.Button(f2, text="...", command=self.get_action).pack(side="right")
        
        f3 = ttk.Frame(self.root)
        f3.pack(pady=20)
        self.start_btn = ttk.Button(f3, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(f3, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.log = tk.Text(self.root, height=6)
        self.log.pack(fill="both", expand=True, padx=10, pady=5)
        self.log.insert("end", "Ready!\n")
        
    def get_state(self):
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f: self.state_var.set(f)
            
    def get_action(self):
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f: self.action_var.set(f)
        
    def start(self):
        if not self.state_var.get() or not self.action_var.get():
            messagebox.showerror("Error", "Select files first")
            return
        self.watching = True
        threading.Thread(target=self.watch, daemon=True).start()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log.insert("end", "Started!\n")
        
    def stop(self):
        self.watching = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log.insert("end", "Stopped!\n")
        
    def watch(self):
        last = 0
        while self.watching:
            try:
                if os.path.exists(self.state_var.get()):
                    t = os.path.getmtime(self.state_var.get())
                    if t > last:
                        last = t
                        with open(self.state_var.get()) as f:
                            data = json.load(f)
                        result = self.ai.decide(data)
                        with open(self.action_var.get(), 'w') as f:
                            json.dump(result, f)
                        self.log.insert("end", f"AI: {result['action']}\n")
                        self.log.see("end")
                time.sleep(1)
            except:
                time.sleep(2)
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
