import patsy
from patsy import ModelDesc

def create_random_formula(mvar, slope, level, trend, var_phase, var_inter, intercept=True, syntax="lm"):
    """
    Create a formula for random effects model.
    
    Parameters:
    ----------
    mvar : str
        Name of the measurement-time variable
    slope : bool
        Whether to include slope parameters
    level : bool
        Whether to include level parameters
    trend : bool
        Whether to include trend parameter
    var_phase : list
        Names of phase dummy variables
    var_inter : list
        Names of interaction dummy variables
    intercept : bool, default=True
        Whether to include intercept
    syntax : str, default="lm"
        Syntax type: "lm" for linear mixed models or "mcmc" for Bayesian models
    
    Returns:
    -------
    patsy.ModelDesc
        Formula object for model fitting
    """
    parameters = []
    
    if intercept:
        parameters.append("1")
    
    if trend:
        parameters.append(mvar)
    
    if level:
        parameters.extend(var_phase)
    
    if slope:
        parameters.extend(var_inter)
    
    if syntax == "lm":
        formula_str = f"~ {' + '.join(parameters)} | case"
    elif syntax == "mcmc":
        formula_str = f"~ us({' + '.join(parameters)}):case"
    else:
        raise ValueError(f"Unknown syntax: {syntax}. Use 'lm' or 'mcmc'.")
    
    # Create a formula object using patsy
    return patsy.ModelDesc.from_formula(formula_str)