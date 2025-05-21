import pandas as pd
from pathlib import Path
from typing import Union
from sklearn.preprocessing import MinMaxScaler


def normalize_dsc(
    input_data: Union[pd.DataFrame, str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Normalizes DSC heat flow data using min-max scaling to range [0,1].
    
    Args:
        input_data: Either a DataFrame or path to cleaned DSC data CSV file
        write_flag: If True, writes normalized data to output directory
        
    Returns:
        Normalized pandas DataFrame with heat flow values scaled between 0 and 1
    """
    # Handle input data
    if isinstance(input_data, (str, Path)):
        df = pd.read_csv(input_data)
    else:
        df = input_data.copy()
    
    # Get min and max heat flow values
    min_flow = df['Heat Flow'].min()
    max_flow = df['Heat Flow'].max()
    
    # Apply min-max scaling
    df['normalized_heat_flow'] = (df['Heat Flow'] - min_flow) / (max_flow - min_flow)
    
    if write_flag:
        output_dir = Path("data/output_data/dsc")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "normalized_dsc_data.csv"
        df.to_csv(output_file, index=False)
    
    return df

