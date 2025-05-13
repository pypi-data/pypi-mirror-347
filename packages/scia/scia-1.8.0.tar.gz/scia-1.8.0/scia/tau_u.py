import numpy as np
import pandas as pd
from scipy.stats import norm

def kendall_tau(x, y, tau_method="b", continuity_correction=False):
    """
    Calculate Kendall's Tau correlation between two variables.

    Parameters:
    - x: First variable (array-like)
    - y: Second variable (array-like)
    - tau_method: 'a' or 'b' (tau-a or tau-b)
    - continuity_correction: Whether to apply continuity correction

    Returns:
    - Dictionary with Kendall's Tau statistics
    """
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")

    # Calculate concordant and discordant pairs
    C = 0
    D = 0
    for i in range(n-1):
        for j in range(i+1, n):
            if x[j] > x[i]:
                if y[j] > y[i]:
                    C += 1
                elif y[j] < y[i]:
                    D += 1
            elif x[j] < x[i]:
                if y[j] < y[i]:
                    C += 1
                elif y[j] > y[i]:
                    D += 1

    # Calculate S (sum of concordant minus discordant pairs)
    S = C - D

    # Count ties
    x_ties = {}
    y_ties = {}
    for i in range(n):
        x_val = x[i]
        y_val = y[i]
        x_ties[x_val] = x_ties.get(x_val, 0) + 1
        y_ties[y_val] = y_ties.get(y_val, 0) + 1

    # Calculate tie adjustments
    ti = sum(t * (t - 1) // 2 for t in x_ties.values() if t > 1)
    ui = sum(t * (t - 1) // 2 for t in y_ties.values() if t > 1)

    # Number of possible pairs
    n0 = n * (n - 1) // 2

    # Calculate tau based on method
    if tau_method == "a":
        Den = n0
        tau = S / Den if Den > 0 else 0
        se = np.sqrt((2 * n + 5) / Den) / 3 if Den > 0 else 0
        sdS = S / (3 * S / np.sqrt(n * (n - 1) * (2 * n + 5) / 2)) if S != 0 else 0
        varS = sdS ** 2
        
        if not continuity_correction:
            z = 3 * S / np.sqrt(n * (n - 1) * (2 * n + 5) / 2) if n > 1 else 0
        else:
            z = 3 * (np.sign(S) * (abs(S) - 1)) / np.sqrt(n * (n - 1) * (2 * n + 5) / 2) if n > 1 else 0
    else:  # tau_method == "b"
        Den = np.sqrt((n0 - ti) * (n0 - ui))
        tau = S / Den if Den > 0 else 0
        
        # Calculate variance components for Tau-b
        v0 = n * (n - 1) * (2 * n + 5)
        vt = sum((t * (t - 1)) * (2 * t + 5) for t in x_ties.values() if t > 1)
        vu = sum((t * (t - 1)) * (2 * t + 5) for t in y_ties.values() if t > 1)
        v1 = sum(t * (t - 1) for t in x_ties.values() if t > 1) * sum(t * (t - 1) for t in y_ties.values() if t > 1)
        v2 = sum((t * (t - 1)) * (t - 2) for t in x_ties.values() if t > 1) * sum((t * (t - 1)) * (t - 2) for t in y_ties.values() if t > 1)
        
        varS = (v0 - vt - vu) / 18 + (v1 / (2 * n * (n - 1))) + (v2 / (9 * n * (n - 1) * (n - 2))) if n > 2 else 0
        sdS = np.sqrt(varS) if varS > 0 else 0
        se = sdS / Den if Den > 0 else 0
        
        if not continuity_correction:
            z = S / sdS if sdS > 0 else 0
        else:
            z = (np.sign(S) * (abs(S) - 1)) / sdS if sdS > 0 else 0

    # Calculate p-value
    p = 2 * (1 - norm.cdf(abs(z))) if not np.isnan(z) and not np.isinf(z) else np.nan
    
    if np.isinf(z) or np.isnan(z):
        p = np.nan
        tau = np.nan

    return {
        "N": n,
        "n0": n0,
        "ti": ti,
        "ui": ui,
        "nC": C,
        "nD": D,
        "S": S,
        "D": Den,
        "tau": tau,
        "varS": varS,
        "sdS": sdS,
        "se": se,
        "z": z,
        "p": p
    }

def tau_z(tau):
    """
    Fisher's z transformation for tau.
    """
    if tau >= 1:
        return float('inf')
    elif tau <= -1:
        return float('-inf')
    else:
        return 0.5 * np.log((1 + tau) / (1 - tau))

def inv_tau_z(z):
    """
    Inverse Fisher's z transformation for tau.
    """
    if z == float('inf'):
        return 1
    elif z == float('-inf'):
        return -1
    else:
        return (np.exp(2 * z) - 1) / (np.exp(2 * z) + 1)

def tau_ci(tau, n, ci=0.95, se_method="z"):
    """
    Calculate confidence interval for Kendall's tau.

    Parameters:
    - tau: Calculated tau value
    - n: Number of observations
    - ci: Confidence interval level (default: 0.95)
    - se_method: Method to calculate standard error ("z" or "tau")

    Returns:
    - Dictionary with tau and CI information
    """
    z_val = norm.ppf(1 - (1 - ci) / 2)
    
    if se_method == "tau":
        se_z = np.sqrt(0.437 / (n - 4)) if n > 4 else np.nan
    elif se_method == "z":
        se_z = 1 / np.sqrt(n - 3) if n > 3 else np.nan
    
    tau_z_val = tau_z(tau)
    tau_z_ci_lower = tau_z_val - z_val * se_z
    tau_z_ci_upper = tau_z_val + z_val * se_z
    
    return {
        "tau": inv_tau_z(tau_z_val),
        "n": n,
        "tau_ci_lower": inv_tau_z(tau_z_ci_lower),
        "tau_ci_upper": inv_tau_z(tau_z_ci_upper),
        "tau_z": tau_z_val,
        "tau_z_ci_lower": tau_z_ci_lower,
        "tau_z_ci_upper": tau_z_ci_upper,
        "se_z": se_z,
        "se_method": se_method
    }

def meta_tau(tau_values, n_values, ci=0.95, se_method="z"):
    """
    Perform meta-analysis of tau values.

    Parameters:
    - tau_values: List of tau values
    - n_values: List of sample sizes
    - ci: Confidence interval level
    - se_method: Method to calculate standard error

    Returns:
    - Dictionary with meta-analysis results
    """
    ci_z = norm.ppf(1 - (1 - ci) / 2)
    tau_z_values = [tau_z(t) for t in tau_values]
    
    if se_method == "tau":
        se_z_values = [np.sqrt(0.437 / (n - 4)) if n > 4 else np.nan for n in n_values]
    elif se_method == "z":
        se_z_values = [1 / np.sqrt(n - 3) if n > 3 else np.nan for n in n_values]
    
    # Filter out NaN values
    valid_indices = [i for i, se in enumerate(se_z_values) if not np.isnan(se) and not np.isinf(se)]
    
    if not valid_indices:
        return {
            "tau": np.nan,
            "lower": np.nan,
            "upper": np.nan,
            "z": np.nan,
            "p": np.nan,
            "se": np.nan
        }
    
    filtered_tau_z = [tau_z_values[i] for i in valid_indices]
    filtered_se_z = [se_z_values[i] for i in valid_indices]
    
    weights = [1 / (se ** 2) for se in filtered_se_z]
    weighted_sum = sum(t * w for t, w in zip(filtered_tau_z, weights))
    sum_weights = sum(weights)
    
    if sum_weights == 0:
        return {
            "tau": np.nan,
            "lower": np.nan,
            "upper": np.nan,
            "z": np.nan,
            "p": np.nan,
            "se": np.nan
        }
    
    weighted_tau_z = weighted_sum / sum_weights
    se_weighted = np.sqrt(1 / sum_weights)
    
    z_stat = weighted_tau_z / se_weighted
    p_value = 2 * (1 - norm.cdf(abs(z_stat)))
    
    return {
        "tau": inv_tau_z(weighted_tau_z),
        "lower": inv_tau_z(weighted_tau_z - ci_z * se_weighted),
        "upper": inv_tau_z(weighted_tau_z + ci_z * se_weighted),
        "z": z_stat,
        "p": p_value,
        "se": se_weighted,
        "ci": ci,
        "se_method": se_method
    }

def format_p_value(p):
    """Format p-value for display"""
    if np.isnan(p):
        return ""
    elif p < 0.001:
        return "<.001"
    elif p < 0.05:
        return "<.05"
    else:
        return f"{p:.2f}"

def create_scd(values, name=None):
    """
    Create a single-case design dataset.
    
    Parameters:
    - values: Dictionary mapping phases to value lists
    - name: Name of the case
    
    Returns:
    - Dictionary representing a single-case dataset
    """
    return {
        "values": values,
        "name": name if name is not None else "Case"
    }

def meta_tau_u(tables, ci=0.95, se_method="z"):
    """
    Perform meta-analysis of Tau-U values across cases.

    Parameters:
    - tables: List of Tau-U tables from individual cases
    - ci: Confidence interval level
    - se_method: Method to calculate standard error

    Returns:
    - DataFrame with meta-analysis results
    """
    models = ["A vs. B", "A vs. B - Trend A", "A vs. B + Trend B", "A vs. B + Trend B - Trend A"]
    meta_df = pd.DataFrame(columns=["Model", "Tau_U", "se", "CI lower", "CI upper", "z", "p"])
    
    for model in models:
        tau_values = []
        n_values = []
        
        for table in tables:
            tau = table.loc[model, "Tau"]
            n = table.loc[model, "n"]
            
            if not np.isnan(tau) and not np.isnan(n):
                tau_values.append(tau)
                n_values.append(n)
        
        if tau_values and n_values:
            meta_result = meta_tau(tau_values, n_values, ci=ci, se_method=se_method)
            
            new_row = pd.DataFrame({
                "Model": [model],
                "Tau_U": [meta_result["tau"]],
                "se": [meta_result["se"]],
                "CI lower": [meta_result["lower"]],
                "CI upper": [meta_result["upper"]],
                "z": [meta_result["z"]],
                "p": [meta_result["p"]]
            })
            
            meta_df = pd.concat([meta_df, new_row], ignore_index=True)
    
    return meta_df

class TauUResult:
    """Class to store the results of a Tau-U analysis."""
    
    def __init__(self, method, tau_method, phases, continuity_correction, ci, ci_method):
        """Initialize the TauUResult object."""
        self.method = method
        self.tau_method = tau_method
        self.phases = phases
        self.continuity_correction = continuity_correction
        self.ci = ci
        self.ci_method = ci_method
        self.case_tables = {}
        self.meta_analysis = None
        self.meta_weight_method = None
    
    def add_case_table(self, case_name, table):
        """Add a case table to the result."""
        # Format the table for display
        display_cols = ["Tau", "CI lower", "CI upper", "SD_S", "Z", "p_formatted"]
        display_names = ["Tau", "CI lower", "CI upper", "SD_S", "Z", "p"]
        
        display_table = table[display_cols].copy()
        display_table.columns = display_names
        
        self.case_tables[case_name] = display_table
    
    def set_meta_analysis(self, meta_analysis, meta_weight_method):
        """Set the meta-analysis results."""
        self.meta_analysis = meta_analysis
        self.meta_weight_method = meta_weight_method
    
    def __str__(self):
        """Create a formatted string representation of the results."""
        output = f"Tau-U\n"
        output += f"Method: {self.method}\n"
        output += f"Applied Kendall's Tau-{self.tau_method}\n"
        
        if self.ci is not None:
            output += f"{int(self.ci*100)}% CIs for tau are reported.\n"
            output += f"CI method: {self.ci_method}\n"
        
        # Add meta-analysis if performed
        if self.meta_analysis is not None:
            output += "\nTau-U meta analyses:\n"
            output += f"Weight method: {self.meta_weight_method}\n"
            output += f"{int(self.ci*100)}% CIs are reported.\n\n"
            
            # Format the meta-analysis DataFrame for display
            meta_display = self.meta_analysis.copy()
            meta_display["Tau_U"] = meta_display["Tau_U"].map(lambda x: f"{x:.2f}")
            meta_display["se"] = meta_display["se"].map(lambda x: f"{x:.1f}")
            meta_display["CI lower"] = meta_display["CI lower"].map(lambda x: f"{x:.2f}")
            meta_display["CI upper"] = meta_display["CI upper"].map(lambda x: f"{x:.2f}")
            meta_display["z"] = meta_display["z"].map(lambda x: f"{x:.1f}")
            meta_display["p"] = meta_display["p"].map(lambda x: f"{x:.1e}")
            
            output += meta_display.to_string(index=False) + "\n"
        
        # Add individual case results
        for case_name, table in self.case_tables.items():
            output += f"\nCase: {case_name}\n"
            output += table.to_string() + "\n"
        
        return output
    
    def __repr__(self):
        """Return a string representation of the object."""
        return self.__str__()

def tau_u(data_list, dvar="values", pvar="phase", method="complete", phases=("A", "B"),
          meta_analyses=True, ci=0.95, ci_method="z", meta_weight_method="z",
          tau_method="b", continuity_correction=False):
    """
    Compute Tau-U for single-case or multiple-case datasets.

    Parameters:
    - data_list: Single case data or list of single-case datasets
    - dvar: Name of the dependent variable column
    - pvar: Name of the phase variable column
    - method: One of "complete", "parker", or "tarlow"
    - phases: Phases to compare (default: ("A", "B"))
    - meta_analyses: Whether to perform meta-analysis across cases
    - ci: Confidence interval level (default: 0.95)
    - ci_method: Method for CI calculation ("z", "tau", or "s")
    - meta_weight_method: Weighting method for meta-analysis ("z" or "tau")
    - tau_method: Kendall's tau method ("a" or "b")
    - continuity_correction: Whether to apply continuity correction

    Returns:
    - TauUResult object containing tables and meta-analysis results
    """
    # Adjust method parameters
    if method == "parker":
        tau_method = "a"
        continuity_correction = False
    elif method == "tarlow":
        tau_method = "a"
        continuity_correction = True
    
    # Create result object
    result = TauUResult(
        method=method,
        tau_method=tau_method,
        phases=phases,
        continuity_correction=continuity_correction,
        ci=ci,
        ci_method=ci_method
    )
    
    # Convert single case to list if needed
    if not isinstance(data_list, list):
        data_list = [data_list]
    
    # Process data to a standardized format
    processed_data = []
    case_names = []
    
    for i, data in enumerate(data_list):
        if isinstance(data, dict) and "values" in data:
            # Dictionary format with values
            case_name = data.get("name", f"Case{i+1}")
            case_names.append(case_name)
            
            # Convert to DataFrame
            phases_list = []
            values_list = []
            
            for phase, phase_values in data["values"].items():
                phases_list.extend([phase] * len(phase_values))
                values_list.extend(phase_values)
            
            df = pd.DataFrame({
                pvar: phases_list,
                dvar: values_list
            })
            processed_data.append(df)
        else:
            # Already a DataFrame
            case_names.append(f"Case{i+1}")
            processed_data.append(data)
    
    row_names = ["A vs. B", "Trend A", "Trend B", "A vs. B - Trend A",
                 "A vs. B + Trend B", "A vs. B + Trend B - Trend A"]
    col_names = ["n", "pairs", "pos", "neg", "ties", "S", "D", "Tau",
                 "CI lower", "CI upper", "SD_S", "VAR_S", "SE_Tau", "Z", "p"]

    all_tables = []
    tau_u_values = []

    # Process each case
    for case_idx, (case_name, data) in enumerate(zip(case_names, processed_data)):
        # Initialize table for this case
        table_tau = pd.DataFrame(index=row_names, columns=col_names)
        
        # Get A and B phase data
        A_data = data[data[pvar] == "A"][dvar].dropna().values
        B_data = data[data[pvar] == "B"][dvar].dropna().values
        
        # Check if we have enough data
        if len(A_data) < 2 or len(B_data) < 1:
            continue
        
        # Combined data
        AB_data = np.concatenate([A_data, B_data])
        
        # Get dimensions
        nA = len(A_data)
        nB = len(B_data)
        nAB = nA + nB
        
        # Count comparisons
        AvApos, AvAneg, AvAtie = 0, 0, 0
        BvBpos, BvBneg, BvBtie = 0, 0, 0
        AvBpos, AvBneg, AvBtie = 0, 0, 0
        
        # A vs A comparisons
        for i in range(nA - 1):
            for j in range(i + 1, nA):
                if A_data[i] < A_data[j]:
                    AvApos += 1
                elif A_data[i] > A_data[j]:
                    AvAneg += 1
                else:
                    AvAtie += 1
        
        # B vs B comparisons
        for i in range(nB - 1):
            for j in range(i + 1, nB):
                if B_data[i] < B_data[j]:
                    BvBpos += 1
                elif B_data[i] > B_data[j]:
                    BvBneg += 1
                else:
                    BvBtie += 1
        
        # A vs B comparisons
        for a in A_data:
            for b in B_data:
                if a < b:
                    AvBpos += 1
                elif a > b:
                    AvBneg += 1
                else:
                    AvBtie += 1
        
        # Create phase indicators for Kendall calculations
        phase_indicator = np.concatenate([np.zeros(nA), np.ones(nB)])
        time_A = np.arange(1, nA + 1)
        time_B = np.arange(1, nB + 1)
        time_AB_A = np.concatenate([np.arange(nA, 0, -1), np.full(nB, nA + 1)])
        time_AB_B = np.concatenate([np.zeros(nA), np.arange(nA + 1, nAB + 1)])
        time_AB_B_A = np.concatenate([np.arange(nA, 0, -1), np.arange(nA + 1, nAB + 1)])
        
        # Calculate Kendall's tau values
        if method == "complete" and tau_method == "a":
            tau_s = {
                "AvB": kendall_tau(AB_data, phase_indicator, tau_method="a", continuity_correction=continuity_correction),
                "AvA": kendall_tau(A_data, time_A, tau_method="a", continuity_correction=continuity_correction),
                "BvB": kendall_tau(B_data, time_B, tau_method="a", continuity_correction=continuity_correction),
                "AvB_A": kendall_tau(AB_data, time_AB_A, tau_method="a", continuity_correction=continuity_correction),
                "AvB_B": kendall_tau(AB_data, time_AB_B, tau_method="a", continuity_correction=continuity_correction),
                "AvB_B_A": kendall_tau(AB_data, time_AB_B_A, tau_method="a", continuity_correction=continuity_correction)
            }
        else:
            tau_s = {
                "AvB": kendall_tau(AB_data, phase_indicator, tau_method="b", continuity_correction=continuity_correction),
                "AvA": kendall_tau(A_data, time_A, tau_method="b", continuity_correction=continuity_correction),
                "BvB": kendall_tau(B_data, time_B, tau_method="b", continuity_correction=continuity_correction),
                "AvB_A": kendall_tau(AB_data, time_AB_A, tau_method="b", continuity_correction=continuity_correction),
                "AvB_B": kendall_tau(AB_data, time_AB_B, tau_method="b", continuity_correction=continuity_correction),
                "AvB_B_A": kendall_tau(AB_data, time_AB_B_A, tau_method="b", continuity_correction=continuity_correction)
            }
        
        # Fill in N values
        table_tau["n"] = [
            tau_s["AvB"]["N"],
            tau_s["AvA"]["N"],
            tau_s["BvB"]["N"],
            tau_s["AvB_A"]["N"],
            tau_s["AvB_B"]["N"],
            tau_s["AvB_B_A"]["N"]
        ]
        
        # Calculate number of pairs
        AvB_pair = nA * nB
        AvA_pair = nA * (nA - 1) // 2
        BvB_pair = nB * (nB - 1) // 2
        ABvAB_pair = nAB * (nAB - 1) // 2
        
        # Fill in pairs
        table_tau["pairs"] = [
            AvB_pair,
            AvA_pair,
            BvB_pair,
            AvB_pair + AvA_pair,
            AvB_pair + BvB_pair,
            AvB_pair + AvA_pair + BvB_pair
        ]
        
        if method == "parker":
            table_tau.loc["A vs. B - Trend A", "pairs"] = AvB_pair
            table_tau.loc["A vs. B + Trend B - Trend A", "pairs"] = ABvAB_pair
        
        # Fill in pos/neg/ties counts
        table_tau["pos"] = [
            AvBpos,
            AvApos,
            BvBpos,
            AvBpos + AvAneg,
            AvBpos + BvBpos,
            AvBpos + BvBpos + AvAneg
        ]
        
        table_tau["neg"] = [
            AvBneg,
            AvAneg,
            BvBneg,
            AvBneg + AvApos,
            AvBneg + BvBneg,
            AvBneg + BvBneg + AvApos
        ]
        
        table_tau["ties"] = [
            AvBtie,
            AvAtie,
            BvBtie,
            AvBtie + AvAtie,
            AvBtie + BvBtie,
            AvBtie + BvBtie + AvAtie
        ]
        
        # Fill in S values
        table_tau["S"] = [
            tau_s["AvB"]["S"],
            tau_s["AvA"]["S"],
            tau_s["BvB"]["S"],
            tau_s["AvB_A"]["S"],
            tau_s["AvB_B"]["S"],
            tau_s["AvB_B_A"]["S"]
        ]
        
        # Fill in D values
        if method == "complete" and tau_method == "b":
            table_tau["D"] = [
                tau_s["AvB"]["D"],
                tau_s["AvA"]["D"],
                tau_s["BvB"]["D"],
                tau_s["AvB_A"]["D"],
                tau_s["AvB_B"]["D"],
                tau_s["AvB_B_A"]["D"]
            ]
            table_tau.loc["A vs. B", "D"] = table_tau.loc["A vs. B", "pairs"] - table_tau.loc["A vs. B", "ties"] / 2
        else:
            table_tau["D"] = table_tau["pairs"]
        
        # Calculate Tau values
        table_tau["Tau"] = table_tau["S"] / table_tau["D"]
        
        # Calculate standard deviations
        if method == "tarlow":
            table_tau["SD_S"] = [
                tau_s["AvB"]["sdS"],
                tau_s["AvA"]["sdS"],
                tau_s["BvB"]["sdS"],
                tau_s["AvB_A"]["sdS"],
                tau_s["AvB_B"]["sdS"],
                tau_s["AvB_B_A"]["sdS"]
            ]
        else:
            # Use theoretical SD calculation
            table_tau.loc["A vs. B", "SD_S"] = np.sqrt((nA * nB) * (nA + nB + 1) / 12) * 2
            table_tau.loc["Trend A", "SD_S"] = kendall_tau(time_A, time_A, tau_method=tau_method)["sdS"]
            table_tau.loc["Trend B", "SD_S"] = kendall_tau(time_B, time_B, tau_method=tau_method)["sdS"]
            table_tau.loc["A vs. B - Trend A", "SD_S"] = tau_s["AvB_A"]["sdS"]
            table_tau.loc["A vs. B + Trend B", "SD_S"] = tau_s["AvB_B"]["sdS"]
            table_tau.loc["A vs. B + Trend B - Trend A", "SD_S"] = tau_s["AvB_B_A"]["sdS"]
        
        # Calculate variance
        table_tau["VAR_S"] = table_tau["SD_S"] ** 2
        
        # Fill in Z values
        table_tau["Z"] = [
            tau_s["AvB"]["z"],
            tau_s["AvA"]["z"],
            tau_s["BvB"]["z"],
            tau_s["AvB_A"]["z"],
            tau_s["AvB_B"]["z"],
            tau_s["AvB_B_A"]["z"]
        ]
        
        # Fill in p-values
        table_tau["p"] = [
            tau_s["AvB"]["p"],
            tau_s["AvA"]["p"],
            tau_s["BvB"]["p"],
            tau_s["AvB_A"]["p"],
            tau_s["AvB_B"]["p"],
            tau_s["AvB_B_A"]["p"]
        ]
        
        # Calculate standard errors
        table_tau["SE_Tau"] = table_tau["Tau"] / table_tau["Z"]
        table_tau["SE_Tau"] = table_tau["SE_Tau"].replace([np.inf, -np.inf], np.nan)
        
        # Calculate confidence intervals
        if ci is not None:
            if ci_method == "s":
                see = norm.ppf(1 - (1 - ci) / 2)
                S = table_tau["S"].copy()
                if continuity_correction:
                    S = S - 1
                table_tau["CI lower"] = (S - table_tau["SD_S"] * see) / table_tau["D"]
                table_tau["CI upper"] = (S + table_tau["SD_S"] * see) / table_tau["D"]
            else:
                for idx in table_tau.index:
                    n = nAB  # Use total sample size
                    tau_val = table_tau.loc[idx, "Tau"]
                    cis = tau_ci(tau_val, n, ci=ci, se_method=ci_method)
                    table_tau.loc[idx, "CI lower"] = cis["tau_ci_lower"]
                    table_tau.loc[idx, "CI upper"] = cis["tau_ci_upper"]
        else:
            table_tau["CI lower"] = np.nan
            table_tau["CI upper"] = np.nan
        
        # Format p-values for display
        table_tau["p_formatted"] = table_tau["p"].apply(format_p_value)
        
        # Store table
        all_tables.append(table_tau)
        tau_u_values.append(table_tau.loc["A vs. B - Trend A", "Tau"])
        
        # Add the case table to the result
        result.add_case_table(case_name, table_tau)
    
    # Perform meta-analysis if requested and we have multiple cases
    if meta_analyses and len(all_tables) > 1:
        meta_result = meta_tau_u(all_tables, ci=ci, se_method=meta_weight_method)
        result.set_meta_analysis(meta_result, meta_weight_method)
    
    # Return the appropriate output
    if len(all_tables) == 1 and not meta_analyses:
        # For a single case with no meta-analysis, return the case table
        return list(result.case_tables.values())[0]
    else:
        # For multiple cases or with meta-analysis, return the result object
        return result

# # Example usage:
# if __name__ == "__main__":
#     # Create example data
#     charlotte = create_scd(
#         values={"A": [5, 7, 10, 5, 12], "B": [7, 10, 18, 15, 14, 19]},
#         name="Charlotte"
#     )

#     theresa = create_scd(
#         values={"A": [3, 4, 3, 5], "B": [7, 4, 7, 9, 8, 10, 12]},
#         name="Theresa"
#     )

#     antonia = create_scd(
#         values={"A": [9, 8, 8, 7, 5, 7], "B": [6, 14, 15, 12, 16]},
#         name="Antonia"
#     )

#     # Combine cases into a list
#     mbd = [charlotte, theresa, antonia]

#     # Run Tau-U analysis
#     result = tau_u(mbd)
#     print(result)

#     # Single case analysis
#     single_result = tau_u(charlotte)
#     print("\nSingle case analysis:")
#     print(single_result)