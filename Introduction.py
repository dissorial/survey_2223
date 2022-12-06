import streamlit as st

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
    st.info('# Fall 2022: Learning & Engagement Survey Analysis')
    st.markdown(
        '*For the best viewing experience, open the menu in the top right corner, click "Settings" and choose a "Light" theme.*'
    )
    st.markdown('## 1.0 – Introduction')
    st.write(
        'On the left sidebar, there are two pages you can visit. Below is an explanation of each page.'
    )
    st.markdown('### 1.1 – Overview of all classes')
    st.markdown(
        '- On this page, you will find a visual comparison of the survey responses for a particular question across any number of selected classes. You can also select a specific year and/or program to filter the classes you are comparing.'
    )
    st.markdown('### 1.2 – Overview of a single class')
    st.markdown(
        '- On this page, you will find statistics for all quantitative survey questions for a particular class. If you select a class that you teach, you will also be able to see the additional comments that students left for your class in the survey.'
    )

    st.error(
        '**Each page provides detailed explanations of what it does, who it is for, and how to use it. Please go through each page from top to bottom and read these explanations carefully.**'
    )
