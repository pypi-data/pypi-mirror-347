import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.pnd import pnd
from scia.pem import pem
from scia.pet import pet
from scia.nap import nap
from scia.pand import pand
from scia.ird import ird
from scia.tau_u import tau_u
from scia.corrected_tau import corrected_tau
import io
import sys
from contextlib import redirect_stdout

# Define a context manager to suppress stdout
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        return sys.stdout
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

def extract_number_from_ird(result):
    """Extract numeric IRD value from the dictionary output of ird()."""
    if isinstance(result, dict) and "ird" in result:
        return float(result["ird"]) if result["ird"] is not None else np.nan
    return np.nan

def overlap(data, dvar=None, pvar=None, mvar=None, decreasing=False, phases=("A", "B")):
    # Handle missing variable names
    if dvar is None:
        dvar = 'values'
    if pvar is None:
        pvar = 'phase'
    if mvar is None:
        mvar = 'mt'

    # Prepare data
    data = prepare_scd(data)
    
    # Check if 'case' column exists, if not, add it
    # This must be done BEFORE recombine_phases
    if isinstance(data, pd.DataFrame) and 'case' not in data.columns:
        # If it's a single DataFrame, assign case 1
        data['case'] = 1
    elif isinstance(data, list):
        # If it's a list of DataFrames, ensure each has a case column
        for i, df in enumerate(data):
            if 'case' not in df.columns:
                df['case'] = i + 1
    
    # Now recombine phases after adding case column
    data = recombine_phases(data, phases=phases)
    
    # Get case names
    case_names = data["case"].unique()

    # Define DataFrame columns
    vars = ["PND", "PEM", "PET", "NAP", "NAP rescaled", "PAND", 
            "IRD", "Tau_U(A)", "Tau_U(BA)", "Base_Tau", "Diff_mean", 
            "Diff_trend", "SMD", "Hedges_g"]
    
    df = pd.DataFrame(columns=vars, index=range(len(case_names)))
    df['Case'] = case_names

    for i, case in enumerate(case_names):
        case_data = data[data["case"] == case]

        # Suppress output for all function calls
        with SuppressOutput():
            # Extract values safely
            df.at[i, 'PND'] = float(pnd(case_data, decreasing=decreasing)["PND (%)"].iloc[0].replace('%', ''))
            df.at[i, 'PEM'] = float(pem(case_data, decreasing=decreasing)["PEM"].iloc[0])
            df.at[i, 'PET'] = float(pet(case_data, decreasing=decreasing)["PET"].iloc[0])
            df.at[i, 'NAP'] = float(nap(case_data, decreasing=decreasing)["NAP"].iloc[0])
            df.at[i, 'NAP rescaled'] = float(nap(case_data, decreasing=decreasing)["NAP Rescaled"].iloc[0])
            df.at[i, 'PAND'] = float(pand(case_data, decreasing=decreasing, return_values=True)["pand"])
            
            # Extract IRD correctly
            ird_result = ird(case_data, dvar=dvar, pvar=pvar, decreasing=decreasing, phases=phases)
            df.at[i, 'IRD'] = extract_number_from_ird(ird_result)

            # Extract Tau-U values - handle TauUResult object properly
            tau_results = tau_u(case_data)
            try:
                # If it's a TauUResult object
                if hasattr(tau_results, 'case_tables'):
                    # Get the first (and only) case table
                    case_table = list(tau_results.case_tables.values())[0]
                    df.at[i, 'Tau_U(A)'] = float(case_table.loc["A vs. B - Trend A", "Tau"])
                    df.at[i, 'Tau_U(BA)'] = float(case_table.loc["A vs. B + Trend B - Trend A", "Tau"])
                # Try accessing as DataFrame first (for backward compatibility)
                elif hasattr(tau_results, 'loc'):
                    df.at[i, 'Tau_U(A)'] = float(tau_results.loc["A vs. B - Trend A", "Tau"])
                    df.at[i, 'Tau_U(BA)'] = float(tau_results.loc["A vs. B + Trend B - Trend A", "Tau"])
                # If it's a dictionary
                elif isinstance(tau_results, dict):
                    df.at[i, 'Tau_U(A)'] = float(tau_results.get("A vs. B - Trend A", {}).get("Tau", np.nan))
                    df.at[i, 'Tau_U(BA)'] = float(tau_results.get("A vs. B + Trend B - Trend A", {}).get("Tau", np.nan))
                else:
                    # Default to NaN if we can't extract the values
                    df.at[i, 'Tau_U(A)'] = np.nan
                    df.at[i, 'Tau_U(BA)'] = np.nan
            except (KeyError, AttributeError, ValueError):
                # Handle any errors by setting to NaN
                df.at[i, 'Tau_U(A)'] = np.nan
                df.at[i, 'Tau_U(BA)'] = np.nan
            
            # Extract Corrected Tau
            try:
                corrected_tau_results = corrected_tau(case_data)
                if isinstance(corrected_tau_results, pd.DataFrame):
                    baseline_tau = corrected_tau_results[corrected_tau_results["Model"] == "Baseline corrected tau"]["tau"]
                    df.at[i, 'Base_Tau'] = float(baseline_tau.iloc[0]) if not baseline_tau.empty else np.nan
                else:
                    df.at[i, 'Base_Tau'] = np.nan
            except:
                df.at[i, 'Base_Tau'] = np.nan

        # Compute mean differences, SMD, Hedges' g, trend differences
        A = case_data[case_data[pvar] == 'A'][dvar]
        B = case_data[case_data[pvar] == 'B'][dvar]
        mtA = case_data[case_data[pvar] == 'A'][mvar]
        mtB = case_data[case_data[pvar] == 'B'][mvar]

        nA = len(A.dropna())
        nB = len(B.dropna())
        n = nA + nB
        mA = A.mean()
        mB = B.mean()
        sdA = A.std()
        sdB = B.std()

        df.at[i, 'Diff_mean'] = mB - mA
        df.at[i, 'SMD'] = (mB - mA) / sdA if sdA != 0 else np.nan
        sd_hg = np.sqrt(((nA - 1) * sdA**2 + (nB - 1) * sdB**2) / (nA + nB - 2)) if nA + nB - 2 > 0 else np.nan
        df.at[i, 'Hedges_g'] = (mB - mA) / sd_hg if sd_hg is not np.nan else np.nan
        df.at[i, 'Hedges_g'] *= (1 - (3 / (4 * n - 9))) if n > 9 else np.nan

        trend_A = np.polyfit(mtA - mtA.iloc[0] + 1, A, 1)[0] if len(mtA) > 1 else np.nan
        trend_B = np.polyfit(mtB - mtB.iloc[0] + 1, B, 1)[0] if len(mtB) > 1 else np.nan
        df.at[i, 'Diff_trend'] = trend_B - trend_A if trend_A is not np.nan and trend_B is not np.nan else np.nan

    return df  # Return only the final DataFrame with no extra prints