import pandas as pd
import numpy as np

class FeatureEngineer:
    """
        Core logic for Premier League feature extraction.
        Highlights: ELO Rating, EWMA Smoothing, and Dynamic Rolling Averages.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def _calculate_rolling_stats(self, window=5):
        """
        Computes rolling performance with dynamic divisor to prevent 
        early-season underestimation.
        """
        # Logic to handle both Home and Away perspectives
        # ... (Data unification) ...
        grouped = self.df.groupby('Team')
        
        # DYNAMIC DIVISOR FIX:
        # Instead of dividing by 'window', we divide by actual games played
        rolling_count = grouped['GF'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).count())
        rolling_sum = grouped['GF'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).sum())
        
        # Dynamic Average 
        self.df['Goals_Scored_Avg'] = rolling_sum / rolling_count

    def _apply_ewma_efficiency(self, alpha=0.3):
        """
        Uses Exponentially Weighted Moving Average (EWMA) to capture 
        team 'Form' over historical averages.
        """
        grouped = self.df.groupby('Team')
        self.df['Shooting_Eff'] = grouped['Raw_Eff'].transform(
            lambda x: x.ewm(alpha=alpha, min_periods=1).mean().shift(1)
        )

    def build(self):
        # Master pipeline execution
        self._calculate_rolling_stats()
        self._apply_ewma_efficiency()
        return self.df