2024-11-19 22:57


Tags: [[Deep Learning]], [[Machine Learning]], [[regression]], [[classification]], [[Neural Networks]]

# # Common Activation Functions in Neural Networks

## ReLU (Rectified Linear Unit)

### Definition

- Activation function defined as: f(x) = max(0, x)
- Outputs input if positive, zero otherwise

### Mathematical Representation

$$\text{ReLU}(x) = \max(0, x)$$

### Key Characteristics

- Simple computation
- Prevents vanishing gradient problem
- Creates non-linear transformation
- Sparse activation

### Application Domains

1. Computer Vision
    - Image classification
    - Object detection
    - Face recognition
2. Natural Language Processing
    - Text [[classification]]
    - Sentiment analysis
    - Machine translation
3. Signal Processing
    - Speech recognition
    - Time series prediction
    - Medical signal analysis

### Advantages

- Fast computation
- Helps deep networks learn quickly
- Reduces computational complexity
- Mitigates vanishing gradient issue

### Limitations

- Potential "dying" neurons
- No negative output gradient
- Unbounded positive output

## Variants: Leaky ReLU vs ELU

### Leaky ReLU

- Allows small gradient for negative inputs
- Formula: $$\text{LeakyReLU}(x) = \begin{cases} x & \text{if } x \geq 0 \\ \alpha x & \text{if } x < 0 \end{cases} $$
- Simple, computationally efficient

### ELU (Exponential Linear Unit)

- Smooth curve for negative inputs
- Formula: $$\text{ELU}(x) = \begin{cases} x & \text{if } x \geq 0 \\ \alpha (e^x - 1) & \text{if } x < 0 \end{cases} $$
- Better noise handling
- Closer to zero-centered activation

### Comparative Selection

- Leaky ReLU: When speed matters
- ELU: When precision is critical
## Other Common Function

### 1. Sigmoid


$$\text{Sigmoid}(x) = \frac{1}{1 + e^{-x}}$$`

- Output range: (0, 1)
- Soft threshold function
- Used in binary classification
- Prone to vanishing gradient

### 2. Tanh (Hyperbolic Tangent)

$$\text{Tanh}(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

- Output range: (-1, 1)
- Zero-centered
- Better than sigmoid for hidden layers
- Still has vanishing gradient issue

### 3. Softmax

$$\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum_{j} e^{x_j}}$$

- Used in multi-class classification
- Converts scores to probability distribution
- Ensures outputs sum to 1

### 4. Swish

$$\text{Swish}(x) = x \cdot \text{Sigmoid}(x) = x \cdot \frac{1}{1 + e^{-x}}$$
- Smooth, non-monotonic
- Performs better than ReLU in deep networks
- Self-gated activation function

### 5. GELU (Gaussian Error Linear Unit)

$$\text{GELU}(x) = x \cdot \Phi(x) = x \cdot \frac{1}{2}\left(1 + \text{erf}\left(\frac{x}{\sqrt{2}}\right)\right)$$

- Used in transformer models
- Approximates a form of noise-gated linear unit
- Preferred in NLP tasks

### 6. PReLU (Parametric ReLU)

$$\text{PReLU}(x) = \begin{cases} x & \text{if } x \geq 0 \\ \alpha x & \text{if } x < 0 \end{cases} $$

- Learnable slope for negative inputs
- Adaptive compared to Leaky ReLU
- Can adjust based on dataset

Key Considerations:

- Choose based on specific problem
- Consider computational complexity
- Test multiple activation functions



# References
