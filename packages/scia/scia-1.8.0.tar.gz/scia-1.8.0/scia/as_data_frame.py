import pandas as pd
from scia.utils import revise_names
# If you have add_l2 implemented, import it as well:
# from scia.some_module import add_l2

def as_data_frame(x, l2=None, id_col="case"):
    """
    Convert a list of DataFrames (scdf) to a single DataFrame with a case column.
    Optionally merges level-2 data (l2) if provided.

    Parameters:
    - x: list of pandas DataFrames (each representing a case)
    - l2: optional DataFrame with level-2 data to merge
    - id_col: name of the case identifier column

    Returns:
    - A pandas DataFrame with all cases stacked and a case column.
    """
    # If l2 is provided, add level-2 data to each case
    if l2 is not None:
        x = add_l2(x, l2, cvar=id_col)

    label = revise_names([None if hasattr(df, 'name') and df.name is None else df.name for df in x], len(x))
    outdat = []

    for i_case, df in enumerate(x):
        df = df.copy()
        df[id_col] = label[i_case]
        outdat.append(df)

    outdat = pd.concat(outdat, ignore_index=True)

    # Move the id_col to the first column
    cols = [id_col] + [col for col in outdat.columns if col != id_col]
    outdat = outdat[cols]

    # Make id_col a categorical with the correct levels
    outdat[id_col] = pd.Categorical(outdat[id_col], categories=label, ordered=True)

    # Optionally, set an attribute for scdf (not standard in pandas, but can use attrs)
    # If x had an 'scdf' attribute, copy it
    if hasattr(x, 'attrs') and 'scdf' in x.attrs:
        outdat.attrs['scdf'] = x.attrs['scdf']

    return outdat