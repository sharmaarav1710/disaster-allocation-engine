import heapq

def find_optimal_route(network, start_sector, target_sector):


    priority_queue = [(0.0, start_sector, [start_sector])]
    

    visited_weights = {start_sector: 0.0}
    
    while priority_queue:
        current_weight, current_node, path = heapq.heappop(priority_queue)
        

        if current_node == target_sector:
            return current_weight, path
            
  
        if current_weight > visited_weights.get(current_node, float('inf')):
            continue

        for neighbor in network.get_neighbors(current_node):

            road_weight = network.get_dynamic_weight(current_node, neighbor)
            next_weight = current_weight + road_weight
            

            if next_weight < visited_weights.get(neighbor, float('inf')):
                visited_weights[neighbor] = next_weight
                heapq.heappush(priority_queue, (next_weight, neighbor, path + [neighbor]))
                

    return float('inf'), []