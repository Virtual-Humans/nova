"""NOVA Architecture Demo with Predictive Coding Implementation

This module demonstrates a three-layer predictive coding architecture for social human-AI 
interaction, based on the theoretical frameworks of Karl Friston's Free Energy Principle 
and Andy Clark's Prediction Machine perspective.

The NOVA architecture implements a hierarchical predictive coding system operating 
at three distinct timescales:

1. Reactive Layer (50-300ms):
   - Handles immediate emotional responses
   - Based on Friston's work on fast sensory prediction (2010)
   - Implements precision-weighted prediction error minimization

2. Responsive Layer (300-1000ms):
   - Manages context-aware social responses
   - Inspired by Clark's work on hierarchical predictive processing (2013)
   - Maintains sliding context window for pattern detection

3. Reflective Layer (>1000ms):
   - Handles long-term adaptation and learning
   - Based on Hohwy's work on long-term predictive modeling (2013)
   - Implements strategic optimization of interaction patterns

The demo simulates a series of social interactions, demonstrating how the system:
- Processes emotional signals through multiple timescales
- Adapts responses based on prediction errors
- Maintains context awareness and learns from interactions
- Implements the Free Energy Principle through hierarchical prediction

Key References:
    - Friston, K. (2010). The free-energy principle: A unified brain theory?
      Nature Reviews Neuroscience, 11(2), 127-138.
    - Clark, A. (2013). Whatever next? Predictive brains, situated agents, and
      the future of cognitive science. Behavioral and Brain Sciences, 36(3), 181-204.
    - Hohwy, J. (2013). The Predictive Mind. Oxford University Press.
    - Nass, C., & Reeves, B. (1996). The Media Equation. CSLI Publications.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any
import time

@dataclass
class SocialSignal:
    """Represents a social signal detected from user interaction
    
    This class implements the lowest level of predictive coding - direct sensory input
    from user interactions that the system needs to process and predict.
    
    Attributes:
        type: Category of social signal (e.g., 'emotion', 'attention', 'gesture')
        value: Normalized signal strength/value (-1 to 1 for emotions)
        confidence: System's confidence in signal detection (0 to 1)
        timestamp: Unix timestamp when signal was detected
    """
    type: str
    value: float  
    confidence: float
    timestamp: float

class ReactiveLayer:
    """The fast-thinking layer (50-300ms) for immediate social responses
    
    This layer implements the first level of the NOVA architecture, handling rapid
    responses to social signals. It uses predictive coding principles to:
    1. Maintain predictions about expected emotional states
    2. Calculate prediction errors between expected and actual signals
    3. Update internal models using precision-weighted prediction errors
    
    The learning rate adapts based on prediction error magnitude, implementing
    the precision-weighting principle from the Free Energy Framework.
    
    Processing Time: 50-300ms (simulated as 50ms in this demo)
    """
    
    def __init__(self):
        """Initialize reactive layer with baseline emotional state and attention"""
        self.emotional_state = 0.0  # Internal model's predicted emotional state (-1 to 1)
        self.attention_level = 1.0  # Attention allocation for precision-weighting (0 to 1)
        self.prediction_error = 0.0  # Tracks difference between predicted and actual signals
        
    def process_signal(self, signal: SocialSignal) -> Dict[str, float]:
        """Process incoming social signals using predictive coding principles
        
        Implements core predictive coding by:
        1. Generating prediction from current emotional state
        2. Computing prediction error against actual signal
        3. Using dynamic learning rate based on prediction error magnitude
        4. Updating internal model (emotional_state) using weighted error

        Args:
            signal: Incoming social signal to process

        Returns:
            Dict containing:
                - emotion: Updated emotional state
                - prediction_error: Computed prediction error
                - response_time: Processing time in seconds
        """
        # Simulate processing delay
        time.sleep(0.05)  # 50ms for reactive processing
        
        # Update emotional state with some predictive coding magic
        predicted_emotion = self.emotional_state
        actual_emotion = signal.value
        self.prediction_error = actual_emotion - predicted_emotion
        
        # Dynamic learning rate based on prediction error magnitude
        base_learning_rate = 0.3
        confidence_factor = np.exp(-abs(self.prediction_error))  # Lower confidence = higher learning
        learning_rate = base_learning_rate * (2 - confidence_factor)
        
        # Update state using prediction error (core predictive coding principle)
        self.emotional_state += learning_rate * self.prediction_error
        
        return {
            "emotion": self.emotional_state,
            "prediction_error": self.prediction_error,
            "response_time": 0.05
        }

class ResponsiveLayer:
    """The context-aware layer (300-1000ms) for intelligent responses
    
    This layer implements the second level of NOVA architecture, handling:
    1. Context maintenance through a sliding window of recent signals
    2. Pattern detection in social interactions
    3. Generation of context-appropriate responses
    
    It maintains a higher-level predictive model that integrates:
    - Recent interaction history (context_window)
    - Current reactive layer state
    - Learned interaction patterns
    
    Processing Time: 300-1000ms (simulated as 200ms in this demo)
    """
    
    def __init__(self):
        """Initialize responsive layer with empty context history"""
        self.context_window: List[SocialSignal] = []  # Sliding window of recent signals
        self.pattern_predictions = {}  # Storage for detected interaction patterns
        
    def process_context(self, signal: SocialSignal, reactive_output: Dict[str, float]) -> Dict[str, Any]:
        """Process context and generate appropriate responses using predictive coding
        
        Implements hierarchical predictive coding by:
        1. Maintaining context through signal history
        2. Generating higher-level predictions based on context patterns
        3. Integrating reactive layer predictions with contextual understanding
        4. Selecting responses based on prediction accuracy
        
        Args:
            signal: Current social signal
            reactive_output: Output from reactive layer processing

        Returns:
            Dict containing:
                - predicted_next: Expected next signal value
                - response: Selected verbal response
                - context_confidence: Confidence based on context window size
        """
        # Simulate processing delay
        time.sleep(0.2)  # 200ms for contextual processing
        
        # Update context window
        self.context_window.append(signal)
        if len(self.context_window) > 10:
            self.context_window.pop(0)
            
        # Generate context-aware prediction
        context_pattern = np.mean([s.value for s in self.context_window])
        predicted_next = context_pattern * 0.8 + reactive_output["emotion"] * 0.2
        
        # Select appropriate response based on prediction
        response = self._select_response(predicted_next, reactive_output["prediction_error"])
        
        return {
            "predicted_next": predicted_next,
            "response": response,
            "context_confidence": len(self.context_window) / 10
        }
    
    def _select_response(self, prediction: float, error: float) -> str:
        """Select appropriate response based on prediction and error"""
        responses = {
            'high_surprise': [
                "I notice this surprised you. Let me explain differently.",
                "That was unexpected! Let's break this down more clearly.",
                "Interesting reaction! Should we explore this from another angle?"
            ],
            'comfortable': [
                "You seem comfortable with this. Shall we go deeper?",
                "You're following well! Want to explore more advanced aspects?",
                "This seems to resonate with you. Let's build on that."
            ],
            'neutral': [
                "I see you're following along. Let's continue.",
                "We're making good progress here.",
                "You're engaging well with this material.",
                "Let's keep going at this pace."
            ]
        }
        
        if error > 0.5:
            return np.random.choice(responses['high_surprise'])
        elif error < -0.5:
            return np.random.choice(responses['comfortable'])
        else:
            return np.random.choice(responses['neutral'])

class ReflectiveLayer:
    """The deep learning layer (>1000ms) for pattern recognition and adaptation
    
    This layer implements the highest level of the NOVA architecture, responsible for:
    1. Long-term pattern recognition across multiple interactions
    2. Behavioral adaptation based on interaction history
    3. Strategic optimization of interaction patterns
    
    It implements the highest level of predictive coding by:
    - Analyzing trends in prediction errors
    - Detecting interaction stability/volatility
    - Adapting behavior to minimize long-term prediction errors
    
    Processing Time: >1000ms (simulated as 500ms in this demo)
    """
    
    def __init__(self):
        self.interaction_patterns = {}
        self.learning_history = []
        
    def analyze_patterns(self, signal: SocialSignal, 
                        reactive_output: Dict[str, float],
                        responsive_output: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze long-term patterns and adapt behavior"""
        # Simulate processing delay
        time.sleep(0.5)  # 500ms for deep processing
        
        # Store interaction pattern
        pattern = {
            "signal": signal,
            "reactive": reactive_output,
            "responsive": responsive_output,
            "timestamp": time.time()
        }
        self.learning_history.append(pattern)
        
        # Initialize metrics
        history_length = len(self.learning_history)
        min_samples = 3  # Reduced from 5 for faster adaptation
        
        if history_length >= min_samples:
            recent_errors = [p["reactive"]["prediction_error"] for p in self.learning_history[-min_samples:]]
            trend = np.mean(recent_errors)
            
            # Calculate volatility (standard deviation of errors)
            volatility = np.std(recent_errors)
            
            # Determine interaction stability
            stability_status = "stable" if volatility < 0.3 else "volatile"
            
            adaptation = self._adapt_behavior(trend, volatility, stability_status)
        else:
            remaining = min_samples - history_length
            adaptation = f"Building understanding... ({remaining} more samples needed)"
            
        return {
            "adaptation": adaptation,
            "pattern_confidence": min(history_length / 10, 1.0),
            "history_length": history_length
        }
    
    def _adapt_behavior(self, error_trend: float, volatility: float, stability: str) -> str:
        """Adapt behavior based on observed error trends and volatility"""
        trend_desc = "positive" if error_trend > 0 else "negative"
        
        messages = {
            "stable": {
                "positive": "Steady positive engagement detected. Gradually increasing complexity.",
                "negative": "Consistent understanding shown. Maintaining current approach."
            },
            "volatile": {
                "positive": f"Variable engagement (volatility: {volatility:.2f}). Adjusting to stabilize interaction.",
                "negative": f"Inconsistent responses (volatility: {volatility:.2f}). Simplifying approach."
            }
        }
        
        return messages[stability][trend_desc]

class VirtualHuman:
    """Main class integrating all three layers of NOVA architecture
    
    This class implements the complete predictive coding hierarchy through:
    1. Reactive Layer (50-300ms): Immediate emotional responses
    2. Responsive Layer (300-1000ms): Context-aware interactions
    3. Reflective Layer (>1000ms): Long-term adaptation
    
    The architecture follows the Free Energy Framework by:
    - Maintaining predictions at multiple temporal scales
    - Propagating prediction errors up the hierarchy
    - Adapting behavior to minimize prediction errors
    - Using precision-weighted learning at each level
    
    Example:
        vh = VirtualHuman()
        result = vh.process_interaction("emotion", 0.5)
        print(result["responsive"]["response"])
    """
    
    def __init__(self):
        self.reactive = ReactiveLayer()
        self.responsive = ResponsiveLayer()
        self.reflective = ReflectiveLayer()
        
    def process_interaction(self, signal_type: str, value: float) -> Dict[str, Any]:
        """Process user interaction through all three layers"""
        # Create social signal
        signal = SocialSignal(
            type=signal_type,
            value=value,
            confidence=0.9,
            timestamp=time.time()
        )
        
        # Process through each layer
        reactive_output = self.reactive.process_signal(signal)
        responsive_output = self.responsive.process_context(signal, reactive_output)
        reflective_output = self.reflective.analyze_patterns(signal, reactive_output, responsive_output)
        
        return {
            "reactive": reactive_output,
            "responsive": responsive_output,
            "reflective": reflective_output,
            "total_processing_time": (
                reactive_output["response_time"] +
                0.2 +  # responsive layer time
                0.5   # reflective layer time
            )
        }

# Example usage and demo
def run_demo():
    vh = VirtualHuman()
    
    # Simulate a sequence of interactions
    print("🤖 Virtual Human Demo Starting...")
    print("============================")
    
    interactions = [
        ("emotion", 0.2),   # Slightly positive
        ("emotion", 0.8),   # Very positive
        ("emotion", -0.3),  # Slightly negative
        ("emotion", 0.4),   # Moderately positive
        ("emotion", 0.6),   # Quite positive
        ("emotion", -0.2),  # Slightly negative
        ("emotion", 0.5),   # Moderately positive
        ("emotion", 0.7),   # Quite positive
        ("emotion", 0.9),   # Very positive
        ("emotion", -0.1),  # Slightly negative
        ("emotion", 0.3),   # Moderately positive
        ("emotion", 0.6),   # Quite positive
        ("emotion", 0.8),   # Very positive
        ("emotion", -0.4),  # Slightly negative
    ]
    
    for i, (signal_type, value) in enumerate(interactions, 1):
        print(f"\n📍 Interaction {i}")
        print(f"Input: {signal_type} = {value}")
        
        result = vh.process_interaction(signal_type, value)
        
        print("\n🔄 Processing Results:")
        print(f"⚡ Reactive: Emotion={result['reactive']['emotion']:.2f}, "
              f"Error={result['reactive']['prediction_error']:.2f}")
        print(f"🤔 Responsive: {result['responsive']['response']}")
        print(f"🧠 Reflective: {result['reflective']['adaptation']}")
        print(f"⏱️ Total Processing Time: {result['total_processing_time']:.3f}s")
        print("-" * 50)
        
        # Simulate real-time delay between interactions
        time.sleep(1)

if __name__ == "__main__":
    run_demo()