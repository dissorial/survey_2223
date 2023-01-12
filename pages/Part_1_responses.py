import streamlit as st
from pathlib import Path
import pandas as pd
from utils.part1 import get_mean_data, get_median_data, get_std_data, get_question_data, plot_bar_chart
from utils.utils import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Learning & Engagement',
                   initial_sidebar_state='expanded')


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


st.info('# Learning & Engagement: Part 1 responses')
st.warning(
    '*For the best viewing experience, open the menu in the top right corner, click "Settings" and choose a "Light" theme.*'
)

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('Please log in first in the introduction section')
    st.stop()

if logged_user not in ['zavodsky', 'klagova', 'kurian', 'sapak']:
    st.error('You are not authorized to view this page')
    st.stop()

st.markdown('## Response rate information')

st.markdown(read_markdown_file("markdown/response_rate_information.md"),
            unsafe_allow_html=True)

df = decrypt_data('part_1_data_merged.csv')

st.info('## Questions 1-4')
selected_question = st.selectbox(
    label='Choose a question from the questionnaire to display',
    options=df.columns[3:-4].tolist())

years_available = df['Year'].unique().tolist()
programs_available = df['Program'].unique().tolist()

with st.sidebar:
    st.markdown('**Filters**')
    selected_years = st.multiselect(label='Select a year',
                                    options=years_available,
                                    default=years_available)

    selected_programs = st.multiselect(label='Select a program',
                                       options=programs_available,
                                       default=programs_available)
    st.markdown(
        '*Please note that interacting with the filters above will filter responses to everything you see on this page.*'
    )

merged_filtered_by_year_program = df[(df['Year'].isin(selected_years))
                                     & (df['Program'].isin(selected_programs))]

merged_filtered_by_question = get_question_data(df, selected_question)

merged_bar_chart = plot_bar_chart(merged_filtered_by_question)
st.pyplot(merged_bar_chart, use_container_width=True)

st.info('## Question 5')
st.markdown(
    '- **My concerns about the quality of learning that I expressed this year have been addressed (1 - No, not at all  vs 10 - Yes, all of them)**'
)
quality_of_learning_merged = merged_filtered_by_year_program[[
    merged_filtered_by_year_program.columns[7], 'data_year'
]]

leftcol, middlecol, rightcol = st.columns(3)
with leftcol:
    mean_data_21 = get_mean_data(quality_of_learning_merged, '2021-22')
    mean_data_22 = get_mean_data(quality_of_learning_merged, '2022-23')
    st.metric(label='Mean',
              value=mean_data_22,
              delta='{} from previous year'.format(
                  round(mean_data_22 - mean_data_21, 2)))
with middlecol:
    median_data_21 = get_median_data(quality_of_learning_merged, '2021-22')
    median_data_22 = get_median_data(quality_of_learning_merged, '2022-23')
    st.metric(label='Median',
              value=median_data_22,
              delta='{} from previous year'.format(
                  round(median_data_22 - median_data_21, 2)))
with rightcol:
    std_data_21 = get_std_data(quality_of_learning_merged, '2021-22')
    std_data_22 = get_std_data(quality_of_learning_merged, '2022-23')
    st.metric(label='Standard deviation',
              value=std_data_22,
              delta='{} from previous year'.format(
                  round(std_data_22 - std_data_21, 2)))
