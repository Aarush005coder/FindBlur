"""FindBlur — Image blur detection engine.

Combines Laplacian variance and FFT high-frequency energy analysis
to produce a three-level sharpness verdict: Sharp, Borderline, or Blurry.
"""

import cv2
import numpy as np
from typing import TypedDict


# --- Result types -----------------------------------------------------------

class DetectionResult(TypedDict):
    laplacian_score: float
    fft_score: float
    laplacian_confidence: float
    fft_confidence: float
    combined_score: float
    confidence: float
    verdict: str  # "sharp", "borderline", "blurry"
    message: str


# --- Sensitivity presets ----------------------------------------------------
# Each preset adjusts the effective threshold and borderline margin.
# The threshold multiplier is applied to the user's base threshold.
# The margin defines how far above/below the threshold counts as borderline.

SENSITIVITY_PRESETS = {
    "Strict": {
        "threshold_multiplier": 1.3,
        "margin": 25,
        "description": "More likely to flag images as blurry.",
    },
    "Balanced": {
        "threshold_multiplier": 1.0,
        "margin": 15,
        "description": "Normal everyday use.",
    },
    "Lenient": {
        "threshold_multiplier": 0.7,
        "margin": 10,
        "description": "More tolerant of low-texture images.",
    },
}

# --- Default weights --------------------------------------------------------
# Laplacian is our main signal because it reacts strongly to the fine edges
# that usually disappear when an image gets blurred.
# FFT catches some cases Laplacian misses, especially smooth-but-sharp scenes.

DEFAULT_LAPLACIAN_WEIGHT = 0.65
DEFAULT_FFT_WEIGHT = 0.35

# --- Normalization references -----------------------------------------------
# Used to map raw scores into a 0-100 confidence range.
# These aren't hard limits — they're reference points for a sigmoid curve.

LAPLACIAN_REF_LOW = 20.0    # Anything below this is almost certainly blurry
LAPLACIAN_REF_HIGH = 500.0  # Anything above this is clearly sharp

FFT_REF_LOW = 5.0
FFT_REF_HIGH = 60.0

# Max dimension for analysis — larger images get resized to keep things fast.
MAX_ANALYSIS_DIM = 1920


# --- Core analysis functions ------------------------------------------------

def _resize_for_analysis(image: np.ndarray) -> np.ndarray:
    """Resize large images for faster analysis while keeping aspect ratio."""
    h, w = image.shape[:2]
    if max(h, w) <= MAX_ANALYSIS_DIM:
        return image
    scale = MAX_ANALYSIS_DIM / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)


def _to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert to grayscale if needed."""
    if len(image.shape) == 2:
        return image
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def calculate_laplacian_variance(image: np.ndarray) -> float:
    """Compute the variance of the Laplacian — our primary blur signal.

    Higher values mean more edges/detail. A perfectly smooth image
    would score near zero.
    """
    gray = _to_grayscale(image)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return float(laplacian.var())


def calculate_fft_score(image: np.ndarray) -> float:
    """Measure high-frequency energy via FFT.

    We shift the spectrum so low frequencies sit in the center,
    then measure how much energy is outside the central region.
    This helps with smooth-but-sharp scenes like skies and walls
    where Laplacian alone might give a misleadingly low score.
    """
    gray = _to_grayscale(image)
    gray_float = gray.astype(np.float64)

    f_transform = np.fft.fft2(gray_float)
    f_shifted = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shifted)

    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2

    # Define the low-frequency region as the central 10% of the image.
    # Everything outside this is "high frequency" for our purposes.
    radius = int(min(rows, cols) * 0.1)

    # Create a mask that blocks the center
    mask = np.ones((rows, cols), dtype=np.float64)
    y, x = np.ogrid[:rows, :cols]
    center_mask = (x - ccol) ** 2 + (y - crow) ** 2 <= radius ** 2
    mask[center_mask] = 0

    high_freq_energy = np.sum(magnitude * mask)
    total_energy = np.sum(magnitude)

    if total_energy == 0:
        return 0.0

    # Return the percentage of energy in high frequencies.
    # Multiply by 100 to get a more readable number.
    ratio = (high_freq_energy / total_energy) * 100.0
    return float(ratio)


# --- Normalization ----------------------------------------------------------

def _sigmoid_normalize(value: float, ref_low: float, ref_high: float) -> float:
    """Map a raw score to 0-100 using a smooth sigmoid-like curve.

    This gives us a more intuitive confidence value than raw clamping.
    Scores near ref_low map close to 0, scores near ref_high map close to 100.
    """
    midpoint = (ref_low + ref_high) / 2.0
    spread = (ref_high - ref_low) / 2.0
    if spread == 0:
        return 50.0
    x = (value - midpoint) / (spread / 3.0)  # ±3 standard deviations
    sigmoid = 1.0 / (1.0 + np.exp(-x))
    return float(sigmoid * 100.0)


def normalize_laplacian_score(raw_score: float) -> float:
    """Convert raw Laplacian variance to a 0-100 confidence."""
    return _sigmoid_normalize(raw_score, LAPLACIAN_REF_LOW, LAPLACIAN_REF_HIGH)


def normalize_fft_score(raw_score: float) -> float:
    """Convert raw FFT ratio to a 0-100 confidence."""
    return _sigmoid_normalize(raw_score, FFT_REF_LOW, FFT_REF_HIGH)


def _threshold_to_confidence(threshold: float) -> float:
    """Map the user's Laplacian threshold slider (0-1000) to confidence space.

    We use a power curve so the slider feels intuitive:
    - 0 → 0 (everything passes)
    - 100 (default) → ~45 (balanced midpoint)
    - 500 → ~85
    - 1000 → 100 (almost nothing passes)

    The power of 0.55 was chosen so 100/1000 ≈ 0.1 → 0.1^0.55 ≈ 0.32,
    then scaled by 100 and slightly adjusted.
    """
    clamped = max(0.0, min(1000.0, threshold))
    # Normalize to 0-1
    t = clamped / 1000.0
    # Power curve — gives a nice spread where the default (0.1) maps to ~45
    return float(t ** 0.55 * 100.0)


# --- Combined scoring -------------------------------------------------------

def calculate_combined_score(
    laplacian_confidence: float,
    fft_confidence: float,
    laplacian_weight: float = DEFAULT_LAPLACIAN_WEIGHT,
    fft_weight: float = DEFAULT_FFT_WEIGHT,
) -> float:
    """Weighted combination of normalized confidence values."""
    return (laplacian_confidence * laplacian_weight) + (fft_confidence * fft_weight)


# --- Settings ---------------------------------------------------------------

def get_effective_settings(
    base_threshold: float,
    sensitivity: str = "Balanced",
) -> dict:
    """Return the effective threshold and margin for the current sensitivity."""
    preset = SENSITIVITY_PRESETS.get(sensitivity, SENSITIVITY_PRESETS["Balanced"])
    effective_threshold = base_threshold * preset["threshold_multiplier"]
    margin = preset["margin"]
    return {
        "effective_threshold": effective_threshold,
        "margin": margin,
        "sensitivity": sensitivity,
        "description": preset["description"],
    }


# --- Classification ---------------------------------------------------------

def classify_blur(
    combined_score: float,
    effective_threshold: float,
    margin: float,
) -> tuple[str, str]:
    """Three-level verdict based on combined confidence score.

    Returns (verdict, message).
    """
    upper = effective_threshold + margin
    lower = effective_threshold - margin

    if combined_score >= upper:
        return "sharp", "Strong detail detected."
    elif combined_score >= lower:
        return "borderline", "Needs a second look."
    else:
        return "blurry", "Not enough fine detail detected."


# --- Visualization ----------------------------------------------------------

def generate_edge_map(image: np.ndarray) -> np.ndarray:
    """Produce a Canny edge map for diagnostic display."""
    gray = _to_grayscale(image)
    # Auto-threshold using the median — works reasonably for most photos.
    median_val = np.median(gray)
    lower = int(max(0, 0.66 * median_val))
    upper = int(min(255, 1.33 * median_val))
    edges = cv2.Canny(gray, lower, upper)
    return edges


def generate_laplacian_heatmap(image: np.ndarray) -> np.ndarray:
    """Create a heatmap showing where the Laplacian response is strongest.

    This is purely diagnostic — it shows where FindBlur found detail,
    not what the final verdict is.
    """
    gray = _to_grayscale(image)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    abs_lap = np.abs(laplacian)

    # Normalize to 0-255 for display
    if abs_lap.max() > 0:
        normalized = (abs_lap / abs_lap.max() * 255).astype(np.uint8)
    else:
        normalized = np.zeros_like(gray, dtype=np.uint8)

    # Apply a color map — INFERNO reads well in both light and dark themes
    heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_INFERNO)
    heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    return heatmap_rgb


# --- Main analysis entry point ----------------------------------------------

def analyze_image(
    image: np.ndarray,
    threshold: float = 100.0,
    sensitivity: str = "Balanced",
    laplacian_weight: float = DEFAULT_LAPLACIAN_WEIGHT,
    fft_weight: float = DEFAULT_FFT_WEIGHT,
) -> DetectionResult:
    """Run the full detection pipeline on a single image.

    This is the main function that app.py should call.
    It resizes, analyzes, normalizes, combines, and classifies.
    """
    # Resize for analysis speed — the original stays untouched for display.
    analysis_img = _resize_for_analysis(image)

    # Raw scores
    lap_raw = calculate_laplacian_variance(analysis_img)
    fft_raw = calculate_fft_score(analysis_img)

    # Normalize to comparable confidence values
    lap_conf = normalize_laplacian_score(lap_raw)
    fft_conf = normalize_fft_score(fft_raw)

    # Combine
    combined = calculate_combined_score(lap_conf, fft_conf, laplacian_weight, fft_weight)

    # Get effective settings for the current sensitivity mode
    settings = get_effective_settings(threshold, sensitivity)
    effective_threshold = settings["effective_threshold"]
    margin = settings["margin"]

    # Convert the effective threshold from raw Laplacian scale to confidence
    # scale so it's comparable with the combined score.
    effective_conf_threshold = _threshold_to_confidence(effective_threshold)

    # Classify
    verdict, message = classify_blur(combined, effective_conf_threshold, margin)

    # Confidence as a 0-100 percentage
    confidence = min(100.0, max(0.0, combined))

    return DetectionResult(
        laplacian_score=round(lap_raw, 1),
        fft_score=round(fft_raw, 1),
        laplacian_confidence=round(lap_conf, 1),
        fft_confidence=round(fft_conf, 1),
        combined_score=round(combined, 1),
        confidence=round(confidence, 1),
        verdict=verdict,
        message=message,
    )
