import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any
import time

@dataclass
class SocialSignal:
    """Represents a social signal detected from user interaction"""
    type: str  # e.g., 'emotion', 'attention', 'gesture'
    value: float
    confidence: float
    timestamp: float

class ReactiveLayer:
    """The fast-thinking layer (50-300ms) for immediate social responses"""
    
    def __init__(self):
        self.emotional_state = 0.0  # -1 to 1 scale
        self.attention_level = 1.0  # 0 to 1 scale
        self.prediction_error = 0.0
        
    def process_signal(self, signal: SocialSignal) -> Dict[str, float]:
        """Quick pattern matching and emotional state updates"""
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
    """The context-aware layer (300-1000ms) for intelligent responses"""
    
    def __init__(self):
        self.context_window: List[SocialSignal] = []
        self.pattern_predictions = {}
        
    def process_context(self, signal: SocialSignal, reactive_output: Dict[str, float]) -> Dict[str, Any]:
        """Process context and generate appropriate responses"""
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
    """The deep learning layer (>1000ms) for pattern recognition and adaptation"""
    
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
    """Main class integrating all three layers of NOVA architecture"""
    
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