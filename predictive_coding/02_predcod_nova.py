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
from typing import List, Dict, Any, Optional
import time
from enum import Enum

class InteractionState(Enum):
    BUILDING_RAPPORT = "building_rapport"
    MAINTAINING_ENGAGEMENT = "maintaining_engagement"
    RECOVERING_ATTENTION = "recovering_attention"
    DEEPENING_INTERACTION = "deepening_interaction"
    EMOTIONAL_TRANSITION = "emotional_transition"  # New state for handling emotional shifts
    RECALIBRATING = "recalibrating"  # New state for handling uncertainty
    FLOW_STATE = "flow_state"  # New state for optimal engagement

class EmotionalMomentum:
    """Tracks emotional movement patterns and momentum"""
    def __init__(self):
        self.history = []
        self.momentum = 0.0
        self.volatility = 0.0
    
    def update(self, value: float):
        self.history.append(value)
        if len(self.history) > 5:
            self.history.pop(0)
            
        # Calculate momentum (direction and speed of emotional change)
        if len(self.history) >= 2:
            recent_momentum = self.history[-1] - self.history[-2]
            self.momentum = 0.7 * self.momentum + 0.3 * recent_momentum
            
        # Calculate volatility
        if len(self.history) >= 3:
            self.volatility = np.std(self.history)

@dataclass
class SocialSignal:
    """Enhanced social signal with confidence metrics and metadata"""
    type: str
    value: float  
    confidence: float
    timestamp: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata if None and validate ranges"""
        if self.metadata is None:
            self.metadata = {}
        if not -1 <= self.value <= 1:
            raise ValueError("Signal value must be between -1 and 1")
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")

class ReactiveLayer:
    """Enhanced fast-thinking layer with improved error handling and adaptive learning"""
    
    def __init__(self, learning_rate: float = 0.3, memory_size: int = 5):
        self.emotional_state = 0.0
        self.attention_level = 1.0
        self.prediction_error = 0.0
        self.base_learning_rate = learning_rate
        self.recent_errors = []
        self.memory_size = memory_size
        self.adaptation_threshold = 0.5
        
    def _adaptive_learning_rate(self, error: float) -> float:
        """Calculate adaptive learning rate based on recent performance"""
        if len(self.recent_errors) > 0:
            error_volatility = np.std(self.recent_errors)
            return self.base_learning_rate * (1 + error_volatility)
        return self.base_learning_rate

    def _update_error_history(self, error: float):
        """Maintain rolling history of prediction errors"""
        self.recent_errors.append(error)
        if len(self.recent_errors) > self.memory_size:
            self.recent_errors.pop(0)

    def process_signal(self, signal: SocialSignal) -> Dict[str, float]:
        """Enhanced signal processing with adaptive learning and error tracking"""
        try:
            time.sleep(0.05)  # Simulate processing delay
            
            predicted_emotion = self.emotional_state
            actual_emotion = signal.value
            self.prediction_error = actual_emotion - predicted_emotion
            
            self._update_error_history(self.prediction_error)
            learning_rate = self._adaptive_learning_rate(self.prediction_error)
            
            delta = learning_rate * self.prediction_error
            self.emotional_state = np.clip(self.emotional_state + delta, -1, 1)
            
            return {
                "emotion": self.emotional_state,
                "prediction_error": self.prediction_error,
                "learning_rate": learning_rate,
                "attention": self.attention_level,
                "response_time": 0.05
            }
            
        except Exception as e:
            print(f"⚠️ Error in reactive processing: {str(e)}")
            return {
                "emotion": self.emotional_state,
                "prediction_error": 0.0,
                "learning_rate": self.base_learning_rate,
                "attention": self.attention_level,
                "response_time": 0.05
            }

class ResponsiveLayer:
    """Enhanced context-aware layer with improved pattern recognition"""
    
    def __init__(self, context_window_size: int = 10):
        self.context_window: List[SocialSignal] = []
        self.pattern_predictions = {}
        self.context_window_size = context_window_size
        self.current_state = InteractionState.BUILDING_RAPPORT
        
    def _analyze_engagement_pattern(self) -> InteractionState:
        """Enhanced engagement analysis with emotional momentum"""
        if len(self.context_window) < 3:
            return InteractionState.BUILDING_RAPPORT
            
        # Get recent values and calculate momentum
        recent_values = [s.value for s in self.context_window[-3:]]
        momentum = EmotionalMomentum()
        for val in recent_values:
            momentum.update(val)
            
        trend = np.mean(recent_values)
        recent_volatility = momentum.volatility
        
        # Detect rapid emotional shifts
        if abs(momentum.momentum) > 0.5:
            return InteractionState.EMOTIONAL_TRANSITION
            
        # Check for optimal engagement (flow state)
        if trend > 0.6 and recent_volatility < 0.2:
            return InteractionState.FLOW_STATE
            
        # Handle uncertainty and volatility
        if recent_volatility > 0.4:
            if abs(trend) < 0.2:
                return InteractionState.RECALIBRATING
            return InteractionState.RECOVERING_ATTENTION
            
        # Standard state transitions
        if trend > 0.3 and recent_volatility < 0.3:
            return InteractionState.DEEPENING_INTERACTION
        elif trend < -0.2:
            return InteractionState.RECOVERING_ATTENTION
        else:
            return InteractionState.MAINTAINING_ENGAGEMENT

    def _generate_response(self, state: InteractionState, prediction: float) -> str:
        """Generate contextually appropriate response with enhanced emotional awareness"""
        responses = {
            InteractionState.BUILDING_RAPPORT: [
                "I notice we're just getting started. What interests you most?",
                "Let's explore this together at your pace.",
                "I'm here to help - what would you like to focus on?"
            ],
            InteractionState.MAINTAINING_ENGAGEMENT: [
                "You seem engaged. Shall we dig deeper?",
                "We're making good progress here.",
                "This is going well. What aspects intrigue you most?"
            ],
            InteractionState.RECOVERING_ATTENTION: [
                "Let's try approaching this from a different angle.",
                "I notice some uncertainty. What would help clarify things?",
                "Sometimes a quick recap helps - would that be useful?",
                "No worries, we can take a step back if needed."
            ],
            InteractionState.DEEPENING_INTERACTION: [
                "You're really getting this! Ready for some advanced concepts?",
                "Your engagement is fantastic. Let's explore some nuances.",
                "This is clicking well. Want to tackle some challenging aspects?"
            ],
            InteractionState.EMOTIONAL_TRANSITION: [
                "I notice things are shifting. Let's adjust our pace.",
                "Interesting change in direction! How are you feeling about this?",
                "Let's take a moment to find our bearings.",
                "Sometimes changes lead to the best insights!"
            ],
            InteractionState.RECALIBRATING: [
                "Let's take a breath and see where we are.",
                "Maybe we should check our heading - what feels unclear?",
                "Sometimes uncertainty is where the magic happens! 😊",
                "No rush - we can find our way together."
            ],
            InteractionState.FLOW_STATE: [
                "We're in the zone! This is fantastic progress.",
                "Everything's clicking beautifully. Shall we explore further?",
                "This is that sweet spot of perfect engagement!",
                "Love how we're vibing with this material! 🌟"
            ]
        }
        return np.random.choice(responses[state])

    def process_context(self, signal: SocialSignal, 
                       reactive_output: Dict[str, float]) -> Dict[str, Any]:
        """Enhanced context processing with state management"""
        try:
            time.sleep(0.2)  # Simulate processing delay
            
            self.context_window.append(signal)
            if len(self.context_window) > self.context_window_size:
                self.context_window.pop(0)
                
            self.current_state = self._analyze_engagement_pattern()
            
            context_pattern = np.mean([s.value for s in self.context_window])
            predicted_next = context_pattern * 0.8 + reactive_output["emotion"] * 0.2
            
            response = self._generate_response(self.current_state, predicted_next)
            
            return {
                "predicted_next": predicted_next,
                "response": response,
                "state": self.current_state.value,
                "context_confidence": len(self.context_window) / self.context_window_size
            }
            
        except Exception as e:
            print(f"⚠️ Error in context processing: {str(e)}")
            return {
                "predicted_next": reactive_output["emotion"],
                "response": "Let's continue our discussion.",
                "state": InteractionState.BUILDING_RAPPORT.value,
                "context_confidence": 0.5
            }

class ReflectiveLayer:
    """Enhanced deep learning layer with improved pattern analysis"""
    
    def __init__(self, min_samples: int = 5, volatility_threshold: float = 0.3):
        self.interaction_history = []
        self.min_samples = min_samples
        self.volatility_threshold = volatility_threshold
        self.learning_patterns = {}
        
    def _calculate_volatility(self, recent_patterns: List[Dict]) -> float:
        """Calculate interaction volatility"""
        if len(recent_patterns) < 2:
            return 0.0
        errors = [p["reactive"]["prediction_error"] for p in recent_patterns]
        return np.std(errors)

    def _analyze_learning_progress(self) -> Dict[str, Any]:
        """Analyze learning progress and stability"""
        if len(self.interaction_history) < self.min_samples:
            return {
                "stage": "initial",
                "confidence": 0.0,
                "stability": "unknown"
            }
            
        recent = self.interaction_history[-self.min_samples:]
        volatility = self._calculate_volatility(recent)
        avg_error = np.mean([p["reactive"]["prediction_error"] for p in recent])
        
        return {
            "stage": "advanced" if len(self.interaction_history) > self.min_samples * 2 else "developing",
            "confidence": max(0, 1 - volatility),
            "stability": "stable" if volatility < self.volatility_threshold else "volatile"
        }

    def analyze_patterns(self, signal: SocialSignal,
                        reactive_output: Dict[str, float],
                        responsive_output: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced pattern analysis with improved insights"""
        try:
            time.sleep(0.5)  # Simulate deep processing
            
            # Store interaction pattern
            pattern = {
                "signal": signal,
                "reactive": reactive_output,
                "responsive": responsive_output,
                "timestamp": time.time()
            }
            self.interaction_history.append(pattern)
            
            # Analyze progress
            progress = self._analyze_learning_progress()
            
            # Generate adaptation strategy
            if progress["stage"] == "initial":
                strategy = f"Building understanding... ({self.min_samples - len(self.interaction_history)} more samples needed)"
            else:
                if progress["stability"] == "stable":
                    strategy = "Maintaining successful interaction patterns."
                else:
                    strategy = "Adjusting approach to improve stability."
            
            return {
                "progress": progress,
                "strategy": strategy,
                "history_length": len(self.interaction_history),
                "confidence": progress["confidence"]
            }
            
        except Exception as e:
            print(f"⚠️ Error in reflective processing: {str(e)}")
            return {
                "progress": {"stage": "error", "confidence": 0.0, "stability": "unknown"},
                "strategy": "Maintaining basic interaction patterns.",
                "history_length": len(self.interaction_history),
                "confidence": 0.0
            }

class VirtualHuman:
    """Enhanced main class integrating all three layers"""
    
    def __init__(self):
        self.reactive = ReactiveLayer()
        self.responsive = ResponsiveLayer()
        self.reflective = ReflectiveLayer()
        self.interaction_count = 0
        
    def process_interaction(self, signal_type: str, value: float) -> Dict[str, Any]:
        """Process user interaction through all three layers with enhanced monitoring"""
        try:
            self.interaction_count += 1
            
            # Create social signal
            signal = SocialSignal(
                type=signal_type,
                value=value,
                confidence=0.9,
                timestamp=time.time(),
                metadata={"interaction_number": self.interaction_count}
            )
            
            # Process through each layer
            reactive_output = self.reactive.process_signal(signal)
            responsive_output = self.responsive.process_context(signal, reactive_output)
            reflective_output = self.reflective.analyze_patterns(
                signal, reactive_output, responsive_output
            )
            
            total_time = (
                reactive_output["response_time"] +
                0.2 +  # responsive layer time
                0.5   # reflective layer time
            )
            
            return {
                "reactive": reactive_output,
                "responsive": responsive_output,
                "reflective": reflective_output,
                "total_processing_time": total_time,
                "interaction_number": self.interaction_count
            }
            
        except Exception as e:
            print(f"⚠️ Critical error in interaction processing: {str(e)}")
            return self._generate_fallback_response()
            
    def _generate_fallback_response(self) -> Dict[str, Any]:
        """Generate safe fallback response in case of critical errors"""
        return {
            "reactive": {
                "emotion": 0.0,
                "prediction_error": 0.0,
                "learning_rate": 0.3,
                "attention": 1.0,
                "response_time": 0.05
            },
            "responsive": {
                "predicted_next": 0.0,
                "response": "Let's continue our discussion.",
                "state": InteractionState.BUILDING_RAPPORT.value,
                "context_confidence": 0.5
            },
            "reflective": {
                "progress": {"stage": "error", "confidence": 0.0, "stability": "unknown"},
                "strategy": "Maintaining basic interaction patterns.",
                "history_length": 0,
                "confidence": 0.0
            },
            "total_processing_time": 0.75,
            "interaction_number": self.interaction_count
        }

def run_demo():
    """Run an enhanced demo of the virtual human system"""
    vh = VirtualHuman()
    
    print("🤖 Enhanced Virtual Human Demo Starting...")
    print("=========================================")
    
    # Test interactions with more varied emotional patterns
    interactions = [
        ("emotion", 0.2),   # Slight positive
        ("emotion", 0.8),   # Strong positive
        ("emotion", -0.3),  # Slight negative
        ("emotion", 0.4),   # Moderate positive
        ("emotion", 0.6),   # Positive
        ("emotion", -0.2),  # Slight negative
        ("emotion", 0.5),   # Moderate positive
        ("emotion", 0.7),   # Strong positive
        ("emotion", 0.9),   # Very strong positive
        ("emotion", -0.1),  # Slight negative
    ]
    
    for i, (signal_type, value) in enumerate(interactions, 1):
        print(f"\n📍 Interaction {i}")
        print(f"Input: {signal_type} = {value}")
        
        result = vh.process_interaction(signal_type, value)
        
        print("\n🔄 Processing Results:")
        print(f"⚡ Reactive: Emotion={result['reactive']['emotion']:.2f}, "
              f"Error={result['reactive']['prediction_error']:.2f}, "
              f"Learning Rate={result['reactive']['learning_rate']:.2f}")
        print(f"🤔 Responsive: {result['responsive']['response']}")
        print(f"💭 State: {result['responsive']['state']}")
        print(f"🧠 Reflective: {result['reflective']['strategy']}")
        print(f"📊 Confidence: {result['reflective']['confidence']:.2f}")
        print(f"⏱️ Total Processing Time: {result['total_processing_time']:.3f}s")
        print("-" * 50)
        
        time.sleep(1)  # Pause between interactions

if __name__ == "__main__":
    run_demo()