import pandas as pd
from pathlib import Path
from typing import Union

def normalize_tga(
    input_data: Union[pd.DataFrame, str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Normalizes TGA weight data to percentage of initial mass.
    Initial mass is taken as 100% and all subsequent weights are expressed as percentages.
    
    Args:
        input_data: Either a DataFrame or path to cleaned TGA data CSV file
        write_flag: If True, writes normalized data to output directory
        
    Returns:
        Normalized pandas DataFrame with weight expressed as percentage
    """
    # Handle input data
    if isinstance(input_data, (str, Path)):
        df = pd.read_csv(input_data)
    else:
        df = input_data.copy()
    
    # Get initial mass (first weight value)
    initial_mass = df['Weight'].iloc[0]
    
    # Convert weights to percentages
    df['weight_percentage'] = (df['Weight'] / initial_mass) * 100
    
    if write_flag:
        output_dir = Path("data/output_data/tga")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "normalized_tga_data.csv"
        df.to_csv(output_file, index=False)
    
    return df


def prepare_data_for_dtw(df: pd.DataFrame) -> dict:
    """
    Prepare TGA data for Dynamic Time Warping (DTW) analysis.
    
    Args:
        df: DataFrame containing TGA data with columns 'Temperature', 'weight_percentage', and 'file_name'
        
    Returns:
        dict: Mapping of sample_id -> 2D array [Temperature, weight_percentage]
    """
    # Group data by file_name
    grouped = df.groupby('file_name')
    
    # Create dictionary mapping sample_id to 2D array
    profiles = {}
    for sample_id, group in grouped:
        # Sort by temperature to ensure consistent ordering
        sorted_group = group.sort_values('Temperature')
        # Create 2D array [Temperature, weight_percentage]
        profiles[sample_id] = sorted_group[['Temperature', 'weight_percentage']].values
    
    return profiles
