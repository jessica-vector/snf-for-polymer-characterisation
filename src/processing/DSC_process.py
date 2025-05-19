import pandas as pd
from pathlib import Path
from typing import Union
from sklearn.preprocessing import MinMaxScaler


def normalize_dsc_data(
    input_data: Union[pd.DataFrame, str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Normalizes DSC data between -1 and 1 using MinMaxScaler.
    
    Args:
        input_data: Either a DataFrame or path to cleaned DSC data CSV file
        write_flag: If True, writes normalized data to output directory
        
    Returns:
        Normalized pandas DataFrame
    """
    # Handle input data
    if isinstance(input_data, (str, Path)):
        df = pd.read_csv(input_data)
    else:
        df = input_data.copy()
    
    # Initialize scaler and normalize heat flow data
    scaler = MinMaxScaler(feature_range=(-1, 1))
    df['Normalised Heat Flow'] = scaler.fit_transform(df[['Normalised Heat Flow']])
    
    if write_flag:
        output_dir = Path("data/output_data/dsc")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "normalized_dsc_data.csv"
        df.to_csv(output_file, index=False)
    
    return df


