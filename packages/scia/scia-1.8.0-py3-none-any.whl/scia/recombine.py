import pandas as pd

def recombine_phases(data, phases=None, set_phases=None, phase_names=None, pvar="phase"):
    """
    Recombine phases in single-case data.
    
    Parameters:
    ----------
    data : pandas.DataFrame or list
        Single-case data frame or list of data frames
    phases : tuple, optional
        Phases to include
    set_phases : dict, optional
        Dictionary mapping phase names to new phase names
    phase_names : list, optional
        List of phase names
    pvar : str, default="phase"
        Name of the phase variable column
    
    Returns:
    -------
    pandas.DataFrame
        Recombined data
    """
    # If data is a list of DataFrames, process each one and combine them
    if isinstance(data, list):
        # Process each DataFrame separately
        processed_dfs = []
        for i, df in enumerate(data):
            # Ensure each DataFrame has a case column
            if 'case' not in df.columns:
                df = df.copy()
                df['case'] = i + 1
            # Process this DataFrame
            processed_df = recombine_phases(df, phases, set_phases, phase_names, pvar)
            processed_dfs.append(processed_df)
        
        # Combine all processed DataFrames
        if processed_dfs:
            return pd.concat(processed_dfs, ignore_index=True)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data
    
    # Handle single DataFrame case
    dropped_cases = []
    design_list = []
    warning_messages = []  # Initialize warning_messages list
    
    # Get unique case values
    case_names = data["case"].unique()
    
    # Process each case
    for case in case_names:
        case_data = data[data["case"] == case].copy()
        phase_values = case_data[pvar].astype(str).tolist()
        unique_phases = list(pd.Series(phase_values).unique())

        # Determine which phases to select
        if isinstance(phases, (tuple, list)) and len(phases) == 2:
            phases_A, phases_B = phases
        else:
            raise ValueError("Phases argument must contain exactly two elements.")

        # Validate phases
        if isinstance(phases_A, str) and isinstance(phases_B, str):
            if phases_A not in unique_phases or phases_B not in unique_phases:
                warning_messages.append(f"Phase(s) not found for case {case}. Dropping case.")
                dropped_cases.append(case)
                continue

        # Identify indices of selected phases
        A_indices = case_data.index[case_data[pvar] == phases_A]
        B_indices = case_data.index[case_data[pvar] == phases_B]

        # Rename phases if set_phases=True
        if set_phases:
            case_data.loc[A_indices, pvar] = phase_names[0]
            case_data.loc[B_indices, pvar] = phase_names[1]

        # Keep only selected phases
        case_data = case_data.loc[A_indices.union(B_indices)]
        design_list.append(unique_phases)

    # Drop cases with missing phases
    if warning_messages:
        print("\n".join(warning_messages))
    
    data = data[~data["case"].isin(dropped_cases)]
    return data
