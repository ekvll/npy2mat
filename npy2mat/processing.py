import os
import logging

import numpy as np

from load_data import NumpyFileLoader
from logger_setup import logger
from utils import filenames_in_dir, validate_file_type, save_data_as_mat


def process(values: dict) -> None:
    valid_file_type = ".npy"

    path_input = values.get("-NPY_DIR-")  # data input directory
    path_output = values.get("-MAT_DIR-")  # data output directory

    filenames = filenames_in_dir(path_input)

    _intro(valid_file_type)
    
    for idx, filename in enumerate(filenames):
        logger.info(f"Processing file {idx + 1}/{len(filenames)}: {filename}")
        if validate_file_type(filename, valid_file_type):

            npy_filepath, mat_filepath = _gen_filepaths(
                path_input, filename, path_output
            )

            npy_data = NumpyFileLoader(npy_filepath).load_file()

            save_data_as_mat(npy_data, mat_filepath)

        logger.info("-" * 50)

    _outro(path_output)


def _gen_filepaths(npy_dir, npy_filename, mat_dir):
    npy_filepath = os.path.join(npy_dir, npy_filename)
    mat_filename = os.path.splitext(npy_filename)[0] + ".mat"
    mat_filepath = os.path.join(mat_dir, mat_filename)
    return npy_filepath, mat_filepath

def _intro(valid_file_type: str) -> None:
    logger.info(f"Valid file type is {valid_file_type}")
    logger.info("Iterating over files...")
    logger.info("-" * 50)

def _outro(path_output: str) -> None:
    logger.info("All files processed!")
    logger.info(f"Files saved to: {path_output}")
    logger.info("Feel free to close the application")
