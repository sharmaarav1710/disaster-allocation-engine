# Central Luzon Climate-Aware Logistics & Supply Chain Optimization Engine

 An AI-driven Disaster Management routing system designed to optimize emergency resource distribution across flood-prone municipalities in Central Luzon, Philippines (Bulacan, Pampanga, and Nueva Ecija).

This system merges **Machine Learning (Predictive Analytics)** with **Graph Theory (Dynamic Operations Research)** to route ground assets safely around high-risk zones during severe meteorological events.

---

## 🛠️ System Architecture

1. **Predictive Data Layer (`src/predictor.py`):** Trains a Scikit-Learn `RandomForestClassifier` on regional historical traits (elevation profiles, drainage choke points, and localized population metrics) to output a real-time flooding probability map.
2. **Network Topology Layer (`src/graph.py`):** Represents regional road infrastructure as an Adjacency List graph, where edge weights dynamically scale to `infinity` if destination nodes exceed safety risk parameters.
3. **Logistics Optimization Layer (`src/optimizer.py`):** Implements a high-efficiency Priority-Queue (`heapq`) Dijkstra's Algorithm to calculate optimized risk-adjusted supply chain corridors from an inland hub (`Clark_Hub`).

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```bash
python -m pip install -r requirements.txt