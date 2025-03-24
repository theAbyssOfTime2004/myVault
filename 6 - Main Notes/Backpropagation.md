2024-11-22 15:21

[[DeepLearning]] [[Gradient Descent]], [[beginner]], [[Neural Networks]], [[học sâu]] 


Tags:

# Backpropagation in [[Neural Networks]]

## Overview

Backpropagation is the fundamental algorithm behind training [[neural networks]]. It calculates gradients of the loss function with respect to the network's weights and biases, enabling the network to learn from its errors.

## Key Components

### 1. Forward Pass

- Network processes input data through layers
- Each neuron performs:
    - Weighted sum of inputs
    - Addition of bias
    - Application of activation function
- Results in final output prediction

### 2. Error Calculation

- Compare predicted output with actual target
- Calculate loss/error using loss function
- Common loss functions:
    - Mean Squared Error (MSE)
    - Cross-Entropy Loss
    - Binary Cross-Entropy
	![[Pasted image 20241122154250.png]]
	* $L$ = loss function (note: we might see people using "cost" function and "loss" function in a confusing way, basically loss function and cost function is the same but one is for a sample of data and one is for the whole dataset, for example in this case the L loss function is only used for y^ = 17 therefore L = 4.5 )
	* $w_{0}$ = bias 
	* $z$ =weighted sum of inputs
	* $y^$ = activation 

### 3. Backward Pass

- Start from output layer
- Apply chain rule of calculus
- Calculate partial derivatives:
    - ∂Error/∂Weight
    - ∂Error/∂Bias
- Propagate error backwards through layers
	- ![[Pasted image 20241122154556.png]]
### 4. Weight Updates

- Adjust weights and biases using calculated gradients
- Formula: `new_weight = current_weight - learning_rate * gradient`
- Learning rate controls step size
- Smaller learning rate = more stable but slower
- Larger learning rate = faster but might overshoot
- ![[Pasted image 20241122154628.png]]

## Mathematical Example

``` python

# Forward Pass 
z = w * x + b      # weighted sum 
a = sigmoid(z)     # activation 
error = (a - target) 
# Backward Pass 
dE/dw = error * sigmoid_derivative(z) * x 
dE/db = error * sigmoid_derivative(z) 
# Update Step 
w = w - learning_rate * dE/dw 
b = b - learning_rate * dE/db`
```
## Important Considerations

### Advantages

- Efficient computation of gradients
- Scales well to deep networks
- Enables end-to-end training

### Challenges

1. Vanishing Gradients
    - Gradients become very small in deep networks
    - Solution: ReLU activation, skip connections
2. Exploding Gradients
    - Gradients become very large
    - Solution: Gradient clipping, proper initialization
3. Local Minima
    - Risk of getting stuck in suboptimal solutions
    - Solution: Momentum, adaptive learning rates

## Tips for Implementation

- Initialize weights properly (e.g., Xavier/Glorot initialization)
- Use mini-batch training for efficiency
- Implement gradient checking for verification
- Monitor training metrics (loss, accuracy)
- Consider using optimization algorithms:
    - SGD with momentum
    - Adam
    - RMSprop

## Related Concepts

- [[Gradient Descent]]
- Chain Rule
- Activation Functions
- Loss Functions, Cost Functions
- Optimization Algorithms

## References & Further Reading

1. Deep Learning by Goodfellow, Bengio, and Courville
2. Neural Networks and Deep Learning by Michael Nielsen
3. CS231n Stanford Course Materials
4. Neural Networks series video on youtube by 3Blue1Brown



# References
