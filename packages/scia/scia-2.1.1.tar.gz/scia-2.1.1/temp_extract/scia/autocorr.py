import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf
from scia.preprocess import prepare_scd
from scia.utils import revise_names

def autocorr(data, dvar="values", pvar="phase", mvar="mt", lag_max=3):
    """
    Compute autocorrelations for each phase and across all phases.

    Parameters:
    - data (pd.DataFrame): The single-case dataset.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - mvar (str): Name of the measurement time variable.
    - lag_max (int, default=3): The maximum lag for which autocorrelations are computed.

    Returns:
    - pd.DataFrame: A DataFrame containing autocorrelation results for each phase and overall.
    """

    # Prepare the data
    if isinstance(data, list):
        # Process each DataFrame separately and then combine results
        results_list = []
        for i, df in enumerate(data):
            # Ensure each DataFrame has a case column
            if 'case' not in df.columns:
                df = df.copy()
                df['case'] = i + 1
            # Process this DataFrame
            single_result = autocorr(df, dvar, pvar, mvar, lag_max)
            results_list.append(single_result)
        
        # Combine all results
        if results_list:
            return pd.concat(results_list, ignore_index=True)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data
    
    # Ensure data is properly prepared
    data = prepare_scd(data)
    
    # Add case column if missing
    if 'case' not in data.columns:
        data['case'] = 1

    # Extract unique cases
    case_names = data["case"].unique()

    # Define column names
    var_lag = [f"Lag {i+1}" for i in range(lag_max)]
    df_results = pd.DataFrame(columns=["Case", "Phase"] + var_lag)

    for case in case_names:
        case_data = data[data["case"] == case].copy()

        # Identify phases
        phases = case_data[pvar].unique()
        phases = sorted(phases, key=lambda x: case_data[case_data[pvar] == x][mvar].min())  # Sort phases by time

        # Compute autocorrelation for each phase
        for phase in phases:
            phase_data = pd.to_numeric(
                case_data[case_data[pvar] == phase][dvar].dropna(),
                errors='coerce'
            )
            
            if len(phase_data) > 1:
                max_lag = min(len(phase_data) - 1, lag_max)
                ac_values = acf(phase_data, nlags=max_lag, fft=False)[1:]  # Ignore lag 0
            else:
                ac_values = [np.nan] * lag_max  # If not enough data, return NaN
            
            row = [case, phase] + list(ac_values) + [np.nan] * (lag_max - len(ac_values))  # Fill missing lags with NaN
            df_results.loc[len(df_results)] = row

        # Compute autocorrelation across all phases
        all_data = pd.to_numeric(
            case_data[dvar].dropna(),
            errors='coerce'
        )
        
        if len(all_data) > 1:
            max_lag = min(len(all_data) - 1, lag_max)
            ac_values = acf(all_data, nlags=max_lag, fft=False)[1:]
        else:
            ac_values = [np.nan] * lag_max
        
        row = [case, "all"] + list(ac_values) + [np.nan] * (lag_max - len(ac_values))  # Fill missing lags with NaN
        df_results.loc[len(df_results)] = row

    return df_results  # Return as a DataFrame instead of a dictionary
