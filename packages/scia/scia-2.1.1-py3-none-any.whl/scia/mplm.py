import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scia.preprocess import prepare_scd
from scia.std_lm import std_lm
from scia.add_dummy_variables import add_dummy_variables
from scia.create_fixed_formula import create_fixed_formula
from patsy import ModelDesc, Term, EvalFactor

def mplm(data, dvar=None, mvar=None, pvar=None, model="W", 
         contrast="first", contrast_level=None, contrast_slope=None,
         trend=True, level=True, slope=True, formula=None, update=None,
         na_action=None, **kwargs):
    """
    Multivariate piecewise linear model for single-case data.
    
    Parameters:
    ----------
    data : pandas.DataFrame or list
        Single-case data frame or list of data frames
    dvar : str, optional
        Name of the dependent variable column
    mvar : str, optional
        Name of the measurement time variable column
    pvar : str, optional
        Name of the phase variable column
    model : str, default="W"
        Model type: "W", "H-M", "B&L-B", or "JW"
    contrast : str, default="first"
        Contrast type: "first" or "preceding"
    contrast_level : str, optional
        Contrast for level: "first" or "preceding"
    contrast_slope : str, optional
        Contrast for slope: "first" or "preceding"
    trend : bool, default=True
        Include overall trend
    level : bool, default=True
        Include level changes
    slope : bool, default=True
        Include slope changes
    formula : str, optional
        Custom formula for regression
    update : str, optional
        Update to formula
    na_action : function, optional
        Function to handle missing values
    **kwargs : 
        Additional arguments for lm
    
    Returns:
    -------
    None
        Prints MPLM results
    """
    # Handle missing variable names
    if dvar is None:
        dvar = 'values'
    if pvar is None:
        pvar = 'phase'
    if mvar is None:
        mvar = 'mt'
    
    # Handle contrast defaults
    if contrast_level is None:
        contrast_level = contrast
    if contrast_slope is None:
        contrast_slope = contrast
    
    # Handle JW model
    if model == "JW":
        contrast_level = "preceding"
        contrast_slope = "preceding"
        model = "B&L-B"
    
    # Prepare data
    if isinstance(data, list):
        if len(data) > 1:
            print("Procedure could not be applied to more than one case.")
            return None
        else:
            data = data[0]  # Extract the single case
    
    data = prepare_scd(data)
    
    # Add dummy variables using the existing function
    tmp_model = add_dummy_variables(
        data=data, 
        model=model,
        dvar=dvar,
        pvar=pvar,
        mvar=mvar,
        contrast_level=contrast_level, 
        contrast_slope=contrast_slope
    )
    data = tmp_model["data"][0]
    
    # Create formula using the existing function
    if formula is None:
        formula_obj = create_fixed_formula(
            dvar=dvar, 
            mvar=mvar, 
            slope=slope, 
            level=level, 
            trend=trend, 
            var_phase=tmp_model["var_phase"], 
            var_inter=tmp_model["var_inter"]
        )
        # Convert ModelDesc object to string formula
        if isinstance(formula_obj, ModelDesc):
            lhs = " + ".join([factor.name() for term in formula_obj.lhs_termlist for factor in term.factors])
            rhs = " + ".join([factor.name() for term in formula_obj.rhs_termlist for factor in term.factors])
            formula = f"{lhs} ~ {rhs}"
        else:
            formula = str(formula_obj)
    
    # Update formula if needed
    if update is not None:
        # In Python we would need to manually update the formula
        # This is a simplified approach
        formula = formula + " + " + update
    
    # Fit the model
    full_model = ols(formula, data=data).fit()
    
    # Calculate standardized coefficients
    full_model.coef_std = std_lm(full_model)
    
    # Print results
    print("Multivariate piecewise linear model\n")
    print(f"Dummy model: {model} level = {contrast_level}, slope = {contrast_slope}\n")
    
    print("Coefficients:")
    coef_df = pd.DataFrame({"values": full_model.params})
    print(coef_df.to_string())
    print()
    
    print(f"Formula: {formula}")
    
    # Print ANOVA table
    anova_table = anova_lm(full_model, typ=3)
    print("Anova Table (Type III tests)\n")
    print(f"Response: {dvar}")
    
    # Format p-values with stars
    def format_pvalue(p):
        if p < 0.001:
            return f"{p:.4f} ***"
        elif p < 0.01:
            return f"{p:.4f} **"
        elif p < 0.05:
            return f"{p:.4f} *"
        elif p < 0.1:
            return f"{p:.4f} ."
        else:
            return f"{p:.4f}"
    
    # Create a formatted ANOVA table
    anova_formatted = anova_table.copy()
    anova_formatted["PR(>F)"] = anova_formatted["PR(>F)"].apply(format_pvalue)
    
    # Rename variables for better readability
    index_map = {
        "Intercept": "Intercept",
        mvar: f"Trend ({mvar})"
    }
    
    for phase in tmp_model["var_phase"]:
        phase_letter = phase.replace("phase_", "")
        index_map[phase] = f"Level phase {phase_letter} ({phase})"
    
    for inter in tmp_model["var_inter"]:
        inter_letter = inter.replace("inter_", "")
        index_map[inter] = f"Slope phase {inter_letter} ({inter})"
    
    # Apply renaming where possible
    new_index = [index_map.get(idx, idx) for idx in anova_formatted.index]
    anova_formatted.index = new_index
    
    print(anova_formatted.to_string())
    print("---")
    print("Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1")
    
    return None