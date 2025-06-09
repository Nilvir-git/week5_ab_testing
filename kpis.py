import pandas as pd

df_demo = pd.read_csv('df_demo.csv')

df_demo

print("null values per column ", df_demo.isnull().sum())

#remove Variation: Not in test

df_demo = df_demo[df_demo['Variation'] != 'Not in test']

df_demo

df_demo.dtypes

# Convert 'date_time' to datetime format
df_demo['date_time'] = pd.to_datetime(df_demo['date_time'])


## SUCCESS INDICATORS considering df_demo (contains all demographics but not all web data)

#completion rate using client_id, and filtering by test and control variation:

start_counts_cli = df_demo[df_demo['process_step'] == 'start'].groupby('Variation')['client_id'].nunique()

confirm_counts_cli = df_demo[df_demo['process_step'] == 'confirm'].groupby('Variation')['client_id'].nunique()

completion_rate_cli = (confirm_counts_cli / start_counts_cli).fillna(0)

print(f"Completion rate by Variation using client_id: {completion_rate_cli}")


#completion rate using visit_id instead of client_id, and filtering by test and control variation:

start_counts_visit = df_demo[df_demo['process_step'] == 'start'].groupby('Variation')['visit_id'].nunique()

confirm_counts_visit = df_demo[df_demo['process_step'] == 'confirm'].groupby('Variation')['visit_id'].nunique()

completion_rate_visit = (confirm_counts_visit / start_counts_visit).fillna(0)

print(f"Completion rate by Variation using visit_id: {completion_rate_visit}")

#results are actually quite different.. probably makes more sense to use by visit_id.


#sort values by visit_id and date_time

df_demo = df_demo.sort_values(by=['visit_id', 'date_time'])

#addition columns
df_demo['next_time'] = df_demo.groupby('visit_id')['date_time'].shift(-1)

df_demo['duration'] = (df_demo['next_time'] - df_demo['date_time']).dt.total_seconds()

df_demo

#Time spend on each step:

variation_order = ['Control', 'Test']
step_order = ['start', 'step_1', 'step_2', 'step_3', 'confirm']

df_demo['Variation'] = pd.Categorical(df_demo['Variation'], categories = variation_order, ordered=True)
df_demo['process_step'] = pd.Categorical(df_demo['process_step'], categories = step_order, ordered=True)

avg_time_per_step_by_variation = (
    df_demo
    .groupby(['Variation', 'process_step'])['duration']
    .mean()
    .round(2)
    .sort_index()
)
print(f"Average time spend per process step in seconds is: {avg_time_per_step_by_variation}")

###


#client_id to find

client_id_to_find = 7338123
client_data = df_demo_sorted[df_demo_sorted['client_id'] == client_id_to_find]
print(client_data.to_string())

## ERROR RATES - UPDATED..

df_demo

step_order = {
    'start': 0,
    'step_1': 1,
    'step_2': 2,
    'step_3': 3,
    'confirm': 4
}

df_demo['step_order'] = df_demo['process_step'].map(step_order)

df_demo = df_demo.sort_values(by=['visitor_id', 'date_time'])

df_demo['prev_step_order'] = df_demo.groupby('visitor_id')['step_order'].shift(1)
df_demo['error'] = df_demo['step_order'] < df_demo['prev_step_order']

error_summary = df_demo.groupby(['process_step', 'Variation'], observed = True).agg(
    total=('error', 'count'),
    errors=('error', 'sum')
).reset_index()

error_summary['error_rate'] = error_summary['errors'] / error_summary['total']

error_summary = error_summary.sort_values(by=['process_step', 'Variation'])

error_summary['step_order'] = error_summary['process_step'].map(step_order)

variation_order = ['Control', 'Test']
error_summary['Variation'] = pd.Categorical(error_summary['Variation'], categories=variation_order, ordered=True)

error_summary = error_summary.sort_values(by=['Variation', 'step_order']).reset_index(drop=True)

error_summary


