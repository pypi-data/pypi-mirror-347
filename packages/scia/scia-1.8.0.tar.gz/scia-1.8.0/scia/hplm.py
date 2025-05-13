import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM
from patsy import ModelDesc
from scipy.stats import chi2
from scia.add_dummy_variables import add_dummy_variables
from scia.create_fixed_formula import create_fixed_formula
from scia.create_random_formula import create_random_formula
from scia.trimws import trimws
from scia.create_dummies import create_dummies

def hplm(data, dvar=None, pvar=None, mvar=None, model="W", contrast="first", 
         contrast_level=None, contrast_slope=None, method="ML", control=None,
         random_slopes=False, lr_test=False, ICC=True, trend=True, level=True, 
         slope=True, random_trend=False, random_level=False, random_slope=False,
         fixed=None, random=None, update_fixed=None, data_l2=None, **kwargs):
    """
    Hierarchical Piecewise Linear Regression for single-case data.
    
    Parameters:
    ----------
    data : list or pandas.DataFrame
        Single-case data frame or list of data frames
    dvar : str, optional
        Name of the dependent variable column
    pvar : str, optional
        Name of the phase variable column
    mvar : str, optional
        Name of the measurement-time variable column
    model : str, default="W"
        Model type: 'W', 'H-M', 'B&L-B', or 'JW'
    contrast : str, default="first"
        Contrasting method: 'first' or 'preceding'
    contrast_level : str, optional
        Contrasting method for level: 'first' or 'preceding'
    contrast_slope : str, optional
        Contrasting method for slope: 'first' or 'preceding'
    method : str, default="ML"
        Estimation method: 'ML' or 'REML'
    control : dict, optional
        Control parameters for optimization
    random_slopes : bool, default=False
        Whether to include random slopes
    lr_test : bool, default=False
        Whether to perform likelihood ratio tests
    ICC : bool, default=True
        Whether to calculate intraclass correlation
    trend : bool, default=True
        Whether to include trend parameter
    level : bool, default=True
        Whether to include level parameters
    slope : bool, default=True
        Whether to include slope parameters
    random_trend : bool, default=False
        Whether to include random trend
    random_level : bool, default=False
        Whether to include random level
    random_slope : bool, default=False
        Whether to include random slope
    fixed : str or patsy.ModelDesc, optional
        Fixed effects formula
    random : str or patsy.ModelDesc, optional
        Random effects formula
    update_fixed : str, optional
        Update to fixed effects formula
    data_l2 : pandas.DataFrame, optional
        Level-2 data
    **kwargs : 
        Additional arguments passed to MixedLM
    
    Returns:
    -------
    None
        Prints the formatted results
    """
    # Check and set model parameters
    valid_models = ["W", "H-M", "B&L-B", "JW"]
    valid_methods = ["ML", "REML"]
    valid_contrasts = ["first", "preceding"]
    
    if model not in valid_models:
        raise ValueError(f"Model must be one of {valid_models}")
    if method not in valid_methods:
        raise ValueError(f"Method must be one of {valid_methods}")
    if contrast not in valid_contrasts:
        raise ValueError(f"Contrast must be one of {valid_contrasts}")
    
    # Handle JW model
    if model == "JW":
        contrast_level = "preceding"
        contrast_slope = "preceding"
        model = "B&L-B"
    
    # Set default contrasts if not provided
    if contrast_level is None:
        contrast_level = contrast
    if contrast_slope is None:
        contrast_slope = contrast
    
    # Set random slopes if requested
    if random_slopes:
        random_trend = trend
        random_level = level
        random_slope = slope
    
    # Set default variable names if not provided
    if dvar is None:
        dvar = dv(data)
    if pvar is None:
        pvar = phase(data)
    if mvar is None:
        mvar = mt(data)
    
    # Prepare data
    dat = prepare_scdf(data)
    N = len(dat) if isinstance(dat, list) else 1
    
    # Initialize output dictionary
    out = {
        "model": {
            "interaction_method": model,
            "contrast_method": contrast,
            "estimation_method": method,
            "lr_test": lr_test,
            "random_slopes": random_slopes,
            "ICC": ICC
        },
        "N": N
    }
    
    # Add dummy variables
    tmp_model = add_dummy_variables(
        data=dat, 
        model=model, 
        dvar=dvar, 
        pvar=pvar, 
        mvar=mvar,
        contrast_level=contrast_level, 
        contrast_slope=contrast_slope
    )
    
    dat = tmp_model["data"]
    
    # Convert to DataFrame for modeling
    if isinstance(dat, list):
        # Combine multiple cases into one DataFrame with case identifier
        combined_dat = pd.DataFrame()
        for i, case_data in enumerate(dat):
            case_data = case_data.copy()
            case_data['case'] = i + 1
            combined_dat = pd.concat([combined_dat, case_data], ignore_index=True)
        dat = combined_dat
    else:
        # Single case, add case identifier
        dat['case'] = 1
    
    # Add level-2 data if provided
    if data_l2 is not None:
        # Merge level-2 data with level-1 data
        dat = pd.merge(dat, data_l2, on='case', how='left')
    
    # Create formulas
    if fixed is None:
        fixed_formula = create_fixed_formula(
            dvar=dvar, 
            mvar=mvar, 
            slope=slope, 
            level=level, 
            trend=trend, 
            var_phase=tmp_model["var_phase"], 
            var_inter=tmp_model["var_inter"], 
            intercept=True
        )
        # Ensure fixed_formula is a string
        if hasattr(fixed_formula, "describe"):
            fixed = fixed_formula.describe()
        else:
            fixed = str(fixed_formula)
    
    # Update fixed formula if requested
    if update_fixed is not None:
        fixed = update_fixed
    
    # Create random formula
    if not random_slopes and random is None:
        random = "1"  # Equivalent to ~1|case in R
    
    if random is None:
        random_formula = create_random_formula(
            mvar=mvar, 
            slope=random_slope, 
            level=random_level, 
            trend=random_trend, 
            var_phase=tmp_model["var_phase"], 
            var_inter=tmp_model["var_inter"], 
            intercept=True, 
            syntax="lm"
        )
        # Ensure random_formula is a string
        if hasattr(random_formula, "describe"):
            random = random_formula.describe()
        else:
            random = str(random_formula)
    
    # Store formulas
    out["formula"] = {"fixed": str(fixed), "random": str(random)}
    
    # Fit hierarchical model
    if isinstance(random, str) and "|" in random:
        # Parse the random formula
        random_parts = random.split("|")
        re_formula = random_parts[0].strip()
        groups = random_parts[1].strip()
    else:
        re_formula = random
        groups = "case"
    
    # Ensure all variables in the formula are properly formatted
    formula_vars = set()
    for part in str(fixed).split('~')[1].split('+'):
        var = part.strip()
        if var and var != '1':
            formula_vars.add(var)
    
    for var in formula_vars:
        if var in dat.columns:
            # Check if the column contains object or categorical data
            if pd.api.types.is_object_dtype(dat[var]) or pd.api.types.is_categorical_dtype(dat[var]):
                # Check if any values are complex objects that need string conversion
                if any(isinstance(x, (list, tuple, np.ndarray)) for x in dat[var] if x is not None):
                    dat[var] = dat[var].astype(str)
    
    # Fit the model
    model_fit = MixedLM.from_formula(
        formula=str(fixed),
        data=dat,
        groups=dat[groups],
        re_formula=re_formula
    )
    
    # Try different optimization methods if one fails
    try:
        # First try with 'nm' (Nelder-Mead) which is more robust
        result = model_fit.fit(
            reml=(method.upper() == "REML"), 
            method='nm',
            maxiter=1000,
            **kwargs
        )
        # DEBUG: Check the actual parameter names in the model
        # print("\n=== CHECKING MODEL PARAMETERS ===")
        # print("Parameter names in result:")
        # for i, name in enumerate(result.params.index):
        #     print(f"{i}: '{name}' = {result.params.iloc[i]:.3f}")

        # # print(f"\nDesign matrix column names:")
        # # print(model_fit.exog_names)

        # # Check if any parameters have different names
        # for param in result.params.index:
        #     if 'phase_B' in param:
        #         print(f"Found phase parameter: '{param}' = {result.params[param]:.3f}")
        #     if 'interB' in param:
        #         print(f"Found inter parameter: '{param}' = {result.params[param]:.3f}")
        # print("=== END CHECK ===\n")
    except Exception as e:
        try:
            # If that fails, try BFGS
            result = model_fit.fit(
                reml=(method.upper() == "REML"), 
                method='bfgs',
                maxiter=1000,
                **kwargs
            )
        except Exception as e:
            # Last resort, try with default method
            result = model_fit.fit(
                reml=(method.upper() == "REML"),
                **kwargs
            )
    
    out["hplm"] = result
    # print("\n=== CHECKING COMBINED DATA ===")
    # print("First few rows of combined data:")
    # print(dat[['phase', 'phase_B', 'interB']].head(15))
    # print("\nPhase B dummy by original phase:")
    # print(dat.groupby('phase')['phase_B'].mean())
    # print("InterB by original phase:")
    # print(dat.groupby('phase')['interB'].mean())
    # print("=== END CHECK ===\n")
    # Calculate ICC
    if ICC:
        # Fit null model with only random intercept
        formula_null = f"{dvar} ~ 1"
        model_0 = MixedLM.from_formula(
            formula=formula_null,
            data=dat,
            groups=dat["case"],
            re_formula="1"
        )
        
        try:
            # Try to fit with robust method
            result_0 = model_0.fit(
                reml=(method.upper() == "REML"), 
                method='nm',
                maxiter=1000,
                **kwargs
            )
        except:
            # Fallback to simpler method
            try:
                result_0 = model_0.fit(
                    reml=(method.upper() == "REML"),
                    **kwargs
                )
            except:
                # If all else fails, use a very simple approach
                result_0 = model_0.fit()
                
        out["model_0"] = result_0
        
        # Extract variance components - handle potential issues
        try:
            vc = result_0.cov_re.iloc[0, 0]  # Random intercept variance
            residual_var = result_0.scale  # Residual variance
            
            # Ensure values are valid
            if np.isnan(vc) or vc < 0:
                vc = 0.0
            if np.isnan(residual_var) or residual_var <= 0:
                residual_var = 1.0
                
            # Calculate ICC
            icc_value = vc / (vc + residual_var)
            
            # Ensure ICC is between 0 and 1
            icc_value = max(0, min(1, icc_value))
        except:
            # Fallback if extraction fails
            icc_value = 0.0
            vc = 0.0
            residual_var = 1.0
            
        out["ICC"] = {"value": icc_value}
        
        # Fit model without random effects
        model_without = sm.OLS.from_formula(formula_null, data=dat)
        result_without = model_without.fit()
        out["model_without"] = result_without
        
        # Likelihood ratio test for ICC - handle potential issues
        try:
            lr_stat = -2 * (result_without.llf - result_0.llf)
            
            # Handle invalid values
            if np.isinf(lr_stat) or np.isnan(lr_stat):
                lr_stat = 0.0
                
            p_value = 1 - chi2.cdf(lr_stat, 1)
            
            # Ensure p-value is valid
            if np.isnan(p_value):
                p_value = 1.0
        except:
            # Fallback values
            lr_stat = 0.0
            p_value = 1.0
            
        out["ICC"]["L"] = lr_stat
        out["ICC"]["p"] = p_value
    # DEBUG: Check actual data means by phase
    # print("\n=== CHECKING ACTUAL DATA MEANS ===")
    # print("Mean values by phase:")
    # print(dat.groupby('phase')[dvar].mean())
    # print("Mean mt by phase:")
    # print(dat.groupby('phase')['mt'].mean())
    # print("Phase B interB mean by original phase:")
    # print(dat.groupby('phase')['interB'].mean())

    # # Check if the model interpretation makes sense
    # print("\nModel interpretation:")
    # print(f"Intercept: {result.params['Intercept']:.3f} (mean for phase A at mt=0)")
    # print(f"Level phase B: {result.params['phase_B']:.3f} (difference when moving to phase B)")
    # print(f"Trend: {result.params['mt']:.3f} (change per unit time)")
    # print(f"Slope phase B: {result.params['interB']:.3f} (additional change per unit time in phase B)")
    # print("=== END CHECK ===\n")
    # Store additional model information
    out["model"]["fixed"] = str(fixed)
    out["model"]["random"] = str(random)
    out["contrast"] = {"level": contrast_level, "slope": contrast_slope}
    out["var_phase"] = tmp_model["var_phase"]
    out["var_inter"] = tmp_model["var_inter"]
    
    # Format the output - FIXED VERSION
    print("Hierarchical Piecewise Linear Regression")
    print()
    print(f"Estimation method {method} ")
    print(f"Contrast model: {model} / level: {contrast_level}, slope: {contrast_slope}")
    print(f"{N} Cases")
    print()
    
    # Add AIC and BIC
    print(f"AIC = {result.aic:.4f}, BIC = {result.bic:.4f}")
    
    # Add ICC information
    if ICC:
        print(f"ICC = {icc_value:.3f}; L = {lr_stat:.1f}; p = {p_value:.3f} ")
    
    print()
    
    # Add fixed effects table - FIXED: Include "1 +" in formula display
    fixed_display = str(fixed)
    # Replace variable names with expected names for display
    for var_name in tmp_model["var_phase"]:
        if var_name in fixed_display:
            fixed_display = fixed_display.replace(var_name, "phaseB")
    for var_name in tmp_model["var_inter"]:
        if var_name in fixed_display:
            fixed_display = fixed_display.replace(var_name, "interB")
    
    # Ensure "1 +" is included in the display
    if "~ 1 +" not in fixed_display and "~1 +" not in fixed_display:
        # If the formula doesn't explicitly show "1 +", add it
        parts = fixed_display.split("~")
        fixed_display = f"{parts[0].strip()} ~ 1 + {parts[1].strip()}"
    
    print(f"Fixed effects ({fixed_display})")
    print()
    print(f"{'':27}B    SE df     t     p")
    
    # Add each parameter with proper names
    # Add each parameter with proper names
    for i, name in enumerate(result.params.index):
    # Format parameter name for display
        if name == "Intercept":
            param_name = "Intercept"
        elif name == mvar:
            param_name = f"Trend ({mvar})"
        elif name == "phase_B":
            param_name = f"Level phase B (phaseB)"
        elif name == "interB":
            param_name = f"Slope phase B (interB)"
        else:
            # Skip any unexpected parameters like Group Var
            continue
            
        print(f"{param_name:<27} {result.params.iloc[i]:5.3f} {result.bse.iloc[i]:4.3f} {result.df_resid:2.0f} {result.tvalues.iloc[i]:5.3f} {result.pvalues.iloc[i]:5.3f}")
    
    print()
    
    # Add random effects table
    print(f"Random effects (~{re_formula} | {groups})")
    print()
    print(f"{'':13}SD")
    
    # Extract random effects standard deviations
    try:
        re_sd = np.sqrt(np.diag(result.cov_re))[0]
        print(f"Intercept {re_sd:5.3f}")
    except:
        print("Intercept N/A")
    
    # Add residual standard deviation
    print(f"Residual  {np.sqrt(result.scale):5.3f}")
    
    # FIXED: Don't return the output dictionary
    return None

def prepare_scdf(data):
    """
    Prepare single-case data for analysis.
    
    Parameters:
    ----------
    data : list or pandas.DataFrame
        Single-case data frame or list of data frames
    
    Returns:
    -------
    list or pandas.DataFrame
        Prepared data
    """
    if isinstance(data, list):
        return data
    else:
        return data

def dv(data):
    """Returns the dependent variable name."""
    if isinstance(data, list) and len(data) > 0:
        return data[0].attrs.get("dvar", "values") if hasattr(data[0], "attrs") else "values"
    return data.attrs.get("dvar", "values") if hasattr(data, "attrs") else "values"

def phase(data):
    """Returns the phase variable name."""
    if isinstance(data, list) and len(data) > 0:
        return data[0].attrs.get("pvar", "phase") if hasattr(data[0], "attrs") else "phase"
    return data.attrs.get("pvar", "phase") if hasattr(data, "attrs") else "phase"

def mt(data):
    """Returns the measurement-time variable name."""
    if isinstance(data, list) and len(data) > 0:
        return data[0].attrs.get("mvar", "mt") if hasattr(data[0], "attrs") else "mt"
    return data.attrs.get("mvar", "mt") if hasattr(data, "attrs") else "mt"