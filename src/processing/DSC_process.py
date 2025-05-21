import pandas as pd
from pathlib import Path
from typing import Union
from sklearn.preprocessing import MinMaxScaler


def normalize_dsc(
    input_data: Union[pd.DataFrame, str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Normalizes DSC heat flow data using min-max scaling to range [0,1].
    Only keeps the normalized heat flow values, removing the original heat flow data.
    Columns are ordered with normalized_heat_flow appearing after Temperature.
    
    Args:
        input_data: Either a DataFrame or path to cleaned DSC data CSV file
        write_flag: If True, writes normalized data to output directory
        
    Returns:
        Normalized pandas DataFrame with only normalized heat flow values
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
    
    # Drop the original Heat Flow column
    df = df.drop('Heat Flow', axis=1)
    
    # Reorder columns to put normalized_heat_flow after Temperature
    df = df[['Temperature', 'normalized_heat_flow', 'file_name']]
    
    if write_flag:
        output_dir = Path("data/output_data/dsc")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "normalized_dsc_data.csv"
        df.to_csv(output_file, index=False)
    
    return df

