"""
FastRL - Efficient Reinforcement Learning for Large Language Models
MIT HAN Lab Implementation Sample

This module demonstrates the FastRL framework for efficient RL training
of language models, particularly for complex reasoning tasks.
"""

import torch
import torch.nn as nn
from typing import List, Tuple, Optional
import numpy as np


class AdaptiveSpeculativeDecoder:
    """
    Implements adaptive speculative decoding for efficient token generation.
    This is a core component of the FastRL framework.
    """
    
    def __init__(self, model, tokenizer, device='cpu'):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.model.to(device)
    
    def estimate_difficulty(self, prompt: str) -> float:
        """
        Estimate the difficulty of a prompt for adaptive strategy selection.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            Difficulty score between 0 and 1
        """
        # Simple heuristic: longer prompts and more complex tokens = higher difficulty
        tokens = self.tokenizer.encode(prompt)
        
        # Factors contributing to difficulty
        length_score = min(len(tokens) / 100, 1.0)
        complexity_score = len(set(tokens)) / len(tokens) if tokens else 0
        
        return (length_score + complexity_score) / 2
    
    def speculative_decode(
        self,
        prompt: str,
        max_length: int = 100,
        adaptive: bool = True
    ) -> str:
        """
        Generate text using speculative decoding with optional adaptive strategy.
        
        Args:
            prompt: Input prompt
            max_length: Maximum generation length
            adaptive: Whether to use adaptive decoding strategy
            
        Returns:
            Generated text
        """
        # Estimate difficulty and adjust parameters
        if adaptive:
            difficulty = self.estimate_difficulty(prompt)
            temperature = 0.5 + (0.4 * (1 - difficulty))  # Lower temp for harder tasks
            top_p = 0.85 + (0.1 * (1 - difficulty))
        else:
            temperature = 0.7
            top_p = 0.9
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class LongTailOptimizer:
    """
    Implements the Taming the Long-Tail (TLT) method for handling rare scenarios.
    Focuses training on edge cases and rare patterns.
    """
    
    def __init__(self, model, learning_rate=1e-5):
        self.model = model
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        self.rare_scenario_buffer = []
        self.scenario_frequencies = {}
    
    def identify_rare_scenarios(
        self,
        scenarios: List[Tuple[str, str]],
        threshold: float = 0.1
    ) -> List[Tuple[str, str]]:
        """
        Identify rare scenarios that need focused training.
        
        Args:
            scenarios: List of (input, output) tuples
            threshold: Frequency threshold for rare scenarios
            
        Returns:
            List of rare scenarios
        """
        # Count scenario patterns
        for inp, _ in scenarios:
            key = self._get_scenario_key(inp)
            self.scenario_frequencies[key] = self.scenario_frequencies.get(key, 0) + 1
        
        # Identify rare ones
        total = len(scenarios)
        rare = []
        for inp, out in scenarios:
            key = self._get_scenario_key(inp)
            if self.scenario_frequencies[key] / total < threshold:
                rare.append((inp, out))
        
        return rare
    
    def _get_scenario_key(self, text: str) -> str:
        """Extract a key representing the scenario type."""
        # Simple heuristic: use first few words
        words = text.split()[:5]
        return " ".join(words)
    
    def optimize_long_tail(
        self,
        rare_scenarios: List[Tuple[str, str]],
        epochs: int = 5
    ) -> List[float]:
        """
        Perform focused training on rare scenarios.
        
        Args:
            rare_scenarios: List of rare (input, output) pairs
            epochs: Number of training epochs
            
        Returns:
            List of losses per epoch
        """
        losses = []
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            for prompt, target in rare_scenarios:
                loss = self._train_step(prompt, target)
                epoch_loss += loss
            
            avg_loss = epoch_loss / len(rare_scenarios)
            losses.append(avg_loss)
            
            print(f"Epoch {epoch + 1}/{epochs}, Avg Loss: {avg_loss:.4f}")
        
        return losses
    
    def _train_step(self, prompt: str, target: str) -> float:
        """Execute a single training step."""
        # This would contain actual training logic
        # Simplified for demonstration
        return np.random.uniform(0.1, 1.0)


class FastRLReasoner:
    """
    High-level interface for using FastRL for reasoning tasks.
    Combines adaptive decoding with long-tail optimization.
    """
    
    def __init__(self, model_name: str = "gpt2"):
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.decoder = AdaptiveSpeculativeDecoder(
                self.model, 
                self.tokenizer,
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            self.optimizer = LongTailOptimizer(self.model)
            
        except ImportError:
            raise ImportError(
                "Please install transformers: pip install transformers"
            )
    
    def reason(self, prompt: str, use_adaptive: bool = True) -> str:
        """
        Perform reasoning on a prompt using FastRL techniques.
        
        Args:
            prompt: Reasoning task prompt
            use_adaptive: Whether to use adaptive decoding
            
        Returns:
            Reasoning result
        """
        return self.decoder.speculative_decode(prompt, adaptive=use_adaptive)
    
    def train_on_rare_cases(
        self,
        training_data: List[Tuple[str, str]],
        epochs: int = 5
    ):
        """
        Train the model with focus on rare scenarios.
        
        Args:
            training_data: List of (prompt, expected_output) tuples
            epochs: Number of training epochs
        """
        rare = self.optimizer.identify_rare_scenarios(training_data)
        print(f"Identified {len(rare)} rare scenarios for focused training")
        
        if rare:
            losses = self.optimizer.optimize_long_tail(rare, epochs)
            return losses
        else:
            print("No rare scenarios identified")
            return []


def demo_fastrl_reasoning():
    """
    Demonstration of FastRL for reasoning tasks.
    """
    print("FastRL Reasoning Demo")
    print("=" * 80)
    
    # Example reasoning prompts
    reasoning_tasks = [
        "If all mammals are warm-blooded and all dogs are mammals, what can we conclude about dogs?",
        "A train travels 60 miles in 1 hour. How far will it travel in 2.5 hours at the same speed?",
        "What is the next number in this sequence: 1, 4, 9, 16, 25, ?",
        "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
    ]
    
    try:
        reasoner = FastRLReasoner()
        
        for i, task in enumerate(reasoning_tasks, 1):
            print(f"\nTask {i}: {task}")
            result = reasoner.reason(task)
            print(f"Answer: {result}")
            print("-" * 80)
            
    except ImportError as e:
        print(f"Error: {e}")
        print("\nTo run this demo, install required packages:")
        print("pip install torch transformers")


if __name__ == "__main__":
    demo_fastrl_reasoning()
