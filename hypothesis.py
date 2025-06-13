import pandas as pd
from scipy.stats import chi2_contingency

df_demo = pd.read_csv('df_demo.csv')

df_demo

## HYPOTHESIS TESTING

## 1. Completion rate. Use Two sample T-test

# H0: Average completion rate for Test >= Average completion rate for Control
# H1: Average completion rate for Test < Average completion rate for Control

# alpha = 0.05 

visits = df_demo.groupby('visit_id').agg(
    Variation=('Variation', 'first'),
    completed=('process_step', lambda x: 'confirm' in x.values)
).reset_index()

visits['completed'] = visits['completed'].astype(int)

visits.groupby('Variation')['completed'].mean()

visits

import scipy.stats as st

control_completion = visits[visits['Variation'] == 'Control']['completed']
test_completion = visits[visits['Variation'] == 'Test']['completed']

ttest_result = st.ttest_ind(test_completion, control_completion, equal_var = False, alternative='less')

print(f"With the following values: {ttest_result} and a significance level of 5%, we fail to reject H0.")

## In this case with a pvalue = 1, and a significance level of 5%, we fail to reject H0.

import seaborn as sns
import matplotlib.pyplot as plt


sns.barplot(data=visits, x='Variation', y='completed')

plt.title('Completion Rate by Variation')
plt.ylim(0, 1)  
plt.show()

## 2. We posit that there's no gender influence in engagement (starting) in the Control vs Test Groups. Use Chi-Square Test

# H0: Gender and Variation are independent in engagement.
# H1: Gender and Variation are dependent.

df_engagement = df_demo[
    (df_demo['process_step'] == 'start') &
    (df_demo['gender'].isin(['F', 'M']))
]

engaged_visits = df_engagement.groupby('visit_id').agg(
    gender=('gender', 'first'),
    variation=('Variation', 'first')
).reset_index()

engagement_table = pd.crosstab(engaged_visits['gender'], engaged_visits['variation'])
print(engagement_table)

_, chi2_p_value, _, expected_freq = chi2_contingency(engagement_table)

chi2_p_value

if chi2_p_value > 0.05:
    print(f"with a p-value: {chi2_p_value:.4f} we fail to reject H0, hence Gender and variation are independent")

else:
    print(f"with a p-value: {chi2_p_value:.4f} we reject H0, hence Gender and variation are dependent")

