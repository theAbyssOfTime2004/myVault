2024-11-23 10:12


Tags:

# Fuzzy Logic
## Introduction to fuzzy thinking

- Fuzzy logic reflects how people think. It attempts to model our sense of words, our decision making and our common sense. As a result, leading to new, more human and intelligent system
- represent truth values to all real number in the interval $(0;1)$
	- For example, the possibility that a man 181cm tall is really tall might be set to a value of 0.86. It is likely that the man is tall.
- 1965 Zadeh published paper about "Fuzzy sets"
- Unlke binary boolean logic, fuzzy logic is multi-valued, uses the continuum of logical values betwwen 0 (completely false) and 1 (completely true)
- Fuzzy logic is a set of mathematical principles for knowledge representation based on degrees of membership
![[Pasted image 20241123102639.png]]

![[Pasted image 20241123103026.png]]

![[Pasted image 20241123103341.png]]

## Fuzzy sets 
$$ \mu_A(x): X \to [0, 1] $$

where: - $X$ is the universe of discourse. - $\mu_A(x)$ is the degree of membership of element $x$ in fuzzy set $A$. 
-  Types of Membership Functions:
	-  Triangular Membership Function $$ \mu_A(x) = \begin{cases} 0 & x \leq a \, \text{or} \, x \geq c \\ \frac{x - a}{b - a} & a < x \leq b \\ \frac{c - x}{c - b} & b < x < c \end{cases} $$ - Parameters: $a$, $b$, and $c$ define the shape.
# References
