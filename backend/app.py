from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.src.graph import RegionalNetwork
from backend.src.predictor import predict_flood_risk
from backend.src.optimizer import find_optimal_route

app = FastAPI(
    title="Central Luzon Climate-Aware Logistics Engine API",
    description="Backend API powering flood risk predictions and supply chain routing optimization.",
    version="1.0.0"
)

# 🔐 CRITICAL: Enable CORS so your React frontend can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to initialize network
def get_initialized_network():
    network = RegionalNetwork()
    locations = ["Clark_Hub", "Gapan_City", "San_Fernando", "Calumpit", "Malolos_City", "Plaridel"]
    for loc in locations:
        network.add_location(loc)
        
    network.add_road("Clark_Hub", "San_Fernando", 28.0) 
    network.add_road("Clark_Hub", "Gapan_City",   52.0)
    network.add_road("San_Fernando", "Calumpit",  15.0) 
    network.add_road("San_Fernando", "Plaridel",  22.0) 
    network.add_road("Gapan_City", "Plaridel",    41.0) 
    network.add_road("Calumpit", "Malolos_City",  11.0) 
    network.add_road("Plaridel", "Malolos_City",  9.0)  
    network.add_road("Calumpit", "Plaridel",      8.0) 
    return network

# Static registry for specs: (Elevation, Population, Bridges, Latitude, Longitude)
def get_town_specs(town_name: str):
    registry = {
        "Clark_Hub":     (210.0, 450,  0, 15.1794, 120.5397), # Pampanga
        "San_Fernando":  (7.0,   3800, 3, 15.0286, 120.6898), # Pampanga
        "Gapan_City":    (34.0,  1100, 2, 15.3126, 121.0114), # Nueva Ecija
        "Calumpit":      (5.0,   2500, 4, 14.9152, 120.7645), # Bulacan
        "Plaridel":      (11.0,  1900, 2, 14.8872, 120.8572), # Bulacan
        "Malolos_City":  (4.0,   3100, 2, 14.8517, 120.8161)  # Bulacan
    }
    return registry.get(town_name, (200.0, 1000, 1, 15.0, 120.7))

class RouteRequest(BaseModel):
    rainfall: float
    target_town: str

@app.get("/")
def root():
    return {"message": "Disaster Management Resource Allocation API is online."}

@app.post("/api/optimize-route")
def optimize_route(payload: RouteRequest):
    network = get_initialized_network()
    
    # 1. Apply AI flood risk predictions (Fixed the 5-value unpacking issue here)
    for town in list(network.graph.keys()):
        elev, pop, bridges, lat, lon = get_town_specs(town)
        risk_score = predict_flood_risk(elev, payload.rainfall, pop, bridges)
        network.node_risks[town] = risk_score
        
    if payload.target_town not in network.graph:
        raise HTTPException(status_code=442, detail=f"Town '{payload.target_town}' not found in registry.")
        
    # 2. Calculate optimal safe route using Dijkstra's algorithm
    total_cost, path = find_optimal_route(network, "Clark_Hub", payload.target_town)
    
    # 3. Construct a structural map of coordinates for Leaflet map markers
    coordinate_map = {}
    for town in network.graph.keys():
        _, _, _, lat, lon = get_town_specs(town)
        coordinate_map[town] = {"lat": lat, "lon": lon}
    
    # 4. Construct response with both analytics data and physical mapping arrays
    return {
        "rainfall_input_mm": payload.rainfall,
        "destination": payload.target_town,
        "regional_risks": {town: f"{risk*100:.1f}%" for town, risk in network.node_risks.items()},
        "is_accessible": total_cost != float('inf') and len(path) > 0,
        "route": path,
        "route_coordinates": [[coordinate_map[node]["lat"], coordinate_map[node]["lon"]] for node in path if node in coordinate_map],
        "node_metadata": coordinate_map,
        "risk_adjusted_cost": total_cost if total_cost != float('inf') else None
    }