class LearningHistory:
    def __init__(self, min_samples=5, volatility_threshold=0.3):
        """Initialize the learning history.
        
        Args:
            min_samples (int): Minimum number of samples required for statistical calculations.
                             Must be at least 5 for reliable results. Defaults to 5.
            volatility_threshold (float): Threshold for determining interaction stability.
                                        Values below this are considered stable. Defaults to 0.3.
        """
        if min_samples < 5:
            raise ValueError("min_samples must be at least 5 for reliable statistical calculations")
        
        self.min_samples = min_samples
        self.volatility_threshold = volatility_threshold
        self.history = []

    def calculate_statistics(self):
        """Calculate mean and standard deviation of interaction times.
        
        Returns:
            tuple: (mean, std_dev) if enough samples exist, else (None, None)
        """
        if len(self.history) < self.min_samples:
            return None, None
            
        # Rest of existing calculation code...
        
    def is_stable(self):
        """Determine if interactions are stable based on volatility threshold.
        
        Returns:
            bool: True if volatility is below threshold and enough samples exist,
                 False otherwise
        """
        mean, std_dev = self.calculate_statistics()
        if mean is None or std_dev is None:
            return False
            
        volatility = std_dev / mean
        return volatility < self.volatility_threshold 