import streamlit as st
import utils

st.set_page_config(
    page_title="Physics Simulations Collection",
    page_icon="⚛️",
    layout="wide"
)

st.title("⚛️ Physics Simulations Collection")
st.subheader("物理模擬合集")

st.markdown("""
---
Welcome! This application hosts a collection of interactive physics simulations.
Select a simulation from the **sidebar** to get started.

歡迎！本應用程式包含一系列互動式物理模擬工具。
請從 **側邊欄** 選擇一個模擬項目開始使用。

---

### 📦 Available Simulations (可用模擬)

#### 1. 🎸 Standing Waves on a String (弦上的駐波)
*   **Melde's Experiment**: Visualize transverse waves, resonance, and harmonic modes.
*   **Melde 實驗**: 視覺化橫波、共振與諧波模態。

#### 2. 🎻 Chladni Resonance Patterns (克拉德尼共振圖形)
*   **2D Acoustics**: Generate beautiful resonance patterns on square and circular plates.
*   **2D 聲學**: 在正方形與圓形平板上生成美麗的共振圖案。

#### 3. ⭕ Circular Wire Loop Standing Waves (圓形線圈駐波)
*   **Radial Waves**: Observe radial standing waves on a flexible loop.
*   **徑向波**: 觀察柔性線圈上的徑向駐波。

#### 4. 🔊 Longitudinal Standing Waves (縱波駐波)
*   **Sound/Springs**: Visualize compression and rarefaction with particle animation.
*   **聲波/彈簧**: 透過粒子動畫視覺化壓縮與稀疏現象。

---
*Built with Python & Streamlit*
""")

st.sidebar.success("Select a demo above! 👆")

utils.add_footer()
