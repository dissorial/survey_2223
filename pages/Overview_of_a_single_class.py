import streamlit as st
import pandas as pd
from utils import seaborn_violin_plot, TEACHERS, ALL_ACCESS, decrypt_data, altair_class_barchart
from functools import reduce
from PIL import Image

st.set_page_config(layout="wide",
                   page_title='Class drilldown',
                   initial_sidebar_state='expanded')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('Please log in first in the introduction section')
    st.stop()

st.info('# Overview: single class')
st.markdown(
    '- The primary purpose of this page is to provide a detailed overview of each question in the survey for a particular class'
)
violin_image = Image.open('assets/violin_explanation.png')

st.info('## 1.0 – Explanation of the charts below')
st.markdown(
    '- On this page, you will see charts that are similar to the example below. In this example, you can see the following: 50% of responses fall between the values of 7 and 8; ~25% of responses fall between the values of 6 and 7; ~25% of responses fall between the values of 8 and 9; the median value is 8.'
)
st.image(violin_image, use_column_width=True)

df = decrypt_data('survey_data_2223.csv')
# df_summary = pd.read_csv('survey_data_2223_melted.csv')
df_summary = decrypt_data('survey_data_2223_summary.csv')

questions = df.columns[4:-4].tolist()

classes_available = df['Class'].unique().tolist()

st.info('## 1.1 – Filter and select')
st.markdown(
    '- Here, you can select the class you want to see the results for. To choose a class, you can either scroll through the list of classes or directly write the name of one you would like to see. Additionally, you select or deselect the years and programs you would like to see the results for, and the charts below will be updated accordingly.'
)
selected_class = st.selectbox(label='Select a class',
                              options=classes_available)

list_of_teachers = [x for x in TEACHERS.keys()]

filtered_df_by_class = df[(df['Class'] == selected_class)]
summary_filtered_by_class = df_summary[(df_summary['Class'] == selected_class)]
filtered_df_by_class_comments = filtered_df_by_class[['Comments']].dropna()

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

question_std = meta_filtered.groupby('Class').std().reset_index()
question_mean = meta_filtered.groupby('Class').mean().reset_index()
grouped_metrics = [question_std, question_mean]

df_metrics = reduce(
    lambda left, right: pd.merge(left, right, on='Class', how='left'),
    grouped_metrics)

class_size = filtered_df_by_class.iloc[0]['Class size']
n_respondents = filtered_df_by_class.iloc[0]['Respondents']

st.info('## 1.2 – Summary chart')
st.markdown(
    '- The chart below provides a simple summary of the results for the selected class, which can be useful for getting a quick glance of its strengths from the students’ perspective.'
)
st.markdown(
    '- Please note that the statements "I want to learn as much as possible in this class", "I want to get the best mark/grade.", and "I just want to pass the class." are not included in the chart below. This is to discourage rapid comparisons between classes that may lack the sufficient nuance to be meaningful.'
)
aggfunc = st.selectbox('Select an aggregation function for the chart below',
                       options=['mean', 'median'])
summary_filtered_by_class_year_program = filter_df_by_class_program(
    summary_filtered_by_class, selected_years, selected_programs)
summary_bar_chart = altair_class_barchart(
    summary_filtered_by_class_year_program, aggfunc)
st.altair_chart(summary_bar_chart, use_container_width=True)

st.info('## 1.3 – Detailed charts')
st.markdown(
    '- To see the additional comments left by students in this class, scroll to the bottom of the page.'
)
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

        leftcol.warning('Figure {}'.format(i + 1))
        if (i == 14):
            leftcol.markdown(
                '- Be aware that unlike with other questions, lower values on this question are more desirable.'
            )
        leftcol.pyplot(chart)
        leftcol.markdown(
            f'#### Mean: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF;background-color:{get_styles_mean(all_mean[i])}">**{round(all_mean[i],1)}**</span>, Standard deviation: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF; background-color:{get_styles_stdev(all_stdev[i])}">{round(all_stdev[i],1)}</span>',
            unsafe_allow_html=True)
        leftcol.markdown('---')

    else:
        rightcol.warning('Figure {}'.format(i + 1))
        rightcol.pyplot(chart)
        rightcol.markdown(
            f'#### Mean: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF;background-color:{get_styles_mean(all_mean[i])}">**{round(all_mean[i],1)}**</span>, Standard deviation: <span style="border-radius:4px;padding:0 6px; color:#FFFFFF; background-color:{get_styles_stdev(all_stdev[i])}">{round(all_stdev[i],1)}</span>',
            unsafe_allow_html=True)
        rightcol.markdown('---')
        if (i == 13):
            rightcol.warning('Comments')
            rightcol.write(
                'Please note that the numbers in the first column have no relevance to the actual number or content of comments left by students.'
            )
            if logged_user in ALL_ACCESS:
                rightcol.table(filtered_df_by_class_comments)
            elif (selected_class in TEACHERS[logged_user]):
                rightcol.table(filtered_df_by_class_comments)