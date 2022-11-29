import subprocess
import os
import tempfile
import pandas as pd
import platform

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
RT_PATH = os.path.join(DIR_PATH, 'module', 'RawTools', 'RawTools.exe')
PLATFORM = platform.system()


class MSLoader:
    def __init__(self):
        """
        RawTools is a command line tool for extracting data from Thermo RAW files.
        """
        pass

    def version(self):
        """
        Get the version of RawTools.

        :return: version info.
        """
        return self._run_command("version")

    def load(self, raw_file_path) -> (pd.DataFrame, dict[int, pd.DataFrame]):
        """
        Load the raw file and return the raw data and the matrix data.

        - raw data: Full MS data of the raw file.
        - matrix data: List of every single frame MS data.

        :param raw_file_path: Path of the raw file, must end with .RAW or .raw.
        :return: raw data and matrix data.
        """
        if os.path.isfile(raw_file_path) & raw_file_path.lower().endswith(".raw"):
            with tempfile.TemporaryDirectory() as temp_dir:
                print("Start extracting data from raw file...")
                try:
                    self._run_command("load", raw_file_path, temp_dir)
                    print("Data extraction completed, start loading data...")
                    data_path = os.path.join(temp_dir, os.path.basename(raw_file_path) + "_allScansData.txt")
                    raw = pd.read_table(data_path)
                    print("Data loaded.")
                    matrix = self.matrix(raw)
                    return raw, matrix
                except IOError:
                    print("Cannot connect to Terminal.")
                    raise IOError
        else:
            raise FileNotFoundError("Raw file not found.")

    @staticmethod
    def matrix(raw: pd.DataFrame) -> dict[int, pd.DataFrame]:
        matrix = {}
        scan = raw["Scan"].max()
        for m in range(scan):
            matrix[m] = raw.loc[raw["Scan"] == m + 1, ["Mass", "Intensity"]].reset_index(drop=True)
        return matrix

    @staticmethod
    def _run_command(params, raw_file_path=None, temp_dir=None):
        if params == "version":
            command = [RT_PATH, "-version"]
        elif params == "load":
            command = [RT_PATH, "-f", raw_file_path, "-o", temp_dir, "-asd"]
        if PLATFORM != "Windows":
            command = ["mono"] + command
        subprocess.run(command, capture_output=False)