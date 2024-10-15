import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler



df = pd.read_csv("artifacts/spotify_data.csv")
df = df[df["popularity"] >= 5]  # Remove any extremely small values
df.dropna(inplace=True)  # Drop nan values
df = df.drop_duplicates()  # Remove duplicates

# Create an empty dataset for cleaned data. Remove energy, valence, and acousticness with multicollinearity from previous correlation analysis
df_cleaned = pd.DataFrame()

# 1. Log transform of features
df_cleaned["duration_ms"] = np.log1p(df["duration_ms"])
df_cleaned["speechiness"] = np.log1p(df["speechiness"])
df_cleaned["instrumentalness"] = np.log1p(df["instrumentalness"])

# 2. Standard scaling of features
standard_scaler = StandardScaler()
df_cleaned[["danceability", "liveness"]] = standard_scaler.fit_transform(
    df[["danceability", "liveness"]]
)

# 3. Min Max scaling of features
min_max_scaler = MinMaxScaler()
df_cleaned[["tempo", "loudness", "key"]] = min_max_scaler.fit_transform(
    df[["tempo", "loudness", "key"]]
)

# 4. Add other features
df_cleaned["mode"] = df["mode"]
df_cleaned["popularity"] = df["popularity"]

df_cleaned = df_cleaned.reset_index(drop=True)
df_cleaned.to_csv("artifacts/cleaned_data.csv", index=False)
