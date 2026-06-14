# Philippines Climate-Aware Logistics & Supply Chain Optimization Engine

##  Project Overview

The Philippines Climate-Aware Logistics Engine is an AI-driven disaster management platform designed to solve routing failures during humanitarian crises. Traditional GPS navigation relies on static distance metrics, often directing emergency supply trucks straight into severe floodwaters during typhoons.

This engine solves that logistical vulnerability by pairing predictive machine learning with dynamic graph theory. When given a forecasted archipelagic rainfall metric, an AI classifier calculates localized flood probabilities for nationwide municipality and port nodes. The system then dynamically injects risk penalties directly into an underlying weighted graph network, calculating risk-adjusted supply corridors from staging hubs down to disaster-affected target islands and cities.

---

##  File Layout & Component Descriptions

* **`frontend/src/App.jsx`**: The real-time interactive geospatial dashboard. Features a high-contrast dark telemetry theme and an interactive React-Leaflet GIS map component that displays a precipitation slider, archipelagic vulnerability feeds, and dynamic routing chains.
* **`project.py`**: The primary runtime entry point. Functions as a command-line interface (CLI) and loopback system coordinating weather inputs, calling the prediction layer, and displaying optimal routing tables.
* **`src/predictor.py`**: The data science layer. Outlines and executes a Scikit-Learn `RandomForestClassifier` that processes real-time rainfall data against physical municipal traits (elevation, drainage points) to predict specific flood risks.
* **`src/graph.py`**: Structural model of regional and inter-island geography. Utilizes a dynamic **Adjacency List** graph where travel costs automatically scale up toward infinity if a destination node's calculated flood threat passes critical thresholds.
* **`src/optimizer.py`**: Operations research center. Implements a high-efficiency **Dijkstra’s Algorithm** optimized via a binary min-priority queue (`heapq`) to compute the absolute lowest-cost, safest path across penalized networks.
* **`tests/test_project.py`**: Automated testing framework engineered using `pytest` to validate ML probability models, graph edge weights, and pathfinding accuracy under catastrophic constraints.

---

