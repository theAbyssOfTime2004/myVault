2025-10-24 10:05


Tags: [[Deep Learning]], [[optimizer]]
Keyword: **adaptive learning rate & regularization.**

# Adamw and Adam (optimizer)

- Adam is an optimization algorithm that adapts the learning rate for each param. It does this by calculating 2 things:
	- **Momentum**: A running average of past gradients
	- **RMSprop:** A running average of the squared gradients
- The Math:
	1. Gradient calculation: 
		- $g_t$: Gradient of the loss function with respect to the params at time step t
	2. Momentum calculation:
		- $m_t$: This is the momentum at time step t. Its calculated as a weighted average of the current gradient and the previous momentum
		$$m_t = \beta_1 * m_{t-1} + (1-\beta_1) * g_t $$
		- $\beta_1$ is a hyperparameter, typically set to 0.9. It controls how much wight we give to past gradients 
	3. RMSprop calculation: 
		- $v_t$ : this is RMSprop at time step t. Calculated as weighted average of the squared current gradient and the previous RMSprop:
		$$v_t = \beta_2 * v_{t-1} + (1 - \beta_2) * g{_t}^2 * $$
		- $\beta_2$ is another hyperparameter, typically set to 0.999.  
# References
