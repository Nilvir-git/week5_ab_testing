import pandas as pd
df = pd.read_csv("df_final_demo_experiment_roster.csv")
online_clients = df[df['logons_last_6_months'] > 0]

print("Count of online clients:", len(online_clients))

# all clients have logged on at least once in last 6 months´
# find out who has logged on the most (top 25%)
logons_75 = df['logons_last_6_months'].quantile(0.75)
print("75th percentile of logons in last 6 months:", logons_75)
# characterise the clients who logged on the most in laast 6 months
top_users = df[df['logons_last_6_months'] > 7]

avg_age = top_users['age'].mean()
avg_tenure_years = top_users['tenure_years'].mean()
avg_balance = top_users['balance'].mean()
gender_counts = top_users['gender'].value_counts()

print(f"Number of top users: {len(top_users)}")
print(f"Average age: {avg_age:.2f}")
print(f"Average tenure (years): {avg_tenure_years:.2f}")
print(f"Average account balance: {avg_balance:.2f}")
print("Gender distribution:")
print(gender_counts)

non_primary_users = df[df['logons_last_6_months'] <= 7]

avg_age_np = non_primary_users['age'].mean()
avg_tenure_years_np = non_primary_users['tenure_years'].mean()
avg_balance_np = non_primary_users['balance'].mean()

# Gender distribution for non-primary users
gender_counts_np = non_primary_users['gender'].value_counts()

print(f"Non-primary users count: {len(non_primary_users)}")
print(f"Average age (non-primary): {avg_age_np:.2f}")
print(f"Average tenure (years, non-primary): {avg_tenure_years_np:.2f}")
print(f"Average account balance (non-primary): {avg_balance_np:.2f}")
print("Gender distribution (non-primary users):")
print(gender_counts_np)






