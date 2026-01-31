import numpy as np

class InferenceEngine:
    """
    Post-model inference management. 
    Highlights: Probabilistic normalization and Security Layer (Flooring).
    """
    def __init__(self, model):
        self.model = model
        # Defined as a constant for team hierarchy adjustments
        self.TOP_TEAMS = ['Man City', 'Arsenal', 'Liverpool', 'Aston Villa']

    def get_calibrated_prediction(self, features, home_team, away_team):
        """
        Transforms raw model output into an adjusted prediction 
        while maintaining mathematical integrity.
        """
        # 1. Obtain raw probabilities from the model (H/D/A)
        probs = self.model.predict_proba(features)[0]
        p_h, p_d, p_a = probs[0], probs[1], probs[2]

        # 2. SECURITY LAYER (Flooring): 
        # Prevents heuristic adjustments from pushing probabilities to impossible values.
        p_h, p_d, p_a = max(0.001, p_h), max(0.001, p_d), max(0.001, p_a)

        # 3. BUSINESS LOGIC (Optional): Roster-based adjustments
        # This is where penalties are applied if the scraper detects missing key players.
        
        # 4. MATHEMATICAL NORMALIZATION: 
        # Crucial after any adjustment to ensure the final sum is exactly 1.0.
        total = p_h + p_d + p_a
        return {
            'Home': p_h / total,
            'Draw': p_d / total,
            'Away': p_a / total
        }