# pyRawTools

pyRawTools is a Python package for Windows/Linux/Mac processing raw data from mass spectrometry experiments. Base on RawTools and UNIX command line.

# Install
1. Must install mono
   1. For macOS, use brew to install mono
   ```zsh
    brew install mono
    ```
   2. For Linux, use apt or yum to install mono
   ```bash
    sudo apt install mono-complete
    ```
2. Install or Build
   1. Install

      2. ```bash
         pip install pyRawTools
         ```
         
   2. Build
      1. Clone this repository
         ```bash
         git clone https://github.com/EstrellaXD/pyRawTools.git
         ```
      2. Install python package
         ```bash
         cd pyRawTools
         python setup.py install
         ```

# Usage
1. Convert raw file to pandas DataFrame
```python
from pyRawTools import MSLoader


loader = MSLoader()
raw_data, raw_metrix = loader.load('path/to/raw/file.RAW')
```