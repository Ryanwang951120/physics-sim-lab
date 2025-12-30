import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# Page Config
st.set_page_config(page_title="Standing Wave Simulation", layout="wide")

utils.add_footer()

# Apply dark background style for matplotlib
plt.style.use('dark_background')

# Title
st.title("Standing Waves on a String (Melde's Experiment)")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")

# Physical Properties
s_tension = utils.get_setting('sw_tension')
t_val = max(s_tension['min'], min(s_tension['default'], s_tension['max']))
tension_input = st.sidebar.slider("String Tension (N)", min_value=s_tension['min'], max_value=s_tension['max'], value=t_val, step=s_tension['step'])

s_density = utils.get_setting('sw_density')
d_val = max(s_density['min'], min(s_density['default'], s_density['max']))
linear_density = st.sidebar.slider("Linear Density (kg/m)", min_value=s_density['min'], max_value=s_density['max'], value=d_val, step=s_density['step'], format="%.4f")

s_length = utils.get_setting('sw_length')
l_val = max(s_length['min'], min(s_length['default'], s_length['max']))
length = st.sidebar.slider("String Length (m)", min_value=s_length['min'], max_value=s_length['max'], value=l_val, step=s_length['step'])

st.sidebar.markdown("---")
# Control Mode Selection
control_mode = st.sidebar.radio("Control Mode", ["Manual Frequency", "Set Harmonic Number (n)"])

if control_mode == "Manual Frequency":
    frequency_input = st.sidebar.slider("Frequency (Hz)", min_value=1.0, max_value=100.0, value=50.0, step=0.1)
    target_n = 1 # Default
else:
    target_n = st.sidebar.slider("Harmonic Number (n)", min_value=1, max_value=20, value=1, step=1, help="Number of Antinodes (Loops). Total Nodes = n + 1")
    frequency_input = 50.0 # Placeholder

st.sidebar.markdown("---")
run_animation = st.sidebar.checkbox("Start Animation", value=False)

# Analysis Section (Moved Up)
st.markdown("###  Analysis: Frequency vs. Tension")
analysis_expander = st.expander("Show Frequency-Tension Relationship Plot", expanded=False)

with analysis_expander:
    col_analysis1, col_analysis2 = st.columns([1, 3])
    with col_analysis1:
        analysis_n = st.number_input("Select Harmonic Mode (n)", min_value=1, max_value=10, value=1, step=1)
        sweep_tension = st.checkbox("Animate Tension Sweep", value=False, help="Automatically vary tension to see the point move along the curve.")
    
    analysis_plot_placeholder = st.empty()

st.markdown("### Visualization")

# View Controls
with st.expander("Adjust Plot View (Zoom/Pan)"):
    col_view1, col_view2 = st.columns(2)
    with col_view1:
        y_lim = st.slider("Vertical Scale (Amplitude)", 0.05, 1.0, 0.3, 0.05)
    with col_view2:
        x_view = st.slider("Horizontal View (Position)", 0.0, length, (0.0, length))

plot_placeholder = st.empty()

# Main Loop Logic
start_time = time.time()

# Determine if we are in a loop
is_running = run_animation or sweep_tension

if not is_running:
    # Single frame render
    current_tension = tension_input
    
    # Calculate Physics
    wave_speed = np.sqrt(current_tension / linear_density)
    
    if control_mode == "Manual Frequency":
        current_frequency = frequency_input
    else:
        current_frequency = target_n * wave_speed / (2 * length)
        
    wavelength = wave_speed / current_frequency
    k = 2 * np.pi / wavelength
    harmonic_number = (2 * length) / wavelength
    
    # Render Analysis Plot
    fig_analysis, ax_analysis = plt.subplots(figsize=(8, 4))
    fig_analysis.patch.set_facecolor('#0E1117')
    ax_analysis.set_facecolor('#0E1117')
    
    t_values = np.linspace(0.1, 100.0, 200)
    factor = analysis_n / (2 * length * np.sqrt(linear_density))
    f_values = factor * np.sqrt(t_values)
    
    ax_analysis.plot(t_values, f_values, color='#00FFFF', linewidth=2, label=f'Mode n={analysis_n}')
    
    # Current point
    required_f_at_current_T = factor * np.sqrt(current_tension)
    
    ax_analysis.plot(current_tension, required_f_at_current_T, 'o', color='#FF0055', markersize=10)
    ax_analysis.annotate(f'T={current_tension:.1f}N\nReq f={required_f_at_current_T:.1f}Hz', 
                         xy=(current_tension, required_f_at_current_T), 
                         xytext=(current_tension+5, required_f_at_current_T-10),
                         color='white', arrowprops=dict(arrowstyle='->', color='white'))
    
    ax_analysis.set_xlabel("String Tension (N)", color='white')
    ax_analysis.set_ylabel("Required Frequency (Hz)", color='white')
    ax_analysis.set_title(f"Frequency vs Tension (Mode n={analysis_n})", color='white')
    ax_analysis.grid(True, alpha=0.1, color='white')
    ax_analysis.tick_params(colors='white')
    for spine in ax_analysis.spines.values():
        spine.set_color('white')
    
    with analysis_expander:
        analysis_plot_placeholder.pyplot(fig_analysis)
    plt.close(fig_analysis)

    # Render Wave Plot
    x = np.linspace(0, length, 500)
    y_envelope_upper = 0.1 * 2 * np.sin(k * x)
    y_envelope_lower = -0.1 * 2 * np.sin(k * x)
    
    max_m = int(2 * length / wavelength)
    node_indices = np.arange(0, max_m + 1)
    node_positions = node_indices * wavelength / 2
    node_positions = node_positions[node_positions <= length + 1e-5]
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=80)
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    ax.plot(x, y_envelope_upper, '--', color='white', alpha=0.3)
    ax.plot(x, y_envelope_lower, '--', color='white', alpha=0.3)
    
    omega = 2 * np.pi * current_frequency
    y_instant = 0.1 * 2 * np.sin(k * x) * np.cos(0) # t=0
    ax.plot(x, y_instant, '-', color='#00FFFF', linewidth=2)
    ax.plot(node_positions, np.zeros_like(node_positions), 'o', color='#FF0055', markersize=8)
    
    ax.set_xlim(x_view[0], x_view[1])
    ax.set_ylim(-y_lim, y_lim)
    ax.set_xlabel("Position (m)", color='white')
    ax.set_ylabel("Displacement", color='white')
    ax.set_title(f"Standing Wave (n ≈ {harmonic_number:.2f})", color='white')
    
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.grid(True, alpha=0.1, color='white')
    
    plot_placeholder.pyplot(fig)
    plt.close(fig)

else:
    # Animation Loop
    while True:
        elapsed = time.time() - start_time
        
        # Calculate dynamic tension if sweeping
        if sweep_tension:
            # Sweep from 0.1 to 100 and back
            # Period of 10 seconds
            sweep_phase = (elapsed % 10) / 10 * 2 * np.pi
            # Map -1..1 to 0.1..100
            # Let's use a smoother mapping
            current_tension = 50 + 49.9 * np.sin(sweep_phase)
        else:
            current_tension = tension_input
            
        # Calculate Physics
        wave_speed = np.sqrt(current_tension / linear_density)
        
        if control_mode == "Manual Frequency":
            current_frequency = frequency_input
        else:
            current_frequency = target_n * wave_speed / (2 * length)
            
        wavelength = wave_speed / current_frequency
        k = 2 * np.pi / wavelength
        harmonic_number = (2 * length) / wavelength
        
        # 1. Render Analysis Plot
        if sweep_tension:
             # Only re-render analysis plot if tension is changing
            fig_analysis, ax_analysis = plt.subplots(figsize=(8, 4), dpi=80) # Increased DPI for better quality
            fig_analysis.patch.set_facecolor('#0E1117')
            ax_analysis.set_facecolor('#0E1117')
            
            t_values = np.linspace(0.1, 100.0, 100)
            factor = analysis_n / (2 * length * np.sqrt(linear_density))
            f_values = factor * np.sqrt(t_values)
            
            ax_analysis.plot(t_values, f_values, color='#00FFFF', linewidth=2)
            
            required_f_at_current_T = factor * np.sqrt(current_tension)
            ax_analysis.plot(current_tension, required_f_at_current_T, 'o', color='#FF0055', markersize=10)
            
            # Add annotation following the point
            # Flip text to left if we are near the right edge to prevent clipping
            xytext_offset = (10, -10) if current_tension < 70 else (-110, -10)
            
            ax_analysis.annotate(f'T={current_tension:.1f}N\nReq f={required_f_at_current_T:.1f}Hz', 
                         xy=(current_tension, required_f_at_current_T), 
                         xytext=xytext_offset, textcoords='offset points',
                         color='white', fontsize=12,
                         arrowprops=dict(arrowstyle='->', color='white'),
                         bbox=dict(boxstyle="round,pad=0.3", fc="#0E1117", ec="none", alpha=0.7))

            ax_analysis.set_title(f"Frequency vs Tension (Mode n={analysis_n})", color='white')
            
            # Minimal styling for speed
            ax_analysis.tick_params(colors='white')
            for spine in ax_analysis.spines.values(): spine.set_color('white')
            ax_analysis.grid(True, alpha=0.1, color='white')
            
            # Convert to image for speed
            fig_analysis.canvas.draw()
            img_analysis = np.array(fig_analysis.canvas.renderer.buffer_rgba())
            plt.close(fig_analysis)
            
            analysis_plot_placeholder.image(img_analysis, use_container_width=True)

        # 2. Render Wave Plot
        if run_animation or sweep_tension:
            visual_time = elapsed * 0.5
            
            x = np.linspace(0, length, 200) # Reduced points
            y_envelope_upper = 0.1 * 2 * np.sin(k * x)
            y_envelope_lower = -0.1 * 2 * np.sin(k * x)
            
            max_m = int(2 * length / wavelength)
            node_indices = np.arange(0, max_m + 1)
            node_positions = node_indices * wavelength / 2
            node_positions = node_positions[node_positions <= length + 1e-5]
            
            fig, ax = plt.subplots(figsize=(10, 5), dpi=80)
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            
            ax.plot(x, y_envelope_upper, '--', color='white', alpha=0.3)
            ax.plot(x, y_envelope_lower, '--', color='white', alpha=0.3)
            
            omega = 2 * np.pi * current_frequency
            y_instant = 0.1 * 2 * np.sin(k * x) * np.cos(omega * visual_time)
            ax.plot(x, y_instant, '-', color='#00FFFF', linewidth=2)
            ax.plot(node_positions, np.zeros_like(node_positions), 'o', color='#FF0055', markersize=8)
            
            ax.set_xlim(x_view[0], x_view[1])
            ax.set_ylim(-y_lim, y_lim)
            ax.set_xlabel("Position (m)", color='white')
            ax.set_ylabel("Displacement", color='white')
            ax.set_title(f"Standing Wave (n ≈ {harmonic_number:.2f})", color='white')
            
            ax.tick_params(colors='white')
            for spine in ax.spines.values(): spine.set_color('white')
            ax.grid(True, alpha=0.1, color='white')
            
            fig.canvas.draw()
            img_wave = np.array(fig.canvas.renderer.buffer_rgba())
            plt.close(fig)
            
            plot_placeholder.image(img_wave, use_container_width=True)
        
        time.sleep(0.02)
