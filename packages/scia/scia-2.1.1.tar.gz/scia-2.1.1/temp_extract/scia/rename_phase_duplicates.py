import pandas as pd

def rename_phase_duplicates(phase):
    """
    Rename duplicate phase labels in a sequence by appending (1), (2), etc. to consecutive runs.
    Mimics the R function provided.

    Parameters:
    - phase: A pandas Series or list of phase labels.

    Returns:
    - A pandas Categorical with renamed phases.
    """
    # Convert to string for consistency
    phase_str = pd.Series(phase).astype(str)
    # Run-length encoding
    values = []
    lengths = []
    prev = None
    count = 0
    for val in phase_str:
        if val != prev:
            if prev is not None:
                values.append(prev)
                lengths.append(count)
            prev = val
            count = 1
        else:
            count += 1
    if prev is not None:
        values.append(prev)
        lengths.append(count)
    # Count occurrences
    ts = pd.Series(values).value_counts()
    new_phase = values.copy()
    for i, name in enumerate(ts.index):
        if ts[name] > 1:
            idxs = [j for j, v in enumerate(values) if v == name]
            for k, idx in enumerate(idxs):
                new_phase[idx] = f"{name}({k+1})"
    # Expand back to original length
    expanded = []
    for val, length in zip(new_phase, lengths):
        expanded.extend([val] * length)
    return pd.Categorical(expanded)