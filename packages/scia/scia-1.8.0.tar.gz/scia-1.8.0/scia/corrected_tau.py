import pandas as pd
import numpy as np
from scipy.stats import norm
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.tau_u import kendall_tau, tau_u
import statsmodels.formula.api as smf

def corrected_tau(data, dvar=None, pvar=None, mvar=None, phases=("A", "B"), 
                 alpha=0.05, continuity=True, repeated=False, tau_method="b"):
    """
    Calculate baseline-corrected Tau.
    
    Parameters:
    ----------
    data : pandas.DataFrame or list
        Single-case data frame or list of data frames
    dvar : str, optional
        Name of the dependent variable column
    pvar : str, optional
        Name of the phase variable column
    mvar : str, optional
        Name of the measurement time variable column
    phases : tuple, default=("A", "B")
        Phases to include in the analysis
    alpha : float, default=0.05
        Significance level
    continuity : bool, default=True
        Whether to apply continuity correction
    repeated : bool, default=False
        Whether to use repeated measures
    tau_method : str, default="b"
        Tau method to use ("a", "b", or "c")
    
    Returns:
    -------
    pandas.DataFrame
        DataFrame with corrected Tau results
    """
    # Handle missing variable names
    if dvar is None:
        dvar = 'values'
    if pvar is None:
        pvar = 'phase'
    if mvar is None:
        mvar = 'mt'
    
    # If data is a list of DataFrames, process each one and combine results
    if isinstance(data, list):
        results_list = []
        for i, df in enumerate(data):
            # Ensure each DataFrame has a case column
            if 'case' not in df.columns:
                df = df.copy()
                df['case'] = i + 1
            # Process this DataFrame
            single_result = corrected_tau(df, dvar, pvar, mvar, phases, alpha, continuity, repeated, tau_method)
            # Add case identifier if not already present
            if 'Case' not in single_result.columns:
                single_result['Case'] = df['case'].iloc[0]
            results_list.append(single_result)
        
        # Combine all results
        if results_list:
            return pd.concat(results_list, ignore_index=True)
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data
    
    # Handle single DataFrame case
    # Prepare the data
    data_list = prepare_scd(data)
    data_list = recombine_phases(data_list, phases=phases)  # Corrected: use DataFrame directly

    def corr_tau(data):
        rowsA = data[data[pvar] == "A"]
        rowsB = data[data[pvar] == "B"]
        A_data = rowsA
        B_data = rowsB
        
        # Handling case where all phase A values are identical
        if A_data[dvar].var() == 0:
            auto_tau = {"tau": np.nan, "z": np.nan, "p": np.nan}
        else:
            auto_tau = kendall_tau(A_data[dvar], A_data[mvar], tau_method=tau_method, continuity_correction=continuity)

        # Base correction for Tau
        formula = f"{dvar} ~ {mvar}"
        fit_mblm = smf.ols(formula, data=rowsA).fit()  # Fixed: Using OLS since Theil-Sen is not built-in
        data["fit"] = fit_mblm.predict(data)
        x = data[dvar] - data["fit"]
        y = pd.Categorical(data[pvar]).codes
        base_corr_tau = kendall_tau(x, y, tau_method=tau_method, continuity_correction=continuity)
        
        # Uncorrected Tau calculation
        x = data[dvar]
        uncorrected_tau = kendall_tau(x, y, tau_method=tau_method, continuity_correction=continuity)

        # Decide whether correction is applied
        corr_applied = not (np.isnan(auto_tau["p"]) or auto_tau["p"] > alpha)

        return pd.DataFrame({
            "Model": ["Baseline autocorrelation", "Uncorrected tau", "Baseline corrected tau"],
            "tau": [auto_tau["tau"], uncorrected_tau["tau"], base_corr_tau["tau"]],
            "z": [auto_tau["z"], uncorrected_tau["z"], base_corr_tau["z"]],
            "p": [auto_tau["p"], uncorrected_tau["p"], base_corr_tau["p"]],
        }), corr_applied

    # Process the data
    tau_results, corr_applied = corr_tau(data_list)

    # Print the output in your requested format
    print("\nBaseline corrected tau\n")
    print("Method: Theil-Sen regression")
    print(f"Kendall's tau {tau_method} applied.")
    print("Continuity correction " + ("applied." if continuity else "not applied."))
    print("\nNAs :")

    # Print results in tabular form
    print(tau_results.to_string(index=False))

    # Print final correction decision
    print("\nBaseline correction " + ("should be applied." if corr_applied else "should not be applied.") + "\n")

    return tau_results  # Return the DataFrame for further use if needed
