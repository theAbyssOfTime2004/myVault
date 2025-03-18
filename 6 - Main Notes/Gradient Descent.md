2024-11-19 22:55


Tags: [[Machine Learning]], [[DeepLearning]], [[beginner]]


# Gradient Descent: Quick note

## Definition

Gradient descent is an optimization algorithm used to find the minimum value of a function by iteratively adjusting parameters in [[machine learning]] models.

## Core Mechanism

1. **Basic Concept**:
    - Finds the steepest descent direction in a function
    - Takes small steps toward the minimum point
2. **Update Formula**:
    
``` python
    x_new = x_old - learning_rate * gradient(x_old)
```

## Key Components

- **Learning Rate**: Controls step size of descent
- **Gradient**: Indicates direction of steepest increase
- **Objective**: Minimize the loss function

## Learning Process

1. **Forward Pass**: Calculate model output
2. **Backward Pass**: Compute gradients and update weights
3. **Stopping Conditions**:
    - Reach predefined number of epochs
    - Loss falls below threshold
    - Loss stops decreasing

## Applications

- Training neural networks
- Optimizing [[machine learning]] models
- Solving non-linear optimization problems

## Important Considerations

- Choose appropriate learning rate
- Avoid getting stuck in local minima
- Adapt to specific problem characteristics

## Mathematical Intuition

- Resembles walking down a hill
- Continuously adjusts parameters
- Minimizes error/loss function systematically

# References
