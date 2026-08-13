# 🔎 FindBlur

<div align="center">

<img src="assets/logo.png" alt="FindBlur Logo" width="130">

# FIND<span>BLUR</span>

### Know before you post.

**A practical computer-vision tool for detecting image blur and sharpness.**

FindBlur combines **Laplacian Variance** and **FFT-based frequency analysis** to evaluate image detail and classify images as **Sharp, Borderline, or Blurry**.

<br>

<a href="https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/">
<img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-OPEN%20FIND%20BLUR-2ea44f?style=for-the-badge" alt="Live Demo">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">

<br><br>

[Live Demo](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)
&nbsp; • &nbsp;
[GitHub Repository](https://github.com/Aarush005coder/FindBlur)

</div>

---

## 🚀 Live Demo

Try FindBlur directly in your browser:

### [Open FindBlur →](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)

Upload an image, analyze multiple images, or capture an image using your camera.

> **Know before you post.**

---

# 📌 Overview

**FindBlur** is a lightweight image sharpness and blur detection application built with **Python, OpenCV, NumPy, Pandas, and Streamlit**.

The idea is simple:

> **Check your image before you publish it.**

Instead of relying on a single blur metric, FindBlur combines two complementary signals:

- **Laplacian Variance** — measures edge and fine-detail strength.
- **FFT Analysis** — evaluates high-frequency image information.

The signals are normalized, weighted, and combined into a final detection score.

The final result is classified into three practical categories:

| Verdict | Meaning |
|---|---|
| 🟢 **Sharp** | Strong image detail detected |
| 🟡 **Borderline** | Close to the threshold — manual review recommended |
| 🔴 **Blurry** | Low image detail detected |

---

# ✨ Features

### 🔍 Dual-Metric Blur Detection

FindBlur uses two independent image-analysis signals:

```text
Laplacian Variance
        +
FFT Frequency Analysis
        ↓
Combined Score
        ↓
Final Verdict
```

This provides a second signal instead of relying entirely on one measurement.

---

### 🎯 Three-Level Classification

FindBlur doesn't force every image into:

```text
Sharp / Blurry
```

Instead, it uses:

```text
🟢 Sharp
🟡 Borderline
🔴 Blurry
```

The **Borderline** category is useful when an image falls close to the configured threshold.

---

### ⚙️ Adjustable Detection

Detection settings can be customized from the sidebar:

- Laplacian threshold
- Sensitivity mode
- Borderline margin
- Laplacian weight
- FFT weight

The detection threshold is configurable rather than permanently fixed.

---

### 🎚️ Sensitivity Modes

| Mode | Behavior |
|---|---|
| 🔴 **Strict** | More aggressive blur detection |
| 🟡 **Balanced** | General everyday use |
| 🟢 **Lenient** | More tolerant of low-texture images |

---

### 🖼️ Single Image Check

Upload:

- JPG
- JPEG
- PNG
- WEBP

FindBlur provides:

- Original image
- Detail map
- Edge map
- Laplacian score
- FFT score
- Combined score
- Confidence
- Detection breakdown
- Final verdict

---

### 📁 Batch Analysis

Analyze multiple images in one session.

Batch mode supports:

- Multiple image uploads
- Progress tracking
- Thumbnail previews
- Individual scores
- Verdict filtering
- Score sorting
- Filename sorting
- Manual review
- CSV export

---

### 📷 Live Camera

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

---

### 🧪 Visual Diagnostics

FindBlur provides visual information alongside numerical scores.

It generates:

- Laplacian detail maps
- Canny edge maps
- Original image comparison

This helps users understand where image detail is being detected.

---

### 📝 Manual Review

Automated detection isn't perfect.

FindBlur allows results to be manually reviewed:

```text
✅ Correct
⚠️ Disagree
○ Not Reviewed
```

Review information is maintained within the current Streamlit session.

---

### 📊 CSV Export

Batch results can be exported for further analysis.

Typical result fields include:

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

FindBlur also uses **Fast Fourier Transform (FFT)** analysis.

FFT provides information about the frequency components present in an image.

Higher-frequency components are generally associated with:

- Fine structures
- Edges
- Textures
- Rapid intensity changes

This creates a second signal that can be compared with the Laplacian result.

---

## 3. Combined Score

The two signals are normalized before being combined.

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
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       🟢 Sharp    🟡 Borderline   🔴 Blurry
```

The default configuration gives greater weight to Laplacian analysis while FFT provides additional validation.

---

# 🎯 Why Borderline?

A low sharpness score does not always mean an image is actually blurry.

For example:

- Clear blue skies
- Plain walls
- Smooth backgrounds
- Minimal-detail scenes

can naturally contain fewer strong edges.

FindBlur therefore uses a **Borderline** zone.

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

This allows the user to manually review uncertain images instead of blindly trusting a single threshold.

---

# 🖥️ Application Preview

<div align="center">

<table>
<tr>

<td align="center" width="50%">

### 🔍 Single Image Check

<img src="docs/single-check.png" alt="FindBlur Single Image Check" width="100%">

</td>

<td align="center" width="50%">

### 📁 Batch Analysis

<img src="docs/batch-check.png" alt="FindBlur Batch Analysis" width="100%">

</td>

</tr>

<tr>

<td align="center" width="50%">

### 📷 Live Camera

<img src="docs/live-camera.png" alt="FindBlur Live Camera Detection" width="100%">

</td>

<td align="center" width="50%">

### ⚙️ Detection Settings

<img src="docs/settings.png" alt="FindBlur Detection Settings" width="100%">

</td>

</tr>
</table>

</div>

---

# 🏗️ Architecture

FindBlur separates the Streamlit interface from the computer-vision detection engine.

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

Handles:

- Streamlit interface
- Tabs
- Sidebar controls
- Image uploads
- Camera input
- Batch processing
- Result rendering
- CSV downloads

### `blur_detector.py`

Handles:

- Image preprocessing
- Laplacian analysis
- FFT analysis
- Score normalization
- Weighted scoring
- Verdict classification
- Confidence calculation

This separation keeps the UI and detection logic independent and easier to maintain.

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
├── .streamlit/
│   └── config.toml
│
└── .devcontainer/
```

---

# 🛠️ Tech Stack

<div align="center">

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Core application logic |
| 🎈 **Streamlit** | Interactive web interface |
| 👁️ **OpenCV** | Computer vision and image processing |
| 🔢 **NumPy** | Numerical computation and FFT |
| 🐼 **Pandas** | Batch processing and CSV export |
| 🖼️ **Pillow** | Image handling |
| 📊 **Matplotlib** | Diagnostic visualization |

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

Open:

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

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

# ☁️ Deployment

FindBlur is deployed using **Streamlit Community Cloud**.

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
Streamlit Community Cloud
       │
       ▼
   Live FindBlur App
```

### 🌐 Live Application

**[Launch FindBlur](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)**

---

# ⚠️ Limitations

FindBlur focuses specifically on **image sharpness and blur detection**.

It is not intended to be a complete image-quality assessment system.

Some cases can be difficult to classify automatically:

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

A **Borderline** result should therefore be treated as a signal for manual review rather than an absolute decision.

---

# 🔮 Future Improvements

Potential future improvements include:

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
- [ ] Improved low-texture detection
- [ ] Large-batch optimization
- [ ] Additional image-quality metrics

---

# 🧪 Testing

When changing the detection engine, test against different image categories.

### Sharp Images

```text
High-detail scenes
Text
Objects with strong edges
Detailed landscapes
```

### Blurry Images

```text
Defocused photos
Motion blur
Soft-focus images
Low-detail photographs
```

### Difficult Cases

```text
Clear sky
Plain walls
Smooth backgrounds
Low-texture scenes
Noisy images
```

The goal is not only to identify obvious blur, but also to reduce false positives on naturally low-detail images.

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

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

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Developer

<div align="center">

## FindBlur

**Built with Python, OpenCV, NumPy & Streamlit.**

A practical computer-vision project for evaluating image sharpness before publishing.

<br>

[🚀 Live Demo](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)
&nbsp; • &nbsp;
[💻 GitHub](https://github.com/Aarush005coder/FindBlur)

</div>

---

<div align="center">

# 🔎 FindBlur

### Know before you post.

**Stop guessing. Start checking.**

<br>

⭐ If you find FindBlur useful, consider giving the repository a star.

</div>
