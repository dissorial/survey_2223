import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from utils import seaborn_violin_plot, plot_bar_chart_classes, TEACHERS, ALL_ACCESS, CLASS_LIST
from functools import reduce
from PIL import Image

st.set_page_config(layout="wide",
                   page_title='Introduction',
                   initial_sidebar_state='expanded')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('Please log in first in the introduction section')
    st.stop()

st.title('Learning & Engagement 2022/2023')

violin_image = Image.open('assets/violin_explanation.png')

with st.expander('Explanation of the charts below'):
    st.image(violin_image, use_column_width=True)

df = pd.read_csv('sample_test.csv')

questions = df.columns[4:-4].tolist()

classes_available = df['Class'].unique().tolist()

selected_class = st.selectbox(label='Select a class',
                              options=classes_available)

list_of_teachers = [x for x in TEACHERS.keys()]

filtered_df_by_class = df[(df['Class'] == selected_class)]
filtered_df_by_class_comments = filtered_df_by_class[['Comments']].dropna()

if logged_user in ALL_ACCESS:
    with st.expander('Comments', expanded=True):
        st.table(filtered_df_by_class_comments)
elif (selected_class in TEACHERS[logged_user]):
    with st.expander('Comments', expanded=True):
        st.table(filtered_df_by_class_comments)

left_filter_col, right_filter_col = st.columns(2)

years_available = filtered_df_by_class['Year'].unique().tolist()
programs_available = filtered_df_by_class['Program'].unique().tolist()

with left_filter_col:
    selected_years = st.multiselect(label='Select a year',
                                    options=years_available,
                                    default=years_available)

with right_filter_col:
    selected_programs = st.multiselect(label='Select a program',
                                       options=programs_available,
                                       default=programs_available)


def filter_df_by_class_program(df, years_input, programs_input):
    df_filtered = df[(df['Year'].isin(years_input))
                     & (df['Program'].isin(programs_input))]
    return df_filtered


meta_filtered = filter_df_by_class_program(filtered_df_by_class,
                                           selected_years, selected_programs)

# meta_filtered = filtered_df_by_class.copy()
question_std = meta_filtered.groupby('Class').std().reset_index()
question_mean = meta_filtered.groupby('Class').mean().reset_index()
grouped_metrics = [question_std, question_mean]

df_metrics = reduce(
    lambda left, right: pd.merge(left, right, on='Class', how='left'),
    grouped_metrics)

class_size = filtered_df_by_class.iloc[0]['Class size']
n_respondents = filtered_df_by_class.iloc[0]['Respondents']

st.success(f'Response rate: {n_respondents} out of {class_size} students.')


def get_all_questions_mean(df, questions):
    questions_mean = []
    for question in questions:
        question_mean = df[question].mean()
        questions_mean.append(question_mean)
    return questions_mean


def get_all_questions_stdev(df, questions):
    questions_stdev = []
    for question in questions:
        question_stdev = df[question].std()
        questions_stdev.append(question_stdev)
    return questions_stdev


all_mean = get_all_questions_mean(meta_filtered, questions)
all_stdev = get_all_questions_stdev(meta_filtered, questions)


def get_all_charts(df_filtered, questions):
    charts_array = []
    for question in questions:
        chart = seaborn_violin_plot(df_filtered, question)
        charts_array.append(chart)
    return charts_array


def get_styles_mean(val):
    color = ''
    if val >= 9:
        color = '#2cba00'
    elif val >= 7:
        color = '#77D970'
    elif val >= 5:
        color = '#FBD148'
    else:
        color = '#ffa700'
    return color


def get_styles_stdev(val):
    color = ''
    if val <= 1:
        color = '#2cba00'
    elif val <= 1.5:
        color = '#77D970'
    elif val <= 2:
        color = '#FBD148'
    elif val <= 2.5:
        color = '#ffa700'
    else:
        color = '#ff0000'
    return color


all_charts = get_all_charts(meta_filtered, questions)

leftcol, rightcol = st.columns(2)
for i, chart in enumerate(all_charts):
    if i % 2 == 0:

        leftcol.info('Figure {}'.format(i + 1))
        leftcol.pyplot(chart)
        leftcol.markdown(
            f'#### Mean: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF;background-color:{get_styles_mean(all_mean[i])}">**{round(all_mean[i],1)}**</span>, Standard deviation: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF; background-color:{get_styles_stdev(all_stdev[i])}">{round(all_stdev[i],1)}</span>',
            unsafe_allow_html=True)
        leftcol.markdown('---')

    else:
        rightcol.info('Figure {}'.format(i + 1))
        rightcol.pyplot(chart)
        rightcol.markdown(
            f'#### Mean: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF;background-color:{get_styles_mean(all_mean[i])}">**{round(all_mean[i],1)}**</span>, Standard deviation: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF; background-color:{get_styles_stdev(all_stdev[i])}">{round(all_stdev[i],1)}</span>',
            unsafe_allow_html=True)
        rightcol.markdown('---')
