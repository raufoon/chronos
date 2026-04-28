#!/bin/bash

# Update Kali's package lists
sudo apt update

# 1. Base C-compilers and environment tools
# Required to bypass Kali's PEP 668 (externally managed environment) restriction
# and provides the initial C-headers for building basic extensions.
sudo apt install -y build-essential python3-dev python3-venv pkg-config libfftw3-dev libgsl-dev

# 2. Create and activate the isolated virtual environment
python3 -m venv astro_env
source astro_env/bin/activate

# 3. Upgrade core build tools before compiling any packages
pip install --upgrade pip wheel setuptools

# 4. The Python 3.13 Dependency Matrix
# Because Python 3.13 lacks pre-built wheels for older scientific libraries, 
# this installs Fortran (for SciPy), advanced math headers (BLAS/LAPACK), 
# and image headers (for Matplotlib) to compile everything from raw source code.
sudo apt install -y build-essential gfortran python3.13-dev pkg-config libopenblas-dev liblapack-dev libfreetype6-dev libpng-dev libjpeg-dev libfftw3-dev libgsl-dev

# 5. Compile 21cmFAST and install JupyterLab
# Kali uses GCC 15, which strictly rejects legacy C code. 
# The CFLAGS temporarily downgrade these strict errors to warnings so 21cmFAST can successfully compile.
CFLAGS="-Wno-error=incompatible-pointer-types -Wno-error=implicit-int" pip install 21cmFAST==3.3.1 tools21cm==2.1.3 jupyterlab==4.1.5

# 6. Install visualization and interactive UI libraries
pip install ipywidgets plotly

# 7. Compile the core scientific stack from source
# This step utilizes the Fortran and math headers installed in Step 4.
pip install numpy==1.26.4 scipy==1.13.1 matplotlib==3.7.3