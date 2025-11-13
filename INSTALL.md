Installation guide
===================

This project uses `onnxruntime`, which does not currently publish PyPI wheels for
Windows + Python 3.14. The easiest, most reliable way to get a working `onnxruntime`
installation on Windows is to use conda (Miniconda/Anaconda) or create a Python 3.11
virtual environment and install from PyPI.

Recommended (conda) — fast and reliable on Windows
--------------------------------------------------

1. Install Miniconda or Anaconda if you don't have it already: https://docs.conda.io/en/latest/miniconda.html

2. From PowerShell, run:

```powershell
conda env create -f environment.yml
conda activate rag-env
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r .\requirements.txt
```

This will create a `rag-env` environment with Python 3.11 and install `onnxruntime`
via conda-forge, then install the rest of the project's pip requirements.

Alternative (pip + venv) — use when you prefer system Python
-----------------------------------------------------------

If you want to use pip only, install Python 3.11 and create a venv:

```powershell
# create a 3.11 venv (adjust path to your python3.11 executable if needed)
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install onnxruntime
python -m pip install -r .\requirements.txt
```

Notes
-----
- If you must use Python 3.14, install `onnxruntime` via conda:
  `conda install -c conda-forge onnxruntime` — then use pip to install the rest.
- On Windows, if you want GPU acceleration with DirectML, consider `onnxruntime-directml`:
  `python -m pip install onnxruntime-directml` (check Microsoft docs for DirectML runtime requirements).
- The repository `requirements.txt` contains a conditional marker that will skip
  installing `onnxruntime` via pip when running under Python 3.14, because PyPI
  wheels are not available for that combination.

If you want, I can also add a short script to automate the conda flow or pin a
specific `onnxruntime==x.y.z` in `requirements.txt` for a chosen Python version.
