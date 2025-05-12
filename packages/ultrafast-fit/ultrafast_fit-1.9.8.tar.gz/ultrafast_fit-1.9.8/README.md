# Ultrafast-Fit: CLI-Based Spectroscopy Fitting Tool

Ultrafast-Fit is a command-line tool for analyzing ultrafast spectroscopy data. It supports robust model fitting, automatic exponential component estimation, batch fitting, and various visualizations for both 1D and 2D data formats.

## 🚀 Installation
```bash
pip install ultrafast-fit
```

For editable local development:
```bash
pip install -e .
```

---

## 📁 Input Format
- **1D Data**: CSV with two columns: `time` and `signal`
- **2D Data**: CSV with time as rows, wavelengths as columns

---

## 📦 CLI Usage
```bash
ultrafast-fit --data-file <path> [options]
```

### Required
- `--data-file <file>`: Path to input `.csv`, `.txt`, `.xlsx`, or `.mat` file

### Optional Arguments
- `--n-components <int>`: Specify number of exponential components manually
- `--max-components <int>`: Max number of components to test for best AIC model [Default: 4]
- `--show-plots`: Show all fit plots interactively
- `--export-summary`: Export CSV summaries of fits
- `--plot-aic`: Plot AIC vs. number of components (for 1D data)
- `--save-extra`: Save extra visualizations like heatmaps and average fit (2D only)
- `--show-every <int>`: Show every N-th plot during 2D batch fitting [Default: 10]
- `--heatmap`: Create model comparison heatmap (2D only)
- `--global-fit`: Perform global fitting across all wavelengths (shared lifetimes, 2D only)
- `--thermo`: Run thermodynamic analysis to estimate activation energies (2D only)

---

## ✅ Example Commands

### 1D Fit (Single Trace)
```bash
ultrafast-fit --data-file sample_data.csv --n-components 3 --show-plots --export-summary
```

### 2D Batch Fitting with Heatmap + Thermo
```bash
ultrafast-fit --data-file synthetic_2d_data.csv \
  --n-components 4 \
  --show-plots \
  --export-summary \
  --save-extra \
  --heatmap \
  --thermo \
  --show-every 25
```

---

## 📊 Output
- `results/<timestamp>/`
  - `best_fit_signal.csv`, `residuals.csv`, `batch_fit_summary.csv`
  - `best_fit_only.png`, `aic_vs_components.png`
  - Extra: `residual_heatmap.png`, `average_dynamic_fit.png`, `model_comparison_heatmap.png`

---

## 📌 Notes
- The `--thermo` flag performs Arrhenius-style activation energy estimation using effective rate constants across wavelengths.
- `--global-fit` enables multi-wavelength fitting with shared exponential lifetimes, useful for spectral consistency.

---

## 👨‍🔬 Author
Created by Alan Arana © 2025.

---

## 📤 PyPI Upload
To publish to TestPyPI:
```bash
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

To install from TestPyPI:
```bash
pip install -i https://test.pypi.org/simple/ ultrafast-fit
```

To publish to PyPI:
```bash
python3 -m twine upload dist/*
```
