from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


plt.style.use("seaborn-v0_8-whitegrid")

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "report_assets"
ASSETS_DIR.mkdir(exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fir_utils import (  # noqa: E402
    align_linear_phase,
    ap6_reference_filter,
    apply_linear_phase_fir,
    apply_window,
    build_fir_cascade,
    ideal_bandpass,
    ideal_bandstop,
    ideal_highpass,
    ideal_lowpass,
    load_handel_audio,
    mse,
    q2a_ideal,
    q2a_magnitude,
    q2b_ideal,
    q2b_magnitude,
    q2c_ideal,
    q2c_magnitude,
    quantize_coefficients,
    residual_power,
    response_data,
    restore_length_after_delay,
    rms_frequency_error,
    snr_db,
    spectrum_magnitude,
)


FS = 20000.0
Q1_WINDOWS = ["retangular", "triangular", "bartlett", "hamming", "hann", "blackman"]
Q2_WINDOWS = ["retangular", "triangular", "hamming", "hann", "blackman"]
COLORS = {
    "retangular": "#1f77b4",
    "triangular": "#ff7f0e",
    "bartlett": "#2ca02c",
    "hamming": "#d62728",
    "hann": "#9467bd",
    "blackman": "#8c564b",
}


def format_br(value, digits=4):
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    return f"{value:.{digits}f}".replace(".", ",")


def ideal_lp_mag(freqs_hz, fc_hz):
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    return np.where(freqs_hz <= fc_hz, 1.0, 0.0)


def ideal_hp_mag(freqs_hz, fc_hz):
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    return np.where(freqs_hz >= fc_hz, 1.0, 0.0)


def ideal_bp_mag(freqs_hz, fc1_hz, fc2_hz):
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    return np.where((freqs_hz >= fc1_hz) & (freqs_hz <= fc2_hz), 1.0, 0.0)


def ideal_bs_mag(freqs_hz, fc1_hz, fc2_hz):
    freqs_hz = np.asarray(freqs_hz, dtype=float)
    return np.where((freqs_hz >= fc1_hz) & (freqs_hz <= fc2_hz), 0.0, 1.0)


def q1_cases():
    return [
        (
            "Passa-baixas 1000 Hz",
            lambda order: ideal_lowpass(1000.0, order, FS),
            lambda freqs_hz: ideal_lp_mag(freqs_hz, 1000.0),
            (0.0, 4000.0),
        ),
        (
            "Passa-altas 2000 Hz",
            lambda order: ideal_highpass(2000.0, order, FS),
            lambda freqs_hz: ideal_hp_mag(freqs_hz, 2000.0),
            (0.0, 6000.0),
        ),
        (
            "Passa-faixas 500-2000 Hz",
            lambda order: ideal_bandpass(500.0, 2000.0, order, FS),
            lambda freqs_hz: ideal_bp_mag(freqs_hz, 500.0, 2000.0),
            (0.0, 5000.0),
        ),
        (
            "Rejeita-faixas 1000-2500 Hz",
            lambda order: ideal_bandstop(1000.0, 2500.0, order, FS),
            lambda freqs_hz: ideal_bs_mag(freqs_hz, 1000.0, 2500.0),
            (0.0, 5000.0),
        ),
    ]


def q2_cases():
    omega_c = np.pi / 8.0
    return [
        ("Item (a)", q2a_ideal, q2a_magnitude),
        (
            "Item (b)",
            lambda order: q2b_ideal(order, omega_c=omega_c),
            lambda omega: q2b_magnitude(omega, omega_c=omega_c),
        ),
        ("Item (c)", q2c_ideal, q2c_magnitude),
    ]


def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def plot_q1_responses():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (title, builder, _, xlim) in zip(axes.ravel(), q1_cases()):
        for window_name in Q1_WINDOWS:
            coefficients = apply_window(builder(100), window_name, 100)
            freqs, response = response_data(coefficients, fs_hz=FS)
            ax.plot(freqs, 20.0 * np.log10(np.maximum(np.abs(response), 1e-8)), label=window_name, color=COLORS[window_name])
        ax.set_title(title)
        ax.set_xlim(*xlim)
        ax.set_ylim(-120, 10)
        ax.set_xlabel("Frequencia (Hz)")
        ax.set_ylabel("Magnitude (dB)")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)
    savefig(ASSETS_DIR / "q1_responses_m100.png")


def plot_q1_pz():
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    theta = np.linspace(0.0, 2.0 * np.pi, 512)
    for ax, (title, builder, _, _) in zip(axes.ravel(), q1_cases()):
        coefficients = apply_window(builder(100), "blackman", 100)
        zeros = np.roots(coefficients)
        poles = np.zeros(len(coefficients) - 1, dtype=complex)
        ax.plot(np.cos(theta), np.sin(theta), "k--", alpha=0.45)
        ax.scatter(zeros.real, zeros.imag, facecolors="none", edgecolors="#1f77b4", s=18, label="zeros")
        if len(poles):
            ax.scatter(poles.real, poles.imag, marker="x", color="#d62728", s=18, label="polos")
        ax.axhline(0.0, color="0.4", linewidth=0.8)
        ax.axvline(0.0, color="0.4", linewidth=0.8)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title)
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8, loc="upper right")
    savefig(ASSETS_DIR / "q1_pz_blackman_m100.png")


def write_q1_table():
    rows = []
    for title, builder, ideal_fn, _ in q1_cases():
        row = [title]
        for order in [20, 50, 100]:
            coefficients = apply_window(builder(order), "blackman", order)
            rms_error, _ = rms_frequency_error(coefficients, ideal_fn, fs_hz=FS)
            row.append(rms_error)
        rows.append(row)

    lines = [
        "\\begin{tabular}{lccc}",
        "\\toprule",
        "Filtro & $M=20$ & $M=50$ & $M=100$ \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{row[0]} & {format_br(row[1])} & {format_br(row[2])} & {format_br(row[3])} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    (ASSETS_DIR / "table_q1_blackman.tex").write_text("\n".join(lines), encoding="utf-8")


def plot_q2_responses():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    omega = np.linspace(0.0, np.pi, 4096)
    for ax, (title, builder, ideal_fn) in zip(axes, q2_cases()):
        ax.plot(omega, ideal_fn(omega), "k--", linewidth=2.0, label="ideal")
        for window_name in Q2_WINDOWS:
            coefficients = apply_window(builder(100), window_name, 100)
            w, response = response_data(coefficients, fs_hz=None)
            ax.plot(w, np.abs(response), label=window_name, color=COLORS[window_name])
        ax.set_title(title)
        ax.set_xlim(0.0, np.pi)
        ax.set_ylim(0.0, 2.2)
        ax.set_xlabel(r"$\omega$ (rad/amostra)")
        ax.set_ylabel(r"$|H(e^{j\omega})|$")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)
    savefig(ASSETS_DIR / "q2_responses_m100.png")


def write_q2_table():
    rows = []
    for title, builder, ideal_fn in q2_cases():
        best_50 = None
        best_100 = None
        for window_name in Q2_WINDOWS:
            coeff_50 = apply_window(builder(50), window_name, 50)
            coeff_100 = apply_window(builder(100), window_name, 100)
            rms_50, _ = rms_frequency_error(coeff_50, ideal_fn, fs_hz=None)
            rms_100, _ = rms_frequency_error(coeff_100, ideal_fn, fs_hz=None)
            if best_50 is None or rms_50 < best_50[1]:
                best_50 = (window_name, rms_50)
            if best_100 is None or rms_100 < best_100[1]:
                best_100 = (window_name, rms_100)
        rows.append((title, best_50[0], best_50[1], best_100[0], best_100[1]))

    lines = [
        "\\begin{tabular}{lcccc}",
        "\\toprule",
        "Caso & Melhor janela, $M=50$ & Erro RMS & Melhor janela, $M=100$ & Erro RMS \\\\",
        "\\midrule",
    ]
    for title, w50, e50, w100, e100 in rows:
        lines.append(
            f"{title} & {w50} & {format_br(e50)} & {w100} & {format_br(e100)} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    (ASSETS_DIR / "table_q2_best.tex").write_text("\n".join(lines), encoding="utf-8")


def audio_setup():
    fs_audio, x = load_handel_audio(ROOT.parent / "data")
    t = np.arange(len(x), dtype=float) / fs_audio
    rng = np.random.default_rng(2026)
    sigma_values = [1e-2, 1e-1, 1.0]
    contaminated = {}
    for sigma2 in sigma_values:
        contaminated[sigma2] = (
            x
            + 0.05 * np.cos(200.0 * np.pi * t)
            + 0.075 * np.sin(4000.0 * np.pi * t)
            + rng.normal(0.0, np.sqrt(sigma2), size=len(x))
        )
    hp_fir = apply_window(ideal_highpass(180.0, 120, fs_audio), "blackman", 120)
    bs_fir = apply_window(ideal_bandstop(1850.0, 2150.0, 260, fs_audio), "blackman", 260)
    lp_fir = apply_window(ideal_lowpass(2400.0, 100, fs_audio), "blackman", 100)
    fir_system, fir_delay = build_fir_cascade([hp_fir, bs_fir, lp_fir])
    b_iir, a_iir = ap6_reference_filter(fs_audio, r=0.70)
    return fs_audio, x, contaminated, fir_system, fir_delay, b_iir, a_iir


def plot_q3_system_response(fs_audio, fir_system, b_iir, a_iir):
    fig, ax = plt.subplots(figsize=(10, 4))
    f_fir, h_fir = response_data(fir_system, fs_hz=fs_audio)
    f_iir, h_iir = signal.freqz(b_iir, a_iir, worN=8192, fs=fs_audio)
    ax.plot(f_fir, 20.0 * np.log10(np.maximum(np.abs(h_fir), 1e-8)), linewidth=2.0, label="FIR AP7")
    ax.plot(f_iir, 20.0 * np.log10(np.maximum(np.abs(h_iir), 1e-8)), linewidth=1.7, label="IIR AP6")
    ax.set_xlim(0.0, fs_audio / 2.0)
    ax.set_ylim(-120, 15)
    ax.set_xlabel("Frequencia (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("Resposta em frequencia do sistema de filtragem")
    ax.grid(True, alpha=0.25)
    ax.legend()
    savefig(ASSETS_DIR / "q3_system_response.png")


def plot_q3_compare(fs_audio, x, contaminated, fir_system, fir_delay):
    sigma2 = 1e-1
    y = contaminated[sigma2]
    fir_raw = apply_linear_phase_fir(fir_system, y)
    x_hat = restore_length_after_delay(fir_raw, fir_delay)

    sample_count = min(len(x), len(y), len(x_hat), int(0.08 * fs_audio))
    time_axis = np.arange(sample_count, dtype=float) / fs_audio
    freq_x, mag_x = spectrum_magnitude(x, fs_audio)
    freq_y, mag_y = spectrum_magnitude(y, fs_audio)
    freq_hat, mag_hat = spectrum_magnitude(x_hat, fs_audio)

    fig, axes = plt.subplots(2, 2, figsize=(12, 6.5))
    axes[0, 0].plot(time_axis, x[:sample_count], label="x(t)")
    axes[0, 0].plot(time_axis, y[:sample_count], label="y(t)", alpha=0.75)
    axes[0, 0].set_title("Tempo: original vs contaminado")
    axes[0, 0].legend()

    axes[0, 1].plot(time_axis, x[:sample_count], label="x(t)")
    axes[0, 1].plot(time_axis, x_hat[:sample_count], label=r"$\hat{x}(t)$", alpha=0.8)
    axes[0, 1].set_title("Tempo: original vs recuperado")
    axes[0, 1].legend()

    axes[1, 0].plot(freq_x, mag_x, label="x(t)")
    axes[1, 0].plot(freq_y, mag_y, label="y(t)", alpha=0.75)
    axes[1, 0].set_xlim(0.0, fs_audio / 2.0)
    axes[1, 0].set_title("Espectro: original vs contaminado")
    axes[1, 0].legend()

    axes[1, 1].plot(freq_x, mag_x, label="x(t)")
    axes[1, 1].plot(freq_hat, mag_hat, label=r"$\hat{x}(t)$", alpha=0.8)
    axes[1, 1].set_xlim(0.0, fs_audio / 2.0)
    axes[1, 1].set_title("Espectro: original vs recuperado")
    axes[1, 1].legend()

    for ax in axes.ravel():
        ax.grid(True, alpha=0.25)

    savefig(ASSETS_DIR / "q3_compare_sigma_0_1.png")


def write_q3_metrics_table(x, contaminated, fir_system, fir_delay, b_iir, a_iir):
    lines = [
        "\\begin{tabular}{lcccccc}",
        "\\toprule",
        "$\\sigma^2$ & SNR entrada (dB) & FIR SNR (dB) & FIR MSE & FIR pot. residual & IIR SNR (dB) & IIR MSE \\\\",
        "\\midrule",
    ]
    for sigma2 in [1e-2, 1e-1, 1.0]:
        y = contaminated[sigma2]
        fir_raw = apply_linear_phase_fir(fir_system, y)
        x_ref_fir, x_hat_fir = align_linear_phase(x, fir_raw, fir_delay)
        iir_raw = signal.lfilter(b_iir, a_iir, y)
        lines.append(
            " & ".join(
                [
                    format_br(sigma2, digits=2).rstrip("0").rstrip(","),
                    format_br(snr_db(x, y)),
                    format_br(snr_db(x_ref_fir, x_hat_fir)),
                    format_br(mse(x_ref_fir, x_hat_fir)),
                    format_br(residual_power(x_ref_fir, x_hat_fir)),
                    format_br(snr_db(x, iir_raw)),
                    format_br(mse(x, iir_raw)),
                ]
            )
            + " \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    (ASSETS_DIR / "table_q3_metrics.tex").write_text("\n".join(lines), encoding="utf-8")


def plot_q3_quantized_response(fs_audio, fir_system):
    fig, ax = plt.subplots(figsize=(10, 4))
    labels = ["float", "2 bits", "4 bits", "8 bits", "16 bits"]
    filters = {"float": fir_system}
    for bits in [2, 4, 8, 16]:
        filters[f"{bits} bits"] = quantize_coefficients(fir_system, bits)
    for label in labels:
        freqs, response = response_data(filters[label], fs_hz=fs_audio)
        ax.plot(freqs, 20.0 * np.log10(np.maximum(np.abs(response), 1e-8)), linewidth=1.6, label=label)
    ax.set_xlim(0.0, fs_audio / 2.0)
    ax.set_ylim(-120, 15)
    ax.set_xlabel("Frequencia (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("Resposta em frequencia do sistema FIR quantizado")
    ax.grid(True, alpha=0.25)
    ax.legend()
    savefig(ASSETS_DIR / "q3_quantized_response.png")


def write_q3_quant_table(x, contaminated, fir_system, fir_delay):
    y = contaminated[1e-1]
    lines = [
        "\\begin{tabular}{lcccc}",
        "\\toprule",
        "Filtro & SNR saida (dB) & MSE & Pot. residual & Coef. nao nulos \\\\",
        "\\midrule",
    ]
    filters = {"float": fir_system}
    for bits in [2, 4, 8, 16]:
        filters[f"{bits} bits"] = quantize_coefficients(fir_system, bits)

    for label, coefficients in filters.items():
        filtered = apply_linear_phase_fir(coefficients, y)
        x_ref, x_hat = align_linear_phase(x, filtered, fir_delay)
        lines.append(
            f"{label} & {format_br(snr_db(x_ref, x_hat))} & {format_br(mse(x_ref, x_hat))} & "
            f"{format_br(residual_power(x_ref, x_hat))} & {int(np.count_nonzero(coefficients))} \\\\"
        )

    lines += ["\\bottomrule", "\\end{tabular}"]
    (ASSETS_DIR / "table_q3_quant.tex").write_text("\n".join(lines), encoding="utf-8")


def main():
    plot_q1_responses()
    plot_q1_pz()
    write_q1_table()
    plot_q2_responses()
    write_q2_table()

    fs_audio, x, contaminated, fir_system, fir_delay, b_iir, a_iir = audio_setup()
    plot_q3_system_response(fs_audio, fir_system, b_iir, a_iir)
    plot_q3_compare(fs_audio, x, contaminated, fir_system, fir_delay)
    write_q3_metrics_table(x, contaminated, fir_system, fir_delay, b_iir, a_iir)
    plot_q3_quantized_response(fs_audio, fir_system)
    write_q3_quant_table(x, contaminated, fir_system, fir_delay)


if __name__ == "__main__":
    main()
