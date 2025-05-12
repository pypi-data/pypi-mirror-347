
import numpy as np
import sys
from lmfit import Model
from ultra.fitting import (convolved_model, multi_exp_model, triple_exp_model,
    quadruple_exp_model,
    quintuple_exp_model)
from lmfit import Parameters


def run_double_exp_fit(signal, t): # to automate both fits 
    # fiitng both models into the input signal and time
    

    model_mono= Model(convolved_model)
    params_mono = model_mono.make_params(
        A=.85,      
        tau=.5,    
        t0=.195,     
        fwhm=.25,   
    )
    result_mono = model_mono.fit(signal, params_mono, t=t)
    model_multi = Model(multi_exp_model)
    params_multi = model_multi.make_params(
        A1= .75,       
        tau1=.5,     
        A2=.25,       
        tau2=.45,     
        fwhm= .4,     
        t0= .1,       
    )
    result_multi = model_multi.fit(signal, params_multi, t=t)
    return result_mono, result_multi

def general_multi_exp_model(t, t0, fwhm, *params): # general multi-exponential decay model with IRF convolution
    # t is time array, t0 is center of the pulse where the sample is hit, fwhm is Full width at half max
    # this creates Gaussian shaped curves like a bell curve
    # params = [A1, tau1, A2, tau2, A3, tau3, ...]
    # A is starting amplitude, tau is the decay constant (lifetime) how fast it decays
    # thus is Classical exponential decay function (single-exponential decay curve)
    # Simple exponential decay function
    """
    General multi-exponential decay model with IRF convolution.
    params = [A1, tau1, A2, tau2, A3, tau3, ...]
    """
    signal = np.zeros_like(t)
    n = int(len(params) / 2)
    for i in range(n): # loop through the number of exponential decay components to see which fit best
        A = params[2 * i]
        tau = params[2 * i + 1]
        signal += A * np.exp(-(t - t0) / tau) * (t >= t0)
    # Apply Gaussian IRF convolution
    irf = np.exp(-4 * np.log(2) * ((t - t0) / fwhm)**2) # makes Gausian IRF 
    convolved = np.convolve(signal, irf, mode='same')
    return convolved

def make_initial_params(n_components):
    # create initial parameters for the multi-exponential decay model
    # n_components is the number of exponential decay components
    # params = [A1, tau1, A2, tau2, A3, tau3, ...]
    """
    Creates an initial parameters for the multi-exponential decay model.
    n_components is the number of exponential decay components.
    """
    params = {}
    for i in range(n_components):
        params[f"A{i+1}"] = 1.0 / n_components  # Spreads the amplitudes evenly
        params[f"tau{i+1}"] = 0.5 * (i + 1)    # guess
    # Adding the IRF params
    params["t0"] = 0.2
    params["fwhm"] = 0.3
    return params

def create_lmfit_params(initial_dict): # takes my dictionary and converts it to lmfit parameters
    # initial_dict is the initial parameters dictionary
    # returns the lmfit Parameters object
    params = Parameters()
    for key, value in initial_dict.items():
        params.add(key, value=value)
    return params

def run_general_multi_exp_fit(signal, t, n_components): # to automate both fits
    # fitting the general multi-exponential decay model into the input signal and time
    # n_components is the number of exponential decay components
    model = Model(general_multi_exp_model, independent_vars=['t']) # makes the model
    intial_dict = make_initial_params(n_components) # makes the initial parameters
    param = create_lmfit_params(intial_dict) # makes teh inital parmaters into lmfit parameters
    result = model.fit(signal, param, t=t) # fits the model
    return result
   
   

def run_n_exp_fit(signal, t, n_components):
    if n_components == 3:
        model = Model(triple_exp_model)
        params = model.make_params(
            A1=0.5, tau1=0.5,
            A2=0.3, tau2=0.3,
            A3=0.2, tau3=0.2,
            t0=0.2, fwhm=0.3
        )
    elif n_components == 4:
        model = Model(quadruple_exp_model)
        params = model.make_params(
            A1=0.4, tau1=0.4,
            A2=0.3, tau2=0.3,
            A3=0.2, tau3=0.2,
            A4=0.1, tau4=0.1,
            t0=0.2, fwhm=0.3
        )
    elif n_components == 5:
        model = Model(quintuple_exp_model)
        params = model.make_params(
            A1=0.3, tau1=0.3,
            A2=0.25, tau2=0.25,
            A3=0.2, tau3=0.2,
            A4=0.15, tau4=0.15,
            A5=0.1, tau5=0.1,
            t0=0.2, fwhm=0.3
        )
    else:
        raise ValueError("Only 3, 4, or 5 components supported for now.")

    result = model.fit(signal, params, t=t)
    return result

def evaluate_fit_quality(result):
    """
    Takes an lmfit result object and returns a dictionary of fit quality metrics.
    """
    metrics = {
        "n_params": result.nvarys,        # number of parameters
        "aic": result.aic,                # Akaike Information Criterion
        "bic": result.bic,                # Bayesian Information Criterion
        "Chi2": result.chisqr,            # Chi-square
        "r_squared": result.rsquared,     # R-squared
    }
    return metrics

def find_best_fit(signal_noisy, t, max_components=5):
    """
    Tries multiple multi-exponential fits (1 to max_n components)
    and selects the best fit based on AIC.
    """
    from lmfit import Model
    results = []
    
    # Always include the mono & double fits
    result_mono, result_double = run_double_exp_fit(signal_noisy, t)
    results.append((1, result_mono))
    results.append((2, result_double))
    
    # Then try n=3, 4, 5
    for n in range(3, max_components + 1):
        try:
            result = run_n_exp_fit(signal_noisy, t, n_components=n)
            results.append((n, result))
        except Exception as e:
            print(f"Fit failed for n={n}: {e}")
    
    # Evaluate quality
    scores = []
    for n, result in results:
        metrics = evaluate_fit_quality(result)
        metrics["n_components"] = n
        metrics["result"] = result
        scores.append(metrics)
    
    # Pick best by lowest AIC
    best = min(scores, key=lambda x: x["aic"])
    
    return best, scores


# now for dynamic model better for fitting multi-exponential decay models
# this is a general multi-exponential decay model
def dynamic_model(t, params, n_components):
    result = 0
    for i in range(n_components):
        Ai = params[f"A{i+1}"]
        taui = params[f"tau{i+1}"]
        result += Ai * np.exp(-t / taui) # this is the general multi-exponential decay model equation
    return result


import matplotlib.pyplot as plt
from scipy.linalg import svd

def estimate_svd_components(signal_2d, threshold_ratio=0.01):
    """
    Estimate number of significant SVD components per wavelength column.
    Returns list of estimated component counts and shows/saves plot.
    """
    components_per_wavelength = []

    for i in range(signal_2d.shape[1]):
        column = signal_2d[:, i]
        u, s, vh = svd(column.reshape(-1, 1), full_matrices=False)
        s_normalized = s / np.max(s)
        n_components = np.sum(s_normalized > threshold_ratio)
        components_per_wavelength.append(n_components)

    return components_per_wavelength

def export_top_n_fits(df_summary, metric="Chi2", top_n=5, save_path=None):
    """
    Export the top-N fits based on a given metric.
    """
    df_sorted = df_summary.sort_values(by=metric, ascending=False).head(top_n)
    if save_path:
        df_sorted.to_csv(save_path, index=False)
    return df_sorted

def export_worst_residuals(df_summary, metric="RMSE", bottom_n=5, save_path=None):
    """
    Export the bottom-N fits (worst) based on a given metric like RMSE.
    """
    df_sorted = df_summary.sort_values(by=metric, ascending=True).head(bottom_n)
    if save_path:
        df_sorted.to_csv(save_path, index=False)
    return df_sorted

def estimate_average_lifetime(df_summary):
    """
    Estimate average lifetime across wavelengths.
    """
    lifetimes = []
    for i, row in df_summary.iterrows():
        taus = [float(val) for key, val in row.items() if "tau" in key]
        amps = [float(val) for key, val in row.items() if "A" in key]
        if taus and amps:
            avg_lifetime = np.average(taus, weights=amps)
            lifetimes.append(avg_lifetime)
        else:
            lifetimes.append(np.nan)
    df_summary["Avg_Lifetime"] = lifetimes
    return df_summary


import seaborn as sns
import matplotlib.pyplot as plt

def plot_model_comparison_heatmap(summary_df, save_path):
    """
    Creates a heatmap of n_components vs. wavelength vs. fit quality (e.g., AIC or chi-squared).
    """
    pivoted = summary_df.pivot(index="Wavelength", columns="n_components", values="Chi2")
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivoted, annot=True, cmap="viridis", cbar_kws={"label": "Chi-Squared"})
    plt.title("Model Comparison Heatmap (Chi-Squared)")
    plt.xlabel("Number of Components")
    plt.ylabel("Wavelength")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


from lmfit import Minimizer, Parameters

def fit_global_model(t, signal_2d, n_components=2):
    """
    Global fit across wavelengths with shared taus and unique amplitudes.
    Returns: result, model_signal
    """
    n_wavelengths = signal_2d.shape[1]

    # Initialize Parameters
    params = Parameters()
    for j in range(n_wavelengths):
        for i in range(n_components):
            params.add(f"A{j}_{i+1}", value=1.0 / n_components, min=0, max=2)
    for i in range(n_components):
        params.add(f"tau{i+1}", value=0.5 * (i+1), min=0.01, max=10)
    params.add("fwhm", value=0.3, vary=False)
    params.add("t0", value=0.2, vary=False)

    # Model & residual
    def model_func(params):
        out = np.zeros_like(signal_2d)
        for j in range(n_wavelengths):
            decay = np.zeros_like(t)
            for i in range(n_components):
                A = params[f"A{j}_{i+1}"]
                tau = params[f"tau{i+1}"]
                decay += A * np.exp(-t / tau)
            irf = np.exp(-4 * np.log(2) * ((t - params["t0"]) / params["fwhm"]) ** 2)
            irf /= np.sum(irf)
            conv = np.convolve(decay, irf, mode="same")
            out[:, j] = conv
        return out


    call_counter = [0]
    total_calls_estimate = 5000 

    def residual(params):
        call_counter[0] += 1
        if call_counter[0] % 100 == 0:
            percent = 100 * call_counter[0] / total_calls_estimate
            print(f"\rProgress: {percent:.1f}% ", end="", flush=True)
        return (signal_2d - model_func(params)).ravel()



    mini = Minimizer(residual, params)
    result = mini.minimize(method="leastsq")
    fitted = model_func(result.params)

    return result, fitted



def estimate_effective_activation_energy(df_summary, time_array, temperature_scaling=False):
    """
    Optional thermodynamic-style analysis if time can be related to temperature.
    Returns DataFrame with estimated Ea values (if applicable).
    """
    if not temperature_scaling:
        print("⚠️ Skipping thermodynamic analysis (no temperature scaling)")
        return df_summary

    from scipy.stats import linregress
    Ea_list = []

    for i, row in df_summary.iterrows():
        taus = [float(val) for key, val in row.items() if "tau" in key]
        if taus:
            try:
                inv_T = 1 / (time_array + 273.15)  # Fake conversion: time to K
                ln_tau = np.log(taus)
                slope, _, _, _, _ = linregress(inv_T[:len(taus)], ln_tau)
                Ea_est = -slope * 8.314  # R = 8.314 J/mol·K
                Ea_list.append(Ea_est)
            except:
                Ea_list.append(np.nan)
        else:
            Ea_list.append(np.nan)

    df_summary["Effective_Ea_J_per_mol"] = Ea_list
    return df_summary







"""def find_best_fit(signal, t, max_components=5):
    from ultra.fitting import fit_exp_model
    from lmfit import fit_report
    from sklearn.metrics import r2_score
    import numpy as np

    results = []

    for n in range(1, max_components + 1):
        result = fit_exp_model(t, signal, n)
        residual = signal - result.best_fit
        r2 = r2_score(signal, result.best_fit)
        results.append({
            "n_components": n,
            "result": result,
            "aic": result.aic,
            "bic": result.bic,
            "r2": r2,
            "residual": residual,
        })

    # Select best by AIC
    best = min(results, key=lambda r: r["aic"])
    return best, results
"""



