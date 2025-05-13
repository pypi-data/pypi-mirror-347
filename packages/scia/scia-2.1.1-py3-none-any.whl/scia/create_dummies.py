import pandas as pd
import numpy as np

def create_dummies(data, dvar, pvar, mvar, model, contrast_level, contrast_slope):
    """
    Create dummy variables for phases and interactions - faithful R reproduction.
    
    Parameters:
    ----------
    data : pandas.DataFrame
        Single-case data frame
    dvar : str
        Name of dependent variable column
    pvar : str
        Name of phase variable column  
    mvar : str
        Name of measurement time variable column
    model : str
        Model type: 'W', 'H-M', 'B&L-B', or 'JW'
    contrast_level : str
        Contrast method for level: 'first' or 'preceding'
    contrast_slope : str
        Contrast method for slope: 'first' or 'preceding'
    
    Returns:
    -------
    pandas.DataFrame
        DataFrame with added dummy variables
    """
    # Extract measurement time
    mt = data[mvar].copy()
    
    # Adjust measurement time based on model
    if model == "W":
        mt = mt - mt.iloc[0]
    
    # Create output dataframe with adjusted measurement time
    out = pd.DataFrame({'mt': mt})
    
    # Get phase information
    phases = data[pvar]
    unique_phases = sorted(phases.unique())
    n_phases = len(unique_phases)
    
    # Skip if only one phase
    if n_phases <= 1:
        return out
    
    # Create contrast matrices exactly like R does
    if contrast_level == "first":
        # R's contr.treatment: compare each level to first level
        # This creates an identity matrix without the first row
        contr_level = np.eye(n_phases - 1)  # Remove first column
    elif contrast_level == "preceding":
        # R's contr.sum or helmert-style: compare each level to preceding
        contr_level = np.eye(n_phases)
        for i in range(1, n_phases):
            contr_level[i, :i] = -1.0 / i
        contr_level = contr_level[:, 1:]  # Remove first column
    else:
        raise ValueError(f"Wrong declaration of level contrast: {contrast_level}")
    
    # Create phase dummy variables
    phase_names = [f"phase_{unique_phases[i]}" for i in range(1, n_phases)]
    phase_dummies = pd.DataFrame(0.0, index=range(len(phases)), columns=phase_names)
    
    # Apply contrast matrix
    for i, phase in enumerate(unique_phases):
        mask = phases == phase
        for j, col in enumerate(phase_dummies.columns):
            if i > 0:  # Skip the first phase (reference level)
                phase_dummies.loc[mask, col] = contr_level[i-1, j]
    
    # Add to output
    out = pd.concat([out, phase_dummies], axis=1)
    
    # Create slope contrasts (usually same as level)
    if contrast_slope == "first":
        contr_slope = np.eye(n_phases)[:, 1:]  # Remove first column
    elif contrast_slope == "preceding":
        contr_slope = np.eye(n_phases)
        for i in range(1, n_phases):
            contr_slope[i, :i] = -1.0 / i
        contr_slope = contr_slope[:, 1:]  # Remove first column
    else:
        raise ValueError(f"Wrong declaration of slope contrast: {contrast_slope}")
    
    # Create interaction dummies
    inter_names = [f"inter{unique_phases[i]}" for i in range(1, n_phases)]
    inter_dummies = pd.DataFrame(0.0, index=range(len(phases)), columns=inter_names)
    
    # Calculate interactions based on model
    for i, phase in enumerate(unique_phases):
        mask = phases == phase
        indices = np.where(mask)[0]
        
        for j, col in enumerate(inter_dummies.columns):
            # Get measurement times for this phase
            phase_mt = mt.iloc[indices]
            contrast_value = contr_slope[i, j]
            
            if model == "W":
                    if phase == unique_phases[0]:  # First phase (A)
                        inter_dummies.loc[mask, col] = 0  # No interaction for reference phase
                    else:
                        # For other phases, interaction starts from 0 within that phase
                        phase_start_idx = indices[0]  # First index of this phase
                        inter_dummies.loc[mask, col] = (indices - phase_start_idx) * contrast_value
                # For other phases, interaction starts from 0 within that phase
            elif model == "H-M":
                if phase == unique_phases[0]:  # First phase (A)
                        inter_dummies.loc[mask, col] = 0  # No interaction for reference phase
                else:
                    # For other phases, interaction starts from 0 within that phase
                    phase_start_idx = indices[0]  # First index of this phase
                    inter_dummies.loc[mask, col] = (indices - phase_start_idx) * contrast_value
            elif model == "B&L-B":
                # B&L-B model: (1:(phase_length)) * contrast
                phase_length = len(indices)
                inter_dummies.loc[mask, col] = np.arange(1, phase_length + 1) * contrast_value
    
    # Add to output
    out = pd.concat([out, inter_dummies], axis=1)
    
    return out

# Additional debugging function to check contrast matrices
def debug_contrasts(phases, contrast_type="first"):
    """Debug function to see what contrast matrices are being created"""
    unique_phases = sorted(phases.unique())
    n_phases = len(unique_phases)
    
    if contrast_type == "first":
        contr = np.eye(n_phases)[:, 1:]
    elif contrast_type == "preceding":
        contr = np.eye(n_phases)
        for i in range(1, n_phases):
            contr[i, :i] = -1.0 / i
        contr = contr[:, 1:]
    
    print(f"Contrast matrix for {contrast_type}:")
    print(contr)
    return contr