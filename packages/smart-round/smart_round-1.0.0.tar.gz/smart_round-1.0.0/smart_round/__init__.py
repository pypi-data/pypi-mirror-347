try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None


def smart_round(i: float, tail: int=2) -> float:
    """
    Rounds a float value with intelligent precision handling.
    
    For numbers less than 1 but not 0, this function ensures that at least one significant digit 
    is preserved after rounding, even if it requires more decimal places than specified in 'tail'.
    For numbers greater than or equal to 1, standard rounding to 'tail' decimal places is applied.
    For zero, it returns 0.0.
    
    Args:
        i: The float value to be rounded
        tail: The desired number of decimal places (default: 2)
        
    Returns:
        A rounded float value with appropriate precision
        
    Examples:
        >>> smart_round(1.2345, 2)
        1.23
        >>> smart_round(0.00123, 2)
        0.0012
        >>> smart_round(0, 2)
        0.0
    """
    if i == 0:
        return 0.0
    if abs(i) >= 1:
        return round(i, tail)
    c_tail = 0
    while round(i, c_tail) == 0:
        c_tail += 1
    return round(i, max(tail, c_tail))


def format_value(val: float, tail=3) -> str:
    """
    Formats a float value as a readable string with smart rounding.
    
    This function handles NaN values (returns empty string) and ensures that the 
    result has appropriate decimal places. It preserves trailing zeros if needed.
    
    Args:
        val: The float value to be formatted
        tail: The target number of decimal places (default: 3)
        
    Returns:
        A formatted string representation of the value
        
    Raises:
        ImportError: If NumPy is not installed
        
    Examples:
        >>> format_value(1.2)
        '1.2'
        >>> format_value(1.200)
        '1.2'
        >>> format_value(np.nan)
        ''
    """
    if np is None:
        raise ImportError('Install NumPy module with `pip install numpy`')
    if np.isnan(val):
        return ''
    rt = np.format_float_positional(smart_round(val, tail))
    if rt.endswith('.'):
        rt = rt+'0'
    return rt


def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats float columns in a pandas DataFrame using the format_value function.
    
    This function identifies float columns and applies the format_value function to each value,
    converting them to formatted strings with appropriate precision.
    
    Args:
        df: The pandas DataFrame with float columns to format
        
    Returns:
        A pandas DataFrame with formatted float columns
        
    Raises:
        ImportError: If pandas is not installed
        
    Example:
        >>> df = pd.DataFrame({'A': [1.23456, 0.00123], 'B': ['text', 'data']})
        >>> format_dataframe(df)
           A      B
        0  1.235  text
        1  0.001  data
    """
    if pd is None:
        raise ImportError('Install pandas module with `pip install pandas`')
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].apply(format_value)
    return df