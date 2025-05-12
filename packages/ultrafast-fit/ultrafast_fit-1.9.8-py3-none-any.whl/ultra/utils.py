

import numpy as np
import pandas as pd
import scipy.io
import os

def load_data(filepath=None):
    """
    Loads data from .csv, .txt, .xlsx, or .mat file.
    Detects if 1D kinetic data or 2D spectral data.
    If no file is provided, generates simulated data.
    Returns:
        t (np.ndarray): time array
        signal (np.ndarray): signal array or matrix
    """
    if filepath is None:
        # === Simulated Data (default) ===
        t = np.linspace(-1, 5, 500)
        from ultra.fitting import convolved_model
        signal_clean = convolved_model(t, A=1.0, tau=0.8, t0=0.2, fwhm=0.3)
        np.random.seed(42)
        noise = 0.03 * np.random.normal(size=len(t))
        signal_noisy = signal_clean + noise
        print("\n✅ Loaded simulated 1D data")
        return t, signal_noisy

    # === Real Data ===
    ext = os.path.splitext(filepath)[1].lower()

    # --- Load file ---
    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext in [".txt", ".dat"]:
        df = pd.read_csv(filepath, delim_whitespace=True)
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    elif ext == ".mat":
        mat = scipy.io.loadmat(filepath)
        try:
            t = np.squeeze(mat["time"])
            signal = np.squeeze(mat["signal"])
            print("\n Loaded .mat data")
            return t, signal
        except KeyError:
            raise ValueError("MAT file must contain 'time' and 'signal' variables")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # --- Clean Columns ---
    df.columns = df.columns.str.lower().str.strip().str.replace(r"\(.*\)", "", regex=True)
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # --- Detect 1D vs 2D ---
    if "signal" in df.columns:
        # 1D kinetic data
        t = df["time"].values
        signal = df["signal"].values
        print("\n Loaded 1D kinetic data")
    else:
        # 2D spectral data
        if "time" not in df.columns:
            raise ValueError("Your data must contain a 'time' column")
        t = df["time"].values
        wavelengths = df.columns[1:].tolist()
        signal = df.iloc[:, 1:].values
        print(f"\n Loaded 2D spectral data → shape = {signal.shape}")
        print(f" Wavelengths: {wavelengths}")

    return t, signal


from fpdf import FPDF
from fpdf import FPDF
import os
import pandas as pd

def generate_pdf_report(output_folder, summary_path, heatmap_path, overlay_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Ultrafast Spectroscopy Report", ln=True, align='C')

    # Summary Table
    pdf.ln(10)
    pdf.cell(200, 10, txt="Summary Table (First 15 Rows):", ln=True)

    df = pd.read_csv(summary_path)
    col_width = 38
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(220, 220, 220)

    # Header
    headers = ["Wavelength", "n_components", "AIC", "Chi2", "RMSE"]
    for h in headers:
        pdf.cell(col_width, 8, h, border=1, fill=True)
    pdf.ln()

    # Data rows
    for _, row in df.head(15).iterrows():
        pdf.cell(col_width, 8, str(row.get("Wavelength", "")), border=1)
        pdf.cell(col_width, 8, str(row["n_components"]), border=1)
        pdf.cell(col_width, 8, f"{row['AIC']:.1f}", border=1)
        pdf.cell(col_width, 8, f"{row['Chi2']:.1f}", border=1)
        pdf.cell(col_width, 8, f"{row['RMSE']:.4f}", border=1)
        pdf.ln()

    # Heatmap
    pdf.add_page()
    pdf.cell(200, 10, txt="Model Comparison Heatmap:", ln=True)
    pdf.image(heatmap_path, w=180)

    # Overlay Plot
    if overlay_path:
        pdf.add_page()
        pdf.cell(200, 10, txt="Overlay of Top 5 Fits:", ln=True)
        pdf.image(overlay_path, w=180)

    # Residual Heatmap
    residual_path = os.path.join(output_folder, "residual_heatmap.png")
    if os.path.exists(residual_path):
        pdf.add_page()
        pdf.cell(200, 10, txt="Residual Heatmap:", ln=True)
        pdf.image(residual_path, w=180)

    # Average Dynamic Fit
    avg_fit_path = os.path.join(output_folder, "average_dynamic_fit.png")
    if os.path.exists(avg_fit_path):
        pdf.add_page()
        pdf.cell(200, 10, txt="Average Dynamic Fit:", ln=True)
        pdf.image(avg_fit_path, w=180)
    
    lifetime_path = os.path.join(output_folder, "lifetime_spectrum.png")
    if os.path.exists(lifetime_path):
        pdf.add_page()
        pdf.cell(200, 10, txt="Lifetime Spectrum:", ln=True)
        pdf.image(lifetime_path, w=180)


    # Summary Stats
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Summary Statistics:", ln=True)
    avg_chi2 = df["Chi2"].mean()
    avg_aic = df["AIC"].mean()
    avg_rmse = df["RMSE"].mean()
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Average AIC: {avg_aic:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Average Chi²: {avg_chi2:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Average RMSE: {avg_rmse:.4f}", ln=True)

    # Output PDF
    pdf.output(f"{output_folder}/report.pdf")
