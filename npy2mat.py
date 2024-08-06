import PySimpleGUI as sg
import numpy as np
import scipy.io
import logging
import os
from typing import Union


class Npy2Mat:
    def __init__(self):
        self.layout = self.create_layout()
        self.window = sg.Window("NPY to MAT Converter", self.layout)
        self.logger = self.setup_logger()

    def create_layout(self) -> list:
        """
        Create the layout for the GUI.

        This method defines the layout of the graphical user interface (GUI) using PySimpleGUI.
        It includes input fields for selecting directories containing .npy files and the target directory
        for saving .mat files, as well as buttons for converting files, canceling the operation, and displaying
        contact information for the creator of the software.

        Returns:
        list: A list of lists defining the layout of the GUI elements.
        """
        return [
            [sg.Text("Browse to a directory containing only .npy files:")],
            [sg.Input(key="-NPY_DIR-"), sg.FolderBrowse()],
            [sg.Text("Browse to a directory where to save .mat files:")],
            [sg.Input(key="-MAT_DIR-"), sg.FolderBrowse()],
            [sg.Button("Convert"), sg.Button("Cancel"), sg.Button("Contact Info")],
        ]

    def setup_logger(self) -> logging.Logger:
        """
        Set up and configure the logger for the application.

        This method creates a logger with the name of the current module, sets its logging level to DEBUG,
        and adds a StreamHandler with a specific log message format.

        Returns:
        logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def run(self) -> None:
        """
        Run the main application loop.

        This method starts the application, listens for events, and handles user interactions.
        It logs the start of the application, processes events such as window closure and file conversion,
        and closes the application window when the loop is exited.

        Events:
        - sg.WIN_CLOSED, "Cancel": Closes the application.
        - "Convert": Initiates the conversion process for .npy files to .mat files.
        - "Contact Info": Displays contact information for the creator of the software.

        Returns:
        None
        """
        self.logger.info("Starting application...")

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                self.logger.info("Application closed by user")
                break

            if event == "Convert":
                self.handle_conversions(values)

            if event == "Contact Info":
                sg.popup("Contact Information", "Creator: Erik Lindvall\nEmail: erik.lindvall@ri.se", keep_on_top=True)


        self.window.close()

    def handle_conversions(self, values: dict) -> None:
        """
        Handle the conversion of .npy files to .mat files based on the provided values.

        Parameters:
        values (dict): A dictionary containing the paths for .npy and .mat directories.

        Returns:
        None
        """
        npy_dir, mat_dir = self.get_directories(values)
        npy_filenames = self.filenames_in_dir(npy_dir)

        if self.validate_file_types(npy_filenames, ".npy"):
            self.convert_files(npy_filenames, npy_dir, mat_dir)
        else:
            self.show_invalid_file_type_error()

    def get_directories(self, values: dict) -> tuple:
        """
        Extract directories from the provided values.

        Parameters:
        values (dict): A dictionary containing the paths for .npy and .mat directories.

        Returns:
        tuple: A tuple containing the .npy directory and .mat directory.
        """
        npy_dir = values.get("-NPY_DIR-")
        mat_dir = values.get("-MAT_DIR-")
        return npy_dir, mat_dir

    def validate_file_types(self, filenames: list, target_type: str) -> bool:
        """
        Validate if the filenames match the target file type.

        Parameters:
        filenames (list): A list of filenames to validate.
        target_type (str): The target file extension to check against.

        Returns:
        bool: True if all filenames match the target file type, False otherwise.
        """
        if self.check_file_type(filenames, target_type):
            self.logger.info(f"Found {len(filenames)} files to convert")
            return True
        return False

    def convert_files(self, filenames: list, npy_dir: str, mat_dir: str):
        """
        Convert .npy files to .mat files.

        Parameters:
        filenames (list): A list of .npy filenames to convert.
        npy_dir (str): The directory containing the .npy files.
        mat_dir (str): The directory where the .mat files will be saved.

        Returns:
        None
        """
        for npy_file in filenames:
            mat_file = os.path.join(mat_dir, os.path.splitext(npy_file)[0] + ".mat")
            self.convert_npy_to_mat(os.path.join(npy_dir, npy_file), mat_file)
        sg.popup("Conversion successful!")

    def show_invalid_file_type_error(self):
        """
        Show an error popup for invalid file types.

        Returns:
        None
        """
        sg.popup(
            "Invalid file type: .npy files required",
            title="Error",
            keep_on_top=True,
        )
        self.logger.warning("Invalid file type: .npy files required")

    def convert_npy_to_mat(self, npy_file: str, mat_file: str) -> None:
        """
        Convert a .npy file to a .mat file.

        Parameters:
        npy_file (str): The path to the .npy file to be converted.
        mat_file (str): The path where the .mat file will be saved.

        Returns:
        None

        Exceptions:
        If an error occurs during the conversion, a popup with the error message is displayed and the error is logged.
        """
        try:
            data = self.load_npy_file(npy_file)
            self.save_mat_file(data, mat_file)
            self.logger.info(f"Converted {npy_file}")
        except Exception as e:
            sg.popup("Error during converion", str(e))
            self.logger.error(f"Error during conversion: {e}")

    def filenames_in_dir(self, path: str) -> list:
        """
        Get a list of filenames in the specified directory.

        Parameters:
        path (str): The path to the directory to list files from.

        Returns:
        list: A list of filenames in the specified directory. If an error occurs, an empty list is returned.

        Exceptions:
        If an error occurs while reading the directory, a popup with the error message is displayed and the error is logged.
        """
        try:
            return [
                f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
            ]
        except Exception as e:
            sg.popup("Error reading directory", str(e))
            self.logger.error(f"Error reading directory: {e}")
            return []

    @staticmethod
    def check_file_type(filename: Union[str, list], target_type: str) -> bool:
        """
        Check if the given filename(s) match the target file type.

        Parameters:
        filename (str or list): The filename or list of filenames to check.
        target_type (str): The target file extension to check against.

        Returns:
        bool: True if all filenames match the target file type, False otherwise.
        """
        if isinstance(filename, str):
            if not filename.endswith(target_type):
                return False

        if isinstance(filename, list):
            for fn in filename:
                if not fn.endswith(target_type):
                    return False
        return True

    @staticmethod
    def load_npy_file(npy_file: str) -> np.ndarray:
        """
        Load data from a .npy file.

        Parameters:
        npy_file (str): The path to the .npy file to be loaded.

        Returns:
        numpy.ndarray: The data loaded from the .npy file.

        Raises:
        ValueError: If there is an error loading the .npy file.
        """
        try:
            return np.load(npy_file)
        except Exception as e:
            raise ValueError(f"Failed to load npy file: {e}")

    @staticmethod
    def save_mat_file(data: any, mat_file: str) -> None:
        """
        Save data to a .mat file.

        Parameters:
        data (any): The data to be saved in the .mat file.
        mat_file (str): The path to the .mat file where the data will be saved.

        Raises:
        ValueError: If there is an error saving the .mat file.
        """
        try:
            scipy.io.savemat(mat_file, {"data": data})
        except Exception as e:
            raise ValueError(f"Failed to save mat file: {e}")


if __name__ == "__main__":
    app = Npy2Mat()
    app.run()
