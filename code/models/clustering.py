import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler



df = pd.read_csv('artifacts/cleaned_data.csv')

audio_features = ['danceability', 'tempo', 'liveness', 'instrumentalness','loudness','speechiness']
features = df[audio_features].dropna()

kmeans = KMeans(n_clusters=5, random_state=42)
df['cluster'] = kmeans.fit_predict(features)

cluster_popularity = df.groupby('cluster')['popularity'].mean()
print(cluster_popularity)

plt.figure(figsize=(10, 6))  
sns.boxplot(x='cluster', y='popularity', data=df)
plt.title('Popularity by Cluster')  
plt.xlabel('Cluster')  
plt.ylabel('Popularity')  

plt.savefig('images/cluster_popularity_boxplot.png', dpi=300, bbox_inches='tight')

plt.show()


