####all the feature
# id,name,artists,duration (ms),popularity,url,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,type,uri,track_href,analysis_url,duration_ms,time_signature
#####choose artists,duration,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,type

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


plt.ion()

# read csv
# url = 'https://github.com/ClaireLu0608/eco395m_midterm_project/blob/main/artifacts/results.csv'
df = pd.read_csv(r"D:/python_hw/mid/eco395m_midterm_project/artifacts/spotify_data.csv")
df_unique = df.drop_duplicates(subset=["id"])

# df = pd.read_csv(df)
df_unique["release date"] = pd.to_datetime(df_unique["release date"])
df_unique["year"] = df_unique["release date"].dt.year
variables = [
    "popularity",
    "duration (ms)",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "year",
]

# calculate correlation_matrix
correlation_matrix = df_unique[variables].corr(method="pearson")

plt.figure(figsize=(12, 10))

# use seaborn yo draw heat map
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    annot_kws={"size": 10},
    xticklabels=variables,
    yticklabels=variables,
    cbar_kws={"shrink": 0.8},
)

plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.title("Correlation Matrix of Music Features")
plt.savefig(
    r"D:/python_hw/mid/eco395m_midterm_project/artifacts/correlation.png",
    bbox_inches="tight",
)

plt.show()
print("missing value:")
print(df_unique[variables].isnull().sum())
df_cleaned = df_unique[variables].dropna()
print("missing value after cleaning:")
print(df_cleaned.isnull().sum())

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Extract features for VIF calculation (excluding name, artists, and popularity)

df_cleaned = df_cleaned.drop(columns=["popularity"])
variables_new = [
    "duration (ms)",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "year",
]
features = df_cleaned[variables_new]


X = sm.add_constant(features)


vif_data = pd.DataFrame()
vif_data["Feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]


print(vif_data)
vif_data.to_csv(
    r"D:/python_hw/mid/eco395m_midterm_project/artifacts/vif_values_pearson.csv",
    index=False,
)
