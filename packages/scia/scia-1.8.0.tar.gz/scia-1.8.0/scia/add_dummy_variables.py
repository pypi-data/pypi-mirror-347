from scia.create_dummies import create_dummies
import pandas as pd
def add_dummy_variables(data, model, dvar=None, pvar=None, mvar=None, 
                       contrast_level=None, contrast_slope=None):
    """
    Add dummy variables to single-case data.
    
    Parameters:
    ----------
    data : list or pandas.DataFrame
        Single-case data frame or list of data frames
    model : str
        Model type: 'W', 'H-M', 'B&L-B', or 'JW'
    dvar : str
        Name of dependent variable column
    pvar : str  
        Name of phase variable column
    mvar : str
        Name of measurement time variable column
    contrast_level : str
        Contrast method for level: 'first' or 'preceding'
    contrast_slope : str
        Contrast method for slope: 'first' or 'preceding'
    
    Returns:
    -------
    dict
        Dictionary with 'data', 'var_phase', and 'var_inter' keys
    """
    # Handle single case
    if not isinstance(data, list):
        data = [data]
    
    # Process each case
    for case in range(len(data)):
        case_data = data[case].copy()
        
        # Create dummies for this case
        dat_inter = create_dummies(
            data=case_data,
            dvar=dvar,
            pvar=pvar, 
            mvar=mvar,
            model=model,
            contrast_level=contrast_level,
            contrast_slope=contrast_slope
        )
        
        # Replace mt column with adjusted mt from create_dummies
        case_data[mvar] = dat_inter['mt']
        
        # Add dummy variables (skip mt column which is first)
        dummy_cols = dat_inter.columns[1:]  # Skip 'mt' column
        case_data = pd.concat([case_data, dat_inter[dummy_cols]], axis=1)
        
        # Update the case in the list
        data[case] = case_data
        
        # Get variable names from the last case (they're all the same)
        n_dummies = len(dummy_cols)
        half_n = n_dummies // 2
        
        # First half are interaction variables, second half are phase variables
        var_phase = [col for col in dummy_cols if col.startswith('phase_')]
        var_inter = [col for col in dummy_cols if col.startswith('inter')]
    
    # Return the modified data and variable names
    return {
        'data': data,
        'var_inter': var_inter,
        'var_phase': var_phase
    }