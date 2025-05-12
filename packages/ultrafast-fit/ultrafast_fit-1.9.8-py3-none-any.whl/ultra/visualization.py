
import matplotlib.pyplot as plt
from ultra.fitting import dynamic_convolved_model
import pandas as pd
from .fitting import evaluate_dynamic_model  
from lmfit import fit_report
import numpy as np
from ultra.fitting import unpack_dynamic_params
from ultra.fitting import evaluate_dynamic_fit_curve
import seaborn as sns




def plot_all_fits_and_residuals(t, signal_noisy, scores, show=True, save=False, folder="plots"):
    import os
    if save and not os.path.exists(folder):
        os.makedirs(folder)

    for model in scores:
        n = model["n_components"]
        result = model["result"]
        
        # Skip if result is None or failed
        if result is None:
            continue
        
        residual = signal_noisy - result.best_fit

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        
        # Fit Plot
        axs[0].plot(t, signal_noisy, label="Noisy Data", color="royalblue")
        axs[0].plot(t, result.best_fit, label=f"{n}-Exp Fit", color="green")
        axs[0].set_title(f"{n}-Exp Fit")
        axs[0].set_xlabel("Time (ns)")
        axs[0].set_ylabel("Signal (a.u.)")
        axs[0].legend()
        axs[0].grid(True)

        # Residual Plot
        axs[1].plot(t, residual, color="crimson", label=f"{n}-Exp Residual")
        axs[1].axhline(0, color="black", linestyle="--")
        axs[1].set_title(f"{n}-Exp Residual")
        axs[1].set_xlabel("Time (ns)")
        axs[1].legend()
        axs[1].grid(True)

        plt.suptitle(f"{n}-Exp Model: Fit + Residual", fontsize=14)
        plt.tight_layout()

        if save:
            plt.savefig(f"{folder}/fit_residual_{n}exp.png", dpi=300)
        if show:
            plt.show()

        plt.close()


import pandas as pd
import matplotlib.pyplot as plt
import os

def export_fit_summary(all_scores, dynamic_result=None, n_dynamic=None, output_path="fit_summary.csv"):
    summary_data = []
    for score in all_scores:
        summary_data.append({
            "Components": score["n_components"],
            "AIC": round(score["aic"], 2),
            "BIC": round(score["bic"], 2),
            "R²": round(score["r_squared"], 4),
            "Chi²": round(score["Chi2"], 4),
        })
    
    # Add Dynamic Fit Result
    if dynamic_result is not None and n_dynamic is not None:
        summary_data.append({
            "Components": n_dynamic,
            "AIC": round(dynamic_result.aic, 2) if hasattr(dynamic_result, "aic") else None,
            "BIC": round(dynamic_result.bic, 2) if hasattr(dynamic_result, "bic") else None,
            "R²": None,
            "Chi²": round(dynamic_result.chisqr, 4),
        })

    df = pd.DataFrame(summary_data)
    df.to_csv(output_path, index=False)
    print(f"✅ Summary table saved to {output_path}")
    return df

def plot_aic_vs_components(all_scores, save_path=None):
    """
    Plots AIC vs n_components and optionally saves the plot.
    """
    import matplotlib.pyplot as plt

    components = [score["n_components"] for score in all_scores]
    aic_values = [score["aic"] for score in all_scores]

    plt.figure(figsize=(6, 4))
    plt.plot(components, aic_values, marker="o", color="purple")
    plt.xlabel("Number of Components")
    plt.ylabel("AIC")
    plt.title("AIC vs. Number of Components")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()


# safe skip

def plot_fit_and_residuals(t, signal_noisy, signal_clean, fit_results, save_path=None, show=True):
    """
    Plot fit and residuals side by side for each model.
    Automatically skips broken fits.
    """
    n_models = len(fit_results)
    fig, axes = plt.subplots(n_models, 2, figsize=(12, 4 * n_models))
    

    for i, (n, result) in enumerate(fit_results):
        if result is None:
            continue  # Skip broken fit

        # Left plot: Fit
        axes[i, 0].plot(t, signal_noisy, color="royalblue", label="Noisy Data")
        # Only plot true signal if available
        if signal_clean is not None:
            axes[i, 0].plot(t, signal_clean, color="orange", linestyle="--", label="True Signal")

        axes[i, 0].plot(t, result.best_fit, color="green", label=f"{n}-Exp Fit")
        axes[i, 0].set_title(f"{n}-Exp Fit")
        axes[i, 0].set_xlabel("Time (ns)")
        axes[i, 0].set_ylabel("Signal (a.u.)")
        axes[i, 0].legend()
        axes[i, 0].grid(True)

        # Right plot: Residual
        residual = signal_noisy - result.best_fit
        axes[i, 1].plot(t, residual, color="crimson")
        axes[i, 1].axhline(0, color="black", linestyle="--", linewidth=1)
        axes[i, 1].set_title(f"{n}-Exp Residual")
        axes[i, 1].set_xlabel("Time (ns)")
        axes[i, 1].set_ylabel("Residual")
        axes[i, 1].grid(True)
    plt.tight_layout()
    plt.suptitle("Fits & Residuals Comparison", fontsize=16, y=1.02)

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f" Saved: {save_path}")
        plt.close()
    elif show:
        plt.show()
    else:
        plt.close()




def plot_dynamic_fit_clean(t, signal, result, n_components, save_path=None, show=False, title=None):
    """Plots dynamic fit and noisy data"""
    n_components = int(n_components)  # ← first line inside the function

    plt.figure(figsize=(8, 5))

    # Plot noisy data
    plt.plot(t, signal, label="Noisy Data", color="blue")

    # Plot IRF-convolved dynamic fit
    fitted_curve = evaluate_dynamic_fit(t, result, int(np.squeeze(n_components)))
    plt.plot(t, fitted_curve, color="green", label=f"Dynamic Fit ({int(n_components)}-exp)")

    plt.xlabel("Time (ns)")
    plt.ylabel("Signal (a.u.)")
    plt.legend()

    # Title logic
    if title:
        plt.title(title)
    else:
        plt.title(f"Dynamic Fit with {int(n_components)} Exponentials (Advanced)")

    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()







def export_batch_summary(batch_results, save_path):
    """
    Export dynamic fit summary table for all wavelengths.
    """
    summary_data = []
    for index, result, signal_fit, n_dyn in batch_results:  # 

        # Get metrics
        aic = result.aic if hasattr(result, 'aic') else None
        chi2 = result.chisqr if hasattr(result, 'chisqr') else None
        rmse = np.sqrt(result.redchi) if hasattr(result, 'redchi') else None

        # Add row

        summary_data.append({
            "Wavelength Index": index + 1,
            "Wavelength": f"{400 + 6 * index}nm",  # Adjust if your spacing differs
            "n_components": n_dyn,
            "AIC": aic,
            "Chi2": chi2,
            "RMSE": rmse
        })



    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv(save_path, index=False)
    print(f"\n Batch summary table saved to: {save_path}")
    return df_summary


def evaluate_dynamic_fit(t, result, n_components):
    """
    Evaluate dynamic fit model (with IRF convolution) using fitted parameters.
    """
    # Extract parameter values
    params_dict = result.params.valuesdict()

    # Unpack A, tau, t0, fwhm
    A_list = [v for k, v in params_dict.items() if k.startswith("A")]
    tau_list = [v for k, v in params_dict.items() if k.startswith("tau")]
    t0 = params_dict["t0"]
    fwhm = params_dict["fwhm"]

    A_array = np.array(A_list)
    tau_array = np.array(tau_list)

    # --- IRF ---
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    irf = np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))
    irf /= np.sum(irf)  # normalize

    # --- Model ---
    model = np.zeros_like(t)
    for A, tau in zip(A_array, tau_array):
        model += A * np.exp(-t / tau)

    # --- Convolve ---
    convolved = np.convolve(model, irf, mode="same")

    return convolved


def plot_residual_heatmap(batch_results, t, signal_noisy, save_path=None, show=False):
    """
    Plot residual heatmap for batch dynamic fitting.
    """
    residual_matrix = []

    for index, result, signal_fit, n_dyn in batch_results:  

        if result is None:
            continue
        fitted = evaluate_dynamic_fit(t, result, n_dyn)
        residual = signal_noisy[:, index] - fitted
        residual_matrix.append(residual)

    residual_matrix = np.array(residual_matrix).T  # shape = (time, wavelength)

    plt.figure(figsize=(10, 6))
    sns.heatmap(residual_matrix, cmap="coolwarm", cbar=True)
    plt.title("Residual Heatmap (Time vs Wavelength)")
    plt.xlabel("Wavelength Index")
    plt.ylabel("Time Index")

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f" Residual heatmap saved to: {save_path}")
        plt.close()
    elif show:
        plt.show()
    else:
        plt.close()


def plot_average_fit(batch_results, t, save_path=None, show=False):
    """
    Plot average fitted signal across all wavelengths.
    """
    all_fits = []

    for index, result, signal_fit, n_dyn in batch_results: 

        if result is None:
            continue
        fitted = evaluate_dynamic_fit(t, result, n_dyn)
        all_fits.append(fitted)

    avg_fit = np.mean(np.array(all_fits), axis=0)

    plt.figure(figsize=(8, 5))
    plt.plot(t, avg_fit, color="green", label="Average Dynamic Fit")
    plt.xlabel("Time (ns)")
    plt.ylabel("Signal (a.u.)")
    plt.title("Average Dynamic Fit (All Wavelengths)")
    plt.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f" Average fit plot saved to: {save_path}")
        plt.close()
    elif show:
        plt.show()
    else:
        plt.close()

def plot_model_comparison_heatmap(df_summary, save_path=None, metric="Chi2"):
    import seaborn as sns
    import matplotlib.pyplot as plt

    
    if "Wavelength" in df_summary.columns:
        pivot = df_summary.pivot(index="Wavelength", columns="n_components", values=metric)
    else:
        pivot = df_summary.pivot(index="Wavelength Index", columns="n_components", values=metric)


    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="viridis")
    plt.title(f"Model Comparison Heatmap ({metric.upper()})")
    plt.xlabel("Number of Exponential Components")
    plt.ylabel("Wavelength")
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_svd_component_estimates(svd_counts, save_path=None):
    plt.figure(figsize=(10, 5))
    plt.plot(svd_counts, marker="o")
    plt.xlabel("Wavelength Index")
    plt.ylabel("Estimated SVD Components")
    plt.title("SVD Component Estimate per Wavelength")
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f" SVD component estimate plot saved to: {save_path}")
    plt.close()

def plot_overlay_top_fits(t, signal_2d, batch_results, top_indices, save_path=None, show=False):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    for idx in top_indices:
        i, result, fit_signal, n = batch_results[idx]
        plt.plot(t, fit_signal, label=f"Wavelength {i+1} ({n}-exp)")  
        plt.plot(t, signal_2d[:, i], '--', alpha=0.4, label=f"Original {i+1}")
    plt.xlabel("Time (ns)")
    plt.ylabel("Signal")
    plt.title("Overlay of Top 5 Fits")
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    plt.close()

def plot_lifetime_spectrum(df_summary, save_path=None, show=False):
    """
    Plot average lifetime vs. wavelength.
    """
    wavelengths = df_summary["Wavelength Index"]
    lifetimes = df_summary["Avg_Lifetime"]

    plt.figure(figsize=(8, 5))
    plt.plot(wavelengths, lifetimes, marker='o', color="darkorange")
    plt.xlabel("Wavelength Index")
    plt.ylabel("Avg Lifetime (ns)")
    plt.title("Lifetime Spectrum")
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f" Lifetime spectrum saved to: {save_path}")
    if show:
        plt.show()
    plt.close()

