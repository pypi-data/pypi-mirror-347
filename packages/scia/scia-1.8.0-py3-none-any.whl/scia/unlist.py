import numpy as np
import pandas as pd

def unlist(x, recursive=True, use_names=True):
    """
    Flatten a list-like object into a simple vector.
    
    Parameters:
    ----------
    x : list or other iterable
        The object to be flattened
    recursive : bool, default=True
        Whether to recursively flatten nested lists
    use_names : bool, default=True
        Whether to preserve names in the result
    
    Returns:
    -------
    list or numpy.ndarray
        Flattened version of the input
    """
    # Check recursive parameter
    if not isinstance(recursive, bool):
        raise ValueError("'recursive' must be a boolean value")
    
    # Handle factor-like objects (categorical data)
    if isinstance(x, (pd.Categorical, pd.Series)) and hasattr(x, 'cat'):
        # Extract levels from categorical data
        levels = x.cat.categories.tolist()
        
        # Convert to codes (integer representation)
        result = x.cat.codes.tolist()
        
        # Add names if requested
        if use_names and hasattr(x, 'index'):
            result = pd.Series(result, index=x.index)
        
        return result
    
    # Handle pandas Series
    if isinstance(x, pd.Series):
        return x.tolist()
    
    # Handle pandas DataFrame
    if isinstance(x, pd.DataFrame):
        if recursive:
            # Flatten to a single list
            return x.values.flatten().tolist()
        else:
            # Return list of columns
            return [x[col].tolist() for col in x.columns]
    
    # Handle dictionaries
    if isinstance(x, dict):
        result = []
        names = []
        
        for key, value in x.items():
            # Recursively unlist nested structures if requested
            if recursive and isinstance(value, (list, dict, pd.Series, pd.DataFrame)):
                flattened = unlist(value, recursive, use_names)
                result.extend(flattened if isinstance(flattened, list) else [flattened])
                
                # Add names if available and requested
                if use_names:
                    if isinstance(value, (pd.Series, pd.DataFrame)) and hasattr(value, 'index'):
                        names.extend([f"{key}.{idx}" for idx in value.index])
                    else:
                        names.extend([f"{key}.{i}" for i in range(len(flattened) if isinstance(flattened, list) else 1)])
            else:
                result.append(value)
                if use_names:
                    names.append(key)
        
        # Return with names if requested
        if use_names and names:
            return pd.Series(result, index=names)
        return result
    
    # Handle lists and other iterables
    if isinstance(x, (list, tuple, set)):
        result = []
        names = []
        
        for i, item in enumerate(x):
            # Recursively unlist nested structures if requested
            if recursive and isinstance(item, (list, dict, tuple, set, pd.Series, pd.DataFrame)):
                flattened = unlist(item, recursive, use_names)
                result.extend(flattened if isinstance(flattened, list) else [flattened])
                
                # Add names if available and requested
                if use_names:
                    if isinstance(item, (pd.Series, pd.DataFrame)) and hasattr(item, 'index'):
                        names.extend([f"{i}.{idx}" for idx in item.index])
                    else:
                        names.extend([f"{i}.{j}" for j in range(len(flattened) if isinstance(flattened, list) else 1)])
            else:
                result.append(item)
                if use_names:
                    names.append(str(i))
        
        # Return with names if requested
        if use_names and names:
            return pd.Series(result, index=names)
        return result
    
    # If not a container type, return as is
    return x