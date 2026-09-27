import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
import base64

def original_graph(scenario, title):
  plt.figure(figsize=(5, 5), dpi=80)
  plt.scatter(scenario['X'], scenario['Y'], s=10, alpha=0.6)
  plt.xlim(0, 1)
  plt.ylim(0, 1)
  plt.xlabel("X Axis")
  plt.ylabel("Y Axis")
  plt.title(title)
  
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format='png', bbox_inches='tight')
  img_buffer.seek(0)
  img_bytes = img_buffer.getvalue()
  plt.close()
  
  return img_bytes

colors = ['red', 'lightskyblue', 'lime', 'mediumpurple', 'aquamarine','cadetblue','orange','tan','pink','lavender',
          'green','deeppink','yellow','salmon','steelblue','purple','royalblue','powderblue','thistle','saddlebrown']

def kmeans_graph(scenario, title, k, centroids, iter, ev=None):
  plt.figure(figsize=(5, 5),dpi=80)
  color_per_point = []
  for i in range(len(scenario)):
    color_per_point.append(colors[scenario['Clusters'].iloc[i]])
  
  # Plots the points and their clusters
  plt.scatter(scenario['X'], scenario['Y'], s=10, alpha=0.6, c=color_per_point)
  each_variability = ev
  patches = []
  for c in range(k):
    patch = mpatches.Patch(color=colors[c], label=f'Cluster {c+1}: {each_variability[c]:.2f}') # fix ev list
    patches.append(patch)
  plt.legend(handles=patches, bbox_to_anchor=(1, 1), loc='upper left')
  
  # Plots the centroids
  plt.scatter(centroids['X'].iloc[-k:], centroids['Y'].iloc[-k:], c='red', marker='X', s=70, edgecolors='black', zorder=5, label='Current Centroids')
  plt.xlim(0, 1)
  plt.ylim(0, 1)
  plt.xlabel("X Axis")
  plt.ylabel("Y Axis")
  plt.title(title)

  for c in range(k):
    # Extracts the complete history of this specific centroid 'c' up to the current iteration
    # The history starts at the initial index (0 to k-1) and skips every k at each iteration
    centroid_history = centroids.iloc[c::k]
    # Plots the movement line (trajectory)
    plt.plot(centroid_history['X'], centroid_history['Y'], color='black', linestyle='--', linewidth=2, alpha=0.8)
    # Plots smaller dots to indicate the past positions it passed through
    plt.scatter(centroid_history['X'].iloc[:-1], centroid_history['Y'].iloc[:-1], color='white', marker='o', s=30, edgecolors='black', alpha=0.6)
    
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format='png', bbox_inches='tight')
  img_buffer.seek(0)
  img_bytes = img_buffer.getvalue()
  plt.close()
  
  return img_bytes
  
  
def metrics_graphs(vh, dh, iter):
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5), dpi=80)

  # Variability Graph
  ax1.plot(range(0, iter + 1), vh, marker='o', color='blue')
  ax1.set_title('History: Variability')
  ax1.set_xlabel('Iteration')
  ax1.set_ylabel('Variability')
  ax1.set_xticks(range(0, iter + 1))
  ax1.grid(True)

  # Dissimilarity Graph
  ax2.plot(range(0, iter + 1), dh, marker='s', color='orange')
  ax2.set_title('History: Dissimilarity')
  ax2.set_xlabel('Iteration')
  ax2.set_ylabel('Dissimilarity')
  ax2.set_xticks(range(0, iter + 1))
  ax2.grid(True)

  plt.tight_layout()
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format='png', bbox_inches='tight')
  img_buffer.seek(0)
  img_bytes = img_buffer.getvalue()
  plt.close()
  
  return img_bytes
  
  
def movement_graph(df, iter, title):
  plt.figure(figsize=(8, 5),dpi=80)
  plt.plot(df.index, df['Value'])
  plt.xlabel("Iteration")
  plt.ylabel("Total movement of centroids")
  plt.xticks(range(iter + 1))
  plt.title(title)
  
  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format='png', bbox_inches='tight')
  img_buffer.seek(0)
  img_bytes = img_buffer.getvalue()
  plt.close()
  
  return img_bytes