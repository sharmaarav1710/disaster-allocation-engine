class RegionalNetwork:
    def __init__(self):
        # We use a dictionary to represent the adjacency list
        # Format: { 'Sector_A': {'Sector_B': 5.0, 'Sector_C': 12.2} }
        self.graph = {}
        # Stores the environmental risk multiplier for each node
        self.node_risks = {}

    def add_location(self, sector_id, risk_score=0.0):
        """Adds a sector to the network map along with its baseline AI risk score."""
        if sector_id not in self.graph:
            self.graph[sector_id] = {}
        self.node_risks[sector_id] = risk_score

    def add_road(self, sector_u, sector_v, distance_km):
        """Creates a two-way road between two geographic sectors with a set distance."""
        if sector_u in self.graph and sector_v in self.graph:
            self.graph[sector_u][sector_v] = float(distance_km)
            self.graph[sector_v][sector_u] = float(distance_km)  # Bidirectional

    def get_dynamic_weight(self, sector_u, sector_v):
        """
        Calculates the real-world travel 'cost' of a road.
        As the destination sector's flooding risk increases, the road becomes 
        much harder/slower to traverse, mathematically increasing its weight.
        """
        base_distance = self.graph[sector_u][sector_v]
        destination_risk = self.node_risks.get(sector_v, 0.0)
        
        # Choke-point formula: If risk is 100%, traveling here is severely penalized or impossible
        if destination_risk >= 0.9:
            return float('inf')  # Road is entirely flooded/impassable
            
        # Dynamic Multiplier: A higher risk score increases the travel weight
        # Example: 5km road with 50% risk becomes a weight of 5 * (1 + 0.5) = 7.5
        return base_distance * (1.0 + destination_risk)

    def get_neighbors(self, sector_id):
        """Returns all sectors directly connected to the given sector."""
        return self.graph.get(sector_id, {}).keys()