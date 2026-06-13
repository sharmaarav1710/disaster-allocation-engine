import heapq

def find_optimal_route(network, start_sector, target_sector):
    """
    Implements a risk-aware Dijkstra's Algorithm.
    Returns a tuple: (total_weight, path_list)
    If no safe path exists, returns (float('inf'), [])
    """
    # Priority Queue elements format: (cumulative_weight, current_node, path_taken)
    priority_queue = [(0.0, start_sector, [start_sector])]
    
    # Track the minimum weight to reach each sector
    visited_weights = {start_sector: 0.0}
    
    while priority_queue:
        current_weight, current_node, path = heapq.heappop(priority_queue)
        
        # If we reached our destination, return the optimized path and cost
        if current_node == target_sector:
            return current_weight, path
            
        # If we found a worse path to an already processed node, skip it
        if current_weight > visited_weights.get(current_node, float('inf')):
            continue
            
        # Explore connected neighboring roads
        for neighbor in network.get_neighbors(current_node):
            # Calculate weight dynamically considering real-time AI risk scores
            road_weight = network.get_dynamic_weight(current_node, neighbor)
            next_weight = current_weight + road_weight
            
            # If this road is safer/faster than previously recorded routes, traverse it
            if next_weight < visited_weights.get(neighbor, float('inf')):
                visited_weights[neighbor] = next_weight
                heapq.heappush(priority_queue, (next_weight, neighbor, path + [neighbor]))
                
    # If the priority queue empties out without hitting the target, the sector is cut off
    return float('inf'), []