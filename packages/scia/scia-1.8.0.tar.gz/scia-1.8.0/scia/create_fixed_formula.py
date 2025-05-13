import patsy
from patsy import ModelDesc

def create_fixed_formula(dvar, mvar, slope, level, trend, var_phase, var_inter, intercept=True):
    """
    Create a formula for fixed effects model.
    
    Parameters:
    ----------
    dvar : str
        Name of the dependent variable
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
    
    formula_str = f"{dvar} ~ {' + '.join(parameters)}"
    
    # Create a formula object using patsy
    return patsy.ModelDesc.from_formula(formula_str)