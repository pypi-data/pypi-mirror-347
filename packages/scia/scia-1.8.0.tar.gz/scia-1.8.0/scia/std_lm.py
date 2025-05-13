import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import RegressionResultsWrapper

def std_lm(model):
    """
    Calculate standardized coefficients for a linear model.
    
    Parameters:
    ----------
    model : statsmodels.regression.linear_model.RegressionResultsWrapper
        A fitted linear model from statsmodels
    
    Returns:
    -------
    pandas.DataFrame
        DataFrame containing standardized coefficients
    """
    # Extract coefficients
    coef = model.params
    
    # Check if intercept is included in the model
    has_intercept = 'const' in model.model.exog_names
    
    # Function to calculate standard deviation
    def sd(x):
        if has_intercept:
            # If there's an intercept, center the data
            return np.sqrt(np.sum((x - np.mean(x) * has_intercept)**2))
        else:
            # If no intercept, use raw values
            return np.sqrt(np.sum(x**2))
    
    # Get predictor matrix
    X = model.model.exog
    
    # Get response variable
    y = model.model.endog
    
    # Calculate standard deviations for predictors
    sd_predictors = np.apply_along_axis(sd, 0, X)
    
    # Calculate standard deviation for response variable
    sd_criteria = sd(y)
    
    # Calculate standardized coefficients
    coef_std = coef.copy()
    for i in range(len(coef)):
        coef_std.iloc[i] = coef.iloc[i] * sd_predictors[i] / sd_criteria
    
    # Create DataFrame for output
    coef_std_df = pd.DataFrame({
        'Standardized': coef_std
    }, index=model.params.index)
    
    return coef_std_df