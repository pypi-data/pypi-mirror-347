
import pandas as pd
import numpy as np
from scia.preprocess import prepare_scd
from scia.recombine import recombine_phases
from scia.utils import revise_names
from scia.pand import pand

def ird(data, dvar="values", pvar="phase", decreasing=False, phases=("A", "B")):
    """
    Compute the Improvement Rate Difference (IRD) for single-case data.
    
    Parameters:
    - data (pd.DataFrame or list): The single-case dataset or list of datasets.
    - dvar (str): Name of the dependent variable column.
    - pvar (str): Name of the phase variable column.
    - decreasing (bool, default=False): If True, considers lower values in Phase B as improvement.
    - phases (tuple, default=("A", "B")): Phases to compare.
    """
    
    # Handle list of DataFrames (multiple cases)
    if isinstance(data, list):
        # Process each DataFrame separately but suppress their individual output
        results = []
        for i, df in enumerate(data):
            # Ensure each DataFrame has a case column
            if 'case' not in df.columns:
                df = df.copy()
                df['case'] = i + 1
                
            # Calculate IRD for this case without printing
            # Prepare the data
            case_data = prepare_scd(df)
            recombined_data = recombine_phases(case_data, phases=phases)
            keep = recombined_data["data"] if isinstance(recombined_data, dict) else recombined_data
            
            # Calculate PAND with 'minimum' method
            pa = pand(case_data, dvar=dvar, pvar=pvar, decreasing=decreasing, 
                      phases=phases, method="minimum", return_values=True)
            
            # Calculate IRD
            ird_value = 1 - (((pa["n"]**2) / (2 * pa["n_a"] * pa["n_b"])) * (1 - (pa["pand"] / 100)))
            results.append(ird_value)
        
        # Print results for each case
        for i, result in enumerate(results):
            print(f"Case {i+1}: IRD = {result}")
        
        # Calculate and print average IRD
        avg_ird = sum(results) / len(results)
        print(f"All cases Average: {avg_ird}")
        
        # Return None instead of the average IRD
        return None
    
    # Ensure "case" column exists
    if "case" not in data.columns:
        data["case"] = "Default_Case"
        
    # Prepare the data
    data = prepare_scd(data)
    recombined_data = recombine_phases(data, phases=phases)
    keep = recombined_data["data"] if isinstance(recombined_data, dict) else recombined_data
    
    # Get case names
    case_names = revise_names(keep["case"].unique(), len(keep["case"].unique()))
    
    # Calculate PAND with 'minimum' method (as used in R function)
    # Using return_values=True to get only the numeric values needed for IRD calculation
    pa = pand(data, dvar=dvar, pvar=pvar, decreasing=decreasing, 
              phases=phases, method="minimum", return_values=True)
    
    # Calculate IRD using the formula from the R function
    # IRD = 1 - ((n² / (2 * n_a * n_b)) * (1 - (pand / 100)))
    ird_value = 1 - (((pa["n"]**2) / (2 * pa["n_a"] * pa["n_b"])) * (1 - (pa["pand"] / 100)))
    
    # For single case, just print the IRD value once
    print(f"IRD = {ird_value}")
    
    # Return None instead of the IRD value
    return None