import sys
from src.graph import RegionalNetwork
from src.predictor import predict_flood_risk
from src.optimizer import find_optimal_route

def main():
    print("====================================================")
    print("  DISASTER MANAGEMENT RESOURCE ALLOCATION ENGINE   ")
    print("====================================================\n")
    
    # 1. Initialize our geographic map layout
    network = initialize_network()
    
    # 2. Get current event parameters from user (e.g., severe weather forecast)
    print("--- Real-Time Disaster Weather Inputs ---")
    try:
        current_rainfall = float(input("Enter forecasted regional rainfall (mm) [e.g., 50 - 400]: "))
    except ValueError:
        print("Invalid numerical input. Defaulting to critical rainfall (350mm).")
        current_rainfall = 350.0
        
    # 3. Process data through our Machine Learning Layer
    network = apply_ai_predictions(network, current_rainfall)
    
    # 4. Display current state of the towns
    print("\n--- AI Regional Risk Assessment ---")
    for town, risk in network.node_risks.items():
        print(f" * {town:12} | Elevation: {get_town_specs(town)[0]:3}m | AI Flood Risk: {risk*100:5.1f}%")
        
    # 5. Run Routing Optimization Layer
    print("\n--- Supply Chain Logistics Optimization ---")
    start = "Clark_Hub"
    target = input(f"Enter destination town to route supplies from {start}: ").strip()
    
    if target not in network.graph:
        print(f"Error: Town '{target}' does not exist on our map registry.")
        sys.exit(1)
        
    total_cost, path = optimize_supply_route(network, start, target)
    
    print("\n=================== ROUTING RESULT ===================")
    if total_cost == float('inf') or not path:
        print(f"CRITICAL ALERT: {target} is ENTIRELY CUT OFF due to extreme flood risks!")
        print("Action Required: Deploy aerial rescue assets. Ground routes impassable.")
    else:
        print(f"OPTIMAL SAFE ROUTE FOUND:")
        print(" -> ".join(path))
        print(f"Risk-Adjusted Travel Cost: {total_cost:.2f} units (Base mileage + safety penalties)")
    print("======================================================\n")


def get_town_specs(town_name):
    """
    Registry helper containing real-world baseline geography details for Central Luzon.
    Format: (elevation_meters, population_density, bridge_count)
    """
    registry = {
        "Clark_Hub":     (210.0, 450,  0),  # High safety inland plateau
        "Gapan_City":    (34.0,  1100, 2),  # Inland river-adjacent plains
        "San_Fernando":  (7.0,   3800, 3),  # Low-lying dense urban center
        "Calumpit":      (5.0,   2500, 4),  # Extreme bottleneck confluence point
        "Malolos_City":  (4.0,   3100, 2),  # Coastal plain, tidal vulnerability
        "Plaridel":      (11.0,  1900, 2)   # Intermediate transit sector
    }
    return registry.get(town_name, (200.0, 1000, 1))


def initialize_network():
    """Function 1: Generates our regional network graph based on Philippine highway connections."""
    network = RegionalNetwork()
    locations = ["Clark_Hub", "Gapan_City", "San_Fernando", "Calumpit", "Malolos_City", "Plaridel"]
    
    # Register locations into graph
    for loc in locations:
        network.add_location(loc)
        
    # Map out realistic highway routing networks (e.g., via NLEX and MacArthur Highway)
    network.add_road("Clark_Hub", "San_Fernando", 28.0) # Down NLEX
    network.add_road("Clark_Hub", "Gapan_City",   52.0) # Eastern highway route
    network.add_road("San_Fernando", "Calumpit",  15.0) # Critical transit link
    network.add_road("San_Fernando", "Plaridel",  22.0) # Bypass route
    network.add_road("Gapan_City", "Plaridel",    41.0) # Cagayan Valley Road link
    network.add_road("Calumpit", "Malolos_City",  11.0) # Coastal arterial connection
    network.add_road("Plaridel", "Malolos_City",  9.0)  # Alternative coastal entry
    network.add_road("Calumpit", "Plaridel",      8.0)  # Inter-municipal linker
    
    return network


def apply_ai_predictions(network, rainfall):
    """Function 2: Feeds live variables into ML model to dynamically change graph nodes."""
    for town in list(network.graph.keys()):
        elev, pop, bridges = get_town_specs(town)
        # Call our trained random forest model to output a custom float probability
        risk_score = predict_flood_risk(elev, rainfall, pop, bridges)
        network.node_risks[town] = risk_score
    return network


def optimize_supply_route(network, start, target):
    """Function 3: Executes our custom dynamic pathfinding operations."""
    return find_optimal_route(network, start, target)


if __name__ == "__main__":
    main()