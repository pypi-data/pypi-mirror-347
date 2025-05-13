import numpy as np
import pandas as pd

def print_hplm(hplm_result):
    """
    Format and print hierarchical piecewise linear regression results.
    
    Parameters:
    ----------
    hplm_result : dict
        The result dictionary from hplm function
    
    Returns:
    -------
    str
        Formatted string representation of the results
    """
    # Extract model information
    model = hplm_result["model"]
    n_cases = hplm_result["N"]
    contrast = hplm_result["contrast"]
    result = hplm_result["hplm"]
    
    # Create header
    output = "Hierarchical Piecewise Linear Regression\n\n"
    output += f"Estimation method {model['estimation_method']}\n"
    output += f"Contrast model: {model['interaction_method']} / "
    output += f"level: {contrast['level']}, slope: {contrast['slope']}\n"
    output += f"{n_cases} Cases\n\n"
    
    # Add AIC and BIC
    output += f"AIC = {result.aic:.4f}, BIC = {result.bic:.4f}\n"
    
    # Add ICC information if available
    if "ICC" in hplm_result and hplm_result["ICC"] is not None:
        icc = hplm_result["ICC"]
        output += f"ICC = {icc['value']:.3f}; L = {icc['L']:.1f}; p = {icc['p']:.3f}\n"
    
    # Add fixed effects table
    output += "\nFixed effects (" + model['fixed'] + ")\n\n"
    
    # Get parameter estimates
    params = result.params
    bse = result.bse
    tvalues = result.tvalues
    pvalues = result.pvalues
    df_resid = result.df_resid
    
    # Create fixed effects table
    output += " " * 28 + "B    SE df     t     p\n"
    
    # Add each parameter
    for i, name in enumerate(params.index):
        # Format parameter name for display
        if name == "Intercept":
            param_name = "Intercept"
        elif name == "mt":
            param_name = "Trend (mt)"
        elif name in hplm_result.get("var_phase", []):
            phase_name = name.replace("phase_", "")
            param_name = f"Level phase {phase_name} ({name})"
        elif name in hplm_result.get("var_inter", []):
            param_name = f"Slope phase {name.replace('inter', '')} ({name})"
        else:
            param_name = name
            
        # Format the row with proper spacing
        output += f"{param_name:<28} {params[i]:5.3f} {bse[i]:4.3f} {df_resid:2.0f} {tvalues[i]:5.3f} {pvalues[i]:5.3f}\n"
    
    # Add random effects table
    output += "\nRandom effects (~" + model['random'] + " | case)\n\n"
    output += " " * 14 + "SD\n"
    
    # Extract random effects standard deviations
    try:
        re_sd = np.sqrt(np.diag(result.cov_re))
        output += f"Intercept {re_sd[0]:5.3f}\n"
    except:
        output += "Intercept N/A\n"
    
    # Add residual standard deviation
    output += f"Residual  {np.sqrt(result.scale):5.3f}\n"
    
    return output

# Example usage:
# formatted_result = print_hplm(hplm_result)
# print(formatted_result)