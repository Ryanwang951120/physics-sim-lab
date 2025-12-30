import streamlit as st
import sys
import os

# Add parent directory to path to allow importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
utils.add_footer()

st.title("⚙️ Simulation Settings (設定)")
st.markdown("Adjust the range limits for sliders in the simulations. (調整模擬中滑桿的數值範圍)")

utils.init_settings()

def render_setting_group(title, prefix):
    st.subheader(title)
    keys = [k for k in st.session_state['settings'].keys() if k.startswith(prefix)]
    
    for key in keys:
        setting = st.session_state['settings'][key]
        is_int = isinstance(setting['default'], int)
        step = setting.get('step', 1 if is_int else 0.1)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{key}**")
        
        with col2:
            val_min = int(setting['min']) if is_int else float(setting['min'])
            new_min = st.number_input(f"Min", value=val_min, step=step, key=f"{key}_min")
            
        with col3:
            val_max = int(setting['max']) if is_int else float(setting['max'])
            new_max = st.number_input(f"Max", value=val_max, step=step, key=f"{key}_max")
            
        if new_min >= new_max:
            st.error(f"⚠️ Error: Min must be less than Max")
        else:
            st.session_state['settings'][key]['min'] = new_min
            st.session_state['settings'][key]['max'] = new_max

render_setting_group("1. Standing Waves", "sw_")
st.markdown("---")
render_setting_group("2. Chladni Patterns", "ch_")
st.markdown("---")
render_setting_group("3. Circular Wave", "cw_")
st.markdown("---")
render_setting_group("4. Longitudinal Wave", "lw_")

if st.button("Reset All to Defaults"):
    del st.session_state['settings']
    utils.init_settings()
    st.rerun()
