from setuptools import find_packages, setup

VERSION = '0.1.0'

setup(
    name='MSLoader',
    version=VERSION,
    author='EstrellaXD',
    author_email="estrellaxd05@gmail.com",
    description='MSLoader is a Python package for loading MS data.',
    keywords="RAW MS data",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
    python_requires='>=3.6',
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        ],
)