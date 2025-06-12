#!/usr/bin/env python3
"""
Heroes III AI Opponent - Standalone Game Simulator
Play directly against AI without needing VCMI setup
"""

import json
import random
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class GameState:
    def __init__(self):
        self.turn = 1
        self.current_player = "human"
        self.human_resources = {"gold": 1000, "wood": 10, "ore": 10}
        self.ai_resources = {"gold": 1000, "wood": 10, "ore": 10}
        self.human_army = {"archers": 20, "swordsmen": 15}
        self.ai_army = {"archers": 18, "swordsmen": 12}
        self.map_locations = {
            "mine": {"owner": None, "income": 500},
            "castle": {"owner": None, "defense": 100},
            "artifact": {"owner": None, "bonus": "attack+2"}
        }
        self.game_over = False
        self.winner = None

class HeroesAI:
    def __init__(self):
        self.strategy = "balanced"
        
    def make_decision(self, game_state):
        """AI decides what action to take"""
        ai_gold = game_state.ai_resources["gold"]
        turn = game_state.turn
        
        # Early game: focus on resources
        if turn <= 5:
            if ai_gold >= 800:
                return {"action": "recruit", "units": "archers", "amount": 10, "cost": 600}
            else:
                return {"action": "capture", "target": "mine", "reason": "Need income"}
        
        # Mid game: balanced approach
        elif turn <= 10:
            if ai_gold >= 1200:
                return {"action": "recruit", "units": "swordsmen", "amount": 8, "cost": 800}
            else:
                return {"action": "capture", "target": "castle", "reason": "Strategic position"}
        
        # Late game: aggressive
        else:
            if sum(game_state.ai_army.values()) >= sum(game_state.human_army.values()):
                return {"action": "attack", "target": "human", "reason": "Strong enough to attack"}
            else:
                return {"action": "recruit", "units": "swordsmen", "amount": 5, "cost": 500}

class GameEngine:
    def __init__(self, ui_callback):
        self.state = GameState()
        self.ai = HeroesAI()
        self.ui_callback = ui_callback
        
    def process_human_action(self, action):
        """Process human player action"""
        if action["type"] == "recruit":
            cost = action["cost"]
            if self.state.human_resources["gold"] >= cost:
                self.state.human_resources["gold"] -= cost
                unit_type = action["units"]
                amount = action["amount"]
                if unit_type in self.state.human_army:
                    self.state.human_army[unit_type] += amount
                else:
                    self.state.human_army[unit_type] = amount
                return True, f"Recruited {amount} {unit_type}"
            else:
                return False, "Not enough gold"
                
        elif action["type"] == "capture":
            target = action["target"]
            if target in self.state.map_locations:
                location = self.state.map_locations[target]
                if location["owner"] != "human":
                    location["owner"] = "human"
                    if target == "mine":
                        self.state.human_resources["gold"] += location["income"]
                    return True, f"Captured {target}"
                else:
                    return False, f"Already own {target}"
            else:
                return False, "Invalid target"
                
        elif action["type"] == "attack":
            return self.resolve_combat("human", "ai")
            
        return False, "Invalid action"
    
    def process_ai_turn(self):
        """AI takes its turn"""
        decision = self.ai.make_decision(self.state)
        
        if decision["action"] == "recruit":
            cost = decision["cost"]
            if self.state.ai_resources["gold"] >= cost:
                self.state.ai_resources["gold"] -= cost
                unit_type = decision["units"]
                amount = decision["amount"]
                if unit_type in self.state.ai_army:
                    self.state.ai_army[unit_type] += amount
                else:
                    self.state.ai_army[unit_type] = amount
                return f"AI recruited {amount} {unit_type}"
            else:
                return "AI tried to recruit but lacks gold"
                
        elif decision["action"] == "capture":
            target = decision["target"]
            if target in self.state.map_locations:
                location = self.state.map_locations[target]
                if location["owner"] != "ai":
                    location["owner"] = "ai"
                    if target == "mine":
                        self.state.ai_resources["gold"] += location["income"]
                    return f"AI captured {target}"
                else:
                    return f"AI already owns {target}"
                    
        elif decision["action"] == "attack":
            success, result = self.resolve_combat("ai", "human")
            return f"AI attacked: {result}"
            
        return f"AI: {decision['action']} - {decision.get('reason', '')}"
    
    def resolve_combat(self, attacker, defender):
        """Resolve combat between armies"""
        if attacker == "human":
            att_army = self.state.human_army
            def_army = self.state.ai_army
        else:
            att_army = self.state.ai_army
            def_army = self.state.human_army
            
        att_power = sum(att_army.values())
        def_power = sum(def_army.values())
        
        # Simple combat resolution with randomness
        att_roll = att_power * random.uniform(0.8, 1.2)
        def_roll = def_power * random.uniform(0.8, 1.2)
        
        if att_roll > def_roll:
            # Attacker wins
            damage_ratio = 0.3
            for unit in def_army:
                def_army[unit] = max(0, int(def_army[unit] * (1 - damage_ratio)))
            
            if sum(def_army.values()) == 0:
                self.game_over = True
                self.winner = attacker
                return True, f"{attacker.title()} wins the game!"
            else:
                return True, f"{attacker.title()} wins battle, {defender} army weakened"
        else:
            # Defender wins
            damage_ratio = 0.2
            for unit in att_army:
                att_army[unit] = max(0, int(att_army[unit] * (1 - damage_ratio)))
            return False, f"{defender.title()} defends successfully"
    
    def next_turn(self):
        """Advance to next turn"""
        self.state.turn += 1
        
        # Income phase
        for location, data in self.state.map_locations.items():
            if data["owner"] == "human" and location == "mine":
                self.state.human_resources["gold"] += data["income"] // 2
            elif data["owner"] == "ai" and location == "mine":
                self.state.ai_resources["gold"] += data["income"] // 2
    
    def get_game_status(self):
        """Get current game status for display"""
        return {
            "turn": self.state.turn,
            "human_resources": self.state.human_resources.copy(),
            "ai_resources": self.state.ai_resources.copy(),
            "human_army": self.state.human_army.copy(),
            "ai_army": self.state.ai_army.copy(),
            "map_locations": self.state.map_locations.copy(),
            "game_over": self.state.game_over,
            "winner": self.state.winner
        }

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.engine = GameEngine(self.update_display)
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        self.root.title("Heroes III vs AI")
        self.root.geometry("600x500")
        
        # Game status frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.turn_label = ttk.Label(status_frame, text="Turn 1", font=("Arial", 12, "bold"))
        self.turn_label.pack()
        
        # Resources frame
        res_frame = ttk.LabelFrame(self.root, text="Resources")
        res_frame.pack(fill="x", padx=10, pady=5)
        
        self.human_res_label = ttk.Label(res_frame, text="Your Gold: 1000")
        self.human_res_label.pack(anchor="w")
        
        self.ai_res_label = ttk.Label(res_frame, text="AI Gold: 1000")
        self.ai_res_label.pack(anchor="w")
        
        # Armies frame
        army_frame = ttk.LabelFrame(self.root, text="Armies")
        army_frame.pack(fill="x", padx=10, pady=5)
        
        self.human_army_label = ttk.Label(army_frame, text="Your Army: ")
        self.human_army_label.pack(anchor="w")
        
        self.ai_army_label = ttk.Label(army_frame, text="AI Army: ")
        self.ai_army_label.pack(anchor="w")
        
        # Map locations frame
        map_frame = ttk.LabelFrame(self.root, text="Map Locations")
        map_frame.pack(fill="x", padx=10, pady=5)
        
        self.map_label = ttk.Label(map_frame, text="")
        self.map_label.pack(anchor="w")
        
        # Actions frame
        action_frame = ttk.LabelFrame(self.root, text="Your Actions")
        action_frame.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ttk.Frame(action_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Recruit Archers (600g)", 
                  command=lambda: self.player_action("recruit", "archers", 10, 600)).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Recruit Swordsmen (800g)", 
                  command=lambda: self.player_action("recruit", "swordsmen", 8, 800)).pack(side="left", padx=5)
        
        btn_frame2 = ttk.Frame(action_frame)
        btn_frame2.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame2, text="Capture Mine", 
                  command=lambda: self.player_action("capture", "mine")).pack(side="left", padx=5)
        ttk.Button(btn_frame2, text="Capture Castle", 
                  command=lambda: self.player_action("capture", "castle")).pack(side="left", padx=5)
        ttk.Button(btn_frame2, text="Attack AI", 
                  command=lambda: self.player_action("attack", "ai")).pack(side="left", padx=5)
        
        # End turn button
        ttk.Button(self.root, text="End Turn", command=self.end_turn, 
                  style="Accent.TButton").pack(pady=10)
        
        # Log area
        ttk.Label(self.root, text="Game Log:").pack(anchor="w", padx=10)
        self.log_text = tk.Text(self.root, height=8, wrap="word")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.log("Game started! Choose your actions and click End Turn.")
        
    def player_action(self, action_type, target, amount=0, cost=0):
        """Handle player action"""
        action = {
            "type": action_type,
            "target": target,
            "amount": amount,
            "cost": cost,
            "units": target if action_type == "recruit" else None
        }
        
        success, message = self.engine.process_human_action(action)
        self.log(f"You: {message}")
        self.update_display()
        
        if self.engine.state.game_over:
            self.show_game_over()
            
    def end_turn(self):
        """End current turn and let AI play"""
        self.log("--- Turn ended ---")
        
        # AI turn
        ai_result = self.engine.process_ai_turn()
        self.log(f"AI: {ai_result}")
        
        # Next turn
        self.engine.next_turn()
        self.update_display()
        
        if self.engine.state.game_over:
            self.show_game_over()
        else:
            self.log(f"--- Turn {self.engine.state.turn} begins ---")
            
    def update_display(self):
        """Update all display elements"""
        status = self.engine.get_game_status()
        
        self.turn_label.config(text=f"Turn {status['turn']}")
        self.human_res_label.config(text=f"Your Gold: {status['human_resources']['gold']}")
        self.ai_res_label.config(text=f"AI Gold: {status['ai_resources']['gold']}")
        
        human_army_text = ", ".join([f"{k}: {v}" for k, v in status['human_army'].items()])
        ai_army_text = ", ".join([f"{k}: {v}" for k, v in status['ai_army'].items()])
        
        self.human_army_label.config(text=f"Your Army: {human_army_text}")
        self.ai_army_label.config(text=f"AI Army: {ai_army_text}")
        
        map_text = ""
        for location, data in status['map_locations'].items():
            owner = data['owner'] or 'neutral'
            map_text += f"{location.title()}: {owner}  "
        self.map_label.config(text=map_text)
        
    def show_game_over(self):
        """Show game over dialog"""
        winner = self.engine.state.winner
        if winner == "human":
            messagebox.showinfo("Victory!", "Congratulations! You defeated the AI!")
        else:
            messagebox.showinfo("Defeat", "The AI has conquered your forces!")
            
    def log(self, message):
        """Add message to game log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
        
    def run(self):
        """Run the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = GameUI()
    game.run()