# RedVector

Small Python experiments for reading and analyzing Mars elevation data.

## Requirements

- Python 3.11 or later
- The compatible packages listed in `requirements.txt`
- The MOLA elevation raster at `data/megt90n000fb.img` for scripts that read the full dataset

Create an isolated environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run an analysis script from the project root:

```powershell
python src\plot_mars.py
python src\read_mola.py
python src\slope.py
```

## Data

The full `data/megt90n000fb.img` raster is intentionally not stored in this Git
repository because it is larger than GitHub's regular per-file limit. Keep a
locally obtained copy at that path when running the full-raster scripts. The
small accompanying metadata files may be versioned; verify dataset provenance
and license terms before redistributing either the data or its metadata.

For team sharing of large files, use Git LFS or an approved external data store
after confirming the source's redistribution terms. Avoid committing
credentials, personal information, local environments, or private working
notes.

## Development

GitHub Actions checks Python syntax on supported Python versions for pushes
and pull requests. Add tests under `tests/` as project behavior becomes
testable.
