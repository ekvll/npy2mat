import os
from typing import Union, Tuple, List

import PySimpleGUI as sg

from logger_setup import logger
from processing import process


class Npy2Mat:
    def __init__(self):
        self.layout = self.create_layout()
        self.window = sg.Window("npy2mat", self.layout)

    def create_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("Browse to the directory containing .npy files:")],
            [sg.Input(key="-NPY_DIR-"), sg.FolderBrowse()],
            [sg.Text("Browse to the directory for saving .mat files:")],
            [sg.Input(key="-MAT_DIR-"), sg.FolderBrowse()],
            [sg.Button("Convert"), sg.Button("Contact Info"), sg.Button("Cancel")],
        ]

    def run(self) -> None:
        logger.info("Starting application...")

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                logger.info("Application closed by user")
                break

            if event == "Convert":
                process(values)

            if event == "Contact Info":
                sg.popup(
                    "Contact Information",
                    "Creator: Erik Lindvall\nEmail: erik.lindvall@ri.se",
                    keep_on_top=True,
                )

        self.window.close()


if __name__ == "__main__":
    Npy2Mat().run()
