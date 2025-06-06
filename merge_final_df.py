import pandas as pd

df_final_demo = pd.read_csv('df_final_demo_experiment_roster.csv')
df_final_web = pd.read_csv('df_final_web_data_combined.csv')

df_final_demo.head(),df_final_web.head()

common_clients = set(df_final_demo['client_id']).intersection(set(df_final_web['client_id']))
print(f"Number of common clients: {len(common_clients)}")

print("number of unique client_id in df_final_demo: ", df_final_demo['client_id'].nunique())
print("number of unique client_id in df_final_web: ", df_final_web['client_id'].nunique())

df_final_demo.value_counts(), df_final_web.value_counts()


# Merge the two DataFrames on 'client_id'. Left join on df_final_web to keep all records from df_final_web

df_final_merged = pd.merge(df_final_web, df_final_demo, on='client_id', how='left')

df_final_merged.shape

print("null values per column ", df_final_merged.isnull().sum())


df_demo_only = df_final_merged.dropna(subset = ['age', 'gender', 'Variation'])
df_demo_only.shape

# Now we have 2 df, one that contains all demographics, and one that contains all web data (without some demographics)

df_all = df_final_merged.copy() # This contains all web data and demographics, with NaNs for missing demographics
df_demo = df_demo_only.copy() # This contains only the rows with complete demographics


# save them as csv files:

df_all.to_csv('df_all.csv', index=False)
df_demo.to_csv('df_demo.csv', index=False)



