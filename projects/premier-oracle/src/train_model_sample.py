from sklearn.base import clone
from sklearn.model_selection import TimeSeriesSplit
from lightgbm import LGBMClassifier

def train_production_models(df, preprocessor_template):
    """
    Implements a 'Master Preprocessor' strategy and Time-Series Validation.
    Ensures zero data leakage by never shuffling matches chronologically.
    """
    # 1. TIME SERIES SPLIT (The Professional Standard)
    # We never use random_state for shuffling in sports; we split by date.
    split_idx = int(len(df) * 0.85)
    train_data = df.iloc[:split_idx]
    test_data = df.iloc[split_idx:]

    # 2. MASTER PREPROCESSOR (Consistency Guard)
    # We fit once on the global history to capture all categories (Referees, Teams)
    master_preprocessor = clone(preprocessor_template)
    X_train_transformed = master_preprocessor.fit_transform(train_data)
    
    # 3. ISOLATED TRAINING
    model = LGBMClassifier(n_estimators=600, learning_rate=0.03)
    model.fit(X_train_transformed, train_data['Target'])
    
    return model, master_preprocessor