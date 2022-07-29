#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def return_year(data):
    return data.date.isocalendar()[0]

def return_week_num(data):
    return data.date.isocalendar()[1]

OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
#     filename1 = 'reddit-counts.json.gz'
    filename1 = sys.argv[1]

    counts = pd.read_json(filename1, lines=True)

    counts = counts.drop(counts[counts['date'].dt.year < 2012].index)
    counts = counts.drop(counts[counts['date'].dt.year > 2013].index)

    counts = counts.drop(counts[counts['subreddit'] != 'canada'].index)
    counts['year'] = counts.apply(return_year, axis =1)
    counts['week_number'] = counts.apply(return_week_num, axis =1)


    weekends = counts[(counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6)]
    weekdays = counts[(counts['date'].dt.weekday == 0) | (counts['date'].dt.weekday == 1) | (counts['date'].dt.weekday == 2) | (counts['date'].dt.weekday == 3) | (counts['date'].dt.weekday == 4)]


    # Student's T-Test
    ttest = stats.ttest_ind(weekends.comment_count, weekdays.comment_count)

    normal_weekday = stats.normaltest(weekdays.comment_count)

    normal_weekend = stats.normaltest(weekends.comment_count)

    eq_var_test = stats.levene(weekdays.comment_count,weekends.comment_count )

    
    
    # Fix 1: transforming data might save us.
    
    # referred to https://stackoverflow.com/questions/25539195/multiple-histograms-in-pandas
    # HISTOGRAM
    #     fig, ax = plt.subplots()
    #     a_heights, a_bins = np.histogram(weekends['comment_count'])
    #     b_heights, b_bins = np.histogram(weekdays['comment_count'], bins=a_bins)
    #     width = (a_bins[1] - a_bins[0])/3
    #     ax.bar(a_bins[:-1], a_heights, width=width, facecolor='cornflowerblue')
    #     ax.bar(b_bins[:-1]+width, b_heights, width=width, facecolor='seagreen')
    #     plt.legend(['weekend','weekday'])

    weekday_transf = np.sqrt(weekdays.comment_count)
    weekend_transf = np.sqrt(weekends.comment_count)
    
    weekday_transf_normal = stats.normaltest(weekday_transf)
    weekend_transf_normal = stats.normaltest(weekend_transf)
    transf_eq_var = stats.levene(weekday_transf, weekend_transf)

    
    
    # Fix 2: the Central Limit Theorem might save us.
    
    grouped_weekend = weekends.groupby(['year','week_number']).mean()
    grouped_weekday = weekdays.groupby(['year','week_number']).mean()
    
    grouped_weekend_normal= stats.normaltest(grouped_weekend.comment_count)
    grouped_weekday_normal = stats.normaltest(grouped_weekday.comment_count)
    grouped_eq_var = stats.levene(grouped_weekend.comment_count, grouped_weekday.comment_count)
    grouped_ttest = stats.ttest_ind(grouped_weekend.comment_count, grouped_weekday.comment_count)


    # Fix 3: a non-parametric test might save us. 
    utest = stats.mannwhitneyu(weekends.comment_count, weekdays.comment_count)
       

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p = ttest.pvalue,
        initial_weekday_normality_p = normal_weekday.pvalue,
        initial_weekend_normality_p = normal_weekend.pvalue,
        initial_levene_p = eq_var_test.pvalue,
        transformed_weekday_normality_p = weekday_transf_normal.pvalue,
        transformed_weekend_normality_p = weekend_transf_normal.pvalue,
        transformed_levene_p = transf_eq_var.pvalue,
        weekly_weekday_normality_p = grouped_weekday_normal.pvalue,
        weekly_weekend_normality_p = grouped_weekend_normal.pvalue,
        weekly_levene_p = grouped_eq_var.pvalue,
        weekly_ttest_p = grouped_ttest.pvalue,
        utest_p = utest.pvalue,
    ))


if __name__ == '__main__':
    main()

