import pandas as pd
import re

df = pd.read_csv("./IRAhandle_tweets_1.csv").head(10000)
df = df.loc[(df["language"] == "English") & (df["content"].str.contains("?", regex=False)==False)]

columns = ["tweet_id", "publish_date", "content"]
df = df[columns]
df['trump_mention'] = df.apply(lambda row: "T" if re.match(r"(.*(^|[^a-zA-Z0-9])Trump([^a-zA-Z0-9]|$).*)", row.content) else "F", axis=1)

df.to_csv("dataset.tsv", sep="\t", index=False)

contains = df.loc[(df['trump_mention'] == 'T')]

data = {"result": ["frac-trump-mentions"], "value": [round(len(contains)/len(df), 3)]}
result = pd.DataFrame(data=data)

result.to_csv("results.tsv", sep="\t", index=False)