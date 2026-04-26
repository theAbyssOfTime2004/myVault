*2024-10-26 18:14


Tags: [[Machine Learning]], [[data scientist]], [[regression]], [[supervised learning]]


# Logistic Regression

### Logistic Regression Overview

Logistic regression is a mathematical model used to predict the outcome of a categorical dependent variable based on one or more predictor variables. It's commonly used in binary classification problems, where the target variable can only take two possible values.

#### Key Concepts

- **Binary Target Variable**: A categorical variable that can only take on two distinct categories (e.g., 0 and 1, yes and no, etc.).
- **Binary Response**: The probability of an event occurring (0 or 1, yes or no, etc.).
- **Sigmoid Function**: The logistic function used to model the relationship between the input features and the output probabilities.
	- $\sigma(x) = \frac{1}{1 + e^{-x}}$

#### How Logistic Regression Works

- Logistic Regression is a statistical technique that is used to modelize the relationship between binary dependent variable and 1 or many independent variables 
- Rather than directly predicting the binary outcome, logistic regression estimates the probability of occurrence of one of the two cases. This probability is calculated through a logistic or sigmoid function, which transforms the linear combination of predictor variables into probability values ranging from 0 to 1.
- The optimization goal of the model is to find a linear combination of predictor variables such that the logistic function produces results that best fit the observed data. The optimization technique commonly used is Maximum Likelihood Estimation (MLE).

#### Advantages and Applications

Logistic regression has several advantages, including:

- **Interpretability**: It provides coefficients that represent the strength and direction of relationships between the predictors and the response variable.
- **Handling Categorical Variables**: Logistic regression can handle categorical predictor variables with more than two categories using techniques like one-vs-all or multinomial logistic regression.

Some applications of logistic regression include:

- **Credit Risk Assessment**
- **Medical Diagnosis**
- **Social Network Analysis**

### Example Code

Here is an example of how to implement logistic regression using Python and the scikit-learn library:

```python
# To support both python 2 and python 3
from __future__ import division, print_function, unicode_literals
import numpy as np 
import matplotlib.pyplot as plt
np.random.seed(2)

X = np.array([[0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 1.75, 2.00, 2.25, 2.50, 
              2.75, 3.00, 3.25, 3.50, 4.00, 4.25, 4.50, 4.75, 5.00, 5.50]])
y = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1])

# extended data
X = np.concatenate((np.ones((1, X.shape[1])), X), axis = 0)
def sigmoid(s):
    return 1/(1 + np.exp(-s))

def logistic_sigmoid_regression(X, y, w_init, eta, tol = 1e-4, max_count = 10000):
    w = [w_init]    
    it = 0
    N = X.shape[1]
    d = X.shape[0]
    count = 0
    check_w_after = 20
    while count < max_count:
        # mix data 
        mix_id = np.random.permutation(N)
        for i in mix_id:
            xi = X[:, i].reshape(d, 1)
            yi = y[i]
            zi = sigmoid(np.dot(w[-1].T, xi))
            w_new = w[-1] + eta*(yi - zi)*xi
            count += 1
            # stopping criteria
            if count%check_w_after == 0:                
                if np.linalg.norm(w_new - w[-check_w_after]) < tol:
                    return w
            w.append(w_new)
    return w
eta = .05 
d = X.shape[0]
w_init = np.random.randn(d, 1)

w = logistic_sigmoid_regression(X, y, w_init, eta)
print(w[-1])
#the output will be
#[[-4.092695  ]
#[ 1.55277242]]
"""

with the output we have calculated. y could be predicted by the following formula: y = sigmoid(-4.1 + 1.55*x) and with generated data in training X set, the result will be:

[[ 0.03281144  0.04694533  0.06674738  0.09407764  0.13102736  0.17961209
   0.17961209  0.24121129  0.31580406  0.40126557  0.49318368  0.58556493
   0.67229611  0.74866712  0.86263755  0.90117058  0.92977426  0.95055357
   0.96541314  0.98329067]]

"""

#To plot this:
X0 = X[1, np.where(y == 0)][0]
y0 = y[np.where(y == 0)]
X1 = X[1, np.where(y == 1)][0]
y1 = y[np.where(y == 1)]

plt.plot(X0, y0, 'ro', markersize = 8)
plt.plot(X1, y1, 'bs', markersize = 8)

xx = np.linspace(0, 6, 1000)
w0 = w[-1][0][0]
w1 = w[-1][1][0]
threshold = -w0/w1
yy = sigmoid(w0 + w1*xx)
plt.axis([-2, 8, -1, 2])
plt.plot(xx, yy, 'g-', linewidth = 2)
plt.plot(threshold, .5, 'y^', markersize = 8)
plt.xlabel('studying hours')
plt.ylabel('predicted probability of pass')
plt.show()

```

We have the following visualization:

![[Pasted image 20241110233359.png]]

### DISCUSSION

- An advantage of Logistic Regression over PLA (Perceptron Learning Algorithm) is that it doesn't require the assumption that the two classes are linearly separable. However, the decision boundary is still linear in nature. Therefore, this model is only suitable for data where the two classes are nearly linearly separable. One type of data that Logistic Regression cannot handle well is when one class contains points inside a circle while the other class contains points outside that circle. This type of data is called non-linear. In the next few lessons, I will introduce other models that are more suitable for this type of data.
- Another limitation of Logistic Regression is that it requires data points to be generated _independently_ of each other. In reality, data points can be _influenced_ by each other. For example: if a group of students study together for 4 hours and they all pass the exam (assuming they studied very effectively), but a student studying alone for 4 hours might have a lower probability of passing. Nevertheless, for simplicity, when building models, people often assume that data points are independent of each other.
- **Logistic Regression is actually widely used in Classification problems.**
	- Despite the name "Regression," which typically refers to a fitting model, Logistic Regression is widely used in classification problems. After building the model, determining the class $y$ for a data point $x$ is done by comparing the following probability expressions: $$ P(y = 1 \mid x; \mathbf{w}); \quad P(y = 0 \mid x; \mathbf{w}) $$
	- If the first expression is greater than the second, we conclude that the data point belongs to class 1; otherwise, it does not belong to class 1 (thus belongs to class 0). Since the sum of these expressions is always equal to 1, a simpler way is to check whether $P(y = 1 \mid x; \mathbf{w})$ is greater than 0.5. If yes, assign it to class 1; if not, assign it to class 0.
- **The Boundary Created by Logistic Regression is Linear**

In fact, based on the argument above, we need to check:
$$ P(y = 1 \mid x; \mathbf{w}) > 0.5 $$ $$ \Leftrightarrow \frac{1}{1 + e^{-\mathbf{w}^T \mathbf{x}}} > 0.5 $$ $$ \Leftrightarrow e^{-\mathbf{w}^T \mathbf{x}} < 1 $$ $$ \Leftrightarrow \mathbf{w}^T \mathbf{x} > 0 $$
In other words, the boundary between the two classes is a line with the equation $\mathbf{w}^T \mathbf{x} > 0$. This is the equation of a hyperplane. Therefore, Logistic Regression creates a linear boundary.
# References
