import streamlit as st

def add_footer():
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #808080;
        text-align: center;
        padding: 10px;
        font-size: 1.0em;
        border-top: 1px solid #333;
        z-index: 1000;
    }
    .content-spacer {
        height: 50px;
    }
    </style>
    <div class="content-spacer"></div>
    <div class="footer">
        One- and Two-Dimensional Standing Waves | By Group D3 | © 2025  Credit 王宇恩 巫柏翰 李宇桐
    </div>
    """, unsafe_allow_html=True)

def init_settings():
    if 'settings' not in st.session_state:
        st.session_state['settings'] = {
            # Page 1: Standing Waves
            'sw_tension': {'min': 0.1, 'max': 200.0, 'default': 10.0, 'step': 0.1},
            'sw_density': {'min': 0.0001, 'max': 0.0500, 'default': 0.0010, 'step': 0.0001},
            'sw_length': {'min': 0.1, 'max': 10.0, 'default': 1.0, 'step': 0.1},
            
            # Page 2: Chladni
            'ch_n': {'min': 1, 'max': 50, 'default': 3, 'step': 1},
            'ch_m': {'min': 1, 'max': 50, 'default': 5, 'step': 1},
            
            # Page 3: Circular
            'cw_n': {'min': 2, 'max': 20, 'default': 3, 'step': 1},
            'cw_speed': {'min': 0.1, 'max': 10.0, 'default': 2.0, 'step': 0.1},
            'cw_amp': {'min': 0.05, 'max': 2.0, 'default': 0.2, 'step': 0.05},
            
            # Page 4: Longitudinal
            'lw_particles': {'min': 20, 'max': 200, 'default': 50, 'step': 5},
            'lw_n': {'min': 1, 'max': 20, 'default': 3, 'step': 1},
            'lw_amp': {'min': 0.1, 'max': 3.0, 'default': 0.8, 'step': 0.1},
            'lw_speed': {'min': 0.1, 'max': 5.0, 'default': 1.0, 'step': 0.1},
        }

def get_setting(key):
    init_settings()
    return st.session_state['settings'][key]

