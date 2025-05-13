import re

def trimws(x, which="both", whitespace="[ \t\r\n]"):
    """
    Trim whitespace from strings.
    
    Parameters:
    ----------
    x : str or list-like of str
        The string(s) to be trimmed
    which : str, default="both"
        Which side to trim: "both", "left", or "right"
    whitespace : str, default="[ \t\r\n]"
        Regular expression pattern defining whitespace characters to trim
    
    Returns:
    -------
    str or list-like of str
        Trimmed string(s)
    """
    # Validate which parameter
    if which not in ["both", "left", "right"]:
        raise ValueError("'which' must be one of: 'both', 'left', 'right'")
    
    # Define sub function to match R's mysub
    def mysub(pattern, text):
        if isinstance(text, str):
            return re.sub(pattern, "", text)
        else:
            # Handle list-like objects
            return [re.sub(pattern, "", item) if isinstance(item, str) else item for item in text]
    
    # Apply trimming based on which parameter
    if which == "left":
        return mysub(f"^{whitespace}+", x)
    elif which == "right":
        return mysub(f"{whitespace}+$", x)
    else:  # both
        return mysub(f"{whitespace}+$", mysub(f"^{whitespace}+", x))