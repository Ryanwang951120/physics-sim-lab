import streamlit as st
import sys
import os

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

st.set_page_config(page_title="User Guide", page_icon="📖", layout="wide")

utils.add_footer()

st.title("📖 User Guide (使用教學)")

st.markdown("""
---
### 🌟 General Interface (通用介面)
*   **Sidebar (側邊欄)**: All simulation parameters and controls are located in the sidebar on the left. (所有模擬參數與控制項皆位於左側側邊欄)
*   **Main Area (主畫面)**: Displays the real-time visualization and analysis plots. (顯示實時視覺化與分析圖表)
*   **Navigation (導航)**: Use the sidebar menu to switch between different simulations. (使用側邊欄選單切換不同的模擬程式)

---

### 1. 🎸 Standing Waves on a String (弦上的駐波)
**Goal**: Explore the relationship between tension, frequency, and wavelength in a vibrating string.
**目標**: 探索振動弦中張力、頻率與波長之間的關係。

*   **Controls (控制項)**:
    *   `String Tension`: Adjust the tension force applied to the string. (調整弦的張力)
    *   `Linear Density`: Change the mass per unit length of the string. (改變弦的線密度)
    *   `Frequency Mode`:
        *   **Manual**: Manually slide the frequency to find resonance. (手動滑動頻率尋找共振)
        *   **Set Harmonic**: Choose a specific harmonic number ($n$), and the app locks the frequency for you. (選擇特定的諧波數，程式會自動鎖定頻率)
*   **Visuals (視覺效果)**:
    *   **Red Dots**: Indicate **Nodes** (points of zero displacement). (紅點表示波節，即位移為零的點)
    *   **Analysis Plot**: Shows the $f$ vs $\sqrt{T}$ relationship to verify physical laws. (顯示頻率與張力平方根的關係圖，驗證物理定律)

---

### 2. 🎻 Chladni Resonance Patterns (克拉德尼共振圖形)
**Goal**: Visualize 2D resonance modes on vibrating plates.
**目標**: 視覺化振動平板上的二維共振模態。

*   **Controls (控制項)**:
    *   `Plate Shape`: Switch between **Square** and **Circular** plates. (切換正方形或圓形平板)
    *   `Mode Parameters (n, m)`: Adjust the integers determining the nodal line patterns. (調整決定節線圖案的整數參數)
    *   `Superposition`: (Square only) Choose how modes are combined (Sum or Difference) to create different symmetries. ((僅限正方形) 選擇模態疊加方式以產生不同的對稱性)
*   **Features (功能)**:
    *   **Download PNG**: Save the generated high-resolution pattern. (下載高解析度圖案)

---

### 3. ⭕ Circular Wire Loop (圓形線圈駐波)
**Goal**: Observe radial standing waves on a flexible loop.
**目標**: 觀察柔性線圈上的徑向駐波。

*   **Controls (控制項)**:
    *   `Mode Number (n)`: Number of wavelengths around the circumference. (圓周上的波長數量)
    *   `Wave Speed`: Speed of the wave propagation. (波的傳播速度)
    *   `Amplitude`: Height of the wave peaks. (波峰的高度)
*   **Features (功能)**:
    *   **Generate GIF**: Create a looping animation of the current mode. (製作當前模態的循環 GIF 動畫)

---

### 4. 🔊 Longitudinal Waves (縱波駐波)
**Goal**: Visualize sound waves or spring oscillations using particles.
**目標**: 使用粒子視覺化聲波或彈簧振盪。

*   **Controls (控制項)**:
    *   `Number of Particles`: Density of the medium. (介質的密度/粒子數)
    *   `Harmonic Mode (n)`: Number of compression/rarefaction regions. (壓縮/稀疏區域的數量)
*   **Visuals (視覺效果)**:
    *   **Speaker Animation**: Shows the driving source. (顯示驅動源/喇叭動畫)
    *   **Color Coding**:
        *   <span style='color:red'>**Red**</span>: Compression (High Density). (紅色：壓縮/高密度)
        *   <span style='color:blue'>**Blue**</span>: Rarefaction (Low Density). (藍色：稀疏/低密度)

---
*Tips: For the best experience, run these simulations on a desktop browser with a wide screen.*
*提示：為了獲得最佳體驗，請在寬螢幕的桌上型瀏覽器中執行這些模擬。*
""", unsafe_allow_html=True)
