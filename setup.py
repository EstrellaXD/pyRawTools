from setuptools import find_packages, setup


VERSION = '0.1.1'

setup(
    name='pyRawTools',
    version=VERSION,
    author='EstrellaXD',
    author_email="estrellaxd05@gmail.com",
    description='pyRawTools is a Python package for loading MS data.',
    keywords="RAW MS data",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/EstrellaXD/pyRawTools",
    install_requires=[
        'pandas',
    ],
    python_requires='>=3.6',
    classifiers=[
        "Operating System :: macOS / Linux",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        ],
)