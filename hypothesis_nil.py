import pandas as pd

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


## 2. There's no gender influence between test vs control completion.
# We posit that there are no differences between males and females that completed the test vs control.

# Use Two sample T-test

df_demo['gender'].value_counts()

visits2 = df_demo.groupby('visit_id').agg(
    Variation=('Variation', 'first'),
    gender=('gender', 'first'),
    completed=('process_step', lambda x: 'confirm' in x.values)
).reset_index()

visits2['completed'] = visits2['completed'].astype(int)

visits2 = visits2[visits2['gender'].isin(['M', 'F'])]

visits_male_control = visits2[(visits2['gender'] == 'M') & (visits2['Variation'] == 'Control')]['completed']
visits_male_test = visits2[(visits2['gender'] == 'M') & (visits2['Variation'] == 'Test')]['completed']
visits_female_control = visits2[(visits2['gender'] == 'F') & (visits2['Variation'] == 'Control')]['completed']
visits_female_test = visits2[(visits2['gender'] == 'F') & (visits2['Variation'] == 'Test')]['completed']


# 2.1 - Control gender completion results
# H0: mu males control = mu females control
# H1: mu males control != mu females control

#alpha = 0.05

control_gender = st.ttest_ind(visits_male_control, visits_female_control, equal_var = False)   

print(f"With the following values {control_gender} we reject the null (H0) Hypothesis, hence there is gender influence in Control completion")

control_visits = visits2[visits2['Variation'] == 'Control']

#chart

sns.barplot(
    data=control_visits,
    x='gender',
    y='completed',
    errorbar=None 
)
plt.title('Completion Rate by Gender (Control Group)')
plt.ylim(0, 1)
plt.show()


# 2.2 - Test gender completion results
# H0: mu males Test = mu females Test
# H1: mu males Test != mu females Test

#alpha = 0.05

test_gender = st.ttest_ind(visits_male_test, visits_female_test, equal_var = False)   

print(f"With the following values {test_gender} we reject the null (H0) Hypothesis, hence there is gender influence in Test Completion results")

#chart

test_visits = visits2[visits2['Variation'] == 'Test']

sns.barplot(
    data=test_visits,
    x='gender',
    y='completed',
    errorbar=None 
)
plt.title('Completion Rate by Gender (Test Group)')
plt.ylim(0, 1)
plt.show()
