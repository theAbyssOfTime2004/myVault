2025-10-24 10:05


Tags: [[DeepLearning]], [[optimizer]]
Keyword: **adaptive learning rate & regularization.**

# Adamw and Adam (optimizer)

- Adam is an optimization algorithm that adapts the learning rate for each param. It does this by calculating 2 things:
	- **Momentum**: A running average of past gradients
	- **RMSprop:** A running average of the squared gradients
- The Math:
	1. Gradient calculation: 
		- gt: Gradient of the loss function with respect to the params at time step t
		$$m_t = \beta_1 * m_{t-1} + (1-\beta_1) * g_t$$

# References
