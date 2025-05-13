import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
import matplotlib.pyplot as plt

def rci(data, dvar=None, pvar=None, rel=0.8, ci=0.95, graph=False, phases=("A", "B")):
    """
    Calculate the Reliable Change Index (RCI) for single-case data.
    
    Parameters:
    ----------
    data : pandas.DataFrame
        Single-case data frame (cannot be applied to more than one case)
    dvar : str, optional
        Name of the dependent variable column
    pvar : str, optional
        Name of the phase variable column
    rel : float, default=0.8
        Reliability of the measurement (between 0 and 1)
    ci : float, default=0.95
        Confidence level (between 0 and 1)
    graph : bool, default=False
        Whether to display a graph of confidence intervals
    phases : tuple, default=("A", "B")
        Phases to include in the analysis
    
    Returns:
    -------
    None
        Prints RCI results but doesn't return any value
    """
    # Check arguments
    if isinstance(data, list):
        if len(data) > 1:
            print("RCI can not be applied to more than one case.")
            return None
        else:
            data = data[0]  # Extract the single case
    
    # Handle missing variable names
    if dvar is None:
        dvar = 'values'
    if pvar is None:
        pvar = 'phase'
    
    # Prepare data
    data = prepare_scd(data)
    
    # Ensure case column exists
    if 'case' not in data.columns:
        data['case'] = 1
        
    # Recombine phases
    data = recombine_phases(data, phases=phases)
    
    # Extract A and B phase values
    A = data[data[pvar] == "A"][dvar].dropna().values
    B = data[data[pvar] == "B"][dvar].dropna().values
    
    # Calculate statistics
    sA = np.std(A, ddof=1)  # Sample standard deviation
    sB = np.std(B, ddof=1)
    mA = np.mean(A)
    mB = np.mean(B)
    nA = len(A)
    nB = len(B)
    n = nA + nB
    
    # Standard errors
    seA = sA * np.sqrt(1 - rel)
    seB = sB * np.sqrt(1 - rel)
    
    # Standardized difference
    stand_dif = (mB - mA) / np.std(np.concatenate([A, B]), ddof=1)
    
    # Standard error of differences
    se_dif = np.sqrt(2 * seA**2)
    
    # Correlation between A and B
    cor_a_b = rel
    
    # Reliable detectable difference
    rdd = (sA**2 * rel + sB**2 * rel - 2 * sA * sB * cor_a_b) / (sA**2 + sB**2 - 2 * sA * sB * cor_a_b)
    
    # RCI calculations
    rci_jacobsen = (mB - mA) / seA
    rci_christensen = (mB - mA) / se_dif
    
    # Confidence intervals
    z = np.abs(np.percentile(np.random.normal(0, 1, 10000), 100 * (ci + 0.5 * (1 - ci))))
    ci_lower_A = mA - z * seA
    ci_upper_A = mA + z * seA
    ci_lower_B = mB - z * seB
    ci_upper_B = mB + z * seB
    
    # Create descriptives table
    descriptives = pd.DataFrame({
        'n': [nA, nB],
        'mean': [mA, mB],
        'SD': [sA, sB],
        'SE': [seA, seB]
    }, index=['A-Phase', 'B-Phase'])
    
    # Create confidence intervals table
    conf_intervals = pd.DataFrame({
        'Lower': [ci_lower_A, ci_lower_B],
        'Upper': [ci_upper_A, ci_upper_B]
    }, index=['A-Phase', 'B-Phase'])
    
    # Create RCI table
    rci_values = pd.DataFrame({
        'RCI': [rci_jacobsen, rci_christensen]
    }, index=['Jacobson et al.', 'Christensen and Mendoza'])
    
    # Display graph if requested
    if graph:
        plt.figure(figsize=(8, 6))
        plt.boxplot([
            [ci_lower_A, ci_upper_A],
            [ci_lower_B, ci_upper_B]
        ], labels=['A-Phase', 'B-Phase'])
        plt.ylabel('Mean')
        plt.title(f"{int(ci * 100)}% confidence interval (rtt = {rel:.2f})")
        plt.show()
    
    # Print results
    print("Reliable Change Index\n")
    print(f"Mean Difference = {mB - mA:.3f}")
    print(f"Standardized Difference = {stand_dif:.3f}")
    print(f"Standard error of differences = {se_dif:.3f}")
    print(f"Reliability of measurements = {rel}\n")
    
    print("Descriptives:")
    print(descriptives.to_string())
    print()
    
    print(f"{int(ci * 100)}% Confidence Intervals:")
    print(conf_intervals.to_string())
    print()
    
    print("Reliable Change Indices:")
    print(rci_values.to_string())
    
    # Don't return anything to avoid showing the dictionary
    return None