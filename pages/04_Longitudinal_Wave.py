import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as patches
import time
import sys
import os

# Page Config
st.set_page_config(page_title="Longitudinal Standing Wave", layout="wide")

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

utils.add_footer()

st.title("Longitudinal Standing Wave Visualization")
st.markdown("""
This simulation visualizes a **Longitudinal Standing Wave** (like sound waves in a pipe or a spring).
*   **Particles**: Represent air molecules or coils of a spring.
*   **Motion**: Particles oscillate horizontally around an equilibrium position.
*   **Color**: <span style='color:red'>**Red**</span> indicates **Compression** (high density), <span style='color:blue'>**Blue**</span> indicates **Rarefaction** (low density).
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("Wave Parameters")

s_particles = utils.get_setting('lw_particles')
p_val = int(max(s_particles['min'], min(s_particles['default'], s_particles['max'])))
n_particles = st.sidebar.slider("Number of Particles (N)", min_value=int(s_particles['min']), max_value=int(s_particles['max']), value=p_val, step=int(s_particles['step']))

s_n = utils.get_setting('lw_n')
n_val = int(max(s_n['min'], min(s_n['default'], s_n['max'])))
mode_n = st.sidebar.slider("Harmonic Mode (n)", min_value=int(s_n['min']), max_value=int(s_n['max']), value=n_val, step=int(s_n['step']))

s_amp = utils.get_setting('lw_amp')
amp_val = max(s_amp['min'], min(s_amp['default'], s_amp['max']))
amplitude_factor = st.sidebar.slider("Amplitude", min_value=s_amp['min'], max_value=s_amp['max'], value=amp_val, step=s_amp['step'])

s_speed = utils.get_setting('lw_speed')
speed_val = max(s_speed['min'], min(s_speed['default'], s_speed['max']))
speed_factor = st.sidebar.slider("Animation Speed", min_value=s_speed['min'], max_value=s_speed['max'], value=speed_val, step=s_speed['step'])

# --- Physics Setup ---
L = 10.0  # Length of the domain
x0 = np.linspace(0, L, n_particles)  # Equilibrium positions
k = mode_n * np.pi / L  # Wave number for standing wave (fixed ends-ish behavior for displacement nodes at ends? or antinodes?)
# For displacement standing wave in a pipe open at both ends: antinodes at ends.
# For string/spring fixed at ends: nodes at ends.
# Let's assume fixed ends for displacement: x(0)=0, x(L)=0.
# sin(k*x) where k = n*pi/L satisfies this.

omega = 2.0  # Angular frequency

# Style
plt.style.use('dark_background')

# --- Plot Setup ---
# We use a colormap where Red=Compression, Blue=Rarefaction
cmap = plt.get_cmap('coolwarm')

# Animation Container
anim_placeholder = st.empty()
run_animation = st.checkbox("Run Animation", value=True)

t = 0
dt = 0.05 * speed_factor

# Cone parameters
cone_back_x = -3.3
cone_front_x_base = -1.0

if run_animation:
    st.caption("Animation is running...")
    
    # --- INITIALIZE PLOT ONCE ---
    # 3. Create Figure and Plot
    # Lower DPI to improve FPS for large figure
    fig, ax = plt.subplots(figsize=(12, 4), dpi=80)
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    fig.subplots_adjust(bottom=0.2)  # Add more space at the bottom for the large label
    ax.set_xlim(-5, L + 1)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])  # Hide Y axis
    ax.set_xlabel("Position (x)", fontsize=14)
    ax.set_title(f"Longitudinal Standing Wave (Mode n={mode_n})", fontsize=16)
    ax.tick_params(axis='x', labelsize=12, width=2, length=5)

    # Remove spines for cleaner look
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)

    # --- Speaker Graphics ---
    # Housing (Static)
    housing = patches.Rectangle((-4.8, -0.4), 1.5, 0.8, color='#666666', zorder=5)
    ax.add_patch(housing)

    # Cone (Dynamic - Init)
    initial_cone_verts = [
        [cone_back_x, 0.2],
        [cone_back_x, -0.2],
        [cone_front_x_base, -0.6],
        [cone_front_x_base, 0.6]
    ]
    speaker_cone = patches.Polygon(initial_cone_verts, closed=True, color='#888888', alpha=0.9, zorder=6)
    ax.add_patch(speaker_cone)

    # Scatter Plot (Dynamic - Init)
    # Initialize with equilibrium positions and neutral color
    scatter = ax.scatter(x0, np.zeros_like(x0), s=300, c=np.ones_like(x0)*0.5, cmap=cmap, vmin=0, vmax=1, edgecolors='white', alpha=0.9, zorder=10)

    # Draw equilibrium lines (Static)
    ax.vlines(x0, -0.2, 0.2, color='gray', alpha=0.2, linestyle=':', zorder=1)

    while run_animation:
        # 1. Calculate Physics
        # x(t) = x0 + A * sin(kx) * cos(wt)
        spacing = L / (n_particles - 1)
        max_amp = spacing * 0.9 # Prevent crossing mostly
        
        A = max_amp * amplitude_factor
        
        displacement = A * np.cos(k * x0) * np.cos(omega * t)
        x_current = x0 + displacement
        
        # 2. Calculate Strain/Density for Coloring
        strain = -A * k * np.sin(k * x0) * np.cos(omega * t)
        
        # Normalize strain for color mapping
        limit = A * k + 1e-9
        norm_strain = -strain / limit 
        color_values = 0.5 + 0.5 * norm_strain
        
        # 3. Update Plot Objects
        # Update Scatter
        scatter.set_offsets(np.c_[x_current, np.zeros_like(x_current)])
        scatter.set_array(color_values)
        
        # Update Cone
        speaker_disp = 0.3 * np.cos(omega * t)
        current_front_x = cone_front_x_base + speaker_disp
        cone_verts = [
            [cone_back_x, 0.2],
            [cone_back_x, -0.2],
            [current_front_x, -0.6],
            [current_front_x, 0.6]
        ]
        speaker_cone.set_xy(cone_verts)

        # 4. Render Frame
        try:
            # Use buffer_rgba for speed
            fig.canvas.draw()
            
            # Get the RGBA buffer from the figure
            buf = fig.canvas.buffer_rgba()
                
            # Convert to numpy array
            X = np.asarray(buf)
            
            anim_placeholder.image(X, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering animation: {e}")
            break
        
        t += dt
        # time.sleep(0.01) # Removed sleep for max performance
    
    plt.close(fig)

else:
    st.caption("Animation is paused.")
