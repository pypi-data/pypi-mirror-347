import pandas as pd

def phasestructure(data, pvar):
    """
    Mimics the R .phasestructure function.
    Returns a dictionary with phase values, run lengths, start and stop indices.
    
    Parameters:
    - data: pandas DataFrame
    - pvar: str, name of the phase variable column
    
    Returns:
    - dict with keys: 'values', 'lengths', 'start', 'stop'
    """
    # Convert the phase column to string (as.character in R)
    phases = data[pvar].astype(str).values

    # Run-length encoding
    values = []
    lengths = []
    if len(phases) == 0:
        return {"values": [], "lengths": [], "start": [], "stop": []}
    prev = phases[0]
    count = 1
    for curr in phases[1:]:
        if curr == prev:
            count += 1
        else:
            values.append(prev)
            lengths.append(count)
            prev = curr
            count = 1
    values.append(prev)
    lengths.append(count)

    # Calculate start and stop indices (1-based, like R)
    start = [1]
    for l in lengths[:-1]:
        start.append(start[-1] + l)
    stop = [s + l - 1 for s, l in zip(start, lengths)]

    # Return as a dictionary (class "list" in R, just dict in Python)
    return {
        "values": values,
        "lengths": lengths,
        "start": start,
        "stop": stop
    }