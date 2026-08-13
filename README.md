# 🔎 FindBlur

### Know before you post.

**FindBlur** is an image blur and sharpness detection tool built with **Python, Streamlit, and OpenCV**.

It combines **Laplacian variance** with **FFT high-frequency analysis** to evaluate image sharpness and classify images into **Sharp, Borderline, or Blurry**.

---

## 🚀 Live Demo

### 👉 [Try FindBlur](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)

**Know before you post.**

---

## 📸 What FindBlur Does

FindBlur gives you a quick second opinion on image sharpness before you publish or use an image.

Instead of relying on a simple blur/no-blur rule, it combines multiple image-detail signals and gives you a three-level result:

🟢 **Sharp**
🟡 **Borderline**
🔴 **Blurry**

---

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)

</div>

---

## ✨ Features

### 🔍 Dual-Metric Detection

FindBlur combines two complementary image-analysis techniques:

* **Laplacian Variance** — primary sharpness measurement
* **FFT Analysis** — high-frequency detail validation
* **Weighted score combination**
* **Confidence-based classification**

### 🎯 Three-Level Verdict

| Verdict           | Meaning                                 |
| ----------------- | --------------------------------------- |
| 🟢 **Sharp**      | Strong fine-detail response             |
| 🟡 **Borderline** | Close to the threshold; review manually |
| 🔴 **Blurry**     | Insufficient fine detail detected       |

### ⚙️ Adjustable Detection

* Laplacian threshold from `0–1000`
* Strict sensitivity
* Balanced sensitivity
* Lenient sensitivity
* Adjustable metric weighting
* Borderline detection margin

### 🖼️ Single Image Analysis

Supported formats:

* JPG
* JPEG
* PNG
* WEBP

Analyze an image and view:

* Original image
* Edge map
* Laplacian visualization
* Laplacian score
* FFT score
* Combined score
* Confidence
* Final verdict

### 📁 Batch Analysis

Analyze multiple images in one session.

Includes:

* Progress tracking
* Image thumbnails
* Individual scores
* Verdicts
* Sorting
* Filtering
* Manual review
* CSV export

### 📷 Live Camera

Capture an image directly from your browser and analyze its sharpness using Streamlit's camera input.

### 🧭 Visual Diagnostics

FindBlur provides visual analysis using:

* Canny edge detection
* Laplacian detail visualization
* Original vs. diagnostic comparison

### 📝 Manual Review

Results can be marked as:

* ✓ Correct
* ! Disagree
* Not reviewed

Review information is maintained through Streamlit session state.

---

# 🧠 How It Works

FindBlur uses two different signals to make the detection more reliable.

```text
                         IMAGE
                           │
                           ▼
                       GRAYSCALE
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        LAPLACIAN VARIANCE        FFT ANALYSIS
                │                     │
                ▼                     ▼
          EDGE DETAIL          HIGH-FREQUENCY
             SIGNAL                ENERGY
                │                     │
                └──────────┬──────────┘
                           ▼
                    NORMALIZATION
                           │
                           ▼
                    WEIGHTED SCORE
                           │
                           ▼
                  SENSITIVITY CHECK
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          SHARP       BORDERLINE       BLURRY
```

---

## 🔬 Laplacian Variance

The primary sharpness metric is calculated using:

```python
cv2.Laplacian(gray, cv2.CV_64F).var()
```

Sharp images generally contain more fine edges and local intensity changes, producing a stronger Laplacian response.

Blurry images tend to lose fine detail, resulting in lower variance.

---

## 📊 FFT High-Frequency Analysis

FindBlur also analyzes the image in the frequency domain using **Fast Fourier Transform**.

High-frequency components generally represent fine image detail and edges.

This provides a secondary signal that helps cross-check the Laplacian result, particularly for images containing large low-texture areas.

---

## 🎚️ Sensitivity Modes

### Strict

More aggressive detection for potentially soft images.

### Balanced

Default mode for general-purpose image checking.

### Lenient

More tolerant of naturally low-texture images.

---

# 🖥️ Application

## Single Check

Upload an image and receive:

```text
Laplacian       284.2
FFT Energy       81.3
Combined        251.1
Confidence       94%

✓ SHARP

Strong detail detected.
```

---

## Batch Check

Analyze an entire collection of images:

```text
Thumbnail | Filename | Laplacian | FFT | Combined | Verdict
----------|----------|-----------|-----|----------|---------
          | img1.jpg | 284.2     | 81  | 251.1    | Sharp
          | img2.jpg | 104.8     | 61  | 91.2     | Borderline
          | img3.jpg | 32.1      | 28  | 30.4     | Blurry
```

Results can be filtered, sorted, reviewed, and exported as CSV.

---

## 📷 Live Camera

Capture → Analyze → Review.

```text
Camera
   ↓
Capture
   ↓
Laplacian + FFT
   ↓
Combined Score
   ↓
Verdict
```

---

# 🛠️ Tech Stack

<div align="center">

### Core

<a href="https://www.python.org/">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="55" alt="Python"/>
</a>
&nbsp;&nbsp;

<a href="https://opencv.org/">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" width="55" alt="OpenCV"/>
</a>
&nbsp;&nbsp;

<a href="https://streamlit.io/">
<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="55" alt="Streamlit"/>
</a>

### Data & Image Processing

<a href="https://numpy.org/">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="55" alt="NumPy"/>
</a>
&nbsp;&nbsp;

<a href="https://pandas.pydata.org/">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="55" alt="Pandas"/>
</a>
&nbsp;&nbsp;

<a href="https://matplotlib.org/">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg" width="55" alt="Matplotlib"/>
</a>

</div>

### Technology Overview

| Technology        | Role                                 |
| ----------------- | ------------------------------------ |
| 🐍 **Python**     | Application and detection logic      |
| 🎈 **Streamlit**  | Web interface and deployment         |
| 👁️ **OpenCV**    | Image processing and computer vision |
| 🔢 **NumPy**      | Numerical computation and FFT        |
| 🐼 **Pandas**     | Batch results and CSV export         |
| 🖼️ **Pillow**    | Image loading and processing         |
| 📈 **Matplotlib** | Diagnostic visualizations            |

---

# 📁 Project Structure

```text
FindBlur/
│
├── app.py
│   └── Streamlit application and UI
│
├── blur_detector.py
│   └── Blur detection and image-analysis engine
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── assets/
│   └── logo.png
│
└── .streamlit/
    └── config.toml
```

The detection engine is separated from the UI so the computer-vision logic can be maintained and extended independently.

---

# ⚡ Getting Started

## Prerequisites

* Python 3.11+
* Git
* Modern web browser

## Clone the Repository

```bash
git clone https://github.com/Aarush005coder/FindBlur.git
cd FindBlur
```

## Create Virtual Environment

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
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
Streamlit Cloud
       │
       ▼
  🌐 FindBlur
```

### Live Application

**[Launch FindBlur](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)**

---

# 📦 Dependencies

```text
streamlit
opencv-python-headless
numpy
pandas
Pillow
matplotlib
```

Install with:

```bash
pip install -r requirements.txt
```

---

# ⚠️ Limitations

FindBlur is a **sharpness-analysis tool**, not a complete image-quality evaluator.

A low score does not necessarily mean that an image is bad.

Potential edge cases include:

* Intentionally soft photography
* Very low-texture images
* Artistic blur
* Extremely noisy images
* Different camera resolutions
* Images with naturally limited fine detail

The **Borderline** classification exists specifically to avoid treating every uncertain case as a definite failure.

---

# 🔮 Future Improvements

* [ ] Region-based blur detection
* [ ] Motion-blur detection
* [ ] Focus-area detection
* [ ] Resolution-aware threshold calibration
* [ ] Automatic threshold calibration
* [ ] Image-quality history
* [ ] PDF report generation
* [ ] Benchmark dataset
* [ ] Large-batch performance improvements
* [ ] More robust low-texture image handling

---

# 📸 Screenshots

Add screenshots here once you have them:

```text
docs/
├── single-check.png
├── batch-check.png
├── live-camera.png
└── settings.png
```

Example:

```markdown
## Screenshots

### Single Check

![FindBlur Single Check](docs/single-check.png)

### Batch Analysis

![FindBlur Batch Analysis](docs/batch-check.png)

### Live Camera

![FindBlur Live Camera](docs/live-camera.png)
```

---

# 🤝 Contributing

Contributions and improvements are welcome.

Create a feature branch:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them locally, and submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

### Aarush Khandelwal

Built with **Python, OpenCV, and Streamlit**.

---

<div align="center">

## 🔎 FindBlur

### Know before you post.

**[🚀 Try the Live App](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)**

⭐ If you find FindBlur useful, consider giving the repository a star.

</div>
