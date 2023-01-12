import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_bar_chart(df):
    fig = plt.figure(figsize=(10, 5))
    chart = sns.barplot(data=df,
                        x='Count',
                        y='Responses',
                        hue='data_year',
                        orient='h')
    chart.set_title('Response comparison between 2021-22 and 2022-23')
    chart.set_xlabel('Percentage of responses')
    chart.set_ylabel('')
    chart.set_xticks(np.arange(0, 100, 10))
    chart.set_xticklabels(np.arange(0, 100, 10))
    chart.set_yticklabels(chart.get_yticklabels(), rotation=0)
    chart.legend(loc='upper right')
    chart.grid(axis='x')
    return fig


def get_question_data(df, chosen_question):
    responseYear = df[['data_year']]
    isolated_question_df = df[[chosen_question, 'data_year']]
    split_isolated_df = isolated_question_df[chosen_question].str.split(
        ',', expand=True)
    merged = pd.concat([split_isolated_df, responseYear], axis=1)
    melted = merged.melt(id_vars=['data_year'], value_name='Responses')
    melted['Count'] = 1
    melted['Responses'] = melted['Responses'].str.strip()
    grouped = melted.groupby(['Responses', 'data_year']).sum().reset_index()
    filtered_group = grouped[(grouped['Count'] != 0) & (grouped['Count'] != 1)]
    filtered_group['Count'] = filtered_group.apply(
        lambda row: (row['Count'] / 91) * 100
        if row['data_year'] == '2021-22' else (row['Count'] / 58) * 100,
        axis=1)
    return filtered_group


def get_mean_data(df, data_year):
    filtered_df = df[df['data_year'] == data_year]
    return round(filtered_df[filtered_df.columns[0]].mean(), 2)


def get_median_data(df, data_year):
    filtered_df = df[df['data_year'] == data_year]
    return round(filtered_df[filtered_df.columns[0]].median(), 2)


def get_std_data(df, data_year):
    filtered_df = df[df['data_year'] == data_year]
    return round(filtered_df[filtered_df.columns[0]].std(), 2)