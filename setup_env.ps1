# setup_env.ps1
# PowerShell helper to create an environment and install the project's dependencies.

Write-Host "Setting up environment for Local-RAG-with-Ollama"

# If conda is available, use it (recommended on Windows)
try {
    $conda = Get-Command conda -ErrorAction SilentlyContinue
} catch {
    $conda = $null
}

if ($conda) {
    Write-Host "Conda detected. Creating environment 'rag-env' from environment.yml..."
    conda env create -f environment.yml --force
    Write-Host "Activate the environment with: conda activate rag-env"
    Write-Host "Then run: python -m pip install --upgrade pip setuptools wheel"
    Write-Host "And: python -m pip install -r .\requirements.txt"
} else {
    Write-Host "Conda not found. Falling back to venv using Python 3.11 (py -3.11) if available.";
    $py311 = & py -3.11 -c "import sys; print(sys.executable)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Creating venv using Python 3.11..."
        py -3.11 -m venv .venv
        Write-Host "Activate it with: .\\.venv\\Scripts\\Activate.ps1"
        Write-Host "Then run: python -m pip install --upgrade pip setuptools wheel"
        Write-Host "And: python -m pip install onnxruntime && python -m pip install -r .\\requirements.txt"
    } else {
        Write-Host "Python 3.11 not found. Please install Miniconda or Python 3.11 and re-run this script."
    }
}

Write-Host "Setup helper finished."
