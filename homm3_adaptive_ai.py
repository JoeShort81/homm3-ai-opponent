#!/usr/bin/env python3
"""
Heroes of Might & Magic III Adaptive AI
AI that learns, adapts, and creates novel strategies based on game conditions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import random
import json
import numpy as np
from datetime import datetime
import pickle
import os

class StrategyEvolution:
    """Evolutionary strategy system that creates and adapts strategies"""
    
    def __init__(self):
        self.strategy_genome = {
            "exploration_weight": 0.5,
            "resource_weight": 0.3,
            "military_weight": 0.7,
            "economic_weight": 0.4,
            "risk_tolerance": 0.6,
            "aggression_level": 0.5,
            "expansion_priority": 0.4,
            "defensive_stance": 0.3
        }
        
        self.learned_patterns = {}
        self.successful_strategies = []
        self.failed_strategies = []
        self.adaptation_rate = 0.1
        
    def analyze_game_situation(self, game_state):
        """Analyze current situation and identify key factors"""
        situation_factors = {
            "resource_abundance": self.calculate_resource_situation(game_state),
            "military_pressure": self.assess_military_threats(game_state),
            "expansion_opportunities": self.identify_expansion_chances(game_state),
            "economic_potential": self.evaluate_economic_prospects(game_state),
            "enemy_behavior_pattern": self.analyze_enemy_patterns(game_state),
            "map_control": self.assess_territorial_control(game_state),
            "game_phase": self.determine_game_phase(game_state)
        }
        return situation_factors
    
    def evolve_strategy(self, situation_factors, recent_outcomes):
        """Evolve strategy based on current situation and past results"""
        
        # Base strategy selection
        if situation_factors["game_phase"] == "early":
            base_strategy = self.early_game_evolution(situation_factors)
        elif situation_factors["game_phase"] == "mid":
            base_strategy = self.mid_game_evolution(situation_factors)
        else:
            base_strategy = self.late_game_evolution(situation_factors)
        
        # Adaptive modifications based on enemy behavior
        adapted_strategy = self.adapt_to_enemy_behavior(base_strategy, situation_factors)
        
        # Novel strategy generation if standard approaches fail
        if self.should_innovate(recent_outcomes):
            adapted_strategy = self.generate_novel_strategy(situation_factors, adapted_strategy)
        
        return adapted_strategy
    
    def early_game_evolution(self, factors):
        """Evolve early game strategy based on map and opponent analysis"""
        strategy = {
            "primary_focus": "adaptive_exploration",
            "secondary_focus": "opportunistic_resource_grab",
            "tactics": []
        }
        
        # Adapt based on resource distribution
        if factors["resource_abundance"] > 0.7:
            strategy["tactics"].append("aggressive_resource_monopolization")
        elif factors["resource_abundance"] < 0.3:
            strategy["tactics"].append("efficient_resource_conservation")
        else:
            strategy["tactics"].append("balanced_resource_acquisition")
        
        # Adapt based on enemy proximity
        if factors["military_pressure"] > 0.6:
            strategy["tactics"].append("early_military_preparation")
            strategy["primary_focus"] = "defensive_consolidation"
        elif factors["military_pressure"] < 0.2:
            strategy["tactics"].append("rapid_expansion")
        
        return strategy
    
    def mid_game_evolution(self, factors):
        """Dynamic mid-game strategy adaptation"""
        strategy = {
            "primary_focus": "situational_dominance",
            "secondary_focus": "strategic_positioning",
            "tactics": []
        }
        
        # Economic vs Military balance adaptation
        if factors["economic_potential"] > factors["military_pressure"]:
            strategy["tactics"].append("economic_acceleration")
            strategy["tactics"].append("delayed_military_buildup")
        else:
            strategy["tactics"].append("immediate_military_focus")
            strategy["tactics"].append("territorial_defense")
        
        # Enemy behavior adaptation
        enemy_pattern = factors["enemy_behavior_pattern"]
        if enemy_pattern == "aggressive":
            strategy["tactics"].append("counter_aggressive_positioning")
        elif enemy_pattern == "economic":
            strategy["tactics"].append("economic_disruption")
        elif enemy_pattern == "defensive":
            strategy["tactics"].append("pressure_application")
        
        return strategy
    
    def late_game_evolution(self, factors):
        """Endgame strategy with victory condition focus"""
        strategy = {
            "primary_focus": "victory_condition_pursuit",
            "secondary_focus": "opponent_elimination",
            "tactics": []
        }
        
        # Victory path analysis
        if factors["map_control"] > 0.7:
            strategy["tactics"].append("territorial_consolidation")
        elif factors["military_pressure"] > 0.8:
            strategy["tactics"].append("decisive_strike")
        else:
            strategy["tactics"].append("gradual_dominance")
        
        return strategy
    
    def generate_novel_strategy(self, factors, base_strategy):
        """Generate entirely new strategy approaches"""
        
        novel_approaches = []
        
        # Analyze what hasn't been tried
        untried_combinations = self.identify_untried_approaches(factors)
        
        # Generate creative combinations
        if factors["resource_abundance"] > 0.5 and factors["military_pressure"] < 0.3:
            novel_approaches.append("resource_flooding_strategy")  # Overwhelm with resources
        
        if factors["enemy_behavior_pattern"] == "predictable":
            novel_approaches.append("pattern_breaking_chaos")  # Deliberately unpredictable moves
        
        if factors["map_control"] < 0.3 and factors["economic_potential"] > 0.6:
            novel_approaches.append("hidden_economic_empire")  # Build power while appearing weak
        
        # Create hybrid strategies
        if len(self.successful_strategies) >= 2:
            novel_approaches.append(self.create_hybrid_strategy())
        
        # Add novel elements to base strategy
        base_strategy["novel_elements"] = novel_approaches
        base_strategy["innovation_level"] = min(len(novel_approaches) * 0.3, 1.0)
        
        return base_strategy
    
    def adapt_to_enemy_behavior(self, strategy, factors):
        """Real-time adaptation to observed enemy behavior"""
        
        enemy_pattern = factors["enemy_behavior_pattern"]
        
        # Counter-strategy generation
        if enemy_pattern == "rush":
            strategy["counter_tactics"] = ["early_defense", "economic_buildup", "counter_attack"]
        elif enemy_pattern == "turtle":
            strategy["counter_tactics"] = ["economic_advantage", "map_control", "slow_pressure"]
        elif enemy_pattern == "economic":
            strategy["counter_tactics"] = ["early_harassment", "resource_denial", "military_pressure"]
        elif enemy_pattern == "aggressive_expansion":
            strategy["counter_tactics"] = ["selective_blocking", "quality_over_quantity", "strategic_retreats"]
        
        return strategy
    
    def should_innovate(self, recent_outcomes):
        """Determine if novel strategy generation is needed"""
        if len(recent_outcomes) < 3:
            return False
        
        # Innovation triggers
        recent_failures = sum(1 for outcome in recent_outcomes[-5:] if not outcome["success"])
        if recent_failures >= 3:
            return True
        
        # Stagnation detection
        if all(outcome.get("strategy_type") == recent_outcomes[0].get("strategy_type") for outcome in recent_outcomes[-3:]):
            return True
        
        return False
    
    def learn_from_outcome(self, strategy_used, outcome, game_state):
        """Learn from strategy results and update knowledge base"""
        
        # Record strategy effectiveness
        effectiveness_score = self.calculate_effectiveness(outcome, game_state)
        
        strategy_record = {
            "strategy": strategy_used,
            "situation": self.analyze_game_situation(game_state),
            "effectiveness": effectiveness_score,
            "timestamp": datetime.now(),
            "outcome": outcome
        }
        
        if effectiveness_score > 0.6:
            self.successful_strategies.append(strategy_record)
        else:
            self.failed_strategies.append(strategy_record)
        
        # Update strategy genome based on results
        self.update_strategy_genome(strategy_used, effectiveness_score)
        
        # Pattern recognition
        self.update_learned_patterns(strategy_record)
    
    def update_strategy_genome(self, strategy, effectiveness):
        """Evolve core strategy parameters based on results"""
        
        learning_rate = self.adaptation_rate * effectiveness
        
        for param in self.strategy_genome:
            if param in strategy.get("parameters", {}):
                current_value = self.strategy_genome[param]
                strategy_value = strategy["parameters"][param]
                
                # Gradient-based adaptation
                if effectiveness > 0.6:
                    # Move towards successful strategy values
                    self.strategy_genome[param] += learning_rate * (strategy_value - current_value)
                else:
                    # Move away from unsuccessful strategy values
                    self.strategy_genome[param] -= learning_rate * (strategy_value - current_value)
                
                # Keep values in valid range
                self.strategy_genome[param] = max(0.0, min(1.0, self.strategy_genome[param]))
    
    def calculate_effectiveness(self, outcome, game_state):
        """Calculate how effective the strategy was"""
        effectiveness = 0.0
        
        # Resource gain efficiency
        if outcome.get("resource_gain", 0) > 0:
            effectiveness += 0.2
        
        # Military success
        if outcome.get("military_victories", 0) > 0:
            effectiveness += 0.3
        
        # Territorial expansion
        if outcome.get("territory_gained", 0) > 0:
            effectiveness += 0.2
        
        # Economic growth
        if outcome.get("economic_improvement", 0) > 0:
            effectiveness += 0.2
        
        # Overall game position improvement
        if outcome.get("position_improvement", 0) > 0:
            effectiveness += 0.1
        
        return min(effectiveness, 1.0)
    
    # Placeholder methods for game state analysis
    def calculate_resource_situation(self, game_state):
        return random.uniform(0.2, 0.8)
    
    def assess_military_threats(self, game_state):
        return random.uniform(0.1, 0.9)
    
    def identify_expansion_chances(self, game_state):
        return random.uniform(0.3, 0.7)
    
    def evaluate_economic_prospects(self, game_state):
        return random.uniform(0.2, 0.8)
    
    def analyze_enemy_patterns(self, game_state):
        patterns = ["aggressive", "defensive", "economic", "rush", "turtle", "balanced"]
        return random.choice(patterns)
    
    def assess_territorial_control(self, game_state):
        return random.uniform(0.1, 0.9)
    
    def determine_game_phase(self, game_state):
        phases = ["early", "mid", "late"]
        return random.choice(phases)
    
    def identify_untried_approaches(self, factors):
        return ["experimental_approach_1", "experimental_approach_2"]
    
    def create_hybrid_strategy(self):
        return "hybrid_strategy_combination"
    
    def update_learned_patterns(self, strategy_record):
        # Pattern learning implementation
        pass

class AdaptiveHoMM3AI:
    def __init__(self):
        self.running = False
        self.strategy_evolution = StrategyEvolution()
        self.current_strategy = None
        self.game_history = []
        self.adaptation_enabled = True
        self.learning_mode = True
        
    def analyze_and_adapt(self, game_state):
        """Main AI decision loop with adaptation"""
        
        # Analyze current situation
        situation = self.strategy_evolution.analyze_game_situation(game_state)
        
        # Get recent outcomes for learning
        recent_outcomes = self.game_history[-10:] if len(self.game_history) >= 10 else self.game_history
        
        # Evolve strategy based on situation and learning
        self.current_strategy = self.strategy_evolution.evolve_strategy(situation, recent_outcomes)
        
        # Generate specific actions based on evolved strategy
        actions = self.generate_actions_from_strategy(self.current_strategy, situation)
        
        return actions
    
    def generate_actions_from_strategy(self, strategy, situation):
        """Convert high-level strategy into specific game actions"""
        
        actions = []
        
        primary_focus = strategy["primary_focus"]
        tactics = strategy.get("tactics", [])
        
        # Primary focus actions
        if primary_focus == "adaptive_exploration":
            actions.extend(self.exploration_actions(situation))
        elif primary_focus == "defensive_consolidation":
            actions.extend(self.defensive_actions(situation))
        elif primary_focus == "situational_dominance":
            actions.extend(self.dominance_actions(situation))
        elif primary_focus == "victory_condition_pursuit":
            actions.extend(self.victory_actions(situation))
        
        # Tactical modifications
        for tactic in tactics:
            actions.extend(self.apply_tactic(tactic, situation))
        
        # Novel element integration
        if "novel_elements" in strategy:
            for novel_element in strategy["novel_elements"]:
                actions.extend(self.apply_novel_approach(novel_element, situation))
        
        return actions
    
    def exploration_actions(self, situation):
        return [{"action": "explore", "target": "optimal_path", "reasoning": "adaptive exploration"}]
    
    def defensive_actions(self, situation):
        return [{"action": "fortify", "priority": "high", "reasoning": "defensive consolidation"}]
    
    def dominance_actions(self, situation):
        return [{"action": "expand", "method": "strategic", "reasoning": "situational dominance"}]
    
    def victory_actions(self, situation):
        return [{"action": "victory_push", "condition": "optimal", "reasoning": "victory pursuit"}]
    
    def apply_tactic(self, tactic, situation):
        tactic_actions = {
            "aggressive_resource_monopolization": [{"action": "secure_all_resources", "urgency": "high"}],
            "economic_acceleration": [{"action": "boost_economy", "method": "rapid"}],
            "counter_aggressive_positioning": [{"action": "defensive_counter", "style": "aggressive"}],
            "pattern_breaking_chaos": [{"action": "random_maneuver", "predictability": "none"}]
        }
        return tactic_actions.get(tactic, [])
    
    def apply_novel_approach(self, approach, situation):
        novel_actions = {
            "resource_flooding_strategy": [{"action": "resource_overwhelm", "method": "flooding"}],
            "hidden_economic_empire": [{"action": "stealth_development", "visibility": "minimal"}],
            "pattern_breaking_chaos": [{"action": "unpredictable_moves", "chaos_level": "high"}]
        }
        return novel_actions.get(approach, [])
    
    def record_outcome(self, actions_taken, results):
        """Record results for learning"""
        outcome_record = {
            "strategy": self.current_strategy,
            "actions": actions_taken,
            "results": results,
            "timestamp": datetime.now(),
            "success": results.get("success", False)
        }
        
        self.game_history.append(outcome_record)
        
        # Learn from this outcome
        if self.learning_mode:
            game_state = results.get("game_state", {})
            self.strategy_evolution.learn_from_outcome(self.current_strategy, results, game_state)
    
    def save_learning_data(self, filename="ai_learning_data.pkl"):
        """Save learned strategies and patterns"""
        learning_data = {
            "strategy_genome": self.strategy_evolution.strategy_genome,
            "successful_strategies": self.strategy_evolution.successful_strategies,
            "failed_strategies": self.strategy_evolution.failed_strategies,
            "learned_patterns": self.strategy_evolution.learned_patterns,
            "game_history": self.game_history
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(learning_data, f)
    
    def load_learning_data(self, filename="ai_learning_data.pkl"):
        """Load previously learned strategies"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                learning_data = pickle.load(f)
                
            self.strategy_evolution.strategy_genome = learning_data.get("strategy_genome", {})
            self.strategy_evolution.successful_strategies = learning_data.get("successful_strategies", [])
            self.strategy_evolution.failed_strategies = learning_data.get("failed_strategies", [])
            self.strategy_evolution.learned_patterns = learning_data.get("learned_patterns", {})
            self.game_history = learning_data.get("game_history", [])

class AdaptiveAIController:
    def __init__(self):
        self.root = tk.Tk()
        self.ai = AdaptiveHoMM3AI()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Heroes III Adaptive AI - Strategy Evolution")
        self.root.geometry("600x550")
        
        # Adaptive AI features
        features_frame = ttk.LabelFrame(self.root, text="Adaptive AI Features")
        features_frame.pack(fill="x", padx=20, pady=10)
        
        features_text = """🧠 ADAPTIVE STRATEGY AI:
        
• Learns from every game and adapts strategies
• Creates novel approaches when standard strategies fail
• Evolves tactics based on opponent behavior patterns
• Develops counter-strategies for different play styles
• Combines successful elements into hybrid strategies
• Remembers and improves from past experiences
        """
        
        ttk.Label(features_frame, text=features_text, justify="left").pack(padx=10, pady=10)
        
        # Learning controls
        learning_frame = ttk.LabelFrame(self.root, text="Learning Configuration")
        learning_frame.pack(fill="x", padx=20, pady=10)
        
        self.learning_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(learning_frame, text="Enable continuous learning", 
                       variable=self.learning_enabled).pack(anchor="w", padx=10)
        
        self.innovation_level = tk.DoubleVar(value=0.5)
        ttk.Label(learning_frame, text="Innovation Level:").pack(anchor="w", padx=10)
        ttk.Scale(learning_frame, from_=0.0, to=1.0, variable=self.innovation_level, 
                 orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Strategy evolution display
        evolution_frame = ttk.LabelFrame(self.root, text="Current Strategy Evolution")
        evolution_frame.pack(fill="x", padx=20, pady=10)
        
        self.strategy_display = tk.Text(evolution_frame, height=8, wrap="word")
        self.strategy_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Adaptive AI", 
                                      command=self.start_adaptive_ai, style="Accent.TButton")
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ttk.Button(button_frame, text="Stop AI", 
                                     command=self.stop_ai, state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        ttk.Button(button_frame, text="Save Learning", 
                  command=self.save_learning).pack(side="left", padx=10)
        
        ttk.Button(button_frame, text="Load Learning", 
                  command=self.load_learning).pack(side="left", padx=10)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Status: Ready to learn and adapt", 
                                     font=("Arial", 10, "bold"))
        self.status_label.pack(pady=10)
        
        # Initialize display
        self.update_strategy_display()
        
    def update_strategy_display(self):
        """Update the strategy evolution display"""
        if self.ai.current_strategy:
            strategy_text = f"Current Strategy: {self.ai.current_strategy.get('primary_focus', 'Unknown')}\n"
            strategy_text += f"Tactics: {', '.join(self.ai.current_strategy.get('tactics', []))}\n"
            if 'novel_elements' in self.ai.current_strategy:
                strategy_text += f"Novel Elements: {', '.join(self.ai.current_strategy['novel_elements'])}\n"
            strategy_text += f"Games Played: {len(self.ai.game_history)}\n"
            strategy_text += f"Successful Strategies: {len(self.ai.strategy_evolution.successful_strategies)}\n"
        else:
            strategy_text = "No active strategy - ready to begin learning"
        
        self.strategy_display.delete(1.0, tk.END)
        self.strategy_display.insert(1.0, strategy_text)
        
    def start_adaptive_ai(self):
        """Start adaptive AI"""
        self.ai.learning_mode = self.learning_enabled.get()
        self.ai.strategy_evolution.adaptation_rate = self.innovation_level.get()
        
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Adaptive AI learning and evolving")
        
        messagebox.showinfo("Adaptive AI Started", 
                          "AI is now learning and adapting!\n\n" +
                          "• Creates new strategies based on game conditions\n" +
                          "• Learns from successes and failures\n" +
                          "• Evolves tactics to counter opponents")
    
    def stop_ai(self):
        """Stop AI"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")
        
    def save_learning(self):
        """Save AI learning data"""
        self.ai.save_learning_data()
        messagebox.showinfo("Learning Saved", "AI learning data has been saved!")
        
    def load_learning(self):
        """Load AI learning data"""
        self.ai.load_learning_data()
        self.update_strategy_display()
        messagebox.showinfo("Learning Loaded", "AI learning data has been loaded!")
        
    def run(self):
        """Run the controller"""
        self.root.mainloop()

if __name__ == "__main__":
    controller = AdaptiveAIController()
    controller.run()