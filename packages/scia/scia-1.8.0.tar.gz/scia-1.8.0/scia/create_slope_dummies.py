import pandas as pd
import numpy as np
from patsy import ModelDesc
def create_slope_dummies(phase, mt, contrast, model, var_name="inter"):
    """
    Create slope dummy variables for interaction terms.
    
    Parameters:
    ----------
    phase : pandas.Series
        Phase variable
    mt : pandas.Series
        Measurement time variable
    contrast : pandas.DataFrame
        Contrast matrix
    model : str
        Model type: 'W', 'H-M', 'B&L-B', or 'JW'
    var_name : str, default="inter"
        Prefix for dummy variable names
    
    Returns:
    -------
    pandas.DataFrame
        DataFrame with slope dummy variables
    """
    # Create dummy variable names
    if contrast.columns.empty:
        dummy_names = [f"{var_name}{i+1}" for i in range(contrast.shape[1])]
    else:
        dummy_names = [f"{var_name}{col}" for col in contrast.columns]
    
    # Initialize output dataframe
    df = pd.DataFrame(0, index=range(len(phase)), columns=dummy_names)
    
    # Process each contrast column
    for i in range(contrast.shape[1]):
        # Get run-length encoding of the contrast column
        values = contrast.iloc[:, i].values
        phase_str = pd.Series(values).groupby(phase, observed=False).first()
        
        # Calculate start and stop indices for each phase
        unique_phases = phase.unique()
        phase_indices = {p: phase[phase == p].index for p in unique_phases}
        
        # Apply the model to each phase
        for j, p in enumerate(phase_indices):
            selection_phases = [p]
            id_indices = phase_indices[p]
            
            if len(id_indices) > 0:
                if model in ["B&L-B"]:
                    # B&L-B model
                    value = phase_str.get(p, 0)
                    df.loc[id_indices, dummy_names[i]] = (mt.iloc[id_indices] - mt.iloc[0] + 1) * value
                
                if model in ["H-M", "W"]:
                    # H-M or W model
                    value = phase_str.get(p, 0)
                    df.loc[id_indices, dummy_names[i]] = (mt.iloc[id_indices] - mt.iloc[0]) * value
    
    # Add formula attribute (as metadata in Python)
    formula = f". ~ . + {' + '.join(dummy_names)}"
    df.attrs["formula"] = formula
    
    return df