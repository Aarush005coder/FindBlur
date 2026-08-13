# 🔎 FindBlur

<div align="center">

<img src="assets/logo.png" alt="FindBlur Logo" width="120">

# FindBlur

### Know before you post.

**A practical computer-vision tool for detecting image blur and sharpness.**

FindBlur combines **Laplacian Variance** and **FFT-based frequency analysis** to evaluate image detail and classify images as **Sharp, Borderline, or Blurry**.

<br>

<a href="https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/">
  <img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-OPEN%20FIND%20BLUR-2ea44f?style=for-the-badge" alt="Live Demo">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
<img src="https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">

</div>

---

## 🚀 Live Demo

### [Open FindBlur →](https://findblur-hvflnggfs2adoxzgy26wvg.streamlit.app/)

Upload an image, capture one from your camera, or analyze a batch of images and get an immediate sharpness assessment.

> **Know before you post.**

---

# 📌 What is FindBlur?

**FindBlur** is a lightweight image sharpness and blur detection application built with **Python, OpenCV, NumPy, Pandas, and Streamlit**.

The goal is simple:

> **Help you quickly identify images that may be too blurry before you use or publish them.**

Instead of relying only on one numerical measurement, FindBlur combines two complementary signals:

- **Laplacian Variance** → measures edge/detail strength
- **FFT Analysis** → evaluates high-frequency image information

These signals are normalized and combined into a final detection score.

The application then categorizes the image into:

| Result | Meaning |
|---|---|
| 🟢 **Sharp** | Strong detail and edge information detected |
| 🟡 **Borderline** | Result is close to the threshold — manual review recommended |
| 🔴 **Blurry** | Low detail detected |

---

# ✨ Features

## 🔍 Dual-Metric Blur Detection

FindBlur uses two different image-analysis approaches instead of depending on a single metric.

### Laplacian Variance

Measures local intensity changes and edge detail.

### FFT Analysis

Examines the image's frequency content and high-frequency energy.

### Combined Score

The two signals are normalized and combined using configurable weights.

---

## 🎯 Three-Level Classification

FindBlur doesn't force every image into a simple:

```text
Blur / Not Blur
