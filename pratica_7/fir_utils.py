from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile


def find_repo_root(start_path, practice_dir="pratica_7"):
    start_path = Path(start_path).resolve()
    for candidate in [start_path, *start_path.parents]:
        if (candidate / "data").exists() and (candidate / practice_dir).exists():
            return candidate
    raise FileNotFoundError(
        "Repositorio nao encontrado. Execute o notebook dentro da pasta do projeto."
    )


def display_rows(rows, float_digits=6):
    if not rows:
        print("Sem dados para exibir.")
        return

    headers = list(rows[0].keys())
    formatted_rows = []
    for row in rows:
        formatted = []
        for header in headers:
            value = row[header]
            if isinstance(value, float):
                formatted.append(f"{value:.{float_digits}f}")
            else:
                formatted.append(str(value))
        formatted_rows.append(formatted)

    widths = []
    for idx, header in enumerate(headers):
        content_width = max(len(row[idx]) for row in formatted_rows)
        widths.append(max(len(header), content_width))

    header_line = " | ".join(
        header.ljust(widths[idx]) for idx, header in enumerate(headers)
    )
    separator = "-+-".join("-" * width for width in widths)
    print(header_line)
    print(separator)
    for row in formatted_rows:
        print(" | ".join(value.ljust(widths[idx]) for idx, value in enumerate(row)))


def normalize_audio(x):
    x = np.asarray(x)
    if x.ndim > 1:
        x = np.mean(x, axis=1)
    if np.issubdtype(x.dtype, np.integer):
        max_value = np.iinfo(x.dtype).max
        return x.astype(np.float64) / max_value
    return x.astype(np.float64)


def load_handel_audio(data_dir):
    fs_audio, audio_raw = wavfile.read(Path(data_dir) / "handel.wav")
    return fs_audio, normalize_audio(audio_raw)


def centered_indices(order):
    n = np.arange(order + 1, dtype=float)
    return n - order / 2.0


def rectangular_window(order):
    return np.ones(order + 1, dtype=float)


def triangular_window(order):
    n = np.arange(order + 1, dtype=float)
    half = (order + 2) / 2.0
    return 1.0 - np.abs((n - order / 2.0) / half)


def bartlett_window(order):
    if order == 0:
        return np.ones(1, dtype=float)
    n = np.arange(order + 1, dtype=float)
    return 1.0 - 2.0 * np.abs(n - order / 2.0) / order


def hamming_window(order):
    n = np.arange(order + 1, dtype=float)
    return 0.54 - 0.46 * np.cos(2.0 * np.pi * n / order)


def hann_window(order):
    n = np.arange(order + 1, dtype=float)
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * n / order)


def blackman_window(order):
    n = np.arange(order + 1, dtype=float)
    return (
        0.42
        - 0.5 * np.cos(2.0 * np.pi * n / order)
        + 0.08 * np.cos(4.0 * np.pi * n / order)
    )


WINDOW_BUILDERS = {
    "retangular": rectangular_window,
    "triangular": triangular_window,
    "bartlett": bartlett_window,
    "hamming": hamming_window,
    "hann": hann_window,
    "blackman": blackman_window,
}


def window_coefficients(name, order):
    try:
        return WINDOW_BUILDERS[name.lower()](order)
    except KeyError as exc:
        valid = ", ".join(sorted(WINDOW_BUILDERS))
        raise ValueError(f"Janela '{name}' invalida. Use uma de: {valid}.") from exc


def ideal_lowpass(fc_hz, order, fs_hz):
    wc = 2.0 * np.pi * fc_hz / fs_hz
    k = centered_indices(order)
    h = np.empty(order + 1, dtype=float)
    zero_mask = np.isclose(k, 0.0)
    h[zero_mask] = wc / np.pi
    nonzero = ~zero_mask
    h[nonzero] = np.sin(wc * k[nonzero]) / (np.pi * k[nonzero])
    return h


def ideal_highpass(fc_hz, order, fs_hz):
    delta = np.isclose(centered_indices(order), 0.0).astype(float)
    return delta - ideal_lowpass(fc_hz, order, fs_hz)


def ideal_bandpass(fc1_hz, fc2_hz, order, fs_hz):
    return ideal_lowpass(fc2_hz, order, fs_hz) - ideal_lowpass(fc1_hz, order, fs_hz)


def ideal_bandstop(fc1_hz, fc2_hz, order, fs_hz):
    delta = np.isclose(centered_indices(order), 0.0).astype(float)
    return delta - ideal_bandpass(fc1_hz, fc2_hz, order, fs_hz)


def q2a_ideal(order):
    k = centered_indices(order)
    h = np.empty(order + 1, dtype=float)
    zero_mask = np.isclose(k, 0.0)
    h[zero_mask] = 0.5
    nonzero = ~zero_mask
    h[nonzero] = (
        np.sin(np.pi * k[nonzero] / 6.0) + np.sin(np.pi * k[nonzero] / 3.0)
    ) / (np.pi * k[nonzero])
    return h


def q2b_ideal(order, omega_c=np.pi / 8.0):
    k = centered_indices(order)
    h = np.empty(order + 1, dtype=float)
    zero_mask = np.isclose(k, 0.0)
    h[zero_mask] = omega_c / np.pi
    nonzero = ~zero_mask
    h[nonzero] = (
        np.sin(omega_c * k[nonzero]) ** 2
        / (np.pi * omega_c * k[nonzero] ** 2)
    )
    return h


def q2c_ideal(order):
    k = centered_indices(order)
    h = np.empty(order + 1, dtype=float)
    zero_mask = np.isclose(k, 0.0)
    h[zero_mask] = 3.0 / 8.0
    nonzero = ~zero_mask
    h[nonzero] = (
        np.sin(np.pi * k[nonzero] / 2.0) / (np.pi * k[nonzero])
        + 4.0 * (np.cos(np.pi * k[nonzero] / 4.0) - 1.0)
        / (np.pi**2 * k[nonzero] ** 2)
    )
    return h


def q2a_magnitude(omega):
    omega = np.asarray(omega, dtype=float)
    return np.where(
        np.abs(omega) <= np.pi / 6.0,
        2.0,
        np.where(np.abs(omega) <= np.pi / 3.0, 1.0, 0.0),
    )


def q2b_magnitude(omega, omega_c=np.pi / 8.0):
    omega = np.asarray(omega, dtype=float)
    inside = np.abs(omega) <= 2.0 * omega_c
    response = np.zeros_like(omega)
    response[inside] = 1.0 - np.abs(omega[inside]) / (2.0 * omega_c)
    return response


def q2c_magnitude(omega):
    omega = np.asarray(omega, dtype=float)
    abs_omega = np.abs(omega)
    response = np.zeros_like(omega)
    ramp = abs_omega <= np.pi / 4.0
    response[ramp] = 4.0 * abs_omega[ramp] / np.pi
    plateau = (abs_omega > np.pi / 4.0) & (abs_omega <= np.pi / 2.0)
    response[plateau] = 1.0
    return response


def apply_window(ideal_response, window_name, order):
    return ideal_response * window_coefficients(window_name, order)


def fir_from_builder(builder, order, window_name, *builder_args, **builder_kwargs):
    ideal_response = builder(order, *builder_args, **builder_kwargs)
    return apply_window(ideal_response, window_name, order)


def magnitude_db(response):
    return 20.0 * np.log10(np.maximum(np.abs(response), 1e-12))


def fir_poles_zeros(coefficients):
    trimmed = np.trim_zeros(np.asarray(coefficients, dtype=float), "f")
    if len(trimmed) <= 1:
        zeros = np.array([], dtype=complex)
        order = max(len(trimmed) - 1, 0)
    else:
        zeros = np.roots(trimmed)
        order = len(trimmed) - 1
    poles = np.zeros(order, dtype=complex)
    return zeros, poles


def response_data(coefficients, worN=8192, fs_hz=None):
    if fs_hz is None:
        omega, response = signal.freqz(coefficients, [1.0], worN=worN)
        return omega, response
    freqs, response = signal.freqz(coefficients, [1.0], worN=worN, fs=fs_hz)
    return freqs, response


def rms_frequency_error(coefficients, ideal_response_fn, worN=8192, fs_hz=None):
    axis, response = response_data(coefficients, worN=worN, fs_hz=fs_hz)
    error = np.abs(response) - ideal_response_fn(axis)
    return float(np.sqrt(np.mean(error**2))), float(np.max(np.abs(error)))


def summarize_error_bank(filters_by_label, ideal_response_fn, worN=8192, fs_hz=None):
    rows = []
    for label, coefficients in filters_by_label.items():
        rms_error, max_error = rms_frequency_error(
            coefficients, ideal_response_fn, worN=worN, fs_hz=fs_hz
        )
        rows.append(
            {
                "Filtro": label,
                "Erro RMS": rms_error,
                "Erro max": max_error,
                "Ganho max": float(np.max(np.abs(response_data(coefficients, worN=worN, fs_hz=fs_hz)[1]))),
            }
        )
    return rows


def _axes_grid(count, ncols=3, figsize=(14, 8)):
    nrows = int(np.ceil(count / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False)
    flat_axes = axes.ravel()
    for ax in flat_axes[count:]:
        ax.axis("off")
    return fig, flat_axes


def plot_impulse_grid(filters_by_label, title, ncols=3, figsize=(15, 8)):
    labels = list(filters_by_label.keys())
    fig, axes = _axes_grid(len(labels), ncols=ncols, figsize=figsize)
    for ax, label in zip(axes, labels):
        coefficients = np.asarray(filters_by_label[label], dtype=float)
        markerline, stemlines, baseline = ax.stem(
            np.arange(len(coefficients)), coefficients, basefmt=" "
        )
        markerline.set_markersize(3)
        stemlines.set_linewidth(1.0)
        ax.set_title(label)
        ax.set_xlabel("n")
        ax.set_ylabel("h[n]")
        ax.grid(True, alpha=0.3)
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def plot_pole_zero_grid(filters_by_label, title, ncols=3, figsize=(15, 8)):
    labels = list(filters_by_label.keys())
    fig, axes = _axes_grid(len(labels), ncols=ncols, figsize=figsize)
    theta = np.linspace(0.0, 2.0 * np.pi, 512)
    unit_x = np.cos(theta)
    unit_y = np.sin(theta)

    for ax, label in zip(axes, labels):
        zeros, poles = fir_poles_zeros(filters_by_label[label])
        ax.plot(unit_x, unit_y, "k--", alpha=0.5)
        if len(zeros):
            ax.scatter(
                zeros.real,
                zeros.imag,
                marker="o",
                facecolors="none",
                edgecolors="tab:blue",
                label="zeros",
            )
        if len(poles):
            ax.scatter(
                poles.real,
                poles.imag,
                marker="x",
                color="tab:red",
                label="polos",
            )
        ax.axhline(0.0, color="0.4", linewidth=0.8)
        ax.axvline(0.0, color="0.4", linewidth=0.8)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title(label)
        ax.grid(True, alpha=0.3)
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def plot_frequency_grid(
    filters_by_label,
    title,
    ncols=3,
    figsize=(15, 8),
    fs_hz=None,
    xlim=None,
    as_db=False,
    ideal_response_fn=None,
):
    labels = list(filters_by_label.keys())
    fig, axes = _axes_grid(len(labels), ncols=ncols, figsize=figsize)
    for ax, label in zip(axes, labels):
        axis, response = response_data(filters_by_label[label], fs_hz=fs_hz)
        y = magnitude_db(response) if as_db else np.abs(response)
        ax.plot(axis, y, linewidth=1.5, label="projetado")
        if ideal_response_fn is not None:
            reference = ideal_response_fn(axis)
            ref_y = magnitude_db(reference) if as_db else reference
            ax.plot(axis, ref_y, "k--", linewidth=1.0, label="ideal")
        ax.set_title(label)
        ax.set_xlabel("Frequencia (Hz)" if fs_hz is not None else r"$\omega$ (rad/amostra)")
        ax.set_ylabel("Magnitude (dB)" if as_db else r"$|H(e^{j\omega})|$")
        if xlim is not None:
            ax.set_xlim(*xlim)
        if as_db:
            ax.set_ylim(-120, 15)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best")
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def build_fir_cascade(filters):
    coefficients = np.array([1.0], dtype=float)
    total_delay = 0
    for fir_filter in filters:
        coefficients = np.convolve(coefficients, fir_filter)
        total_delay += (len(fir_filter) - 1) // 2
    return coefficients, total_delay


def apply_linear_phase_fir(coefficients, signal_in):
    coefficients = np.asarray(coefficients, dtype=float)
    signal_in = np.asarray(signal_in, dtype=float)
    return signal.lfilter(coefficients, [1.0], signal_in)


def align_linear_phase(reference, estimate, delay):
    reference = np.asarray(reference, dtype=float)
    estimate = np.asarray(estimate, dtype=float)
    delay = int(delay)
    if delay <= 0:
        length = min(len(reference), len(estimate))
        return reference[:length], estimate[:length]
    if delay >= len(estimate):
        return reference[:0], estimate[:0]
    length = min(len(reference), len(estimate) - delay)
    return reference[:length], estimate[delay : delay + length]


def restore_length_after_delay(estimate, delay):
    estimate = np.asarray(estimate, dtype=float)
    delay = int(delay)
    if delay <= 0:
        return estimate
    if delay >= len(estimate):
        return np.zeros_like(estimate)
    shifted = estimate[delay:]
    return np.concatenate([shifted, np.zeros(delay, dtype=float)])


def snr_db(reference, estimate):
    reference = np.asarray(reference, dtype=float)
    estimate = np.asarray(estimate, dtype=float)
    error = reference - estimate
    signal_power = np.mean(reference**2)
    noise_power = np.mean(error**2)
    return float(10.0 * np.log10(signal_power / max(noise_power, 1e-20)))


def mse(reference, estimate):
    reference = np.asarray(reference, dtype=float)
    estimate = np.asarray(estimate, dtype=float)
    return float(np.mean((reference - estimate) ** 2))


def residual_power(reference, estimate):
    reference = np.asarray(reference, dtype=float)
    estimate = np.asarray(estimate, dtype=float)
    return float(np.mean((reference - estimate) ** 2))


def spectrum_magnitude(x, fs_hz):
    x = np.asarray(x, dtype=float)
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs_hz)
    magnitude = np.abs(np.fft.rfft(x))
    return freqs, magnitude


def plot_time_and_spectrum(x, fs_hz, title, seconds=0.08, xlim_freq=None):
    x = np.asarray(x, dtype=float)
    sample_count = min(len(x), max(1, int(seconds * fs_hz)))
    t = np.arange(sample_count, dtype=float) / fs_hz
    freqs, magnitude = spectrum_magnitude(x, fs_hz)

    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
    axes[0].plot(t, x[:sample_count])
    axes[0].set_title(f"{title} - tempo")
    axes[0].set_xlabel("Tempo (s)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(freqs, magnitude)
    axes[1].set_title(f"{title} - espectro")
    axes[1].set_xlabel("Frequencia (Hz)")
    axes[1].set_ylabel("|X(f)|")
    if xlim_freq is not None:
        axes[1].set_xlim(*xlim_freq)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def compare_signals(reference, contaminated, estimate, fs_hz, title, seconds=0.08):
    reference = np.asarray(reference, dtype=float)
    contaminated = np.asarray(contaminated, dtype=float)
    estimate = np.asarray(estimate, dtype=float)
    sample_count = min(len(reference), len(contaminated), len(estimate), int(seconds * fs_hz))
    t = np.arange(sample_count, dtype=float) / fs_hz

    freq_ref, mag_ref = spectrum_magnitude(reference, fs_hz)
    freq_cont, mag_cont = spectrum_magnitude(contaminated, fs_hz)
    freq_est, mag_est = spectrum_magnitude(estimate, fs_hz)

    fig, axes = plt.subplots(2, 2, figsize=(14, 7))
    axes[0, 0].plot(t, reference[:sample_count], label="x(t)")
    axes[0, 0].plot(t, contaminated[:sample_count], label="y(t)", alpha=0.7)
    axes[0, 0].set_title(f"{title} - original vs contaminado")
    axes[0, 0].legend()

    axes[0, 1].plot(t, reference[:sample_count], label="x(t)")
    axes[0, 1].plot(t, estimate[:sample_count], label="x_hat(t)", alpha=0.8)
    axes[0, 1].set_title(f"{title} - original vs recuperado")
    axes[0, 1].legend()

    axes[1, 0].plot(freq_ref, mag_ref, label="x(t)")
    axes[1, 0].plot(freq_cont, mag_cont, label="y(t)", alpha=0.7)
    axes[1, 0].set_title("Espectro: original vs contaminado")
    axes[1, 0].set_xlim(0, fs_hz / 2.0)
    axes[1, 0].legend()

    axes[1, 1].plot(freq_ref, mag_ref, label="x(t)")
    axes[1, 1].plot(freq_est, mag_est, label="x_hat(t)", alpha=0.8)
    axes[1, 1].set_title("Espectro: original vs recuperado")
    axes[1, 1].set_xlim(0, fs_hz / 2.0)
    axes[1, 1].legend()

    for ax in axes.ravel():
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def quantize_coefficients(coefficients, bits):
    coefficients = np.asarray(coefficients, dtype=float)
    if bits < 2:
        raise ValueError("Use pelo menos 2 bits para quantizacao assinada.")
    levels = 2 ** (bits - 1) - 1
    scale = float(np.max(np.abs(coefficients)))
    if levels <= 0 or scale == 0.0:
        return np.zeros_like(coefficients)
    normalized = np.clip(coefficients / scale, -1.0, 1.0)
    quantized = np.round(normalized * levels) / levels
    return scale * quantized


def normalize_tf(b, a):
    b = np.asarray(b, dtype=float)
    a = np.asarray(a, dtype=float)
    if abs(a[0]) < 1e-14:
        raise ValueError("a[0] nao pode ser zero.")
    return b / a[0], a / a[0]


def basic_lowpass_iir(fc_hz, fs_hz, r=0.70):
    theta = 2.0 * np.pi * fc_hz / fs_hz
    a = np.array([1.0, -2.0 * r * np.cos(theta), r**2])
    gain = (1.0 - 2.0 * r * np.cos(theta) + r**2) / 4.0
    b = gain * np.array([1.0, 2.0, 1.0])
    return normalize_tf(b, a)


def basic_highpass_iir(fc_hz, fs_hz, r=0.70):
    theta = 2.0 * np.pi * fc_hz / fs_hz
    a = np.array([1.0, -2.0 * r * np.cos(theta), r**2])
    gain = (1.0 + 2.0 * r * np.cos(theta) + r**2) / 4.0
    b = gain * np.array([1.0, -2.0, 1.0])
    return normalize_tf(b, a)


def cascade_iir(blocks):
    b_total = np.array([1.0], dtype=float)
    a_total = np.array([1.0], dtype=float)
    for b, a in blocks:
        b_total = np.convolve(b_total, b)
        a_total = np.convolve(a_total, a)
    return normalize_tf(b_total, a_total)


def ap6_reference_filter(fs_hz, r=0.70):
    return cascade_iir(
        [
            basic_highpass_iir(180.0, fs_hz, r=r),
            basic_lowpass_iir(1800.0, fs_hz, r=r),
        ]
    )
