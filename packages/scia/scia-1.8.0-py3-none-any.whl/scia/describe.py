import pandas as pd
import numpy as np
from scia.prepare_scdf import prepare_scdf, dv, phase, mt
from scia.rename_phase_duplicates import rename_phase_duplicates
from scia.phasestructure import phasestructure

def describe(data, dvar=None, pvar=None, mvar=None, return_dict=False):
    """
    Describe Single-Case Data (SCDF).
    
    Parameters:
    - data: Single-case data frame or list of data frames
    - dvar: Name of dependent variable column (optional)
    - pvar: Name of phase variable column (optional)
    - mvar: Name of measurement time variable column (optional)
    - return_dict: If True, returns the full dictionary with metadata. If False (default),
                  returns only the descriptive statistics DataFrame.
    
    Returns:
    - If return_dict=True: Dictionary with descriptive statistics DataFrame, design, and N.
    - If return_dict=False: DataFrame with descriptive statistics.
    """
    # Set variable names if not provided
    if dvar is None:
        dvar = dv(data)
    if pvar is None:
        pvar = phase(data)
    if mvar is None:
        mvar = mt(data)

    # Prepare data - ensure we're working with a list of DataFrames
    data_list = prepare_scdf(data)
    if not isinstance(data_list, list):
        data_list = [data_list]
    
    # Ensure all items in data_list are DataFrames
    data_list = [df for df in data_list if isinstance(df, pd.DataFrame)]
    
    N = len(data_list)
    
    if N == 0:
        raise ValueError("No valid DataFrames found in the input data")

    # Get phase designs before renaming
    designs = []
    for case_df in data_list:
        if pvar in case_df.columns:
            phase_series = pd.Series(case_df[pvar]).astype(str)
            design = list(phase_series.groupby((phase_series != phase_series.shift()).cumsum()).first())
            designs.append(design)
        else:
            designs.append([])
    
    phase_designs = ["-".join(design) for design in designs]

    # Rename phase duplicates
    for i in range(N):
        data_list[i] = data_list[i].copy()
        if pvar in data_list[i].columns:
            data_list[i][pvar] = rename_phase_duplicates(data_list[i][pvar])

    # Get phase designs after renaming
    designs = []
    for case_df in data_list:
        if pvar in case_df.columns:
            phase_series = pd.Series(case_df[pvar]).astype(str)
            design = list(phase_series.groupby((phase_series != phase_series.shift()).cumsum()).first())
            designs.append(design)
        else:
            designs.append([])
    
    design = sorted(set([item for sublist in designs for item in sublist]), key=lambda x: str(x))

    # Prepare variable names
    vars_ = ["n", "mis", "m", "md", "sd", "mad", "min", "max", "trend"]
    vars_full = [f"{v}.{ph}" for ph in design for v in vars_]
    desc = pd.DataFrame(np.nan, index=range(N), columns=vars_full)
    desc.insert(0, "Design", phase_designs)
    desc.insert(0, "Case", [getattr(df, "name", f"Case{i+1}") for i, df in enumerate(data_list)])

    # Calculate statistics for each case and phase
    for case_idx, case_df in enumerate(data_list):
        if pvar not in case_df.columns:
            continue
            
        phases = phasestructure(case_df, pvar)
        for i, phase_val in enumerate(phases["values"]):
            start = phases["start"][i] - 1  # Convert to 0-based index
            stop = phases["stop"][i]        # Python slicing is exclusive at end
            x = case_df[mvar].iloc[start:stop]
            y = case_df[dvar].iloc[start:stop]
            phase_name = phase_val

            desc.at[case_idx, f"n.{phase_name}"] = len(y)
            desc.at[case_idx, f"mis.{phase_name}"] = y.isna().sum()
            desc.at[case_idx, f"m.{phase_name}"] = y.mean(skipna=True)
            desc.at[case_idx, f"md.{phase_name}"] = y.median(skipna=True)
            desc.at[case_idx, f"sd.{phase_name}"] = y.std(skipna=True)
            desc.at[case_idx, f"mad.{phase_name}"] = y.mad(skipna=True) if hasattr(y, 'mad') else np.nan
            desc.at[case_idx, f"min.{phase_name}"] = y.min(skipna=True)
            desc.at[case_idx, f"max.{phase_name}"] = y.max(skipna=True)
            
            # Calculate MAD manually
            median = y.median(skipna=True)
            # Use numpy's median without the skipna parameter
            y_no_na = y.dropna().values
            if len(y_no_na) > 0:
                mad = np.median(np.abs(y_no_na - median))
                desc.at[case_idx, f"mad.{phase_name}"] = mad * 1.4826  # Consistent with R's mad()
            else:
                desc.at[case_idx, f"mad.{phase_name}"] = np.nan
            
            # Trend: slope of linear regression y ~ (x - x[0] + 1)
            if len(y.dropna()) > 1:
                x_trend = (x - x.iloc[0] + 1).values.reshape(-1, 1)
                y_trend = y.values
                try:
                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression().fit(x_trend, y_trend)
                    trend = model.coef_[0]
                except ImportError:
                    # Fallback to numpy polyfit
                    trend = np.polyfit(x_trend.flatten(), y_trend, 1)[0]
                desc.at[case_idx, f"trend.{phase_name}"] = trend
            else:
                desc.at[case_idx, f"trend.{phase_name}"] = np.nan

    # Store metadata in DataFrame attributes
    desc.attrs["design"] = design
    desc.attrs["N"] = N
    desc.attrs["pvar"] = pvar
    desc.attrs["mvar"] = mvar
    desc.attrs["dvar"] = dvar

    # Create the output dictionary
    out = {
        "descriptives": desc,
        "design": design,
        "N": N,
        "pvar": pvar,
        "mvar": mvar,
        "dvar": dvar
    }
    
    # Return either the DataFrame or the full dictionary
    return out if return_dict else desc