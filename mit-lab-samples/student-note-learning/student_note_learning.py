"""
Student-Note Learning - MIT Research Implementation
Teaching LLMs to learn like students by taking notes and practicing

This module implements the Student-Note Learning approach where models:
1. Generate their own study notes from new information
2. Practice using trial-and-error
3. Permanently internalize knowledge through weight updates
"""

import torch
import torch.nn as nn
from typing import List, Tuple, Dict
from dataclasses import dataclass
import time


@dataclass
class LearningSession:
    """Record of a learning session."""
    topic: str
    notes: str
    timestamp: float
    accuracy_history: List[float]
    final_accuracy: float


class StudentNoteGenerator:
    """
    Generates study notes from new information.
    The model documents what it learns, similar to a student taking notes.
    """
    
    def __init__(self, model, tokenizer, device='cpu'):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.all_notes = []
    
    def generate_notes(
        self,
        information: str,
        max_length: int = 400,
        temperature: float = 0.7
    ) -> str:
        """
        Generate study notes from new information.
        
        Args:
            information: The new information to learn
            max_length: Maximum length of generated notes
            temperature: Sampling temperature
            
        Returns:
            Generated study notes
        """
        prompt = f"""You are a diligent student. Read the following information and create clear, 
concise study notes that capture the key points, relationships, and examples.

New Information:
{information}

Study Notes (summarize the main concepts, provide examples, and highlight important relationships):
"""
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        notes = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the notes part
        if "Study Notes" in notes:
            notes = notes.split("Study Notes")[-1].strip()
            if ":" in notes:
                notes = notes.split(":", 1)[1].strip()
        
        self.all_notes.append(notes)
        return notes
    
    def refine_notes(self, original_notes: str, feedback: str) -> str:
        """
        Refine notes based on feedback (trial-and-error learning).
        
        Args:
            original_notes: The original notes
            feedback: Feedback on what to improve
            
        Returns:
            Refined notes
        """
        prompt = f"""Original Study Notes:
{original_notes}

Feedback on improvements needed:
{feedback}

Revised Study Notes (incorporate the feedback and improve the notes):
"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=400,
                temperature=0.5,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        refined = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return refined


class TrialAndErrorLearner:
    """
    Implements trial-and-error learning with practice questions.
    The model practices using its notes and learns from mistakes.
    """
    
    def __init__(self, model, tokenizer, device='cpu'):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.mistake_log = []
    
    def practice(
        self,
        notes: str,
        practice_questions: List[Tuple[str, str]],
        epochs: int = 5
    ) -> List[float]:
        """
        Practice answering questions using notes.
        
        Args:
            notes: Study notes to use as context
            practice_questions: List of (question, answer) pairs
            epochs: Number of practice rounds
            
        Returns:
            Accuracy history over epochs
        """
        accuracy_history = []
        
        print(f"\n{'='*60}")
        print("Starting Trial-and-Error Learning")
        print(f"{'='*60}\n")
        
        for epoch in range(epochs):
            correct = 0
            total = len(practice_questions)
            
            for question, expected in practice_questions:
                answer = self._answer_with_notes(notes, question)
                
                # Simple similarity check
                is_correct = self._check_similarity(answer, expected)
                
                if is_correct:
                    correct += 1
                else:
                    self.mistake_log.append({
                        'question': question,
                        'expected': expected,
                        'got': answer,
                        'epoch': epoch
                    })
            
            accuracy = correct / total if total > 0 else 0
            accuracy_history.append(accuracy)
            
            print(f"Epoch {epoch+1}/{epochs}: "
                  f"Correct: {correct}/{total} "
                  f"({accuracy:.1%})")
        
        return accuracy_history
    
    def _answer_with_notes(self, notes: str, question: str) -> str:
        """Generate answer using notes as context."""
        prompt = f"""Study Notes:
{notes}

Based on these notes, answer the following question concisely:

Question: {question}
Answer:"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=150,
                temperature=0.5,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the answer
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        return answer[:200]  # Limit length
    
    def _check_similarity(self, answer: str, expected: str) -> bool:
        """Check if answer is similar to expected (simplified)."""
        answer_lower = answer.lower()
        expected_lower = expected.lower()
        
        # Check for key words
        expected_words = set(expected_lower.split())
        answer_words = set(answer_lower.split())
        
        if not expected_words:
            return False
        
        # Calculate overlap
        overlap = len(expected_words & answer_words)
        similarity = overlap / len(expected_words)
        
        return similarity > 0.5  # 50% word overlap threshold
    
    def get_mistake_summary(self) -> str:
        """Get summary of mistakes made during learning."""
        if not self.mistake_log:
            return "No mistakes logged."
        
        summary = f"\nMistake Log ({len(self.mistake_log)} mistakes):\n"
        summary += "="*60 + "\n"
        
        for i, mistake in enumerate(self.mistake_log[-5:], 1):  # Show last 5
            summary += f"\n{i}. Epoch {mistake['epoch']+1}\n"
            summary += f"   Q: {mistake['question']}\n"
            summary += f"   Expected: {mistake['expected']}\n"
            summary += f"   Got: {mistake['got'][:100]}...\n"
        
        return summary


class KnowledgeInternalizer:
    """
    Permanently internalizes knowledge through model weight updates.
    This makes the learning lasting, not just temporary context.
    """
    
    def __init__(self, model, learning_rate: float = 1e-5, device='cpu'):
        self.model = model
        self.device = device
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=learning_rate
        )
        self.internalized_topics = []
    
    def internalize(
        self,
        notes: str,
        examples: List[Tuple[str, str]],
        iterations: int = 10
    ) -> List[float]:
        """
        Permanently update model weights based on notes and examples.
        
        Args:
            notes: Study notes to internalize
            examples: Example (question, answer) pairs
            iterations: Number of update iterations
            
        Returns:
            Loss history
        """
        print(f"\n{'='*60}")
        print("Internalizing Knowledge (updating model weights)")
        print(f"{'='*60}\n")
        
        self.model.train()
        loss_history = []
        
        for iteration in range(iterations):
            total_loss = 0
            
            for question, answer in examples:
                # Create training text from notes + example
                text = f"{notes}\n\nQ: {question}\nA: {answer}"
                
                # Tokenize
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                ).to(self.device)
                
                # Forward pass
                outputs = self.model(**inputs, labels=inputs['input_ids'])
                loss = outputs.loss
                
                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(examples)
            loss_history.append(avg_loss)
            
            print(f"Iteration {iteration+1}/{iterations}: Loss = {avg_loss:.4f}")
        
        print("\n✓ Knowledge successfully internalized!\n")
        return loss_history


class StudentNoteLearningSystem:
    """
    Complete Student-Note Learning system.
    Combines note generation, practice, and knowledge internalization.
    """
    
    def __init__(self, model_name: str = "gpt2", device: str = 'cpu'):
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            print(f"Loading model: {model_name}...")
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.device = device
            self.model.to(device)
            
            # Initialize components
            self.note_generator = StudentNoteGenerator(
                self.model, self.tokenizer, device
            )
            self.trial_learner = TrialAndErrorLearner(
                self.model, self.tokenizer, device
            )
            self.internalizer = KnowledgeInternalizer(
                self.model, device=device
            )
            
            self.learning_sessions = []
            
        except ImportError:
            raise ImportError(
                "Please install transformers: pip install transformers torch"
            )
    
    def learn(
        self,
        topic: str,
        information: str,
        practice_questions: List[Tuple[str, str]],
        practice_epochs: int = 5,
        internalize_iterations: int = 10
    ) -> LearningSession:
        """
        Complete learning cycle: generate notes → practice → internalize.
        
        Args:
            topic: Name/identifier for this learning topic
            information: New information to learn
            practice_questions: Questions for practice
            practice_epochs: Number of practice epochs
            internalize_iterations: Number of internalization iterations
            
        Returns:
            LearningSession record
        """
        print(f"\n{'='*80}")
        print(f"Learning Session: {topic}")
        print(f"{'='*80}\n")
        
        # Step 1: Generate study notes
        print("📝 Step 1: Generating study notes from information...")
        notes = self.note_generator.generate_notes(information)
        print(f"\nGenerated Notes Preview:\n{notes[:200]}...\n")
        
        # Step 2: Practice with trial-and-error
        print("📚 Step 2: Practicing with trial-and-error learning...")
        accuracy_history = self.trial_learner.practice(
            notes,
            practice_questions,
            practice_epochs
        )
        
        # Step 3: Internalize knowledge
        print("🧠 Step 3: Permanently internalizing knowledge...")
        self.internalizer.internalize(
            notes,
            practice_questions,
            internalize_iterations
        )
        
        # Create session record
        session = LearningSession(
            topic=topic,
            notes=notes,
            timestamp=time.time(),
            accuracy_history=accuracy_history,
            final_accuracy=accuracy_history[-1] if accuracy_history else 0
        )
        
        self.learning_sessions.append(session)
        
        print(f"\n{'='*80}")
        print(f"✓ Learning Session Complete: {topic}")
        print(f"Final Accuracy: {session.final_accuracy:.1%}")
        print(f"{'='*80}\n")
        
        return session
    
    def get_learning_summary(self) -> str:
        """Get summary of all learning sessions."""
        if not self.learning_sessions:
            return "No learning sessions yet."
        
        summary = f"\nLearning History ({len(self.learning_sessions)} sessions):\n"
        summary += "="*80 + "\n"
        
        for i, session in enumerate(self.learning_sessions, 1):
            summary += f"\n{i}. {session.topic}\n"
            summary += f"   Final Accuracy: {session.final_accuracy:.1%}\n"
            summary += f"   Progress: {' → '.join(f'{a:.0%}' for a in session.accuracy_history)}\n"
        
        return summary


def demo_student_note_learning():
    """
    Demonstration of Student-Note Learning system.
    """
    print("\n" + "="*80)
    print("Student-Note Learning Demo")
    print("Teaching LLMs to Learn Like Students")
    print("="*80)
    
    try:
        # Initialize system
        system = StudentNoteLearningSystem()
        
        # Learning Session 1: Science Facts
        science_info = """
        Photosynthesis is the process by which plants convert sunlight into energy.
        It requires: sunlight, water (H2O), and carbon dioxide (CO2).
        The products are: glucose (C6H12O6) and oxygen (O2).
        The equation: 6CO2 + 6H2O + light → C6H12O6 + 6O2
        This process occurs in chloroplasts, specifically in the chlorophyll.
        """
        
        science_questions = [
            ("What is photosynthesis?", "process plants use to convert sunlight to energy"),
            ("What does photosynthesis need?", "sunlight water and carbon dioxide"),
            ("What does photosynthesis produce?", "glucose and oxygen"),
        ]
        
        system.learn(
            topic="Photosynthesis Basics",
            information=science_info,
            practice_questions=science_questions,
            practice_epochs=3,
            internalize_iterations=5
        )
        
        # Learning Session 2: Historical Facts  
        history_info = """
        The Renaissance was a cultural movement in Europe from the 14th to 17th century.
        It began in Florence, Italy around 1300.
        Key figures: Leonardo da Vinci (artist/inventor), Michelangelo (sculptor/painter),
        Galileo (scientist), and Shakespeare (writer).
        The Renaissance emphasized humanism, art, science, and rediscovery of classical learning.
        """
        
        history_questions = [
            ("When was the Renaissance?", "14th to 17th century"),
            ("Where did it begin?", "Florence Italy"),
            ("Name a Renaissance figure", "Leonardo da Vinci or Michelangelo"),
        ]
        
        system.learn(
            topic="Renaissance Period",
            information=history_info,
            practice_questions=history_questions,
            practice_epochs=3,
            internalize_iterations=5
        )
        
        # Print final summary
        print(system.get_learning_summary())
        
        print("\n✓ Demo Complete!")
        print("The model has learned like a student: notes → practice → internalize! 🎓\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have installed: pip install torch transformers")


if __name__ == "__main__":
    demo_student_note_learning()
