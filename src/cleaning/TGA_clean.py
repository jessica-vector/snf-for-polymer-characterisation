import re
from pathlib import Path
from typing import Union

import pandas as pd


def clean_tga_spectrum(
    file_loc: Union[str, Path], write_flag: bool = False
) -> pd.DataFrame:
    """
    Cleans a single TGA spectrum TXT file.
    Extracts temperature and weight columns, ensures float types and no NaNs.
    Optionally writes cleaned data to output directory.

    Args:
        file_loc: Path to the input TXT file.
        write_flag: If True, writes cleaned data to output directory.

    Returns:
        Cleaned pandas DataFrame.
    """
    file_loc = Path(file_loc)

    # Read the data
    df = pd.read_csv(file_loc, sep='\t')

    # Identify temperature and weight columns
    temp_candidates = [
        col for col in df.columns if re.search(r"(?:temp|tr)", col, re.IGNORECASE)
    ]
    weight_candidates = [
        col for col in df.columns if re.search(r"weight", col, re.IGNORECASE)
    ]
    if not temp_candidates:
        raise ValueError(f"No temperature column found in {file_loc.name}")
    if not weight_candidates:
        raise ValueError(f"No weight column found in {file_loc.name}")
    temp_col = temp_candidates[0]
    weight_col = weight_candidates[0]

    cleaned_data = df[[temp_col, weight_col]].copy()
    cleaned_data.columns = ["Temperature", "Weight"]

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
        output_dir = Path("data/output_data/tga")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"cleaned_{file_loc.name}"
        cleaned_data.to_csv(output_file, index=False)

    return cleaned_data


def clean_tga_batch(input_directory: Union[str, Path]) -> pd.DataFrame:
    """
    Cleans all TGA spectrum TXT files in a directory and concatenates them into a single DataFrame.

    Args:
        input_directory: Path to the directory containing TXT files.

    Returns:
        Concatenated DataFrame with an added 'file_name' column.
    """
    input_directory = Path(input_directory)
    batch_frames = []
    for file_path in input_directory.glob("*.txt"):
        try:
            cleaned = clean_tga_spectrum(file_path)
            cleaned["file_name"] = file_path.name
            batch_frames.append(cleaned)
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")
    if not batch_frames:
        raise ValueError(f"No valid TXT files found in {input_directory}")
    batch_data = pd.concat(batch_frames, ignore_index=True)
    return batch_data

