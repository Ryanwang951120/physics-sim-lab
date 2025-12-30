import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import time
import io
import tempfile
import os
import sys

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# Page Config
st.set_page_config(page_title="Circular Wire Loop Simulation", layout="centered")

utils.add_footer()

# Title
st.title("Standing Waves on a Circular Wire Loop")
st.markdown("Visualizing radial oscillations using polar coordinates.")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")

s_n = utils.get_setting('cw_n')
n_val = int(max(s_n['min'], min(s_n['default'], s_n['max'])))
n = st.sidebar.slider("Mode Number (n)", min_value=int(s_n['min']), max_value=int(s_n['max']), value=n_val, step=int(s_n['step']), help="Number of wavelengths around the ring")

s_speed = utils.get_setting('cw_speed')
speed_val = max(s_speed['min'], min(s_speed['default'], s_speed['max']))
speed = st.sidebar.slider("Animation Speed", min_value=s_speed['min'], max_value=s_speed['max'], value=speed_val, step=s_speed['step'])

s_amp = utils.get_setting('cw_amp')
amp_val = max(s_amp['min'], min(s_amp['default'], s_amp['max']))
amplitude = st.sidebar.slider("Amplitude", min_value=s_amp['min'], max_value=s_amp['max'], value=amp_val, step=s_amp['step'])

# Style
plt.style.use('dark_background')

# Setup Plot
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')
ax.set_aspect('equal')
limit = 1.0 + amplitude + 0.1
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

# Initial Data
theta = np.linspace(0, 2*np.pi, 1000)
R0 = 1.0
line, = ax.plot([], [], lw=4, color='#8A2BE2') # BlueViolet color
title = ax.set_title(f"Mode n={n}")

def get_wave_coords(t):
    # R(theta, t) = R0 + A * sin(n * theta) * cos(omega * t)
    omega = speed  # Frequency scaling
    R = R0 + amplitude * np.sin(n * theta) * np.cos(omega * t)
    
    # Polar to Cartesian
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return x, y

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    plot_placeholder = st.empty()

with col2:
    st.write("### Controls")
    run_anim = st.checkbox("Run Real-time", value=True)
    st.markdown("---")
    generate_gif = st.button("Generate GIF")

# Real-time Animation Loop
if run_anim and not generate_gif:
    start_time = time.time()
    while True:
        # Check if user stopped it (Streamlit reruns script on interaction, so this breaks loop naturally)
        # But inside the loop we need to be careful not to block too long
        
        t = time.time() - start_time
        x, y = get_wave_coords(t)
        
        line.set_data(x, y)
        ax.set_title(f"Mode n={n} | Real-time")
        
        plot_placeholder.pyplot(fig)
        time.sleep(0.02)

# GIF Generation using Matplotlib Animation
if generate_gif:
    status_text = st.empty()
    progress_bar = st.progress(0)
    status_text.info("Generating Animation Frames...")
    
    # Define update function for FuncAnimation
    def update(frame):
        # Create a loop of 2*pi / omega duration roughly, or just arbitrary frames
        # Let's make one full oscillation cycle
        # cos(omega * t) -> period T = 2*pi / omega
        omega = speed
        period = 2 * np.pi / omega
        t = frame * period / 50 # 50 frames per cycle
        
        x, y = get_wave_coords(t)
        line.set_data(x, y)
        ax.set_title(f"Mode n={n}")
        
        # Update progress
        prog = int((frame / 50) * 100)
        if prog <= 100:
            progress_bar.progress(prog)
            
        return line,

    # Create Animation
    ani = animation.FuncAnimation(fig, update, frames=50, blit=False)
    
    status_text.info("Saving GIF... (This might take a few seconds)")
    
    # Save to temporary file first (Matplotlib requires a file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmp_file:
        tmp_path = tmp_file.name

    ani.save(tmp_path, writer=PillowWriter(fps=20))
    
    # Read into buffer
    with open(tmp_path, "rb") as f:
        gif_buffer = io.BytesIO(f.read())
    
    # Cleanup
    os.remove(tmp_path)
    
    progress_bar.empty()
    status_text.success("GIF Generated Successfully!")
    
    # Display GIF
    st.image(gif_buffer, caption=f"Standing Wave Mode n={n}")
    
    # Download Button
    st.download_button(
        label="⬇️ Download GIF",
        data=gif_buffer,
        file_name=f"circular_wave_n{n}.gif",
        mime="image/gif"
    )
