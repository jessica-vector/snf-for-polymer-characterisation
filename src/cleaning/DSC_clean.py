import re
from pathlib import Path
from typing import Union

import pandas as pd


def clean_dsc_spectrum(
    file_loc: Union[str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Cleans a single DSC spectrum CSV file.
    Extracts temperature and normalised heat flow columns, ensures float types and no NaNs.
    Optionally writes cleaned data to output directory.

    Args:
        file_loc: Path to the input CSV file.
        write_flag: If True, writes cleaned data to output directory.

    Returns:
        Cleaned pandas DataFrame.
    """
    file_loc = Path(file_loc)

    # Read the first two rows to check for units row
    preview = pd.read_csv(file_loc, nrows=2)

    def is_units_row(row):
        return any(re.search(r"[a-zA-Z]", str(val)) for val in row)

    skiprows = 1 if len(preview) > 1 and is_units_row(preview.iloc[1]) else 0

    # Read the data, skipping the units row if present
    if skiprows:
        df = pd.read_csv(file_loc, skiprows=[1])
    else:
        df = pd.read_csv(file_loc)

    # Identify temperature and heat flow columns
    temp_candidates = [
        col for col in df.columns if re.search(r"temp", col, re.IGNORECASE)
    ]
    heat_candidates = [
        col for col in df.columns if re.search(r"heat.*flow", col, re.IGNORECASE)
    ]
    if not temp_candidates:
        raise ValueError(f"No temperature column found in {file_loc.name}")
    if not heat_candidates:
        raise ValueError(f"No normalised heat flow column found in {file_loc.name}")
    temp_col = temp_candidates[0]
    heat_col = heat_candidates[0]

    cleaned_data = df[[temp_col, heat_col]].copy()
    cleaned_data.columns = ["Temperature", "Normalised Heat Flow"]
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
        output_dir = Path("data/output_data/dsc")
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / file_loc.name
        cleaned_data.to_csv(out_path, index=False)

    return cleaned_data


def clean_dsc_batch(input_directory: Union[str, Path]) -> pd.DataFrame:
    """
    Cleans all DSC spectrum CSV files in a directory and concatenates them into a single DataFrame.

    Args:
        input_directory: Path to the directory containing CSV files.

    Returns:
        Concatenated DataFrame with an added 'file_name' column.
    """
    input_directory = Path(input_directory)
    batch_frames = []
    for file_path in input_directory.glob("*.csv"):
        try:
            cleaned = clean_dsc_spectrum(file_path)
            cleaned["file_name"] = file_path.name
            batch_frames.append(cleaned)
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")
    if not batch_frames:
        raise ValueError(f"No valid CSV files found in {input_directory}")
    batch_data = pd.concat(batch_frames, ignore_index=True)
    return batch_data
    cleaned_data.columns = ["Temperature", "Heat Flow"]
