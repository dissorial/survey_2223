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
    def password_entered():
        if (st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]):
            st.session_state["password_correct"] = True
            st.session_state['logged_user'] = st.session_state["username"]
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password",
                      type="password",
                      on_change=password_entered,
                      key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password",
                      type="password",
                      on_change=password_entered,
                      key="password")
        st.error("😕 User not known or password incorrect")
        return False
    else:
        return True


if check_password():
    st.session_state['logged_in'] = True
    st.title('Fall 2022: Learning & Engagement Survey Analysis')
    st.info(
        'For the best viewing experience, open the menu in the top right corner, click "Settings", make sure "Wide mode" is checked, and choose a "Light" theme.'
    )
    st.subheader(
        'On the left sidebar, there are two pages you can visit. Below is an explanation of each page.'
    )
    st.markdown('## Class drilldown')
    st.markdown(
        '- This page allows you to view statistics for all quantitative survey questions for a selected class. If you select a class that you teach, you will also be able to see the additional comments that students left for your class in the survey.'
    )
    st.markdown('## Class overview')
    st.markdown(
        '- This page allows for a visual comparison of the responses for a particular question across any number of selected classes. You can also select a specific year and/or program to filter the classes you are comparing.'
    )
