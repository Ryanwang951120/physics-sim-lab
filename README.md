# Physics Simulations Collection (物理模擬合集)

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## 🇬🇧 English

### Overview
This repository contains a collection of interactive physics simulations built with **Python** and **Streamlit**. These tools are designed to visualize complex wave phenomena and resonance patterns in an intuitive and aesthetically pleasing way.

### 📦 Included Simulations

#### 1. Standing Waves on a String (Melde's Experiment)
*   **File**: `standing_waves.py`
*   **Description**: Simulates transverse waves on a string with adjustable tension, density, and frequency.
*   **Features**: Real-time animation, resonance detection, harmonic locking, and tension-frequency analysis.

#### 2. Chladni Resonance Patterns
*   **File**: `chladni_patterns.py`
*   **Description**: Generative visualization of acoustic resonance on 2D plates (Square & Circular).
*   **Features**: 
    *   Switch between Square and Circular plates.
    *   Adjust vibrational modes ($n, m$).
    *   High-contrast "Sci-Fi" visualization with nodal lines.
    *   **Download** generated patterns as high-res PNGs.

#### 3. Circular Wire Loop Standing Waves
*   **File**: `circular_wave.py`
*   **Description**: Visualizes radial standing waves on a flexible circular wire loop.
*   **Features**:
    *   Real-time deformation animation.
    *   Adjustable mode number ($n$), speed, and amplitude.
    *   **GIF Generation**: Create and download looping GIFs of the oscillation.

#### 4. Longitudinal Standing Waves
*   **File**: `longitudinal_wave.py`
*   **Description**: Visualizes longitudinal waves (like sound or a spring) using oscillating particles.
*   **Features**:
    *   Particle animation showing compression and rarefaction.
    *   Color-coded density (Red=Compression, Blue=Rarefaction).
    *   Adjustable particle count, mode ($n$), and amplitude.

### 🚀 Quick Start

#### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```
*Requirements: `streamlit`, `numpy`, `matplotlib`, `scipy`, `seaborn`*

#### 2. Run the Application
Run the main entry point to access all simulations via a menu:
```bash
streamlit run Home.py
```

---

<a name="chinese"></a>
## 🇹🇼 中文

### 簡介
本專案包含一系列使用 **Python** 和 **Streamlit** 構建的互動式物理模擬工具。這些程式旨在以直觀且美觀的方式視覺化複雜的波動現象與共振圖案。

### 📦 模擬項目

#### 1. 弦上的駐波 (Standing Waves / Melde's Experiment)
*   **檔案**: `pages/01_Standing_Waves.py`
*   **描述**: 模擬弦上的橫波，可調整張力、線密度和頻率。
*   **功能**: 實時動畫、共振偵測、諧波鎖定以及張力-頻率關係分析。

#### 2. 克拉德尼共振圖形 (Chladni Resonance Patterns)
*   **檔案**: `pages/02_Chladni_Patterns.py`
*   **描述**: 2D 平板（正方形與圓形）聲學共振的生成式視覺化。
*   **功能**:
    *   切換正方形或圓形板。
    *   調整振動模態參數 ($n, m$)。
    *   高對比度「科幻風」視覺效果與節線標示。
    *   **下載** 高解析度圖案圖片 (PNG)。

#### 3. 圓形線圈駐波 (Circular Wire Loop Standing Waves)
*   **檔案**: `pages/03_Circular_Wave.py`
*   **描述**: 視覺化柔性圓形線圈上的徑向駐波。
*   **功能**:
    *   實時變形動畫。
    *   可調整模態數 ($n$)、速度和振幅。
    *   **GIF 生成**: 製作並下載循環播放的 GIF 動畫。

#### 4. 縱波駐波 (Longitudinal Standing Waves)
*   **檔案**: `pages/04_Longitudinal_Wave.py`
*   **描述**: 使用粒子振盪視覺化縱波（如聲波或彈簧）。
*   **功能**:
    *   顯示壓縮與稀疏區域的粒子動畫。
    *   密度顏色編碼（紅色=壓縮，藍色=稀疏）。
    *   可調整粒子數量、模態 ($n$) 和振幅。

### 🚀 快速開始

#### 1. 安裝依賴套件
請確保您已安裝 Python，然後執行以下指令：
```bash
pip install -r requirements.txt
```
*所需套件：`streamlit`, `numpy`, `matplotlib`, `scipy`, `seaborn`*

#### 2. 執行應用程式
執行主程式即可透過選單訪問所有模擬：
```bash
streamlit run Home.py
```
