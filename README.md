# FindBlur

**Know before you post.**

FindBlur is a desktop-style image sharpness detection tool. It combines edge-detail analysis (Laplacian variance) with frequency analysis (FFT) to give you a second opinion on image quality.

## Features

- **Single Check** — Analyze a single image for blur with detailed diagnostics
- **Batch Check** — Process multiple images at once with sortable, filterable results
- **Live Camera** — Capture and analyze images directly from your webcam
- **Visual Analysis** — Edge maps and Laplacian heatmaps show where detail was detected
- **Three-Level Verdict** — Sharp, Borderline, or Blurry — not just a binary answer
- **Adjustable Sensitivity** — Strict, Balanced, or Lenient detection modes
- **Manual Review** — Mark results as Correct or Disagree during your session
- **CSV Export** — Download batch results for further analysis

## Setup

Requires Python 3.11+

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

```
FindBlur/
├── app.py              # Streamlit UI and application flow
├── blur_detector.py    # All image-analysis logic
├── requirements.txt
├── README.md
├── assets/
│   └── logo.png
└── .streamlit/
    └── config.toml
```

## How It Works

FindBlur looks at tiny changes in brightness around edges. Sharp photos usually contain more fine detail, which produces a stronger Laplacian response. We also check high-frequency detail using FFT. Both signals are combined before deciding whether an image looks sharp, borderline, or blurry.

## Privacy

All processing happens locally. No images leave your machine.
