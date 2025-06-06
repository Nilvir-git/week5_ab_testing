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

# TOTAL TIME SPENT UNTIL COMPLETION 

complete_visits = df_demo[df_demo['process_step'] == 'confirm']['visit_id'].unique()
df_complete_visits = df_demo[df_demo['visit_id'].isin(complete_visits)]
visit_start_times = df_complete_visits.groupby('visit_id')['date_time'].min()
visit_end_times = df_complete_visits.groupby('visit_id')['date_time'].max()

time_to_completion = (visit_end_times - visit_start_times).dt.total_seconds()
time_to_completion_df = time_to_completion.reset_index()
time_to_completion_df.columns = ['visit_id', 'time_to_completion_sec']

visit_variations = df_complete_visits.groupby('visit_id')['Variation'].first().reset_index()
time_to_completion_df = time_to_completion_df.merge(visit_variations, on='visit_id')

overall_avg = time_to_completion_df['time_to_completion_sec'].mean()
by_variation = time_to_completion_df.groupby('Variation')['time_to_completion_sec'].mean()

print(" Average Time to Completion (seconds): {overall_avg:.2f}\n")
print("Average Time to Completion by Variation:")
print(by_variation.round(2))

#client_id to find

client_id_to_find = 7338123
client_data = df_demo_sorted[df_demo_sorted['client_id'] == client_id_to_find]
print(client_data.to_string())

## ERROR RATES - PART NOT UPDATED..

step_order = {
    'start': 0,
    'step_1': 1,
    'step_2': 2,
    'step_3': 3,
    'confirm': 4
}

df_demo_sorted['step_num'] = df_demo_sorted['process_step'].map(step_order)

df_demo_sorted['next_step_num'] = df_demo_sorted.groupby('visit_id')['step_num'].shift(-1)

df_demo_sorted['backward_move'] = df_demo_sorted['next_step_num'] < df_demo_sorted['step_num']

num_backward_moves = df_demo_sorted['backward_move'].sum()
print(f"Number of backward moves (possible errors): {num_backward_moves}")

visits_with_backward = df_demo_sorted.loc[df_demo_sorted['backward_move'], 'visit_id'].unique()
print(f"Visits with backward moves: {len(visits_with_backward)}")

df_demo_sorted

# Steps conversion rates by variation
def step_by_variation(df, variation_value):
    df_var = df[df['Variation'] == variation_value].copy()
    
    step_counts = df_var.groupby('process_step')['visit_id'].nunique().reindex(step_order.keys())
    step_counts_df = step_counts.reset_index().rename(columns={'visit_id': 'num_visits'})
    
    step_counts_df['conversion_to_next'] = step_counts_df['num_visits'].shift(-1) / step_counts_df['num_visits']
    step_counts_df['drop_off_rate'] = 1 - step_counts_df['conversion_to_next']
    
    step_counts_df['Variation'] = variation_value
    return step_counts_df

step_test = step_by_variation(df_demo, 'Test')
step_control = step_by_variation(df_demo, 'Control')

step_variation_comparison = pd.concat([step_test, step_control], ignore_index=True)
print(step_variation_comparison)

#Redesign Order.. 





print("null values per column ", df_step_duration.isnull().sum())