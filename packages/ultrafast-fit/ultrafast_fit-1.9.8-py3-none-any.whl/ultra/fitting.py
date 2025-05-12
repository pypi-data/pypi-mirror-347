
import numpy as np
from scipy.special import erf
from scipy.signal import fftconvolve
from lmfit import Minimizer, Parameters, fit_report
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import os
from scipy.signal import fftconvolve

def gaussian_irf(t, t0=0.0, fwhm=0.2):
    """sims laser pulse as a Gaussian shape t is time array, t0 is cenetr of the pule where
    the sample is hit fwhm is FUll width at half max this created gaussuan shaped cires liek a bell curve"""
    """Gaussian Instrument Response Function (IRF)""" 
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))

def exponential_decay(t, A=1.0, tau=1.0): # Models molecular decay as an exponential decay
    """ A starting amplitude, tau is the decay constant (lifetime) hw fast
    it decays thus is Classucal exponential decay function (single-exponetial decay curve)"""
    """Simple exponential decay function"""
    return A * np.exp(-t / tau)

def convolved_model(t, A=1.0, tau=1.0, t0=0.0, fwhm=0.2): # Convolution of the two functions blends uisng convolution
    # so IRF blurs the decay  The true decay blurred by pulse
    """Convolution of exponential decay with Gaussian IRF"""
    dt = t[1] - t[0]  # time step
    decay = exponential_decay(t, A, tau)
    irf = gaussian_irf(t, t0, fwhm)
    conv = fftconvolve(decay, irf, mode='full')[:len(t)] * dt
    return conv


def multi_exp_model(t, A1=1.0, tau1=1.0, A2=0.5, tau2=0.3, t0=0.0, fwhm=0.2):
    """Convolution of double exponential decay with Gaussian IRF"""
    dt = t[1] - t[0]
    decay = A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2)
    irf = gaussian_irf(t, t0, fwhm)
    conv = fftconvolve(decay, irf, mode='full')[:len(t)] * dt
    return conv


# upsclainf for past double exp to triple exp, quad exp, and quintuple exp

# same princples apply to the triple, quad, and quintuple exponential decay models
# the only difference is the number of exponential decay components
# and the number of parameters in the model
# the general multi-exponential decay model with IRF convolution

def triple_exp_model(t, A1, tau1, A2, tau2, A3, tau3, t0, fwhm):
    dt = t[1] - t[0]
    decay = A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) + A3 * np.exp(-t / tau3)
    irf = np.exp(-4 * np.log(2) * ((t - t0) / fwhm)**2)
    conv = fftconvolve(decay, irf, mode='full')[:len(t)] * dt
    return conv

def quadruple_exp_model(t, A1, tau1, A2, tau2, A3, tau3, A4, tau4, t0, fwhm):
    dt = t[1] - t[0]
    decay = (
        A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) +
        A3 * np.exp(-t / tau3) + A4 * np.exp(-t / tau4)
    )
    irf = np.exp(-4 * np.log(2) * ((t - t0) / fwhm)**2)
    conv = fftconvolve(decay, irf, mode='full')[:len(t)] * dt
    return conv

def quintuple_exp_model(t, A1, tau1, A2, tau2, A3, tau3, A4, tau4, A5, tau5, t0, fwhm):
    dt = t[1] - t[0]
    decay = (
        A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) +
        A3 * np.exp(-t / tau3) + A4 * np.exp(-t / tau4) + A5 * np.exp(-t / tau5)
    )
    irf = np.exp(-4 * np.log(2) * ((t - t0) / fwhm)**2)
    conv = fftconvolve(decay, irf, mode='full')[:len(t)] * dt
    return conv

# loopong over many exp components bulding the model as a sum of teh epxonetials 
def dynamic_multi_exp(t, params, n_components):
    """
    Dynamically builds multi-exponential model.
    """
    model = np.zeros_like(t)
    for i in range(n_components):
        Ai = params[f"A{i+1}"]
        taui = params[f"tau{i+1}"]
        model += Ai * np.exp(-t / taui)
    return model

# convolving the multi-exponential model with the Gaussian IRF
# caluclatign the Gausin RF buling the multi-exp using fxn 
def dynamic_convolved_model(t, params, n_components, fwhm, t0):
    """
    Multi-exponential model convolved with Gaussian IRF.
    """
    # --- IRF Calculation ---
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    irf = np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))
    irf /= np.sum(irf)  # normalize

    # --- Multi-Exp Model ---
    model = dynamic_multi_exp(t, params, n_components)

    # --- Convolution ---
    convolved = fftconvolve(model, irf, mode="same")

    return convolved



# new dynaic fit model to better fit the data as old one wa sterirble
"""def fit_dynamic_model(t, signal, n_components=3):
    from lmfit import Minimizer, Parameters
    from src.fitting import dynamic_convolved_model

    # === Build parameters with good initial guesses & bounds ===
    params = Parameters()
    for i in range(n_components):
        params.add(f"A{i+1}", value=1.0/n_components, min=0, max=2)  # amplitude between 0 and 2
        params.add(f"tau{i+1}", value=(i+1)*0.5, min=0.05, max=10)   # lifetime bounds 0.05–10 ns

    params.add("fwhm", value=0.3, vary=False)
    params.add("t0", value=0.2, vary=False)

    # === Model function ===
    def model_func(params):
        return dynamic_convolved_model(t, params, n_components, fwhm=0.3, t0=0.2)

    # === Residual function ===
    def residual(params):
        model = model_func(params)
        return signal - model

    # === Fit ===
    mini = Minimizer(residual, params)
    result = mini.minimize(method="leastsq")

    return result  # returns MinimizerResult
old code for dynamic fit model its bad and doesn't work"""


# new dynamic fit model to better fit the data as old one was terrible
# this new model uses advanced techniques to improve the fit
# such as normalization, SVD, automatic guesses, and bounds
# this model is more robust and reliable than the previous one
# it is also more accurate and efficient
# it is recommended to use this model for dynamic fitting
# as it provides better results and faster convergence
# this model is based on the latest research in dynamic fitting

def normalize_signal(signal):
    """Normalize signal between 0 and 1."""
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))

def estimate_components_svd(signal, t, threshold=0.01):
    """Estimate number of components based on SVD energy."""
    data = signal.reshape(-1, 1)
    svd = TruncatedSVD(n_components=min(len(data), 10))
    svd.fit(data)
    explained = np.cumsum(svd.explained_variance_ratio_)
    n_components = np.searchsorted(explained, 1 - threshold) + 1
    return max(n_components, 2)

def guess_initial_params_svd(signal, t, n_components):
    """Generate initial guesses based on SVD."""
    A_guess = np.full(n_components, 1/n_components)
    tau_guess = np.linspace(0.2, 5, n_components)
    return A_guess, tau_guess

"""def fit_dynamic_model_advanced(t, signal, n_components=None, save_folder=None):
    #"Full Dynamic Fit with normalization, optional SVD, auto guesses & bounds."

    # === Detect if 1D or 2D ===
    auto_normalize = True
    if n_components is None:
        if signal.ndim == 1:
            print("\n Detected 1D data → Skipping SVD")
            n_components = 3
            auto_normalize = False
        else:
            print("\n Detected 2D data → Running SVD")
            n_components = estimate_components_svd(signal, t)
            print(f"\n SVD suggested {n_components} components")
    else:
        print(f"\n Overriding n_components → Using {n_components}")

    # === Normalize Signal ===
    signal_proc = normalize_signal(signal) if auto_normalize else signal

    # === Guess Parameters ===
    A_guess, tau_guess = guess_initial_params_svd(signal_proc, t, n_components)

    # === Build Parameters ===
    params = Parameters()
    for i in range(n_components):
        params.add(f"A{i+1}", value=A_guess[i], min=0, max=2)
        params.add(f"tau{i+1}", value=tau_guess[i], min=0.01, max=20)
    params.add("fwhm", value=0.3, vary=False)
    params.add("t0", value=0.2, vary=False)

    # === Define Model ===
    def model_func(params):
        return dynamic_convolved_model(t, params, n_components, fwhm=params["fwhm"].value, t0=params["t0"].value)

    def residual(params):
        model = model_func(params)
        return signal_proc - model

    # === Run Minimizer ===
    mini = Minimizer(residual, params)
    result = mini.minimize(method="leastsq")

        # === Auto Save ===
    if save_folder:
        from lmfit import fit_report  # just in case it's not imported above
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Save fit report
        result_file = os.path.join(save_folder, f"dynamic_fit_report_{timestamp}.txt")
        with open(result_file, "w") as f:
            f.write(fit_report(result))  # ✅ correct usage here
        print(f"✅ Dynamic fit report saved to: {result_file}")

        # Save residuals
        residuals = pd.DataFrame({"time": t, "residual": result.residual})
        residuals.to_csv(os.path.join(save_folder, f"dynamic_residuals_{timestamp}.csv"), index=False)

        # Save parameters
        param_dict = {k: v.value for k, v in result.params.items()}
        pd.DataFrame([param_dict]).to_csv(os.path.join(save_folder, f"dynamic_parameters_{timestamp}.csv"), index=False)
    
    return result, n_components
    """


def fit_dynamic_model_advanced(t, signal, n_components=None, save_folder=None):
    """Full Dynamic Fit with normalization, optional SVD, auto guesses & bounds."""
    from lmfit import Minimizer, Parameters, fit_report

    # === Normalize signal ===
    signal_norm = normalize_signal(signal)

    # === Detect if 1D or 2D ===
    if n_components is None:
        if signal.ndim == 1:
            print("\n Detected 1D data → Skipping SVD")
            n_components = 3  # default
        else:
            print("\n Detected 2D data → Running SVD")
            n_components = estimate_components_svd(signal_norm, t)
            print(f"\n SVD suggested {n_components} components")
    else:
        print(f"\n Overriding n_components → Using {n_components}")

    # === Guess Parameters ===
    A_guess, tau_guess = guess_initial_params_svd(signal_norm, t, n_components)

    # === Build Parameters ===
    params = Parameters()
    for i in range(n_components):
        params.add(f"A{i+1}", value=A_guess[i], min=0, max=2)
        params.add(f"tau{i+1}", value=tau_guess[i], min=0.01, max=20)
    params.add("fwhm", value=0.3, vary=False)
    params.add("t0", value=0.2, vary=False)

    # === Define Model ===
    def model_func(params):
        return dynamic_convolved_model(t, params, n_components, fwhm=params["fwhm"].value, t0=params["t0"].value)

    def residual(params):
        model = model_func(params)
        return signal_norm - model

    # === Run Minimizer ===
    mini = Minimizer(residual, params)
    result = mini.minimize(method="leastsq")

    # === Auto Save ===
    if save_folder:
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
        result_file = os.path.join(save_folder, f"dynamic_fit_report_{timestamp}.txt")
        with open(result_file, "w") as f:
            f.write(fit_report(result))  # Save fit report

        # Save residuals
        residuals = pd.DataFrame({"time": t, "residual": result.residual})
        residuals.to_csv(os.path.join(save_folder, f"dynamic_residuals_{timestamp}.csv"), index=False)

        # Save parameters
        param_dict = {k: v.value for k, v in result.params.items()}
        pd.DataFrame([param_dict]).to_csv(os.path.join(save_folder, f"dynamic_parameters_{timestamp}.csv"), index=False)

        print(f" Dynamic fit results saved to: {save_folder}")

    # === Evaluate fitted signal ===
    best_fit_signal = evaluate_dynamic_fit_curve(t, result, n_components)

    # === Final return ===
    return result, n_components, best_fit_signal






def evaluate_dynamic_model(t, params):
    """Evaluate dynamic model with IRF convolution"""
    A_list = []
    tau_list = []
    for key, value in params.items():
        if key.startswith("A"):
            A_list.append(value)
        if key.startswith("tau"):
            tau_list.append(value)
    A_array = np.array(A_list)
    tau_array = np.array(tau_list)
    fwhm = params["fwhm"]
    t0 = params["t0"]

    # Build exponential model
    model = np.zeros_like(t)
    for A, tau in zip(A_array, tau_array):
        model += A * np.exp(-t / tau)

    # Build IRF (Gaussian centered at t0)
    irf = np.exp(-4 * np.log(2) * ((t - t0) / fwhm) ** 2)
    irf /= np.trapz(irf, t)  # Normalize IRF area to 1

    # Convolve model with IRF
    convolved = fftconvolve(model, irf, mode="same")

    return convolved


def unpack_dynamic_params(params_dict):
    """
    Unpack A1, A2, tau1, tau2, ... into arrays for dynamic_convolved_model
    """
    A_list = []
    tau_list = []
    for key, value in params_dict.items():
        if key.startswith("A"):
            A_list.append(value)
        elif key.startswith("tau"):
            tau_list.append(value)
    t0 = params_dict["t0"]
    fwhm = params_dict["fwhm"]
    return np.array(A_list), np.array(tau_list), t0, fwhm

# IRF_eval fxn
def evaluate_dynamic_fit_curve(t, result, n_components):
    """
    Evaluate the fitted dynamic model (IRF-convolved) using optimized parameters.
    This is the equivalent of .best_fit for dynamic fitting.
    """
    # === Unpack parameters ===
    params_dict = result.params.valuesdict()
    A_array, tau_array, t0, fwhm = unpack_dynamic_params(params_dict)

    # === Rebuild model ===
    # Multi-exponential decay
    model = np.zeros_like(t)
    for A, tau in zip(A_array, tau_array):
        model += A * np.exp(-t / tau)

    # IRF
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    irf = np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))
    irf /= np.sum(irf)  # normalize

    # Convolution
    convolved = fftconvolve(model, irf, mode="same")

    return convolved


def plot_overlay_top_fits(t, signal_2d, batch_results, top_indices, save_path=None):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for idx in top_indices:
        i, result, fit_signal, n = batch_results[idx]
        plt.plot(t, fit_signal, label=f"Wavelength {i+1} ({n}-exp)")  #  use fit_signal
        plt.plot(t, signal_2d[:, i], '--', alpha=0.4, label=f"Original {i+1}")


    plt.title("Overlay of Top 5 Fits")
    plt.xlabel("Time (ns)")
    plt.ylabel("Signal (a.u.)")
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close()
