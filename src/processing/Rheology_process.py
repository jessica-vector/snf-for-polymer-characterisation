import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from dtw import dtw

def normalize_rheology(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process rheology data by applying Min-Max scaling to viscosity values.
    
    Args:
        data: DataFrame containing rheology data with 'Shear Rate' and 'Viscosity' columns
        
    Returns:
        DataFrame with scaled viscosity values
    """
    # Create a copy to avoid modifying original data
    processed_data = data.copy()
    
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    
    # Reshape viscosity data for scaling
    viscosity = processed_data['Viscosity'].values.reshape(-1, 1)
    
    # Apply scaling
    scaled_viscosity = scaler.fit_transform(viscosity)
    
 
  
      # Update the viscosity column with scaled values
    processed_data['Viscosity'] = scaled_viscosity
    
    return processed_data
