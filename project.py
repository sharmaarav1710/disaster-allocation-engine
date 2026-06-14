import sys
from src.graph import RegionalNetwork
from src.predictor import predict_flood_risk
from src.optimizer import find_optimal_route

def main():
    print("====================================================")
    print("  DISASTER MANAGEMENT RESOURCE ALLOCATION ENGINE   ")
    print("====================================================\n")
    
    
    network = initialize_network()
    
    
    print("--- Real-Time Disaster Weather Inputs ---")
    try:
        current_rainfall = float(input("Enter forecasted regional rainfall (mm) [e.g., 50 - 400]: "))
    except ValueError:
        print("Invalid numerical input. Defaulting to critical rainfall (350mm).")
        current_rainfall = 350.0
        
   
    network = apply_ai_predictions(network, current_rainfall)
    
    
    print("\n--- AI Regional Risk Assessment ---")
    for town, risk in network.node_risks.items():
        print(f" * {town:12} | Elevation: {get_town_specs(town)[0]:3}m | AI Flood Risk: {risk*100:5.1f}%")
        
    
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
 
    registry = {
        "Clark_Hub":     (210.0, 450,  0),
        "Gapan_City":    (34.0,  1100, 2),  
        "San_Fernando":  (7.0,   3800, 3),  
        "Calumpit":      (5.0,   2500, 4),  
        "Malolos_City":  (4.0,   3100, 2),  
        "Plaridel":      (11.0,  1900, 2)   
    }
    return registry.get(town_name, (200.0, 1000, 1))


def initialize_network():
    
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


def apply_ai_predictions(network, rainfall):

    for town in list(network.graph.keys()):
        elev, pop, bridges = get_town_specs(town)
        risk_score = predict_flood_risk(elev, rainfall, pop, bridges)
        network.node_risks[town] = risk_score
    return network


def optimize_supply_route(network, start, target):

    return find_optimal_route(network, start, target)


if __name__ == "__main__":
    main()