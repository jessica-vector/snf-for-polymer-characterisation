import re
from pathlib import Path
from typing import Union

import pandas as pd


def clean_rheology_spectrum(
    file_loc: Union[str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Cleans a single Flow Rheology spectrum CSV file.
    Extracts shear rate and viscosity columns, ensures float types and no NaNs.
    Optionally writes cleaned data to output directory.

    Args:
        file_loc: Path to the input CSV file.
        write_flag: If True, writes cleaned data to output directory.

    Returns:
        Cleaned pandas DataFrame.
    """
    file_loc = Path(file_loc)

    # Read the data
    df = pd.read_csv(file_loc)

    # Identify shear rate and viscosity columns
    shear_candidates = [
        col for col in df.columns if re.search(r"shear.*rate", col, re.IGNORECASE)
    ]
    visc_candidates = [
        col for col in df.columns if re.search(r"viscosity", col, re.IGNORECASE)
    ]
    if not shear_candidates:
        raise ValueError(f"No shear rate column found in {file_loc.name}")
    if not visc_candidates:
        raise ValueError(f"No viscosity column found in {file_loc.name}")
    shear_col = shear_candidates[0]
    visc_col = visc_candidates[0]

    cleaned_data = df[[shear_col, visc_col]].copy()
    cleaned_data.columns = ["Shear Rate", "Viscosity"]

    # Remove any rows that are not fully numeric before conversion
    cleaned_data = cleaned_data[
        cleaned_data.apply(
            lambda x: x.map(
                lambda val: isinstance(val, (int, float))
                or (
                    isinstance(val, str)
                    and re.match(r"^-?\d+(?:\.\d+)?$", str(val).strip())
                )
            )
        ).all(axis=1)
    ]

    try:
        cleaned_data = cleaned_data.astype(float)
    except Exception as e:
        raise ValueError(f"Could not convert data to float in {file_loc.name}: {e}")

    cleaned_data = cleaned_data.dropna()

    if write_flag:
        output_dir = Path("data/output_data/rheology")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"cleaned_{file_loc.name}"
        cleaned_data.to_csv(output_file, index=False)

    return cleaned_data


def clean_rheology_batch(input_directory: Union[str, Path]) -> pd.DataFrame:
    """
    Cleans all Flow Rheology spectrum CSV files in a directory and concatenates them into a single DataFrame.

    Args:
        input_directory: Path to the directory containing CSV files.

    Returns:
        Concatenated DataFrame with an added 'file_name' column.
    """
    input_directory = Path(input_directory)
    batch_frames = []
    for file_path in input_directory.glob("*.csv"):
        try:
            cleaned = clean_rheology_spectrum(file_path)
            cleaned["file_name"] = file_path.name
            batch_frames.append(cleaned)
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")
    if not batch_frames:
        raise ValueError(f"No valid CSV files found in {input_directory}")
    batch_data = pd.concat(batch_frames, ignore_index=True)
    return batch_data
