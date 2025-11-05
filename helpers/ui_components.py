import streamlit as st

def message_bubble(sender, text, is_user=False):
    bg = "#007BFF" if is_user else "#F1F1F1"
    color = "white" if is_user else "black"
    align = "right" if is_user else "left"
    st.markdown(
        f"<div style='background:{bg}; color:{color}; padding:10px; border-radius:10px; text-align:{align}; margin:5px;'>{text}</div>",
        unsafe_allow_html=True,
    )

def section_header(title, icon="⚖️"):
    st.markdown(f"## {icon} {title}")

def info_card(title, content):
    st.markdown(
        f"<div style='background:#F9FAFB; padding:10px; border-radius:8px; margin:4px 0; box-shadow:0 0 3px rgba(0,0,0,0.1);'><b>{title}</b><br>{content}</div>",
        unsafe_allow_html=True,
    )