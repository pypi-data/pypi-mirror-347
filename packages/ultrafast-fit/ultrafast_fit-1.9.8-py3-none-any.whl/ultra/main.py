
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import time
import os
from lmfit import Parameters, Minimizer, fit_report
from ultra.analysis import export_top_n_fits, export_worst_residuals
from ultra.analysis import plot_model_comparison_heatmap
from lmfit import fit_report
from lmfit import conf_interval, printfuncs 
from lmfit import Minimizer, conf_interval, report_ci

from ultra.utils import load_data
from ultra.analysis import run_double_exp_fit, find_best_fit
from ultra.fitting import (
    convolved_model,
    dynamic_convolved_model,
    fit_dynamic_model_advanced
)

from ultra.visualization import (
    export_fit_summary,
    plot_all_fits_and_residuals,
    plot_aic_vs_components,
    plot_fit_and_residuals,
    plot_dynamic_fit_clean,
    export_batch_summary     
)

from ultra.fitting import fit_dynamic_model_advanced
from ultra.visualization import plot_dynamic_fit_clean
import traceback
traceback.print_exc()
from ultra.visualization import plot_residual_heatmap, plot_average_fit
from ultra.analysis import find_best_fit



start_time = time.time()
print(f"\n🔁 Script started at: {time.strftime('%H:%M:%S')}")


def main():
    print("\n Starting ultrafast Fitting Project...\n")

    parser = argparse.ArgumentParser(description="ultrafast Signal Fitting Options")
    parser.add_argument("--max-components", type=int, default=4, help="Maximum number of exponential components to try")
    parser.add_argument("--export-summary", action="store_true", help="Export summary table to CSV")
    parser.add_argument("--show-plots", action="store_true", help="Show fit & residual plots")
    parser.add_argument("--plot-aic", action="store_true", help="Plot AIC vs n_components graph")
    parser.add_argument("--data-file", type=str, default=None, help="Path to input data file (.csv, .txt, .xlsx, .mat)")
    parser.add_argument("--n-components", type=int, default=None, help="Manually specify number of dynamic components (optional)")
    parser.add_argument("--show-every", type=int, default=10, help="Show every N-th plot during batch fitting (optional)")  
    parser.add_argument("--save-extra", action="store_true", help="Save extra plots: residual heatmap & average dynamic fit")
    parser.add_argument("--heatmap", action="store_true", help="Plot model comparison heatmap (for 2D only)")
    parser.add_argument("--global-fit", action="store_true", help="Run global fit across all wavelengths")
    parser.add_argument("--thermo", action="store_true", help="Run thermodynamic-style activation energy estimation")



    args = parser.parse_args()

    # === Load Data ===
    t, signal_noisy = load_data(args.data_file)
    signal_clean = convolved_model(t, A=1.0, tau=0.8, t0=0.2, fwhm=0.3) if args.data_file is None else None

    # === Output Folder ===
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"results/{timestamp}"
    os.makedirs(output_folder, exist_ok=True)

    # === Normalize Signal ===
    signal_noisy = (signal_noisy - np.min(signal_noisy)) / (np.max(signal_noisy) - np.min(signal_noisy))

    # === If 1D → Standard Fitting ===
    if signal_noisy.ndim == 1:
        print("\n Detected 1D kinetic data → Running standard multi-exp fit")

        # === AIC/BIC Model Comparison ===
        best_fit, all_scores = find_best_fit(signal_noisy, t, max_components=args.max_components)

        print(f"\n=== BEST MODEL: {best_fit['n_components']} Components ===")
        print(best_fit["result"].fit_report())

        #from lmfit import Minimizer, conf_interval, report_ci

                # === Confidence Intervals ===
        from lmfit import Minimizer, conf_interval, report_ci

# Define a residual function for confidence interval estimation
        def residual(params):
            return signal_noisy - best_fit["result"].model.eval(params, t=t)

        try:
            minimizer = Minimizer(residual, best_fit["result"].params)
            ci = conf_interval(minimizer, result=best_fit["result"], sigmas=[1], trace=False, maxiter=100)

            ci_text = report_ci(ci)
            if ci_text is not None:
                with open(f"{output_folder}/fit_confidence_intervals.txt", "w") as f:
                    f.write(ci_text)
                print(f"\n Confidence intervals saved to: {output_folder}/fit_confidence_intervals.txt")
            else:
                print("\n Confidence interval report could not be generated (report_ci returned None).")

        except Exception as e:
            print(f"\n Confidence interval estimation failed: {e}")



        # === Save Fit, Residual, Summary ===
        best_fit_signal = pd.DataFrame({"time": t, "best_fit": best_fit["result"].best_fit})
        best_fit_signal.to_csv(f"{output_folder}/best_fit_signal.csv", index=False)

        resid = signal_noisy - best_fit["result"].best_fit
        pd.DataFrame({"time": t, "residual": resid}).to_csv(f"{output_folder}/residuals.csv", index=False)


        # === Visualization ===
        plot_all_fits_and_residuals(t, signal_noisy, all_scores, show=args.show_plots, save=True, folder=output_folder)
        plot_aic_vs_components(all_scores, save_path=f"{output_folder}/aic_vs_components.png")

        if best_fit:
            from matplotlib import pyplot as plt
            n = best_fit["n_components"]
            result = best_fit["result"]
            residual = signal_noisy - result.best_fit

            fig, axs = plt.subplots(1, 2, figsize=(12, 4))

            axs[0].plot(t, signal_noisy, label="Noisy Data", color="royalblue")
            axs[0].plot(t, result.best_fit, label=f"{n}-Exp Best Fit", color="green")
            axs[0].set_title("Best Fit")
            axs[0].set_xlabel("Time (ns)")
            axs[0].set_ylabel("Signal (a.u.)")
            axs[0].legend()
            axs[0].grid(True)

            axs[1].plot(t, residual, color="crimson", label="Residual")
            axs[1].axhline(0, color="black", linestyle="--")
            axs[1].set_title("Best Fit Residual")
            axs[1].set_xlabel("Time (ns)")
            axs[1].legend()
            axs[1].grid(True)

            plt.suptitle(f"Best Fit: {n}-Exponential Model", fontsize=14)
            plt.tight_layout()
            plt.savefig(f"{output_folder}/best_fit_only.png", dpi=300)
            if args.show_plots:
                plt.show()
            plt.close()
    
        # === Best Fit Only Plot ===

        print(f"\n Standard fit results saved to: {output_folder}")
    

    # === If 2D → Batch Dynamic Fit ===
        # === If 2D → Batch Dynamic Fit ===
    else:
        print("\n Detected 2D spectral data → Running Batch Dynamic Fitting")

        batch_results = []
        for i in range(signal_noisy.shape[1]):
            print(f"\n Fitting wavelength {i+1}/{signal_noisy.shape[1]}")
            signal_column = signal_noisy[:, i]
            dynamic_result, n_dyn, signal_fit = fit_dynamic_model_advanced(
                t, signal_column,
                n_components=args.n_components,
                save_folder=output_folder
            )
            try:
                n_dyn_clean = np.ravel(n_dyn)  # flatten it
                if n_dyn_clean.size == 1:
                    n_dyn = int(n_dyn_clean[0])
                else:
                    raise ValueError(f"n_dyn has unexpected shape: {n_dyn}")
            except Exception as e:
                 print(f"\n Could not clean n_dyn → {n_dyn} → {type(n_dyn)}")
                 raise e
                


            print(f"✔️ Cleaned n_dyn = {n_dyn} → type = {type(n_dyn)}")  # Debug check


            batch_results.append((i, dynamic_result, signal_fit, n_dyn))

            # === Save & Show Plot ===
            plot_path = f"{output_folder}/dynamic_fit_wavelength_{i+1}.png"
            show_plot = args.show_plots and (i % args.show_every == 0 or i == signal_noisy.shape[1] - 1) # show every 10th & last

            plot_dynamic_fit_clean(
                t, signal_column, dynamic_result, n_dyn,
                save_path=plot_path,
                show=show_plot,
                title=f"Dynamic Fit ({n_dyn} Exp) - Wavelength {i+1}"
            )

        print(f"\n Batch Dynamic Fitting completed → {len(batch_results)} wavelengths fitted")
        print(f"\n All results saved in: {output_folder}")

            # === Export Batch Summary ===
        print(f"\n Dynamic Fit: Showing every {args.show_every}-th plot (total {signal_noisy.shape[1]} wavelengths)")
        summary_path = f"{output_folder}/batch_fit_summary.csv"
        df_summary = export_batch_summary(batch_results, summary_path)

        # === Optional Summary Filtering Tools ===
        from ultra.analysis import export_top_n_fits, export_worst_residuals

        top_n_path = f"{output_folder}/top5_fits_by_r2.csv"
        worst_n_path = f"{output_folder}/worst5_by_rmse.csv"

        export_top_n_fits(df_summary, metric="Chi2", top_n=5, save_path=top_n_path)
        export_worst_residuals(df_summary, metric="RMSE", bottom_n=5, save_path=worst_n_path)

        print(f"\n Exported Top 5 fits → {top_n_path}")
        print(f" Exported Worst 5 residuals → {worst_n_path}")


        from ultra.analysis import estimate_svd_components
        from ultra.visualization import plot_svd_component_estimates

        svd_counts = estimate_svd_components(signal_noisy)
        plot_svd_component_estimates(svd_counts, save_path=f"{output_folder}/svd_component_estimates.png")


        print(f"\n Batch summary table saved to: {summary_path}")
    """
    # === Optional: Save extra plots ===
    if args.save_extra:
        residual_path = f"{output_folder}/residual_heatmap.png"
        avg_fit_path = f"{output_folder}/average_dynamic_fit.png"

        plot_residual_heatmap(batch_results, t, signal_noisy, save_path=residual_path)
        plot_average_fit(batch_results, t, save_path=avg_fit_path)

        print(f"\n Residual heatmap saved to: {residual_path}")
        print(f" Average fit plot saved to: {avg_fit_path}")




        # === Optional: Export to main directory if requested
        if args.export_summary:
            df_summary.to_csv("batch_fit_summary.csv", index=False)
            print("\n Summary table also exported to: batch_fit_summary.csv (project folder)")
    """
        # === Optional: Save extra plots (only for 2D data) ===
    if signal_noisy.ndim > 1 and args.save_extra:
        residual_path = f"{output_folder}/residual_heatmap.png"
        avg_fit_path = f"{output_folder}/average_dynamic_fit.png"

        plot_residual_heatmap(batch_results, t, signal_noisy, save_path=residual_path)
        plot_average_fit(batch_results, t, save_path=avg_fit_path)

        print(f"\n Residual heatmap saved to: {residual_path}")
        print(f" Average fit plot saved to: {avg_fit_path}")


    if signal_noisy.ndim > 1 and args.export_summary:
        df_summary.to_csv("batch_fit_summary.csv", index=False)
        print("\n Summary table also exported to: batch_fit_summary.csv (project folder)")
        # === Export Batch Summary ===
        summary_path = f"{output_folder}/batch_fit_summary.csv"
        df_summary = export_batch_summary(batch_results, summary_path)

        # === Lifetime Estimation ===
        from ultra.analysis import estimate_average_lifetime
        df_summary = estimate_average_lifetime(df_summary)
        df_summary.to_csv(f"{output_folder}/batch_fit_summary_with_lifetime.csv", index=False)
        print(f"\n Saved lifetime-enhanced summary → {output_folder}/batch_fit_summary_with_lifetime.csv")
        df_summary = estimate_average_lifetime(df_summary)
        # Optional: Thermodynamic Analysis
        from ultra.analysis import estimate_effective_activation_energy
        df_summary = estimate_effective_activation_energy(df_summary, t, temperature_scaling=args.thermo)


        # === Overlay Plot of Top 5 Fits ===
        from ultra.visualization import plot_overlay_top_fits
        top_indices = df_summary.sort_values(by="Chi2", ascending=False).head(5).index.tolist()
        plot_overlay_top_fits(t, signal_noisy, batch_results, top_indices, save_path=f"{output_folder}/overlay_top5_fits.png")
        print(f"\n Overlay plot of top 5 fits saved → {output_folder}/overlay_top5_fits.png")

        # === Auto-generate PDF Report ===
        from ultra.utils import generate_pdf_report
       # First: generate the heatmap
        plot_model_comparison_heatmap(df_summary, save_path=f"{output_folder}/model_comparison_heatmap.png")
        print(f"\n Model comparison heatmap saved to: {output_folder}/model_comparison_heatmap.png")

        from ultra.visualization import plot_lifetime_spectrum
        plot_lifetime_spectrum(df_summary, save_path=f"{output_folder}/lifetime_spectrum.png")

        generate_pdf_report(
            output_folder,
            summary_path=summary_path,
            heatmap_path=f"{output_folder}/model_comparison_heatmap.png",
            overlay_path=f"{output_folder}/overlay_top5_fits.png"
        )
        print(f"\n PDF report generated in: {output_folder}/report.pdf")
    if args.global_fit:
        start_global = time.time()
        print(f"\n Starting global fit using {args.n_components} components for shape = {signal_noisy.shape}")
        print("\n Running global fit across all wavelengths (shared taus)...")

        from ultra.analysis import fit_global_model
        try:
            global_result, global_fit = fit_global_model(t, signal_noisy, n_components=args.n_components)
            duration = time.time() - start_global
            print(f"\n  Global fit completed in {duration:.2f} seconds.")

            # === Global Confidence Intervals ===
            ci = conf_interval(global_result)
            with open(f"{output_folder}/global_fit_confidence_intervals.txt", "w") as f:
                printfuncs.report_ci(ci, file=f)
            print(f" Global fit confidence intervals saved to: {output_folder}/global_fit_confidence_intervals.txt")



            #  Save only if it was successful
            pd.DataFrame(global_fit, columns=[f"W{i+1}" for i in range(global_fit.shape[1])]).to_csv(f"{output_folder}/global_fit.csv", index=False)
            with open(f"{output_folder}/global_fit_report.txt", "w") as f:
                f.write(fit_report(global_result))
            print(f"\n Global fit results saved to: {output_folder}/global_fit.csv")            

        except Exception as e:
            print(f"\n  Global fit failed: {e}")
            import traceback
            traceback.print_exc()
            return







# TEsting if its crahsing in teh background
if __name__ == "__main__":
    try:
        main()
        print("\n Script finished successfully.\n")
    except Exception as e:
        print(f"\n Error occurred: {e}\n")
        import traceback
        traceback.print_exc()



print(f"\n Script finished at: {time.strftime('%H:%M:%S')}")
print(f"⏱ Total runtime: {time.time() - start_time:.2f} seconds.")

# to run: python3 main.py --data-file "your_data.csv" --n-components 5 --show-plots --export-summary
# python3 main.py --data-file "/Users/alanarana/Desktop/Sample Data/Synthetic_Spectral_Data__2D_.csv" --n-components 5 --show-plots --export-summary

# adding CLI toggl efor teh live plotting

#python3 main.py --data-file "..." --n-components 5 --show-plots --show-every 10

#python3 main.py --data-file "/Users/alanarana/Desktop/Sample Data/Synthetic_Spectral_Data__2D_.csv" --n-components 5 --show-plots --show-every 10

# python3 main.py --data-file "/Users/alanarana/Desktop/Sample Data/Synthetic_Spectral_Data__2D_.csv" --n-components 5 --show-plots --export-summary --show-every 10

# python3 main.py --data-file "/Users/alanarana/Desktop/Sample Data/Synthetic_Spectral_Data__2D_.csv" --n-components 5 --show-plots --export-summary --show-every 10


#python3 main.py --data-file "path/to/1d_data.csv" --plot-aic --show-plots

# wuth AUC/BIC compsriosnm:python3 main.py --data-file "your_1D_data.csv" --plot-aic --show-plots
#python3 main.py --data-file "your_1D_data.csv" --plot-aic --show-plots

#  python3 main.py --data-file '/Users/alanarana/Desktop/Sample Data/sample_data.csv' --plot-aic --show-plots




# ultrafast-fit --data-file '/Users/alanarana/Desktop/Sample Data/sample_data.csv' --n-components 5 --show-plots

# ultrafast-fit --data-file '/Users/alanarana/Desktop/Sample Data/sample_data.csv' --n-components 5 --show-plots



# ultrafast-fit --data-file '/Users/alanarana/Desktop/Sample Data/sample_data.csv' --n-components 5 --show-plots


# need these

# "numpy pandas matplotlib lmfit seaborn scikit-learn setuptools" > requirements.txt
#pip3 install -r requirements.txt

# test

#PYTHONPATH=. python3 ultra/main.py --data-file "/Users/alanarana/Desktop/Sample Data/sample_data.csv" --n-components 4 --show-plots --export-summary --save-extra


"""PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/synthetic_2d_data.csv" \
--n-components 4 \
--show-plots \
--export-summary \
--save-extra \
--heatmap \
--global-fit
"""

""" Quick 

PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/synthetic_2d_data.csv" \
--n-components 4 \
--show-plots \
--export-summary \
--save-extra \
--heatmap \
--global-fit \
--show-every 25

global-fit takes a long long long time esouclay depdnign how how many are showing 
"""



"""
testing with Thermo anylsis and quick

PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/synthetic_2d_data.csv" \
--n-components 4 \
--show-plots \
--export-summary \
--save-extra \
--heatmap \
--thermo \
--global-fit \
--show-every 25

"""


"""

tetsign with global fit 


PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/synthetic_2d_data.csv" \
--n-components 4 \
--show-plots \
--export-summary \
--save-extra \
--heatmap \
--thermo \
--show-every 25

"""



"""
confidnce netrval included 
1D data test

PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/sample_data.csv" \
--n-components 3 \
--show-plots \
--export-summary


2D data test 

PYTHONPATH=. python3 ultra/main.py \
--data-file "/Users/alanarana/Desktop/Sample Data/synthetic_2d_data.csv" \
--n-components 4 \
--show-plots \
--export-summary \
--save-extra \
--heatmap \
--thermo \
--global-fit \
--show-every 25


"""