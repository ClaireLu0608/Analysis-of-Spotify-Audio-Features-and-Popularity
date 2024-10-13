import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv('artifacts/results.csv')
df = df[df['popularity'] != 0]
df.dropna(inplace=True) 


y = df['popularity']
X = pd.DataFrame()
X['duration_ms'] = np.log1p(df['duration_ms'])
X['speechiness'] = np.log1p(df['speechiness'])
X['acousticness'] = np.log1p(df['acousticness'])
X['instrumentalness'] = np.log1p(df['instrumentalness'])


standard_scaler = StandardScaler()
X[['danceability', 'energy', 'valence', 'liveness', 'mode']] = standard_scaler.fit_transform(
    df[['danceability', 'energy', 'valence', 'liveness', 'mode']]
)

min_max_scaler = MinMaxScaler()
X[['tempo', 'loudness','key']] = min_max_scaler.fit_transform(df[['tempo', 'loudness', 'key']])

y = y.reset_index(drop=True)
X = X.reset_index(drop=True)