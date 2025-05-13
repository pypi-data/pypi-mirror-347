import pandas as pd
import warnings
from scia.check_scdf import check_scdf
from scia.preprocess import prepare_scd
from scia.utils import revise_names

def opt(option):
    # Placeholder for option retrieval, adjust as needed
    # For now, always return False for "rigorous_class_check"
    if option == "rigorous_class_check":
        return False
    return None

def phase(data):
    # Returns the phase variable name
    return data.attrs.get("pvar", "phase") if hasattr(data, "attrs") else "phase"

def mt(data):
    # Returns the measurement-time variable name
    return data.attrs.get("mvar", "mt") if hasattr(data, "attrs") else "mt"

def dv(data):
    # Returns the dependent variable name
    return data.attrs.get("dvar", "values") if hasattr(data, "attrs") else "values"

def prepare_scdf(data, na_rm=False):
    """
    Prepare a Single-Case DataFrame (SCDF) for further analysis, mimicking the R prepare_scdf function.
    """
    # Rigorous class check if option is set
    if opt("rigorous_class_check"):
        check_scdf(data)

    pvar = phase(data)
    mvar = mt(data)
    dvar_ = dv(data)

    # Revise names if needed
    if hasattr(data, "attrs") and "case" in data.columns:
        data["case"] = revise_names(data["case"], len(data["case"]))

    # If data is a list of DataFrames (like R list), convert to list
    if isinstance(data, list):
        data_list = data
    elif isinstance(data, pd.DataFrame):
        # Assume single-case, wrap in list for uniformity
        data_list = [data]
    else:
        raise ValueError("Input data must be a pandas DataFrame or a list of DataFrames.")

    for i, case_df in enumerate(data_list):
        # Convert tibbles (pandas DataFrames) to DataFrames (already are in Python)
        if isinstance(case_df, pd.DataFrame):
            pass  # No conversion needed in Python
        else:
            raise ValueError("Each case must be a pandas DataFrame.")

        # Remove rows with NA in dependent variable if na_rm is True
        if na_rm:
            case_df = case_df.dropna(subset=[dvar_])
            data_list[i] = case_df

        # Ensure phase column is categorical
        if not pd.api.types.is_categorical_dtype(case_df[pvar]):
            case_df[pvar] = case_df[pvar].astype("category")

        # Drop unused categories in phase
        case_df[pvar] = case_df[pvar].cat.remove_unused_categories()

        data_list[i] = case_df

    # If input was a single DataFrame, return the first element
    if isinstance(data, pd.DataFrame):
        return data_list[0]
    return data_list