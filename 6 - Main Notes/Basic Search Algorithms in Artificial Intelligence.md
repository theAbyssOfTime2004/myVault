2024-11-19 22:39


Tags: [[beginner]], [[search algorithm]]

# Fundamental Search Strategies

### Breadth-First Search (BFS)

- **Strategy**: Explores all neighbor nodes at present depth before moving to next level
- **Characteristics**
    - Guaranteed to find shortest path in unweighted graphs
    - Memory intensive (stores all nodes at current level)
    - Optimal for shallowest goal state
- **Time Complexity**: $O(b^d)$
- **Space Complexity**: $O(b^d)$
- **Best Used**: Shortest path problems with uniform cost edges

### Depth-First Search (DFS)

- **Strategy**: Explores as far as possible along each branch before backtracking
- **Characteristics**
    - Memory efficient
    - Risk of getting trapped in infinite paths
    - Not guaranteed to find optimal solution
- **Time Complexity**: $O(b^m)$
- **Space Complexity**: $O(bm)$
- **Best Used**: Maze solving, topological sorting

### Uniform Cost Search (UCS)

- **Strategy**: Expands node with lowest cumulative path cost
- **Characteristics**
    - Finds lowest-cost path
    - More sophisticated than BFS
    - Handles weighted graphs
- **Time Complexity**: $O(b^{C*/\varepsilon})$
- **Space Complexity**: $O(b^{C*/\varepsilon})$
- **Best Used**: Path finding with variable edge costs

### Greedy Best-First Search (GBFS)

- **Strategy**: Selects node closest to goal based on heuristic
- **Characteristics**
    - Uses problem-specific heuristic
    - Fast but not guaranteed optimal
    - Can get stuck in local optima
- **Time Complexity**: $O(b^m)$
- **Space Complexity**: $O(b^m)$
- **Best Used**: Problems with good heuristic estimates

### Dijkstra's Algorithm

- **Strategy**: Find shortest paths from source to all nodes
- **Characteristics**
    - Works on weighted graphs
    - Handles non-negative edge weights
    - Foundation for many routing protocols
- **Time Complexity**: $O(V^2)$ or $O(E + V log V)$
- **Space Complexity**: $O(V)$
- **Best Used**: Network routing, transportation networks

### A* Search Algorithm

- **Strategy**: Combines cost to reach node and estimated cost to goal
- **Characteristics**
    - Uses admissible heuristic
    - Guarantees optimal solution if heuristic is consistent
    - Most efficient informed search method
- **Time Complexity**: $O(b^d)$
- **Space Complexity**: $O(b^d)$
- **Best Used**: Path finding, game AI, robotics navigation

## Comparative Analysis

| Algorithm | Completeness | Optimality       | Time Complexity         | Space Complexity        |
| --------- | ------------ | ---------------- | ----------------------- | ----------------------- |
| BFS       | Yes          | Yes (unweighted) | $O(b^d)$                | $O(b^d)$                |
| DFS       | No           | No               | $O(b^m)$                | $O(bm)$                 |
| UCS       | Yes          | Yes              | $O(b^{C*/\varepsilon})$ | $O(b^{C*/\varepsilon})$ |
| GBFS      | No           | No               | $O(b^m)$                | $O(b^m)$                |
| Dijkstra  | Yes          | Yes              | $O(V^2)$                | $O(V)$                  |
| A*        | Yes          | Yes              | $O(b^d)$                | $O(b^d)$                |
|           |              |                  |                         |                         |

## Key Considerations

- Choose algorithm based on:
    - Problem characteristics
    - Graph/space properties
    - Computational resources
    - Optimality requirements

# References
