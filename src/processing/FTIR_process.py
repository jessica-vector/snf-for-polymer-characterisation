import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_ftir(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process FTIR data by applying Min-Max scaling to absorbance values.
    
    Args:
        data: DataFrame containing FTIR data with 'Wavenumber' and 'Absorbance' columns
        
    Returns:
        DataFrame with scaled absorbance values
    """
    # Create a copy to avoid modifying original data
    processed_data = data.copy()
    
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    
    # Reshape absorbance data for scaling
    absorbance = processed_data['Absorbance'].values.reshape(-1, 1)
    
    # Apply scaling
    scaled_absorbance = scaler.fit_transform(absorbance)
    
    # Update the absorbance column with scaled values
    processed_data['Absorbance'] = scaled_absorbance
    
    return processed_data

