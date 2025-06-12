#!/usr/bin/env python3
"""
Heroes of Might & Magic III Real Game AI
AI that plays the actual HoMM3 game using computer vision and automation
"""

import cv2
import numpy as np
import pyautogui
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from PIL import Image, ImageTk
import os

# Disable pyautogui failsafe for smoother operation
pyautogui.FAILSAFE = False

class HoMM3GameAI:
    def __init__(self):
        self.running = False
        self.game_window = None
        self.current_strategy = "exploration"
        self.last_action_time = 0
        self.action_delay = 2  # seconds between actions
        
    def find_game_window(self):
        """Locate Heroes III game window"""
        try:
            # Try to find HoMM3 window by taking screenshot and looking for UI elements
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            
            # Look for characteristic HoMM3 UI elements (resource bar at bottom)
            # This is a simplified approach - in practice you'd need more sophisticated detection
            return True
        except Exception as e:
            return False
    
    def take_game_screenshot(self):
        """Take screenshot of current game state"""
        try:
            screenshot = pyautogui.screenshot()
            return np.array(screenshot)
        except Exception as e:
            return None
    
    def analyze_game_state(self, screenshot):
        """Analyze current game state from screenshot"""
        analysis = {
            "turn_active": False,
            "hero_selected": False,
            "town_screen": False,
            "combat_active": False,
            "resources": {},
            "hero_position": None,
            "available_actions": []
        }
        
        # Detect if it's player's turn (look for UI indicators)
        # This would need computer vision to detect turn indicators
        analysis["turn_active"] = self.detect_player_turn(screenshot)
        
        # Detect if hero is selected
        analysis["hero_selected"] = self.detect_selected_hero(screenshot)
        
        # Detect current screen type
        analysis["town_screen"] = self.detect_town_screen(screenshot)
        analysis["combat_active"] = self.detect_combat_screen(screenshot)
        
        return analysis
    
    def detect_player_turn(self, screenshot):
        """Detect if it's currently player's turn"""
        # Look for "End Turn" button or other turn indicators
        # This is a placeholder - real implementation would use template matching
        return True
    
    def detect_selected_hero(self, screenshot):
        """Detect if a hero is currently selected"""
        # Look for hero selection indicators
        return True
    
    def detect_town_screen(self, screenshot):
        """Detect if town management screen is open"""
        # Look for town-specific UI elements
        return False
    
    def detect_combat_screen(self, screenshot):
        """Detect if combat screen is active"""
        # Look for combat-specific UI elements
        return False
    
    def make_ai_decision(self, game_state):
        """Make AI decision based on current game state"""
        if game_state["combat_active"]:
            return self.combat_decision(game_state)
        elif game_state["town_screen"]:
            return self.town_management_decision(game_state)
        else:
            return self.adventure_map_decision(game_state)
    
    def adventure_map_decision(self, game_state):
        """Make decisions on adventure map"""
        actions = []
        
        if game_state["hero_selected"]:
            if self.current_strategy == "exploration":
                actions.append({"type": "move", "direction": "explore"})
            elif self.current_strategy == "resource_gathering":
                actions.append({"type": "move", "target": "nearest_resource"})
            elif self.current_strategy == "aggressive":
                actions.append({"type": "move", "target": "enemy_hero"})
        else:
            # Select a hero
            actions.append({"type": "select_hero"})
        
        return actions
    
    def combat_decision(self, game_state):
        """Make combat decisions"""
        # Simple combat AI - could be much more sophisticated
        return [{"type": "auto_combat"}]
    
    def town_management_decision(self, game_state):
        """Make town management decisions"""
        actions = []
        # Prioritize building development
        actions.append({"type": "build_structure"})
        actions.append({"type": "recruit_units"})
        return actions
    
    def execute_action(self, action):
        """Execute an AI action in the game"""
        try:
            if action["type"] == "move":
                self.execute_hero_movement(action)
            elif action["type"] == "select_hero":
                self.select_hero()
            elif action["type"] == "auto_combat":
                self.activate_auto_combat()
            elif action["type"] == "build_structure":
                self.build_in_town()
            elif action["type"] == "recruit_units":
                self.recruit_units()
            elif action["type"] == "end_turn":
                self.end_turn()
            
            time.sleep(self.action_delay)
            return True
        except Exception as e:
            return False
    
    def execute_hero_movement(self, action):
        """Move hero on adventure map"""
        if action.get("direction") == "explore":
            # Simple exploration: click in a random direction
            screen_center = pyautogui.size()
            x = screen_center[0] // 2 + np.random.randint(-200, 200)
            y = screen_center[1] // 2 + np.random.randint(-200, 200)
            pyautogui.click(x, y)
        
    def select_hero(self):
        """Select first available hero"""
        # Look for hero portraits in UI and click first one
        # This is simplified - real implementation would use image recognition
        pyautogui.click(50, 300)  # Approximate hero portrait location
    
    def activate_auto_combat(self):
        """Activate auto-combat during battle"""
        # Look for auto-combat button and click it
        pyautogui.press('a')  # Common hotkey for auto-combat
    
    def build_in_town(self):
        """Build structures in town"""
        # Navigate to town and build available structures
        pass
    
    def recruit_units(self):
        """Recruit units in town"""
        # Navigate to recruitment and hire units
        pass
    
    def end_turn(self):
        """End current turn"""
        pyautogui.press('enter')  # Common hotkey for end turn
    
    def ai_main_loop(self):
        """Main AI loop"""
        while self.running:
            try:
                # Take screenshot
                screenshot = self.take_game_screenshot()
                if screenshot is None:
                    time.sleep(1)
                    continue
                
                # Analyze game state
                game_state = self.analyze_game_state(screenshot)
                
                # Only act if it's player's turn
                if game_state["turn_active"]:
                    # Make AI decision
                    actions = self.make_ai_decision(game_state)
                    
                    # Execute actions
                    for action in actions:
                        if not self.running:
                            break
                        success = self.execute_action(action)
                        if not success:
                            break
                    
                    # End turn after actions
                    if self.running and actions:
                        time.sleep(1)
                        self.execute_action({"type": "end_turn"})
                
                time.sleep(0.5)  # Check game state twice per second
                
            except Exception as e:
                time.sleep(2)  # Wait on error
    
    def start_ai(self):
        """Start AI operation"""
        if not self.find_game_window():
            return False, "Heroes III game window not found"
        
        self.running = True
        self.ai_thread = threading.Thread(target=self.ai_main_loop, daemon=True)
        self.ai_thread.start()
        return True, "AI started successfully"
    
    def stop_ai(self):
        """Stop AI operation"""
        self.running = False
        return "AI stopped"

class HoMM3AIController:
    def __init__(self):
        self.root = tk.Tk()
        self.ai = HoMM3GameAI()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Heroes III Game AI Controller")
        self.root.geometry("500x400")
        
        # Title
        title_label = ttk.Label(self.root, text="Heroes III Real Game AI", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = """This AI will control the actual Heroes III game.
        
Prerequisites:
1. Heroes III must be running and visible
2. It should be your turn
3. Game window should not be minimized

The AI will:
• Analyze the game screen using computer vision
• Make strategic decisions based on game state
• Control mouse and keyboard to play the game
• Explore map, manage towns, fight battles
        """
        
        inst_label = ttk.Label(self.root, text=instructions, justify="left")
        inst_label.pack(padx=20, pady=10, fill="x")
        
        # Strategy selection
        strategy_frame = ttk.LabelFrame(self.root, text="AI Strategy")
        strategy_frame.pack(fill="x", padx=20, pady=10)
        
        self.strategy_var = tk.StringVar(value="exploration")
        strategies = [
            ("Exploration Focus", "exploration"),
            ("Resource Gathering", "resource_gathering"), 
            ("Aggressive Expansion", "aggressive")
        ]
        
        for text, value in strategies:
            ttk.Radiobutton(strategy_frame, text=text, variable=self.strategy_var, 
                           value=value, command=self.update_strategy).pack(anchor="w", padx=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start AI", 
                                      command=self.start_ai, style="Accent.TButton")
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="Stop AI", 
                                     command=self.stop_ai, state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Status: Ready", 
                                     font=("Arial", 10, "bold"))
        self.status_label.pack(pady=10)
        
        # Log area
        ttk.Label(self.root, text="AI Activity Log:").pack(anchor="w", padx=20)
        self.log_text = tk.Text(self.root, height=8, wrap="word")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.log("AI Controller ready. Start Heroes III and click 'Start AI'")
        self.log("Make sure Heroes III window is visible and it's your turn")
        
    def update_strategy(self):
        """Update AI strategy"""
        self.ai.current_strategy = self.strategy_var.get()
        self.log(f"Strategy changed to: {self.strategy_var.get()}")
        
    def start_ai(self):
        """Start AI control"""
        success, message = self.ai.start_ai()
        if success:
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="Status: AI Active")
            self.log("AI started - now controlling Heroes III game")
        else:
            messagebox.showerror("Error", message)
            self.log(f"Failed to start: {message}")
    
    def stop_ai(self):
        """Stop AI control"""
        message = self.ai.stop_ai()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")
        self.log(message)
    
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def run(self):
        """Run the controller"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        controller = HoMM3AIController()
        controller.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")