import subprocess
import os
import logging
from tempfile import TemporaryDirectory
import pandas as pd
import platform

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
RT_PATH = os.path.join(DIR_PATH, 'module', 'RawTools', 'RawTools.exe')
PLATFORM = platform.system()

logger = logging.getLogger(__name__)


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
        return self.__run_command("version")

    def load(self, raw_file_path, temp_dir: str | None = None) -> pd.DataFrame:
        """
        Load the raw file and return the raw data and the matrix data.

        - raw data: Full MS data of the raw file.
        - matrix data: List of every single frame MS data.

        :param raw_file_path: Path of the raw file, must end with .RAW or .raw.
        :param temp_dir: Temporary directory for storing data.
        :return: raw data and matrix data.
        """
        if os.path.isfile(raw_file_path) & raw_file_path.lower().endswith(".raw"):
            with TemporaryDirectory(dir=temp_dir) as temp_dir:
                logger.info("Start extracting data from raw file...")
                try:
                    self.__run_command("load", raw_file_path, temp_dir)
                    logger.info("Data extraction completed, start loading data...")
                    data_path = os.path.join(temp_dir, os.path.basename(raw_file_path) + "_allScansData.txt")
                    raw = pd.read_table(data_path)
                    logger.info("Data loaded.")
                    raw = raw.set_index("Scan")
                    return raw
                except IOError:
                    logger.warning("Cannot connect to Terminal.")
                    raise IOError
        else:
            logger.warning("Raw file not found.")
            raise FileNotFoundError("Raw file not found.")

    @staticmethod
    def __run_command(params, raw_file_path=None, temp_dir=None):
        if params == "version":
            command = [RT_PATH, "-version"]
        elif params == "load":
            command = [RT_PATH, "-f", raw_file_path, "-o", temp_dir, "-asd"]
        elif params == "folder":
            command = [RT_PATH, "-d", raw_file_path, "-o", temp_dir, "-asd"]
        if PLATFORM != "Windows":
            command = ["mono"] + command
        subprocess.run(command, capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)