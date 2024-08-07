import logging

import numpy as np

from logger_setup import logger


class NumpyFileLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_file(self):
        try:
            self.data = np.load(self.file_path)
            logger.info("File loaded successfully")
        
        except (FileNotFoundError, IOError, ValueError) as e:
            logger.error(f"An error occurred: {e.__class__.__name__} - {e}")
        
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e.__class__.__name__} - {e}")
        
        finally:
            if self.data is None:
                logger.info("Returning None")
        
        return self.data
