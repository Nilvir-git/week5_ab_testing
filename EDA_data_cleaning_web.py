
import pandas as pd
df_pt1 = pd.read_csv('df_final_web_data_pt_1.txt')
df_pt2 = pd.read_csv('df_final_web_data_pt_2.txt')

print(df_pt1.head())
print(df_pt2.head())

df_final_web_combined = pd.concat([df_pt1, df_pt2], ignore_index=True)

df_final_web_combined.info()
df_final_web_combined.shape
df_final_web_combined.head()

df_final_web_combined

df_final_web_combined.dtypes

df_final_web_combined['date_time'] = pd.to_datetime(df_final_web_combined['date_time'])

df_final_web_combined['process_step'].value_counts(normalize=True)

df_final_web_combined.nunique()

df_final_web_combined.to_csv('df_final_web_data_combined.csv', index=False)

df_final_web_combined['date_time'].min(), df_final_web_combined['date_time'].max()

df_final_web_combined['date'] = df_final_web_combined['date_time'].dt.date

df_final_web_combined

step_counts_by_date = df_final_web_combined.groupby(['date', 'process_step']).size().unstack(fill_value=0)

import matplotlib.pyplot as plt

step_counts_by_date.plot(kind='line', figsize=(12, 6))

plt.title('Process Step Counts by Date')
plt.xlabel('Date')
plt.ylabel('Count')
plt.grid(True)
plt.legend(title='Process Step', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.show()

df_final_web_combined['client_id'].value_counts()
