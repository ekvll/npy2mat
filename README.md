# NPY to MAT Converter

A simple GUI-based tool for converting `.npy` files to `.mat` files using Python's PySimpleGUI, NumPy, and SciPy libraries.

## Features

- **User-Friendly Interface**: Select directories for input `.npy` files and output `.mat` files with ease.
- **Batch Conversion**: Convert all `.npy` files in a directory to `.mat` format in one go.
- **Logging**: Keep track of conversion processes and errors with detailed logging.
- **Contact Info**: Easily accessible information to contact the creator for support or inquiries.

## Requirements

- Python 3.x
- PySimpleGUI
- NumPy
- SciPy

You can install the required packages using the following command:

```bash
pip install PySimpleGUI numpy scipy
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/ekvll/npy2mat.git
cd npy2mat
```

2. Run the application:
```bash
python npy2mat.py
```

3. Using the GUI:
* Browse and selecet the directory containing the `.npy` files.
* Browse and select the target directory to save the converted `.mat` files.
* Click the **Convert** button to start the conversion process.
* Click the **Cancel** button to close the application.
* Click the **Contact Info** button to view the creator's contact information.

When the conversion is completed, the console will look like something like this:
![alt text](image.png)

## Contact
For any questions or support, please contact:
**Erik Lindvall**
Email: erik.lindvall@ri.se 