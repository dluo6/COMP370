import pandas as pd
import matplotlib.pyplot as plt

mcgill = './final_labeled_dataset_mcgill.tsv'
concordia = './final_labeled_dataset_concordia.tsv'

mcgill_df = pd.read_csv(mcgill, sep='\t', engine='python')
concordia_df = pd.read_csv(concordia, sep='\t', engine='python')

dfs = [mcgill_df, concordia_df]

mcgill_df = mcgill_df.groupby(by=['coding'], as_index=False).count()[['coding', 'title']]
concordia_df = concordia_df.groupby(by=['coding'], as_index=False).count()[['coding', 'title']]

categories = ['school advice', 'exam', 'social life', 'information sharing', 'school services', 'financial advice', 'housing', 'help needed']
index = [i for i in range(len(categories))]
bar_width = 0.35

print(mcgill_df['coding'].tolist())
mcgill_data = []
concordia_data = []
for c in categories:
    mcgill_data.append(0 if c not in mcgill_df['coding'].tolist() else mcgill_df.loc[mcgill_df['coding'] == c, 'title'].iloc[0])
    concordia_data.append(0 if c not in concordia_df['coding'].tolist() else concordia_df.loc[concordia_df['coding'] == c, 'title'].iloc[0])

print(mcgill_data)
fig, ax = plt.subplots()
ax.bar(index, mcgill_data, bar_width, label="McGill")

ax.bar([i+bar_width for i in index], concordia_data, bar_width, label="Concordia")

ax.set_xlabel('Category')
ax.set_ylabel('Category Count')
ax.set_title('Number of Posts With Category Labels')
ax.set_xticks([i+bar_width/2 for i in index])
ax.set_xticklabels(categories)
ax.legend()

plt.show()