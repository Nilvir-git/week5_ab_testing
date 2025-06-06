import pandas as pd

df_demo = pd.read_csv('df_demo.csv')

df_demo

print("null values per column ", df_demo.isnull().sum())

## SUCCESS INDICATORS considering df_demo (contains all demographics but not all web data)

df_demo['process_step'].value_counts()

start_count = df_demo[df_demo['process_step'] == 'start']['client_id'].nunique()
confirm_count = df_demo[df_demo['process_step'] == 'confirm']['client_id'].nunique()

completion_rate = confirm_count / start_count
print(f"Completion rate considering all Variations: {completion_rate:.2%}")

df_demo['Variation'].value_counts()

# calculating completion rate excluding 'Not in test' variation

df_filtered = df_demo[df_demo['Variation'] != 'Not in test']

start_count = df_filtered[df_filtered['process_step'] == 'start']['client_id'].nunique()
confirm_count = df_filtered[df_filtered['process_step'] == 'confirm']['client_id'].nunique()

completion_rate = confirm_count / start_count
print(f"Completion Rate (excluding 'Not in test'): {completion_rate:.2%}")

df_demo.dtypes

# Convert 'date_time' to datetime format
df_demo['date_time'] = pd.to_datetime(df_demo['date_time'])

#Time spend on each step:

df_demo_sorted = df_demo.sort_values(by=['visit_id', 'date_time'])
df_demo_sorted['next_time'] = df_demo_sorted.groupby('visit_id')['date_time'].shift(-1)
df_demo_sorted['duration'] = (df_demo_sorted['next_time'] - df_demo_sorted['date_time']).dt.total_seconds()
df_step_duration = df_demo_sorted.dropna(subset=['duration'])

df_demo_sorted

avg_time_per_step = df_step_duration.groupby('process_step')['duration'].mean().sort_values()
print(f"Average time spend per process step in seconds is: {avg_time_per_step}")


#Time spend on each step (excluding 'Not in test' variation):

df_filtered = df_demo_sorted[df_demo_sorted['Variation'] != 'Not in test']

df_filtered = df_filtered.dropna(subset=['duration'])

avg_time_per_step_filtered = df_filtered.groupby('process_step')['duration'].mean().sort_values()

print(f"Average time per step (seconds), excluding 'Not in test':{avg_time_per_step_filtered}")


###

nan_count_confirm = df_demo_sorted.loc[df_demo_sorted['process_step'] == 'confirm', 'duration'].isna().sum()
print(f"Number of NaN values in 'duration' for 'confirm' step: {nan_count_confirm}")


#client_id to find

client_id_to_find = 7338123
client_data = df_demo_sorted[df_demo_sorted['client_id'] == client_id_to_find]
print(client_data.to_string())

## ERROR RATES

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

#Redesign Order.. 