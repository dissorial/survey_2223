import streamlit as st
import pandas as pd
from utils.utils import plot_bar_chart_classes, CLASS_LIST, decrypt_data
from functools import reduce

st.set_page_config(layout="wide",
                   page_title='Class overview',
                   initial_sidebar_state='expanded')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('Please log in first in the introduction section')
    st.stop()

st.info('# Overview: All classes')

st.markdown(
    '- The primary purpose of this page is compare answers for a particular question in the survey across any number of selected classes.'
)

df = decrypt_data('survey_data_2223.csv')

questions = df.columns[4:-4].tolist()


def get_classes_from_categories(class_category_input):
    res = []
    for key, value in CLASS_LIST.items():
        if value == class_category_input:
            res.append(key)
    return res


ces_classes = get_classes_from_categories('CES')
csem_classes = get_classes_from_categories('CSem')
el_classes = get_classes_from_categories('EL')
ell_classes = get_classes_from_categories('ELL')
leaf_core_classes = get_classes_from_categories('LEAF Core')
math_classes = get_classes_from_categories('MATH')
science_classes = get_classes_from_categories('SCIE')
language_classes = get_classes_from_categories('Language')
ap_classes = get_classes_from_categories('AP')

all_classes_local = ces_classes + csem_classes + el_classes + ell_classes + leaf_core_classes + math_classes + science_classes + language_classes + ap_classes

st.info('## 1.0 – Class filters')
st.markdown(
    '- Because there are many classes one can choose from, they were split into several general categories for easier selection. You can select any number of classes from any number of categories. If you want to select all classes from a particular category, you can click the "Select all" button next to the category name. Clicking the "Select all" button again will deselct all classes from that category.'
)
no_selected_classes_container = st.container()
left_1, mid_1, right_1 = st.columns(3)
with left_1:
    el_container = st.container()
    all_el = st.checkbox('Select all')
    if all_el:
        filtered_el_classes = el_container.multiselect('Select EL classes',
                                                       el_classes,
                                                       default=el_classes)
    else:
        filtered_el_classes = el_container.multiselect('Select EL classes',
                                                       el_classes)

with mid_1:
    science_container = st.container()
    all_science = st.checkbox('Select all', key='science')
    if all_science:
        filtered_science_classes = science_container.multiselect(
            'Select science classes', science_classes, default=science_classes)
    else:
        filtered_science_classes = science_container.multiselect(
            'Select science classes', science_classes)

with right_1:

    ell_container = st.container()
    all_ell = st.checkbox('Select all', key='ell')
    if all_ell:
        filtered_ell_classes = ell_container.multiselect('Select ELL classes',
                                                         ell_classes,
                                                         default=ell_classes)
    else:
        filtered_ell_classes = ell_container.multiselect(
            'Select ELL classes', ell_classes)

left_2, mid_2, right_2 = st.columns(3)

with left_2:
    ces_container = st.container()
    all_ces = st.checkbox('Select all', key='ces')
    if all_ces:
        filtered_ces_classes = ces_container.multiselect('Select CES classes',
                                                         ces_classes,
                                                         default=ces_classes)
    else:
        filtered_ces_classes = ces_container.multiselect(
            'Select CES classes', ces_classes)

with mid_2:
    leaf_core_container = st.container()
    all_leaf_core = st.checkbox('Select all', key='leaf_core')
    if all_leaf_core:
        filtered_leaf_core_classes = leaf_core_container.multiselect(
            'Select LEAF core classes',
            leaf_core_classes,
            default=leaf_core_classes)
    else:
        filtered_leaf_core_classes = leaf_core_container.multiselect(
            'Select LEAF core classes', leaf_core_classes)

with right_2:
    csem_container = st.container()
    all_csem = st.checkbox('Select all', key='csem')
    if all_csem:
        filtered_csem_classes = csem_container.multiselect(
            'Select Character Seminar classes',
            csem_classes,
            default=csem_classes)
    else:
        filtered_csem_classes = csem_container.multiselect(
            'Select Character Seminar classes', csem_classes)

left_3, right_3 = st.columns(2)
with left_3:
    math_container = st.container()
    all_math = st.checkbox('Select all', key='math')
    if all_math:
        filtered_math_classes = math_container.multiselect(
            'Select math classes', math_classes, default=math_classes)
    else:
        filtered_math_classes = math_container.multiselect(
            'Select math classes', math_classes)

with right_3:
    nl_container = st.container()
    all_nl = st.checkbox('Select all', key='nl')
    if all_nl:
        filtered_nl_classes = nl_container.multiselect(
            'Select language classes',
            language_classes,
            default=language_classes)
    else:
        filtered_nl_classes = nl_container.multiselect(
            'Select language classes', language_classes)

ap_container = st.container()
all_ap = st.checkbox('Select all', key='ap')
if all_ap:
    filtered_ap_classes = ap_container.multiselect('Select AP classes',
                                                   ap_classes,
                                                   default=ap_classes)
else:
    filtered_ap_classes = ap_container.multiselect('Select AP classes',
                                                   ap_classes)

filtered_classes = filtered_ces_classes + filtered_csem_classes + filtered_el_classes + filtered_ell_classes + filtered_leaf_core_classes + filtered_math_classes + filtered_nl_classes + filtered_science_classes + filtered_ap_classes

if (len(filtered_classes) == 0):
    no_selected_classes_container.warning(
        'Please select at least one class to continue.')
    st.stop()

class_df = df[df['Class'].isin(filtered_classes)]

years_available = class_df['Year'].unique().tolist()
programs_available = class_df['Program'].unique().tolist()

st.info('## 1.1 – Other filters')
st.markdown('- Here, you can filter the responses by year and program.')
left_filter_col1, right_filter_col1 = st.columns(2)
with left_filter_col1:
    selected_years = st.multiselect(label='Select a year',
                                    options=years_available,
                                    default=years_available)

with right_filter_col1:
    selected_programs = st.multiselect(label='Select a program',
                                       options=programs_available,
                                       default=programs_available)

st.info('## 1.2 – Visualization tools')
st.markdown(
    '- Here, you can further customize the visualization depending on what you want to see displayed. These are optional parameters and you can leave them as is if you do not want to change them.'
)
left_filter_col2, right_filter_col2 = st.columns(2)
with left_filter_col2:
    color_input = st.selectbox(
        label=
        'Select a metric that will be used to color the bar charts at the bottom of the page',
        options=['Response rate (%)', 'Class size', 'Respondents'])

with right_filter_col2:
    selected_aggfunction = st.selectbox(
        label='Choose how to aggregate the data in the bar charts',
        options=['Mean', 'Median'],
        key='aggfunction')

st.info('## 1.3 – Select a question')
selected_question = st.selectbox(
    label='Select one of the survey questions to be plotted below.',
    options=questions)

question_df = df[[selected_question]]
question_df_std = question_df.std()
question_df_mean = question_df.mean()
question_df_median = question_df.median()

st.info('## 1.4 – Question statistics')
st.markdown(
    'The mean, median and standard deviation values below are calculated across the entire dataset of responses (all classes, years and programs). The purpose of this is to give you a sense of how the students respondend to this question in general.'
)
l_expander_col, m_expander_col, r_expander_col = st.columns(3)
with l_expander_col:
    st.metric(label='Mean',
              value=round(question_df_mean[selected_question], 1))
with m_expander_col:
    st.metric(label='Median',
              value=round(question_df_median[selected_question], 1))
with r_expander_col:
    st.metric(label='Standard deviation',
              value=round(question_df_std[selected_question], 1))

st.markdown(
    'In total, there were 722 responses responses in the survey across 74 different classes by 112 students. Each student filled out the survey ~6 times on average. '
)

st.info('## 1.5 – Charts')
st.warning('Hover over the bar charts to see more information')
filtered_df = class_df[(class_df['Year'].isin(selected_years))
                       & (class_df['Program'].isin(selected_programs))]

isolated_df = filtered_df[[selected_question, 'Class', 'Program', 'Year']]

class_std = isolated_df.groupby(['Class']).std().reset_index()
class_mean = isolated_df.groupby('Class').mean().reset_index()
class_median = isolated_df.groupby('Class').median().reset_index()
grouped_metrics = [class_std, class_mean, class_median]

df_metrics = reduce(
    lambda left, right: pd.merge(left, right, on=['Class'], how='left'),
    grouped_metrics)

response_stats = filtered_df[[
    'Class', 'Response rate (%)', 'Class size', 'Respondents'
]].groupby('Class').mean().reset_index()

merged_df = pd.merge(df_metrics, response_stats, on='Class', how='left')

all_bar_chart = plot_bar_chart_classes(merged_df, selected_aggfunction,
                                       color_input)
try:
    st.altair_chart(all_bar_chart, use_container_width=True)
except ValueError:
    no_selected_classes_container.error('Choose at least one class from below')
    st.stop()
