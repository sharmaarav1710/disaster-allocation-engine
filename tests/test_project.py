import pytest
from src.graph import RegionalNetwork
from project import initialize_network, apply_ai_predictions, optimize_supply_route

def test_initialize_network():
    """Verifies that the graph structure properly registers all localized hubs and paths."""
    network = initialize_network()
    
    # Assert that all Central Luzon locations are correctly registered
    assert "Clark_Hub" in network.graph
    assert "Calumpit" in network.graph
    assert "Malolos_City" in network.graph
    
    # Assert that mapped routes are bidirectional
    assert "San_Fernando" in network.get_neighbors("Clark_Hub")
    assert "Clark_Hub" in network.get_neighbors("San_Fernando")


def test_apply_ai_predictions():
    """Verifies that processing weather data updates node risk values within boundaries."""
    network = initialize_network()
    
    # Simulate a moderate rain event (e.g., 150mm)
    network = apply_ai_predictions(network, rainfall=150.0)
    
    # Check that all locations received a valid probability index (between 0.0 and 1.0)
    for location in network.graph:
        risk = network.node_risks[location]
        assert 0.0 <= risk <= 1.0


def test_optimize_supply_route():
    """Verifies that Dijkstra's algorithm successfully computes logical risk-aware paths."""
    network = initialize_network()
    
    # Baseline condition: Force all risk levels to 0% (clear weather)
    for location in network.graph:
        network.node_risks[location] = 0.0
        
    # Test standard shortest path calculation from hub to coastal endpoint
    cost, path = optimize_supply_route(network, "Clark_Hub", "Malolos_City")
    assert cost < float('inf')
    assert path[0] == "Clark_Hub"
    assert path[-1] == "Malolos_City"
    
    # Critical state testing: Force Calumpit to become an impassable flood zone
    network.node_risks["Calumpit"] = 0.95
    
    # Re-route logistics pathing
    alt_cost, alt_path = optimize_supply_route(network, "Clark_Hub", "Malolos_City")
    
    # The optimization engine should automatically bypass Calumpit entirely via Plaridel
    assert "Calumpit" not in alt_path