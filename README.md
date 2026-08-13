# FindBlur

### Know before you post.

**FindBlur** is a lightweight image blur and sharpness detection tool built with **Python, Streamlit, and OpenCV**.

It analyzes image detail using **Laplacian variance** as the primary signal and **FFT high-frequency analysis** as a secondary signal, then combines both measurements to classify an image as **Sharp, Borderline, or Blurry**.

> A quick second opinion before you publish an image.

---

## 🚀 Live Demo

**Try FindBlur:** `https://findblur.streamlit.app`

> Replace the URL above with your actual Streamlit deployment URL after deployment.

---

## ✨ Features

### 🔍 Dual-Metric Blur Detection

FindBlur doesn't depend on a single measurement.

* **Laplacian Variance** — primary sharpness signal
* **FFT High-Frequency Analysis** — secondary validation
* **Weighted score combination** — reduces false positives
* **Confidence-based verdicts**

### 🎯 Three-Level Classification

Instead of a simple blur/no-blur decision:

| Verdict           | Meaning                                           |
| ----------------- | ------------------------------------------------- |
| 🟢 **Sharp**      | Strong fine-detail response                       |
| 🟡 **Borderline** | Close to the threshold; manual review recommended |
| 🔴 **Blurry**     | Insufficient fine detail detected                 |

### ⚙️ Adjustable Detection

Tune the detector according to your images:

* Laplacian threshold: `0–1000`
* **Strict** sensitivity
* **Balanced** sensitivity
* **Lenient** sensitivity
* Configurable Laplacian/FFT weighting
* Automatic borderline margin

### 📷 Single Image Analysis

Upload:

* JPG
* JPEG
* PNG
* WEBP

Get an immediate analysis with:

* Original image
* Edge map
* Laplacian heatmap
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
* Manual review status
* CSV export

### 📹 Live Camera

Use Streamlit's camera input to capture an image and analyze its sharpness directly.

### 🧭 Visual Diagnostics

FindBlur provides additional visual context using:

* Canny edge detection
* Laplacian-based detail visualization
* Original vs. diagnostic comparison

### 📝 Manual Review

Mark results as:

* ✓ Correct
* ! Disagree
* Not reviewed

Review information is stored in the current Streamlit session without requiring a database.

---

# 🧠 How FindBlur Works

FindBlur combines two different signals to make the detection more reliable.

```text
                    Input Image
                         │
                         ▼
                    Grayscale
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
      Laplacian Variance       FFT Analysis
              │                     │
              ▼                     ▼
       Detail Strength        High-Frequency
                              Energy
              │                     │
              └──────────┬──────────┘
                         ▼
                  Score Normalization
                         │
                         ▼
                  Weighted Combination
                         │
                         ▼
                Sensitivity Adjustment
                         │
                         ▼
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          SHARP      BORDERLINE    BLURRY
```

## Laplacian Variance

The primary metric is:

```python
cv2.Laplacian(gray, cv2.CV_64F).var()
```

Sharp images generally contain more fine edges and local intensity changes, producing a higher Laplacian variance.

Blurry images tend to lose fine detail, resulting in a lower value.

## FFT Analysis

FindBlur also examines the frequency content of the image using the **Fast Fourier Transform**.

High-frequency components generally represent fine image detail and edges.

FFT provides a second signal that helps prevent the detector from blindly treating every low-texture image as blurry.

For example:

* A plain wall
* Clear sky
* Smooth background

may naturally contain very little high-frequency information even when the photograph itself is perfectly focused.

---

# 📊 Combined Detection

Raw Laplacian and FFT values operate on different numerical scales, so FindBlur does not simply average them.

Instead:

```text
Laplacian Score
       │
       ▼
   Normalize
       │
       ├──────────────┐
       │              │
       ▼              ▼
FFT Score        Laplacian
   │              Weight
   ▼                │
Normalize            │
   │                │
   └───────┬────────┘
           ▼
     Combined Score
           │
           ▼
      Classification
```

The default weighting prioritizes Laplacian variance while allowing FFT analysis to provide additional validation.

---

# 🎚️ Sensitivity Modes

FindBlur provides three detection modes.

### Strict

Designed to flag potentially soft images more aggressively.

Useful when image quality matters heavily.

### Balanced

The default mode.

Designed for general-purpose image checking.

### Lenient

More tolerant of images with naturally low texture.

Useful for:

* Landscapes
* Product backgrounds
* Minimalist photography
* Low-detail scenes

---

# 🖥️ Application

## Single Check

Upload an image and immediately see:

```text
┌──────────────────────┐
│                      │
│       ORIGINAL       │
│                      │
└──────────────────────┘

           ↓

Laplacian       284.2
FFT Energy       81.3
Combined        251.1
Confidence       94%

        ✓ SHARP
```

---

## Batch Check

Process an entire group of images:

```text
Thumbnail | Filename | Laplacian | FFT | Combined | Verdict
----------|----------|-----------|-----|----------|---------
          | img1.jpg | 284.2     | 81  | 251.1    | Sharp
          | img2.jpg | 104.8     | 61  | 91.2     | Borderline
          | img3.jpg | 32.1      | 28  | 30.4     | Blurry
```

Results can be filtered, sorted, reviewed, and exported.

---

## 📹 Live Camera

Capture an image directly through your browser:

```text
Camera
   ↓
Capture
   ↓
Analyze
   ↓
Score
   ↓
Verdict
```

---

# 🛠️ Tech Stack

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| **Python**     | Application and detection logic |
| **Streamlit**  | Web interface                   |
| **OpenCV**     | Image processing                |
| **NumPy**      | Numerical and FFT operations    |
| **Pandas**     | Batch results and CSV export    |
| **Pillow**     | Image handling                  |
| **Matplotlib** | Diagnostic visualizations       |

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

The detection engine is intentionally separated from the UI so that the computer-vision logic can be tested and extended independently.

---

# ⚡ Getting Started

## Prerequisites

* Python 3.11+
* Git
* A modern web browser

## 1. Clone the Repository

```bash
git clone https://github.com/Aarush005coder/FindBlur.git
cd FindBlur
```

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

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run FindBlur

```bash
streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

---

# ☁️ Deployment

FindBlur can be deployed directly from GitHub using **Streamlit Community Cloud**.

Basic workflow:

```text
Local Project
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
 Public App
```

After pushing the repository to GitHub:

1. Open Streamlit Community Cloud.
2. Connect your GitHub account.
3. Select the `FindBlur` repository.
4. Select the `main` branch.
5. Set the main file to:

```text
app.py
```

6. Deploy.

---

# 📦 Dependencies

The main dependencies are:

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

# ⚠️ Limitations

FindBlur is a **sharpness-analysis tool**, not a complete image-quality or photographic-quality evaluator.

A low sharpness score does not necessarily mean that an image is technically bad.

For example:

* Intentionally soft photography may be classified as borderline.
* Images with very little texture can be difficult to evaluate.
* Artistic blur may be intentional.
* Different cameras and resolutions can produce different score ranges.
* Very noisy images can contain strong high-frequency signals.

For this reason, FindBlur includes the **Borderline** category and manual review functionality.

---

# 🔮 Future Improvements

Potential future improvements include:

* [ ] Automatic threshold calibration by image resolution
* [ ] Region-based blur detection
* [ ] Motion-blur detection
* [ ] Focus-area detection
* [ ] More robust low-texture handling
* [ ] Image-quality history
* [ ] Batch folder processing
* [ ] PDF report generation
* [ ] Detection benchmarking dataset
* [ ] Automated threshold calibration
* [ ] Performance optimization for very large batches

---

# 📸 Screenshots

Add screenshots of the application here:

```text
docs/
├── single-check.png
├── batch-check.png
├── live-camera.png
└── settings.png
```

Then include them in the README:

```markdown
## Screenshots

### Single Check

![Single Check](docs/single-check.png)

### Batch Analysis

![Batch Check](docs/batch-check.png)

### Live Camera

![Live Camera](docs/live-camera.png)
```

---

# 🤝 Contributing

Contributions, ideas, and improvements are welcome.

If you'd like to contribute:

```bash
git checkout -b feature/your-feature
```

Make your changes, test them locally, and open a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

**Aarush Khandelwal**

Built with Python, OpenCV, and Streamlit.

---

## FindBlur

> **Know before you post.**

A simple idea:

**Look at the image. Measure the detail. Make a better call.**
