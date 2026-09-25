import numpy as np
import pandas as pd

# Scenario 1 - Isolated clusters

centers = np.array([
    [0.25, 0.2],
    [0.75, 0.8],
    [0.75, 0.2],
    [0.25, 0.8]
])
strength = 0.055
data = []

for i in range(len(centers)):
    noise = np.random.randn(300, 2) * strength
    cluster = np.round(noise + centers[i], 3)
    data.append(cluster)

data = np.vstack(data)
df_1 = pd.DataFrame(data, columns=['X', 'Y'])
df_1['Clusters'] = None


# Scenario 2 - Undefined clusters

centers = np.array([
    [0.375, 0.4],
    [0.575, 0.5],
    [0.625, 0.6],
    [0.5, 0.4]
])
strength = 0.1
data = []

for i in range(len(centers)):
    noise = np.random.randn(300, 2) * strength
    cluster = np.round(noise + centers[i], 3)
    data.append(cluster)

data = np.vstack(data)
df_2 = pd.DataFrame(data, columns=['X', 'Y'])
df_2['Clusters'] = None


# Scenario 3 - Alike Clusters

centers = np.array([
    [0.3, 0.3],
    [0.7, 0.7],
    [0.7, 0.3],
    [0.3, 0.7]
])

transform = np.array(
    [[0.06, 0.04], 
     [0.02, 0.04]]
    )
data = []

for i in range(len(centers)):
    noise = np.random.randn(300, 2)
    cluster = np.round(np.dot(noise, transform) + centers[i], 3)
    data.append(cluster)

data = np.vstack(data)
df_3 = pd.DataFrame(data, columns=['X', 'Y'])
df_3['Clusters'] = None


# Scenario 4 - Adjacent clusters

centers = np.array([
    [0.1, 0.5],
    [0.3, 0.5],
    [0.4, 0.5],
    [0.6, 0.5],
    [0.7, 0.5],
    [0.9, 0.5]
])

transform = np.array(
    [[0.01, 0.1],
     [0.02, 0.01]]
    )
data = []

for i in range(len(centers)):
    noise = np.random.randn(300, 2)
    cluster = np.round(np.dot(noise, transform) + centers[i], 3)
    data.append(cluster)

data = np.vstack(data)
df_4 = pd.DataFrame(data, columns=['X', 'Y'])
df_4['Clusters'] = None


# Scenario 5 - Totally random

data = np.random.rand(1200, 2)

data = np.vstack(data)
df_5 = pd.DataFrame(data, columns=['X', 'Y'])
df_5['Clusters'] = None