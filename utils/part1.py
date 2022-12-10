import pandas as pd
import altair as alt
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st


def plot_barchart_answers(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Count',
                axis=alt.Axis(
                    gridOpacity=0.5,
                    title='Number of students who chose this answer choice',
                    format='.0f')),
        y=alt.Y('Responses',
                sort=alt.EncodingSortField(field='Count',
                                           op='sum',
                                           order='descending'),
                axis=alt.Axis(labels=False,
                              title='Answer choice',
                              gridOpacity=0)))

    chart_text = chart.mark_text(align='left', baseline='middle',
                                 dx=5).encode(text=alt.Text('Responses'))

    return (chart + chart_text).configure_view(strokeWidth=0).configure_axis(
        grid=True, labelLimit=1000)


def get_question_data(df, chosen_question):
    studentinfo = df[['Year']]

    isolated_question_df = df[[chosen_question, 'Year']]
    split_isolated_df = isolated_question_df[chosen_question].str.split(
        ',', expand=True)

    merged = pd.concat([split_isolated_df, studentinfo], axis=1)

    melted = merged.melt(id_vars=['Year'], value_name='Responses')
    melted['Count'] = 1
    # grouped['Responses'] = grouped['Responses'].str.strip()
    melted['Responses'] = melted['Responses'].str.strip()
    grouped = melted.groupby(['Responses']).sum().reset_index()

    return grouped


def get_mean_data(df):
    return round(df[df.columns[0]].mean(), 1)


def get_median_data(df):
    return round(df[df.columns[0]].median(), 1)


def get_std_data(df):
    return round(df[df.columns[0]].std(), 2)


def get_remaining_questions(df, free_response_question_input):
    return df[[free_response_question_input]]
