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
## Linguistic variables and hedges
- Linguistic variables are variables with a value made up of linguistic concepts (also known as linguistic words) rather than numbers, such as child, young, and so on.
- Linguistic hedges can be used to modify linguistic variables, which is an important feature. Linguistic hedges are primarily employed to aid in the more precise communication of the degree of correctness and truth in a particular statement.    
For example: If a statement John is Young is associated with the value 0.6 then _very young_ is automatically deduced as having the value 0.6 * 0.6 = 0.36. On the other hand, not _very young_ get the value ( 1 – 0.36 ), i.e., 0.64. In this example, the operator _very(X)_ is defined as $X * X$; however, in general, these operators may be uniformly, but flexible, defined to fit the application; this results in great power for the expression of both rules and fuzzy facts.  Linguistic modifiers such as very, more or less, fairly, and extremely rare examples of hedges. They can modify fuzzy predicates and fuzzy truth values.

![[Pasted image 20241123105944.png]]
# References
