import numpy as np
import pandas as pd

from algorithm.graphs_helper import original_graph, kmeans_graph, metrics_graphs, movement_graph
from algorithm.scenarios import df_1, df_2, df_3, df_4, df_5


def kmeans(scenario, k=4, max_iter=20):
    # Identify scenario (for graphs)
    if scenario.equals(df_1):
        title = "Scenario 1"
    elif scenario.equals(df_2):
        title = "Scenario 2"
    elif scenario.equals(df_3):
        title = "Scenario 3"
    elif scenario.equals(df_4):
        title = "Scenario 4"
    elif scenario.equals(df_5):
        title = "Scenario 5"

    # Show the original scenario
    original_graph(scenario, title)

    # Tolerance for total centroid movement
    tol = 0.001

    # Generate initial centroids
    centroids = np.random.uniform(0, 1, size=(k, 2))
    centroids = np.round(centroids, 3)
    centroids = pd.DataFrame(centroids, columns=["X", "Y"])
    centroids.index = centroids.index + 1

    # Initialize history
    variability_history = []
    dissimilarity_history = []
    centroids_mov_history = []
    each_variability = []
    empty_clusters = "No"

    # Iteration zero
    iteration = 0

    # Verify which point belongs to which cluster
    choices = []
    for _, point in scenario.iterrows():
        point = point[["X", "Y"]].values.astype(float)
        distance = np.sqrt(
            np.sum((centroids[["X", "Y"]].iloc[-k:].values - point[:2]) ** 2, axis=1)
        )
        closest_centroid = np.argmin(distance)
        choices.append(closest_centroid)
    scenario["Clusters"] = choices

    # Intra-cluster variability
    total_variability = 0
    each_variability = []
    for c in range(k):
        cluster_points = scenario[scenario["Clusters"] == c][["X", "Y"]].values
        current_centroid = centroids.iloc[c][["X", "Y"]].values
        if len(cluster_points) > 0:
            squared_distance = np.sum((cluster_points - current_centroid) ** 2, axis=1)
            each_variability.append(np.sum(squared_distance))
            total_variability += np.sum(squared_distance)
        else:
            each_variability.append(0)
    variability_history.append(total_variability)

    # Inter-cluster dissimilarity
    distance_between_centroids = []
    centroids_values = centroids[["X", "Y"]].values
    for i in range(k):
        for j in range(i + 1, k):
            pair_distance = np.sqrt(
                np.sum((centroids_values[i] - centroids_values[j]) ** 2)
            )
            distance_between_centroids.append(pair_distance)
    if distance_between_centroids:
        dissimilarity_mean = np.mean(distance_between_centroids)
    else:
        dissimilarity_mean = 0
    dissimilarity_history.append(dissimilarity_mean)

    # Main loop
    while True:
        iteration += 1

        # Recalculate Position
        new_centroids = []
        for c in range(k):
            cluster_points = scenario[scenario["Clusters"] == c]
            if cluster_points.empty:
                new_centroids.append(centroids.iloc[k * iteration - k + c].values)
                empty_clusters = "Yes"
                continue
            new_centroids.append(cluster_points[["X", "Y"]].mean().values)
        new_centroids = pd.DataFrame(new_centroids, columns=["X", "Y"])
        centroids = pd.concat([centroids, new_centroids], ignore_index=True)

        # Intra-cluster variability
        total_variability = 0
        each_variability = []
        for c in range(k):
            cluster_points = scenario[scenario["Clusters"] == c][["X", "Y"]].values
            current_centroid = new_centroids.iloc[c].values
            if len(cluster_points) > 0:
                squared_distance = np.sum(
                    (cluster_points - current_centroid) ** 2, axis=1
                )
                each_variability.append(np.sum(squared_distance))
                total_variability += np.sum(squared_distance)
            else:
                each_variability.append(0)
        variability_history.append(total_variability)

        # Inter-cluster dissimilarity
        distance_between_centroids = []
        centroids_values = new_centroids.values
        for i in range(k):
            for j in range(i + 1, k):
                pair_distance = np.sqrt(
                    np.sum((centroids_values[i] - centroids_values[j]) ** 2)
                )
                distance_between_centroids.append(pair_distance)
        if distance_between_centroids:
            dissimilarity_mean = np.mean(distance_between_centroids)
        else:
            dissimilarity_mean = 0
        dissimilarity_history.append(dissimilarity_mean)

        # Get last k centroids and penultimate k centroids
        mov_centroids = np.sqrt(
            np.sum(
                (
                    centroids[["X", "Y"]].iloc[-2 * k : -k].values
                    - centroids[["X", "Y"]].iloc[-k:].values
                )
                ** 2,
                axis=1,
            )
        )
        centroids_mov_history.append(round(np.sum(mov_centroids), 4))
        mov_centroids_mean = np.mean(mov_centroids)

        # Stopping criterion: mean centroid movement less than tol
        if mov_centroids_mean < tol:
            print("Execution stopped! Centroids are moving below the tolerance.")
            print(f"Total iterations performed: {iteration}")
            break

        # Stopping criterion: maximum number of iterations
        if iteration == max_iter:
            print(
                f"Execution stopped! Reached maximum number of executions: {max_iter}"
            )
            break

        # Verify which point belongs to which cluster
        choices = []
        for _, point in scenario.iterrows():
            point = point[["X", "Y"]].values.astype(float)
            distance = np.sqrt(
                np.sum(
                    (centroids[["X", "Y"]].iloc[-k:].values - point[:2]) ** 2, axis=1
                )
            )
            closest_centroid = np.argmin(distance)
            choices.append(closest_centroid)
        scenario["Clusters"] = choices

    df_mov_centroids = pd.DataFrame(
        centroids_mov_history, columns=["Value"], index=range(1, iteration + 1)
    )

    # Final information
    print(f"\n--- Final ---")

    print(f"  Number of iterations: {iteration}")
    print(f"  Were there empty clusters: {empty_clusters}")
    print(f"  Variability: {total_variability:.4f}")
    print(f"  Dissimilarity: {dissimilarity_mean:.4f}")
    print(f"  Total Movement: {np.sum(mov_centroids):.4f}")

    kmeans_graph(scenario, title, k, centroids, iteration, ev=each_variability)
    metrics_graphs(variability_history, dissimilarity_history, iteration)
    movement_graph(df_mov_centroids, iteration, "History: Total movement")
