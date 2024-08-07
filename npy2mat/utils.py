import os
from typing import Union, List

import scipy.io
import numpy as np

from logger_setup import logger


def validate_file_type(filename: str, target_type: str) -> bool:
    if filename.endswith(target_type):
        logger.info(f"Valid file type")
        return True
    else:
        logger.error(f"Invalid file type. Jumping to next file...")
        return False


def filenames_in_dir(path: str) -> List[str]:
    logger.info(f"Reading files from: {path}")
    try:
        filenames = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]

        logger.info(f"Found {len(filenames)} file(s)")
        return filenames

    except Exception as e:
        logger.error(f"Error reading directory: {e}. Returning empty list")
        return []


def save_data_as_mat(data, filepath: str) -> None:
    if isinstance(data, np.ndarray):
        try:
            logger.info(f"Saving file as .mat file")
            scipy.io.savemat(filepath, {"data": data})
            logger.info(f"Saved successfully")

        except Exception as e:
            logger.error(f"Error when saving as .mat file: {e}")

    else:
        logger.warning(
            "Data is not a numpy array. Cannot save as .mat file. Jumping to next file..."
        )
