import pandas as pd

df_demo = pd.read_csv('df_demo.csv')

df_demo

start_counts_cli = df_demo[df_demo['process_step'] == 'start'].groupby('Variation')['client_id'].nunique()

confirm_counts_cli = df_demo[df_demo['process_step'] == 'confirm'].groupby('Variation')['client_id'].nunique()

completion_rate_cli = (confirm_counts_cli / start_counts_cli).fillna(0)

print(f"Completion rate by Variation using client_id: {completion_rate_cli}")


#completion rate using visit_id instead of client_id, and filtering by test and control variation:

start_counts_visit = df_demo[df_demo['process_step'] == 'start'].groupby('Variation')['visit_id'].nunique()

confirm_counts_visit = df_demo[df_demo['process_step'] == 'confirm'].groupby('Variation')['visit_id'].nunique()

completion_rate_visit = (confirm_counts_visit / start_counts_visit).fillna(0)

print(f"Completion rate by Variation using visit_id: {completion_rate_visit}")

# dict with completion rates for both groups for two metrics: client_id and visit_id

completion_rates = {
    "client_id": {
        "control": 0.659570,
        "test": 0.700435
    },
    "visit_id": {
        "control": 0.519011,
        "test": 0.655473
    }
}

threshold_percent = 5.0

# function to evaluate whether the increase in completion rate meets or exceeds the 5% threshold

def check_threshold(metric_name, control_rate, test_rate, threshold):
    # Calculate absolute increase in percentage points
    absolute_increase = (test_rate - control_rate) * 100
    meets_threshold = absolute_increase >= threshold

    print(f"\nMetric: {metric_name}")
    print(f"Control Rate: {control_rate:.6f}")
    print(f"Test Rate:    {test_rate:.6f}")
    print(f"Absolute Increase: {absolute_increase:.2f}%")
    print(f"Meets 5% Absolute Threshold: {'Yes' if meets_threshold else 'No'}")

# Run the threshold check for each metric
for metric, rates in completion_rates.items():
    check_threshold(metric, rates["control"], rates["test"], threshold_percent)


from statsmodels.stats.proportion import proportions_ztest

#  how many visits started and completed the process by group
start_counts = df_demo[df_demo['process_step'] == 'start'] \
    .groupby('Variation')['visit_id'].nunique()

confirm_counts = df_demo[df_demo['process_step'] == 'confirm'] \
    .groupby('Variation')['visit_id'].nunique()

# Put both groups in correct order (The z-test expects data in a consistent order, i.e., Control first, then Test)
start_counts = start_counts.reindex(['Control', 'Test']).fillna(0).astype(int)
confirm_counts = confirm_counts.reindex(['Control', 'Test']).fillna(0).astype(int)

# Prepare data for z-test
successes = [confirm_counts['Control'], confirm_counts['Test']]
n_obs = [start_counts['Control'], start_counts['Test']]

# Run z-test
z_stat, p_value = proportions_ztest(count=successes, nobs=n_obs)

print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print("Statistically significant difference in completion rates.")
else:
    print("No statistically significant difference in completion rates.")

# there is a statistically significant difference in completion rates between the control and test groups.

