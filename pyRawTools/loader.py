import subprocess
import os
import tempfile
import pandas as pd
import platform

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
RT_PATH = os.path.join(DIR_PATH, 'module/RawTools/RawTools.exe')
PLATFORM = platform.system()


class Loader:
    def __init__(self):
        pass

    def load(self, raw_file_path) -> (pd.DataFrame, pd.DataFrame):
        if os.path.isfile(raw_file_path) & raw_file_path.lower().endswith(".raw"):
            with tempfile.TemporaryDirectory() as temp_dir:
                print("Start extracting data from raw file...")
                data_path = self._run_command("load", raw_file_path, temp_dir)
                print("Data extraction completed, start loading data...")
                raw = pd.read_table(data_path)
                print("Data loaded.")
            metrix = self.metrix(raw)
            return raw, metrix
        else:
            raise FileNotFoundError("Raw file not found.")

    @staticmethod
    def metrix(raw: pd.DataFrame) -> list[pd.DataFrame]:
        scan_number = raw['Scan'].max()
        metrix = [raw.loc[raw["Scan"] == i + 1].drop(columns=["Scan"]) for i in range(scan_number)]
        return metrix

    @staticmethod
    def _run_command(params, raw_file_path=None, temp_dir=None):
        command = [RT_PATH, "-f", raw_file_path, "-o", temp_dir, "-asd"]
        data_path = os.path.join(temp_dir, os.path.basename(raw_file_path) + "_allScansData.txt")
        if PLATFORM != "Windows":
            command = ["mono"] + command
        subprocess.run(command, capture_output=False)
        return data_path