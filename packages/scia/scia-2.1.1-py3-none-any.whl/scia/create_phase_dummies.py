import pandas as pd
import numpy as np

def create_phase_dummies(phase, var_name="phase"):
    """
    Create phase dummy variables - CORRECTED VERSION.
    
    Parameters:
    ----------
    phase : pandas.Series
        Phase variable
    var_name : str, default="phase"
        Prefix for dummy variable names
    
    Returns:
    -------
    pandas.DataFrame
        DataFrame with phase dummy variables
    """
    # Get unique phases in order
    unique_phases = sorted(phase.unique())
    
    # Skip if only one phase
    if len(unique_phases) <= 1:
        return pd.DataFrame()
    
    # Create dummy variables manually to ensure correct coding
    # Phase A = 0, Phase B = 1 (like R's treatment contrasts)
    dummy_data = {}
    
    for i, phase_name in enumerate(unique_phases[1:], 1):  # Skip first phase
        col_name = f"{var_name}_{phase_name}"
        # Create dummy: 1 for this phase, 0 for all others
        dummy_data[col_name] = (phase == phase_name).astype(float)
    
    return pd.DataFrame(dummy_data, index=phase.index)