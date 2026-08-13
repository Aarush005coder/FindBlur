# 🔎 FindBlur

<div align="center">

<img src="assets/logo.png" alt="FindBlur Logo" width="130">

# FIND<span>BLUR</span>

### Know before you post.

**A practical computer-vision tool for detecting image blur and sharpness.**

FindBlur combines **Laplacian Variance** with **FFT-based frequency analysis** to evaluate image detail and classify images as **Sharp, Borderline, or Blurry**.

<br>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-FindBlur-2ea44f?style=for-the-badge)](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Aarush005coder/FindBlur)

<br><br>

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

</div>

---

## 🚀 Live Demo

Try FindBlur directly in your browser:

### [Open FindBlur →](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)

No installation is required for the deployed version.

> **Know before you post.**

---

# 📌 Overview

**FindBlur** is a lightweight image sharpness detection application built with **Python, OpenCV, NumPy, Pandas, and Streamlit**.

It is designed to answer one simple question:

> **Is this image sharp enough to use or publish?**

Instead of depending on a single blur metric, FindBlur combines two independent signals:

- **Laplacian Variance** — measures edge and fine-detail strength.
- **FFT Analysis** — measures high-frequency information.

The results are normalized, weighted, and combined into a final score.

The application then classifies the image into three practical categories:

| Verdict | Meaning |
|---|---|
| 🟢 **Sharp** | Strong image detail detected |
| 🟡 **Borderline** | Close to the threshold — manual review recommended |
| 🔴 **Blurry** | Low detail detected |

---

# ✨ Features

### 🔍 Dual-Metric Detection

FindBlur combines:

```text
Laplacian Variance
        +
FFT High-Frequency Analysis
        ↓
Combined Detection Score
        ↓
Final Verdict
```

This provides a second signal instead of relying entirely on one measurement.

---

### 🎯 Three-Level Classification

Rather than forcing every image into a binary result:

```text
Sharp / Blurry
```

FindBlur uses:

```text
🟢 Sharp
🟡 Borderline
🔴 Blurry
```

The **Borderline** category is especially useful for images with naturally low texture.

---

### ⚙️ Adjustable Threshold

Detection can be tuned from the sidebar.

Users can adjust:

- Laplacian threshold
- Sensitivity
- Borderline margin
- Laplacian weight
- FFT weight

The threshold is configurable instead of being permanently hardcoded.

---

### 🎚️ Sensitivity Modes

Choose between:

| Mode | Description |
|---|---|
| 🔴 **Strict** | More aggressive blur detection |
| 🟡 **Balanced** | General-purpose detection |
| 🟢 **Lenient** | More tolerant of low-texture images |

---

### 🖼️ Single Image Analysis

Upload:

- JPG
- JPEG
- PNG
- WEBP

The result includes:

- Original image
- Detail map
- Edge map
- Laplacian score
- FFT energy
- Combined score
- Confidence
- Final verdict
- Detection breakdown

---

### 📁 Batch Image Analysis

Analyze multiple images in one session.

Batch mode provides:

- Multiple image uploads
- Processing progress
- Image thumbnails
- Individual scores
- Verdict filtering
- Sorting
- Manual review
- CSV export

---

### 📷 Live Camera Detection

Use your browser camera to capture an image and analyze it immediately.

```text
Camera
   ↓
Capture
   ↓
Analyze
   ↓
Calculate Sharpness
   ↓
Verdict
```

Useful for quickly checking images without saving them first.

---

### 🧪 Visual Diagnostics

FindBlur provides more than just a number.

The application generates:

- Laplacian detail maps
- Canny edge maps
- Original image comparison

This helps users understand where image detail is being detected.

---

### 📝 Manual Review

Automated detection isn't perfect.

FindBlur allows users to manually review results:

```text
✅ Correct
⚠️ Disagree
○ Not Reviewed
```

Review information is maintained within the current Streamlit session.

No database is required.

---

### 📊 CSV Export

Batch results can be exported for further analysis.

Example fields include:

```text
Filename
Laplacian Score
FFT Score
Combined Score
Verdict
Review Status
```

---

# 🔬 How FindBlur Works

## 1. Laplacian Variance

The primary blur metric is calculated using:

```python
cv2.Laplacian(gray, cv2.CV_64F).var()
```

The Laplacian responds strongly to rapid changes in image intensity.

These changes commonly occur around:

- Edges
- Object boundaries
- Fine textures
- Small details

Generally:

```text
Higher Laplacian Variance
        ↓
More edge/detail information
        ↓
Potentially sharper image
```

while:

```text
Lower Laplacian Variance
        ↓
Less fine detail
        ↓
Potentially blurrier image
```

---

## 2. FFT Analysis

FindBlur also performs **Fast Fourier Transform (FFT)** analysis.

FFT allows the application to examine frequency information within the image.

High-frequency components are generally associated with:

- Fine details
- Edges
- Rapid intensity changes
- Textures

This creates a second signal that can be compared with the Laplacian result.

---

## 3. Score Combination

The two metrics are normalized before being combined.

Conceptually:

```text
              INPUT IMAGE
                   │
          ┌────────┴────────┐
          ▼                 ▼
     LAPLACIAN              FFT
          │                 │
          ▼                 ▼
    Edge / Detail      Frequency Detail
          │                 │
          └────────┬────────┘
                   ▼
              Normalization
                   │
                   ▼
            Weighted Combination
                   │
                   ▼
             Combined Score
                   │
                   ▼
            Threshold Check
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    🟢 Sharp   🟡 Borderline  🔴 Blurry
```

The default configuration gives more weight to Laplacian analysis while using FFT as a supporting signal.

---

# 🎯 Why the Borderline Result Matters

A low Laplacian score does not always mean an image is blurry.

For example:

- Blue skies
- Plain walls
- Smooth backgrounds
- Minimal-detail scenes

can naturally produce fewer strong edges.

That's why FindBlur uses a **Borderline** zone.

Instead of:

```text
Below threshold → Blurry
Above threshold → Sharp
```

the system uses:

```text
Below threshold
      ↓
🔴 Blurry

Near threshold
      ↓
🟡 Borderline

Clearly above threshold
      ↓
🟢 Sharp
```

This gives the user a chance to make the final decision.

---

# 🖥️ Application Preview

## 🔍 Single Image Check

Upload an image and inspect the detection result, metrics, and visual diagnostics.

<p align="center">
  <img src="docs/single-check.png" alt="FindBlur Single Image Check" width="900">
</p>

---

## 📁 Batch Analysis

Analyze multiple images, sort and filter results, manually review classifications, and export results as CSV.

<p align="center">
  <img src="docs/batch-check.png" alt="FindBlur Batch Analysis" width="900">
</p>

---

## 📷 Live Camera

Capture an image directly through your browser and analyze its sharpness.

<p align="center">
  <img src="docs/live-camera.png" alt="FindBlur Live Camera Detection" width="900">
</p>

---

## ⚙️ Detection Settings

Fine-tune sensitivity, threshold, and the contribution of Laplacian and FFT analysis.

<p align="center">
  <img src="docs/settings.png" alt="FindBlur Detection Settings" width="900">
</p>

---

# 🏗️ Architecture

FindBlur keeps the UI and detection engine separated.

```text
                         FindBlur
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
           app.py                  blur_detector.py
              │                           │
              │                    Detection Engine
              │                           │
              │              ┌────────────┴────────────┐
              │              │                         │
              │              ▼                         ▼
              │         Laplacian                    FFT
              │              │                         │
              │              └────────────┬────────────┘
              │                           │
              │                           ▼
              │                    Score Combination
              │                           │
              └───────────────────────────┤
                                          ▼
                                      Verdict
```

### `app.py`

Responsible for:

- Streamlit layout
- Tabs
- Sidebar controls
- Image uploads
- Camera input
- Batch processing
- Result rendering
- CSV download

### `blur_detector.py`

Responsible for:

- Image preprocessing
- Laplacian calculation
- FFT analysis
- Score normalization
- Weighted scoring
- Verdict classification
- Confidence calculation

Keeping these responsibilities separate makes the project easier to maintain and extend.

---

# 📂 Project Structure

```text
FindBlur/
│
├── app.py
│
├── blur_detector.py
│
├── requirements.txt
│
├── README.md
│
├── assets/
│   └── logo.png
│
├── docs/
│   ├── single-check.png
│   ├── batch-check.png
│   ├── live-camera.png
│   └── settings.png
│
└── .streamlit/
    └── config.toml
```

---

# 🛠️ Tech Stack

<div align="center">

| Technology | Role |
|---|---|
| 🐍 **Python** | Core application logic |
| 🎈 **Streamlit** | Interactive web interface |
| 👁️ **OpenCV** | Image processing and computer vision |
| 🔢 **NumPy** | Numerical operations and FFT |
| 🐼 **Pandas** | Batch results and CSV export |
| 🖼️ **Pillow** | Image handling |
| 📊 **Matplotlib** | Visualization and diagnostic maps |

</div>

---

# ⚡ Getting Started

## Prerequisites

Make sure you have:

- Python 3.11+
- Git
- A modern web browser

---

## 1. Clone the Repository

```bash
git clone https://github.com/Aarush005coder/FindBlur.git
cd FindBlur
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run FindBlur

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

# 📦 Dependencies

The project uses:

```text
streamlit
opencv-python-headless
numpy
pandas
Pillow
matplotlib
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

# ☁️ Deployment

FindBlur is deployed using **Streamlit Community Cloud**.

The deployment flow is:

```text
Local Development
       │
       ▼
     Git
       │
       ▼
    GitHub
       │
       ▼
Streamlit Cloud
       │
       ▼
  Live Application
```

### 🌐 Live Application

**FindBlur:**  
https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/

---

# 🔐 Privacy

FindBlur is designed as a local/session-based image analysis application.

Images are processed for analysis within the application session and are not intentionally stored in a project database.

Avoid uploading sensitive or private images when using any publicly hosted application.

---

# ⚠️ Limitations

FindBlur is focused specifically on **image sharpness and blur detection**.

It is not a complete image-quality assessment system.

Some situations can be difficult to classify automatically:

- Intentional artistic blur
- Motion blur
- Very low-texture images
- Plain walls
- Clear skies
- Extremely noisy images
- Very small images
- Naturally low-detail scenes
- Different camera characteristics
- Different image resolutions

For these cases, a **Borderline** result should be treated as a prompt for manual review rather than an absolute decision.

---

# 🔮 Future Improvements

Potential improvements include:

- [ ] Region-based blur detection
- [ ] Motion-blur detection
- [ ] Focus-area detection
- [ ] Resolution-aware threshold calibration
- [ ] Automatic threshold calibration
- [ ] Image-quality history
- [ ] PDF report generation
- [ ] Benchmark dataset
- [ ] Detection performance evaluation
- [ ] Automated test suite
- [ ] More robust low-texture detection
- [ ] Large-batch optimization
- [ ] Additional image-quality metrics

---

# 🧪 Testing

When making changes to the detection engine, test against different image categories:

```text
Sharp Images
     │
     ├── High-detail scenes
     ├── Text
     └── Objects with strong edges

Blurry Images
     │
     ├── Defocused photos
     ├── Motion blur
     └── Soft-focus images

Difficult Cases
     │
     ├── Clear sky
     ├── Plain walls
     ├── Low-texture scenes
     └── Noisy images
```

The goal is not only to produce high scores for sharp images, but also to reduce false positives on naturally low-detail scenes.

---

# 🤝 Contributing

Contributions and suggestions are welcome.

### Create a feature branch

```bash
git checkout -b feature/your-feature
```

### Make your changes

Run the application locally:

```bash
streamlit run app.py
```

### Commit your changes

```bash
git add .
git commit -m "Add your feature"
```

### Push the branch

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project is released under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Developer

<div align="center">

### FindBlur

**Built with Python, OpenCV, NumPy & Streamlit.**

A practical computer-vision project for evaluating image sharpness before publishing.

<br>

[🚀 Live Demo](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)  
[💻 GitHub Repository](https://github.com/Aarush005coder/FindBlur)

</div>

---

<div align="center">

## 🔎 FindBlur

### Know before you post.

**Stop guessing. Start checking.**

<br>

⭐ If you find the project useful, consider giving the repository a star.

</div>
