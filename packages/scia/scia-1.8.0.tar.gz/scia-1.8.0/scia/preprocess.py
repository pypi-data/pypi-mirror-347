import pandas as pd

def prepare_scd(data, na_rm=False):
    """
    Prepare single-case data for analysis.
    
    Parameters:
    ----------
    data : pandas.DataFrame or list
        Single-case data frame or list of data frames
    na_rm : bool, default=False
        Whether to remove rows with missing values
    
    Returns:
    -------
    pandas.DataFrame or list
        Prepared data
    """
    # If data is a list, process each DataFrame separately
    if isinstance(data, list):
        return [prepare_scd(df, na_rm) for df in data]
    
    # Default variable names
    pvar = "phase"  # Phase variable
    mvar = "mt"     # Measurement time variable
    dvar = "values" # Dependent variable
    
    # Ensure column names are correctly formatted
    data.columns = [col.strip() for col in data.columns]
    
    # Remove rows with missing dependent variable values if na_rm=True
    if na_rm:
        data = data.dropna(subset=[dvar])
    
    return data
