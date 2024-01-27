import streamlit as st

from streamlit_extras.switch_page_button import switch_page
st.set_page_config(page_title="HealthOracle", page_icon="💊", layout="wide")
st.markdown(
    """
        <style>
            [data-testid="stSidebarNav"] {
                background-repeat: no-repeat;                
            }
            [data-testid="stSidebarNav"]::before {
                content: "HealthOracle";
                margin-left: 20px;
                margin-top: 20px;

                font-size: 30px;
                text-align: center;
                position: relative;
            }
        </style>
        """,
    unsafe_allow_html=True,
)

st.title("Welcome to HealthOracle: Decode Your Health")

st.write(
    "This project is made with the goal to help people identify diease with the help of respective scans."
)

aps = st.button("Find Out!")
if aps:
    switch_page("Brain Lens")


