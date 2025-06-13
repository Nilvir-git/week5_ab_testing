import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import get_cmap
import numpy as np
import seaborn as sns

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

##VISUALS ON COMPLETION RATE

variations = completion_rate_cli.index.tolist() 
x = np.arange(len(variations))

bar_width = 0.35 

plt.figure(figsize=(7, 5)) 

cli_id_bar = plt.bar(x - bar_width/2, completion_rate_cli, bar_width, label='Client ID Rate', color='skyblue')

test_id_bar = plt.bar(x + bar_width/2, completion_rate_visit, bar_width, label='Visit ID Rate', color='salmon')

plt.bar_label(cli_id_bar, fmt='%.2f', padding=3) 
plt.bar_label(test_id_bar, fmt='%.2f', padding=3) 

plt.title('Completion Rates by Variation')
plt.ylabel('Completion Rate')
plt.xticks(x, variations) 
plt.ylim(0, 1) 

plt.legend(title='Metric Type')
plt.tight_layout() # Adjust layout to prevent labels/elements from overlapping
plt.show()


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

### VISUALS ON TIME SPEND ON EACH STEP

df_plot_steps = avg_time_per_step_by_variation.reset_index()

df_plot_steps['process_step'] = pd.Categorical(df_plot_steps['process_step'], categories=step_order, ordered=True)

print("DataFrame for Plotting (Average Time per Step):")
print(df_plot_steps)
print("\n" + "="*50 + "\n")


plt.figure(figsize=(10, 6)) 

sns.lineplot(
    data=df_plot_steps,
    x='process_step',    
    y='duration',        
    hue='Variation',     
    marker='o',          
    palette='viridis'    
)


plt.title('Average Time Spent per Process Step by Variation')
plt.xlabel('Process Step')
plt.ylabel('Average Time Spent (seconds)')
plt.grid(axis='y', linestyle='--', alpha=0.7) 
plt.legend(title='Variation') 


# --- Add data labels on each point with staggered positions ---
label_offset = 15 
for variation in df_plot_steps['Variation'].unique():
    subset = df_plot_steps[df_plot_steps['Variation'] == variation]
    
    if variation == 'Control':
        y_offset_multiplier = 1  
        va_align = 'bottom'
    else: # Test
        y_offset_multiplier = -1 
        va_align = 'top'

    for i, row in subset.iterrows():
        plt.text(
            row['process_step'],                               
            row['duration'] + (label_offset * y_offset_multiplier), 
            f"{row['duration']:.2f}",                          
            ha='center',                                       
            va=va_align,                                       
            fontsize=9,                                        
            color=sns.color_palette('viridis')[variation_order.index(variation)] 
        )

min_duration = df_plot_steps['duration'].min()
max_duration = df_plot_steps['duration'].max()
plt.ylim(min_duration - label_offset*2, max_duration + label_offset*2) 

plt.tight_layout()
plt.show()

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

print("Average Time to Completion (seconds): {:.2f}\n".format(overall_avg))
print("Average Time to Completion by Variation:")
print(by_variation.round(2))


### VISUALIZATION TOTAL TIME UNTIL COMPLETION

viridis = cm.get_cmap('viridis')
control_color = viridis(0.3)
test_color = viridis(0.7)
overall_color = 'gray'

data = [
    ('Control', by_variation['Control'], control_color),
    ('Test', by_variation['Test'], test_color),
    ('Overall Avg', overall_avg, overall_color)
]

data.sort(key=lambda x: x[1], reverse=True)

plt.figure(figsize=(5, 5))

for label, value, color in data:
    plt.hlines(value, xmin=0, xmax=1, colors=color, linewidth=5)
    plt.text(-0.05, value, label, va='center', ha='right', fontsize=10, color=color)
    plt.text(1.05, value, f"{value:.2f} sec", va='center', ha='left', fontsize=10, color=color)

plt.xticks([])
plt.yticks([])
plt.box(False)

plt.xlim(-0.2, 1.2)
plt.ylim(min(d[1] for d in data) - 20, max(d[1] for d in data) + 20)

plt.title("Average Time to Completion", fontsize=12, weight='bold')

plt.tight_layout()
plt.show()


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

df_demo = df_demo.sort_values(by=['visit_id', 'date_time'])

df_demo['prev_step_order'] = df_demo.groupby('visit_id')['step_order'].shift(1)
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

print(error_summary)

### VISUALIZATION ERROR RATES

viridis = get_cmap('viridis')
custom_palette = {
    'Control': viridis(0.25),  # blue-ish
    'Test': viridis(0.65)      # green-ish
}

# Plot error_rate by process_step and Variation
sns.set(style='whitegrid')

sns.lineplot(
    data=error_summary,
    x='process_step',
    y='error_rate',
    hue='Variation',
    marker='o',
    palette=custom_palette
)

plt.title("Error Rate by Process Step and Variation")
plt.xlabel("Process Step")
plt.ylabel("Error Rate")
plt.ylim(0, error_summary['error_rate'].max() * 1.2)
plt.tight_layout()
plt.show()



df_demo.head()

