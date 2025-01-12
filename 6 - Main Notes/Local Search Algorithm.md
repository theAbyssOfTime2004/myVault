a2024-11-19 22:46


Tags: [[beginner]], [[search algorithm]]


# Local Search Algorithm

## Idea:
- In many optimization problems, the path to reach the solution is not important - what matters is the final state (goal)
	- Goal = The solution to the problem
- State space = Set of all "complete" configurations
- Objective: Find a configuration that satisfies the constraints
    - Example: n-queens problem (placing n queens on an n×n chessboard so that no queens can attack each other)
- In such problems, we can use local search algorithms
- At each moment, only one "current" state is stored - Goal: try to "improve" the current state (configuration) according to some predetermined criteria

### Hill Climbing: Steepest-Ascent Variant

- **Strategy**: Always move to neighbor with highest value
- **Characteristics**
    - Greedy local optimization
    - Rapidly converges to local maximum
    - Vulnerable to local optima
- **Procedure**
    1. Start at initial state
    2. Evaluate all neighboring states
    3. Move to highest-value neighbor
    4. Repeat until no better neighbor exists
- **Pros**
    - Simple implementation
    - Low memory requirements
- **Cons**
    - Can get trapped in local maxima
    - No backtracking mechanism
![[Pasted image 20250113021220.png]]

### Hill Climbing: First-Choice Variant

- **Strategy**: Select first neighbor that improves current state
- **Characteristics**
    - Less computational overhead
    - Randomized neighbor selection
    - Faster than steepest-ascent for complex landscapes
- **Procedure**
    1. Generate neighbors randomly
    2. Select first neighbor improving current state
    3. Move to that neighbor
    4. Repeat until no improvement possible

### Hill Climbing with Random Restart

- **Strategy**: Overcome local optima through randomized reinitializations
- **Characteristics**
    - Probabilistic escape from local maxima
    - Increases global search capability
- **Procedure**
    1. Perform standard hill climbing
    2. If stuck at local maximum
    3. Randomly restart search from new initial state
    4. Repeat multiple times
- **Pros**
    - More likely to find global optimum
    - Reduces dependency on initial state

### Simulated Annealing

- **Strategy**: Probabilistic technique for global optimization
- **Inspiration**: Physical annealing process in metallurgy
- **Key Characteristics**
    - Allows "downhill" moves with decreasing probability
    - Temperature parameter controls exploration
- **Procedure**
    1. Start at initial state
    2. Probabilistically accept worse states
    3. Probability decreases with "temperature"
    4. Gradually reduce acceptance of worse moves
- **Parameters**
    - Initial temperature
    - Cooling schedule
    - Neighborhood function
- **Pros**
    - Escapes local optima
    - Converges to global optimum
- **Cons**
    - Requires careful parameter tuning
![[Pasted image 20250113021406.png]]

## Comparative Analysis

| Algorithm                     | Completeness | Optimality    | Exploration Capability | Memory Usage |
| ----------------------------- | ------------ | ------------- | ---------------------- | ------------ |
| Steepest-Ascent Hill Climbing | No           | No            | Low                    | Low          |
| First-Choice Hill Climbing    | No           | No            | Medium                 | Low          |
| Random Restart Hill Climbing  | No           | No            | High                   | Medium       |
| Simulated Annealing           | No           | Probabilistic | High                   | Medium       |

## Practical Considerations

- Select algorithm based on:
    - Problem complexity
    - Computational resources
    - Convergence requirements
    - Global vs. local optimization needs

# References
