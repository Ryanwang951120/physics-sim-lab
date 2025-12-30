import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn, jn_zeros
import io
import sys
import os

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# Page Config
st.set_page_config(page_title="Chladni Resonance Patterns", layout="centered")

utils.add_footer()

# Apply dark background style for matplotlib
plt.style.use('dark_background')

# Title & Description
st.title("Chladni Resonance Patterns")
st.markdown("Generative visualization of acoustic resonance on 2D plates.")

# Sidebar Controls
st.sidebar.header("Configuration")
shape = st.sidebar.radio("Plate Shape", ["Square Plate", "Circular Plate"])

if shape == "Square Plate":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Square Parameters")
    superposition_mode = st.sidebar.radio("Superposition", ["Difference (A - B)", "Sum (A + B)"], index=0, help="Determines how the two orthogonal waves combine. 'Difference' is zero when n=m.")
else:
    superposition_mode = "Difference (A - B)" # Default/Ignored for Circle

st.sidebar.markdown("---")
st.sidebar.subheader("Vibrational Modes")

s_n = utils.get_setting('ch_n')
n_val = int(max(s_n['min'], min(s_n['default'], s_n['max'])))
n = st.sidebar.slider("Parameter n", min_value=int(s_n['min']), max_value=int(s_n['max']), value=n_val, step=int(s_n['step']))

s_m = utils.get_setting('ch_m')
m_val = int(max(s_m['min'], min(s_m['default'], s_m['max'])))
m = st.sidebar.slider("Parameter m", min_value=int(s_m['min']), max_value=int(s_m['max']), value=m_val, step=int(s_m['step']))

# Resolution
resolution = 500

def calculate_square_pattern(n, m, res, mode):
    x = np.linspace(-1, 1, res)
    y = np.linspace(-1, 1, res)
    X, Y = np.meshgrid(x, y)
    
    # Chladni formula for square plate (approx)
    # Superposition of two orthogonal standing waves
    term1 = np.cos(n * np.pi * X) * np.cos(m * np.pi * Y)
    term2 = np.cos(m * np.pi * X) * np.cos(n * np.pi * Y)
    
    if mode == "Sum (A + B)":
        Z = term1 + term2
    else:
        Z = term1 - term2
    
    return X, Y, Z

def calculate_circular_pattern(n, m, res):
    # Create Cartesian grid directly to ensure correct aspect ratio and shape
    x = np.linspace(-1, 1, res)
    y = np.linspace(-1, 1, res)
    X, Y = np.meshgrid(x, y)
    
    # Convert to Polar coordinates for the math
    R = np.sqrt(X**2 + Y**2)
    THETA = np.arctan2(Y, X)
    
    # n = radial mode (number of nodal circles)
    # m = angular mode (number of nodal diameters)
    
    # Find the n-th zero of the m-th order Bessel function
    try:
        k = jn_zeros(m, n)[n-1]
    except:
        k = n * np.pi
        
    Z = jn(m, k * R) * np.cos(m * THETA)
    
    # Mask values outside the unit circle
    Z[R > 1] = np.nan
    
    return X, Y, Z

# Generate Data
if shape == "Square Plate":
    X, Y, Z = calculate_square_pattern(n, m, resolution, superposition_mode)
else:
    X, Y, Z = calculate_circular_pattern(n, m, resolution)

# Visualization
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Plot the amplitude field (Magnitude)
# We use abs(Z) to visualize vibration intensity regardless of phase (up or down)
im = ax.imshow(np.abs(Z), extent=[-1, 1, -1, 1], cmap='magma', origin='lower', interpolation='bicubic')

# Overlay Nodal Lines (Amplitude = 0)
# We use a contour plot at level 0 on the original Z to find zero crossings accurately
ax.contour(X, Y, Z, levels=[0], colors='#00FFFF', linewidths=2, alpha=0.8)

# Remove axes for clean art look
ax.axis('off')

# Add Colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.05, aspect=30)
cbar.set_label('Vibration Amplitude', color='white', fontsize=12)
cbar.ax.yaxis.set_tick_params(color='white')
cbar.outline.set_edgecolor('white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Display
st.pyplot(fig, use_container_width=True)

# Save plot to buffer for download
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches='tight', facecolor='black', dpi=300)
buf.seek(0)

# Construct filename based on parameters
shape_str = shape.replace(" ", "_").lower()
filename = f"chladni_{shape_str}_n{n}_m{m}.png"

# Download Button
st.download_button(
    label="⬇️ Download Pattern Image",
    data=buf,
    file_name=filename,
    mime="image/png",
    help="Save the current pattern as a high-resolution PNG image."
)

# Info
st.markdown(f"**Current Mode:** $n={n}, m={m}$ | **Shape:** {shape}")

st.markdown("""
---
### 🎨 Color Legend
*   **Bright (Yellow/Orange)**: **Antinodes** - Regions of maximum vibration.
*   **Dark (Purple/Black)**: **Low Vibration** - Regions with little movement.
*   **Cyan Lines**: **Nodes** - Regions with **Zero Vibration**. In a physical experiment, sand accumulates here.
""")
