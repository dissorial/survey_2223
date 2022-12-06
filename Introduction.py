import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from utils import seaborn_violin_plot, plot_bar_chart_classes, TEACHERS
from functools import reduce

st.set_page_config(layout="wide",
                   page_title='Introduction',
                   initial_sidebar_state='expanded')


def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]):
            st.session_state["password_correct"] = True
            st.session_state['logged_user'] = st.session_state["username"]
            del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password",
                      type="password",
                      on_change=password_entered,
                      key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password",
                      type="password",
                      on_change=password_entered,
                      key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    st.session_state['logged_in'] = True
    st.title('Fall 2022: Learning & Engagement Survey Analysis')
    st.info(
        'For the best viewing experience, open the menu in the top right corner, click "Settings", make sure "Wide mode" is checked, and choose a "Light" theme.'
    )
    st.subheader(
        'On the left sidebar, there are several pages you can visit. Below is an explanation of each page.'
    )
    st.markdown('## Class overview')
    st.markdown(
        '-  Summary statistics for each class you teach or have access to for a particular question from the survey. In other words, this allows for a visual comparison of the responses for a particular question across several classes. As such, this utility of this page is higher the more classes you teach.'
    )
    st.markdown('## Class drilldown')
    st.markdown(
        '- This page functions as somewhat of an inverse of "Class overview". Instead of comparing several classes for one question, this page allows you to compare the responses for all survey questions for one class. This page is useful for getting a sense of how students in a particular class responded to the survey as a whole.'
    )
