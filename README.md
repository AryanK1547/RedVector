# RedVector — Interplanetary Survival Guide: Martian Map

Goal: build an interactive Mars mission-planning platform for the 2026 NASA Space Apps Challenge. The system should combine multiple NASA datasets into a layered Martian map that helps a hypothetical astronaut choose and plan a route.

Core envisioned workflow:

**Start location + Destination + Mission objective**
→ terrain/science analysis
→ route generation
→ route visualization + statistics
→ mission recommendation.

Target capabilities:

* Interactive Mars map
* Start/destination selection
* NASA-derived elevation/terrain
* Shortest/safest/scientific/balanced routes
* Terrain difficulty and slope
* Hazards
* Scientific-interest locations
* Elevation profile
* Route distance/time
* Multiple NASA science layers
* Eventually imagery, ice/water, sunlight, communications, rover/science locations, etc.

Planned architecture:

**Frontend:** React + Leaflet/MapLibre
**Backend:** Python + FastAPI
**Data processing:** NumPy/geospatial tooling
**NASA data:** MOLA, HiRISE, CTX, potentially other mission datasets
**Algorithms:** Dijkstra → A* with terrain-aware cost functions.

The eventual route cost concept is:

`route_cost = distance + elevation_penalty + slope_penalty + terrain_penalty + hazard_penalty`

The MVP priority is to make **one route-planning capability excellent**, then add layers around it rather than attempting every feature immediately. 

---


## Requirements

- Python 3.12 or later
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
