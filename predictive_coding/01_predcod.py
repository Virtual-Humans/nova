"""
Predictive Coding Network Implementation

This module implements a hierarchical predictive coding network based on the 
theoretical framework first proposed by Rao and Ballard (1999) and later 
expanded by Karl Friston (2005, 2010).

Historical Context:
------------------
Predictive coding originated from:
- Helmholtz's (1860s) idea of perception as unconscious inference
- Modern implementations began with Rao & Ballard's 1999 paper on visual cortex
- Friston's Free Energy Principle (2005) provided a unified theoretical framework
- Clark's (2013) "Whatever Next" paper popularized predictive processing

This Implementation:
------------------
Demonstrates core principles of predictive coding:
1. The brain constantly generates predictions about sensory input
2. Only prediction errors are passed forward through the hierarchy
3. Higher levels learn more abstract, slower-changing patterns
4. The system aims to minimize prediction errors at all levels

The experiment uses a sine wave with noise as input to show how:
- Lower levels rapidly adapt to short-term patterns
- Higher levels extract stable underlying patterns
- The hierarchy naturally separates signal from noise

Example Usage:
-------------
    network = PredictiveCodingNetwork(num_nodes=3)
    for value in sensor_input:
        errors = network.process_input(value)

References:
----------
- Rao, R. P., & Ballard, D. H. (1999). Predictive coding in the visual cortex
- Friston, K. (2005). A theory of cortical responses
- Clark, A. (2013). Whatever next? Predictive brains, situated agents...
"""

import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt

class PredictiveCodingNode:
    """
    A single node in the predictive coding network that generates and updates predictions.
    
    This implements a basic predictive processing unit that:
    1. Maintains a current prediction about incoming signals
    2. Computes prediction errors (difference between prediction and actual input)
    3. Updates its predictions to minimize these errors over time
    
    Attributes:
        prediction (float): Current prediction value of the node
        learning_rate (float): Rate at which predictions are updated based on errors
        prediction_history (list): History of predictions for visualization
        error_history (list): History of prediction errors for visualization
    """
    def __init__(self, learning_rate: float = 0.1):
        self.prediction = 0.0  # Current prediction
        self.learning_rate = learning_rate
        self.prediction_history = []
        self.error_history = []
        
    def update(self, actual_value: float) -> Tuple[float, float]:
        """
        Update prediction based on actual value observed.
        
        Implements the core predictive coding update equation:
        prediction += learning_rate * prediction_error
        
        Args:
            actual_value: The true value observed by this node
            
        Returns:
            Tuple containing:
            - prediction_error: Difference between prediction and actual value
            - prediction: Updated prediction after learning
        """
        # Calculate prediction error (surprise signal)
        prediction_error = actual_value - self.prediction
        
        # Update prediction using prediction error (error minimization)
        self.prediction += self.learning_rate * prediction_error
        
        # Store history for visualization
        self.prediction_history.append(self.prediction)
        self.error_history.append(prediction_error)
        
        return prediction_error, self.prediction

class PredictiveCodingNetwork:
    """
    A hierarchical network of predictive coding nodes.
    
    Implements key principles of predictive coding theory:
    1. Hierarchical Processing: Multiple levels of prediction
    2. Error Propagation: Each level predicts errors from level below
    3. Multiple Timescales: Different learning rates at different levels
    
    Args:
        num_nodes: Number of hierarchical levels in the network
        learning_rates: Learning rate for each level (slower rates at higher levels)
    """
    def __init__(self, num_nodes: int = 3, learning_rates: List[float] = None):
        if learning_rates is None:
            learning_rates = [0.1] * num_nodes
            
        self.nodes = [PredictiveCodingNode(lr) for lr in learning_rates]
        
    def process_input(self, input_value: float) -> List[float]:
        """
        Process input through the predictive coding hierarchy.
        
        Each level:
        1. Receives a signal (input or error from below)
        2. Generates a prediction
        3. Computes prediction error
        4. Passes error to next level
        
        Args:
            input_value: The sensory input to process
            
        Returns:
            List of prediction errors at each level
        """
        current_signal = input_value
        errors = []
        
        # Process up the hierarchy, with each level predicting the error below
        for node in self.nodes:
            error, prediction = node.update(current_signal)
            errors.append(error)
            # The error becomes the signal for the next level (error prediction)
            current_signal = abs(error)  
            
        return errors
    
    def plot_predictions(self):
        """Plot prediction history for each node"""
        fig, axes = plt.subplots(len(self.nodes), 1, figsize=(10, 3*len(self.nodes)))
        if len(self.nodes) == 1:
            axes = [axes]
            
        for i, node in enumerate(self.nodes):
            axes[i].plot(node.prediction_history, label='Prediction')
            axes[i].plot(node.error_history, label='Error', alpha=0.5)
            axes[i].set_title(f'Node {i+1}')
            axes[i].legend()
            axes[i].grid(True)
        
        plt.tight_layout()
        return fig

# Example usage
def generate_pattern(n_steps: int = 100) -> np.ndarray:
    """
    Generate a test signal combining a sine wave with random noise.
    
    This creates a partially predictable pattern that the network can learn:
    - Sine wave: The predictable component
    - Random noise: The unpredictable component
    
    Args:
        n_steps: Length of the signal to generate
        
    Returns:
        numpy array containing the generated signal
    """
    t = np.linspace(0, 4*np.pi, n_steps)
    signal = np.sin(t) + 0.2 * np.random.randn(n_steps)
    return signal

def demo_predictive_coding():
    """
    Demonstrate the predictive coding network on a simple pattern.
    
    This demo shows how:
    1. Lower levels learn faster but are more sensitive to noise
    2. Higher levels learn slower but capture more stable patterns
    3. Prediction errors decrease as the network learns
    """
    # Create input pattern
    signal = generate_pattern(100)
    
    # Create network with 3 levels, each level learning slower than the one below
    network = PredictiveCodingNetwork(
        num_nodes=3, 
        learning_rates=[0.1, 0.05, 0.02]  # Different learning rates for each level
    )
    
    # Process signal
    errors = []
    for value in signal:
        level_errors = network.process_input(value)
        errors.append(level_errors)
    
    # Plot results
    network.plot_predictions()
    plt.show()

if __name__ == "__main__":
    demo_predictive_coding()