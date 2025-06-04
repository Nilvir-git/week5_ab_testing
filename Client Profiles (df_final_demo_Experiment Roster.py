import pandas as pd
df = pd.read_csv("df_final_demo.txt", sep=",")  # Or sep="\t" for tab-delimited

print(df.head())

df.info()
df.shape
df.isnull().sum()
num_all_null_rows = df.isnull().all(axis=1).sum()
print(f"Rows with all null values: {num_all_null_rows}")
df = df.rename(columns={
    'clnt_tenure_yr': 'tenure_years',
    'clnt_tenure_mnth': 'tenure_months',
    'clnt_age': 'age',
    'gendr': 'gender',
    'num_accts': 'num_accounts',
    'bal': 'balance',
    'calls_6_mnth': 'calls_last_6_months',
    'logons_6_mnth': 'logons_last_6_months'
})
df[df['tenure_years'].isnull()]
df[df['tenure_months'].isnull()]

# Remove rows where all columns except 'client_id' are null
cols_except_id = df.columns.difference(['client_id'])
mask = df[cols_except_id].isnull().all(axis=1)
df = df[~mask]
df.isnull().sum()
df[df['age'].isnull()]

df_experiment_clients = pd.read_csv("df_final_experiment_clients.txt", sep=",")  # Or sep="\t" for tab-delimited
df = df.merge(df_experiment_clients, on="client_id", how="left")
print(df.head())
df.isnull().sum()
null_count = df_experiment_clients['Variation'].isnull().sum()
null_count
df['Variation'] = df['Variation'].fillna("Not in test")
df.to_csv("df_final_demo_experiment_roster.csv", index=False)
unique_genders = df['gender'].unique()
print(unique_genders)
