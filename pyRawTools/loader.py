import subprocess
import os
import tempfile
import pandas as pd

from pyRawTools import DIR_PATH

RT_PATH = os.path.join(DIR_PATH, 'module/RawTools/RawTools.exe')


class Loader:
    def __init__(self):
        pass

    def version(self):
        self._run_command("version")

    def load(self, raw_file_path) -> (pd.DataFrame, pd.DataFrame):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_path = self._run_command("load", raw_file_path, temp_dir)
            raw = pd.read_table(data_path)
        metrix = self.metrix(raw)
        return raw, metrix

    def metrix(self, raw: pd.DataFrame) -> list[pd.DataFrame]:
        scan_number = raw['Scan'].max()
        metrix = [raw.loc[raw["Scan"] == i + 1].drop(columns=["Scan"]) for i in range(scan_number)]
        return metrix

    def _run_command(self, params, raw_file_path=None, temp_dir=None):
        if params == "version":
            command = ["mono", RT_PATH, "-version"]
            subprocess.run(command)
        elif params == "load":
            command = ["mono", RT_PATH, "-f", raw_file_path, "-o", temp_dir, "-asd"]
            data_path = os.path.join(temp_dir, os.path.basename(raw_file_path) + "_allScansData.txt")
            subprocess.run(command)
            return data_path


if __name__ == '__main__':
    loader = Loader()
    loader.version()
    data, metrix = loader.load("/Users/Estrella/Developer/pyRawTools/Data_Example/HeLa.RAW")
