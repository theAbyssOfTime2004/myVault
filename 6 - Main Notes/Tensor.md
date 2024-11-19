2024-11-08 21:28


Tags: [[DeepLearning]]


# Tensor

Tensor is an umbrella term for "mathematical objects" or "containers" that have a rank/dimensionality associated with them.
### *Tensor Properties:*

Some key properties of tensors include:
- Scalars are rank-0 tensors, vectors are rank-1 tensors, matrices are rank-2 tensors and so on.
- One important property of a tensor is its shape. Shape is defined as: the number of _elements_ present in each axis/dimension of the tensor.
- Shape is written as entries for each dimension between parenthesis ( and ).
- From the shape we can determine: the rank/dimensionality of the tensor by shape's length, and the total number of values a tensor contains by multiplying all entries of shape.
### *Understanding shape equality*
-  The concept of shape equality can be simplified as below:
	- Two shapes $S1$ and $S2$ are considered equal if they have the same **values** at each corresponding position (or axis) when compared
	- Example 1: The shapes given below that correspond to rank-4 tensors are equal.
		$S1=(2,2,4,5)$
		$S2=(2,2,4,5)$
	- Example 2: The shapes given below that correspond to rank-5 tensors are not equal because when axis=2 (starting at left from 0) the entries is two shapes are different i.e.
		$S1=(2,3,5,4,9)$
		$S2=(2,3,6,4,9)$

### *Elementwise binary operations*
- **The following types of element-wise binary operations can be performed on tensors:**
	- **Addition**: $a + b$ <=> adds corresponding elements from two tensors
	- **Multiplication**: $a × b$ <=> multiplies corresponding elements from two tensors
	- **Exponentiation**: $a ^ b$ <=> raises corresponding elements in the first tensor to the power of corresponding elements in the second tensor
	- **Maximum**: $max(a, b)$ <=> returns the maximum value between corresponding elements in two tensors
	- **Minimum**: $min(a, b)$ <=> returns the minimum value between corresponding elements in two tensors
- **N-dimensional indices**
	- Example: N-dimensional indices for rank-4 tensor having shape $\begin{pmatrix}2&3&2&1\end{pmatrix}$
			$\begin{bmatrix}0&0&0&0\end{bmatrix}$
			$\begin{bmatrix}0&0&1&0\end{bmatrix}$
			$\begin{bmatrix}0&1&0&0\end{bmatrix}$
			$\begin{bmatrix}0&1&1&0\end{bmatrix}$
			$\begin{bmatrix}0&2&0&0\end{bmatrix}$
			$\begin{bmatrix}0&2&1&0\end{bmatrix}$
			$\begin{bmatrix}1&0&0&0\end{bmatrix}$
			$\begin{bmatrix}1&0&1&0\end{bmatrix}$
			$\begin{bmatrix}1&1&0&0\end{bmatrix}$
			$\begin{bmatrix}1&1&1&0\end{bmatrix}$
			$\begin{bmatrix}1&2&0&0\end{bmatrix}$
			$\begin{bmatrix}1&2&1&0\end{bmatrix}$
		To explain this in more detail:
		- When a tensor has a shape of $\begin{pmatrix}2&3&2&1\end{pmatrix}$, it means:
			1. The first dimension has 2 elements, so the indices in this dimension can only be 0 or 1.
			2. The second dimension has 3 elements, so the indices in this dimension can only be 0, 1, or 2.
			3. The third dimension has 2 elements, so the indices in this dimension can only be 0 or 1.
			4. The fourth dimension has 1 element, so the sole index in this dimension is 0.
			=> Therefore, the valid combinations of indices will be the values that fall within this range. For example: (0, 0, 0, 0), (0, 0, 1, 0), (1, 2, 1, 0), etc.	
-  **Shape broadcasting**
	- Shape broadcasting is a mechanism used to handle tensors of different sizes by aligning their shapes. This allows us to perform element-wise operations on tensors of varying dimensions.
	- **Algorithm for broadcasting**:
		1. Compare the shapes of the input tensors element-wise, starting from the rightmost dimension.
		2. If the dimensions are equal, or one of them is 1, move to the next dimension.
		3. If the dimensions differ and neither is 1, raise an error.
		4. If one tensor has fewer dimensions, prepend 1s to its shape until both tensors have the same number of dimensions.
		5. The resulting tensor will have the maximum size along each dimension of the input arrays.
		6. For dimensions where one tensor had size 1, that tensor is virtually copied along that dimension to match the other tensor's size.
		7. The resultant shape will be the final shape for both the input tensors.
	- **Example 1**: Let's have two tensors A and B with shapes (3,1) and (2) respectively. The steps to find the new shape for both tensors after broadcasting would be:
	
	1. Compare rightmost dimensions: 1 of $(A)$ vs 2 of $(B)$
	    - 1 can be broadcast to 2
	2. Move to next dimension: 3 of $(A)$ vs no dimension of $(B)$
	    - B's shape is expanded to $(1,2)$ for broadcasting
	3. Final broadcast shape: $(3,2)$
	
	Result: Both tensors are broadcast to the shape $(3,2)$
	
	**Example 2**: A and B with shapes $(4,3,2)$ and $(3,1)$ respectively. The steps for resultant shape after broadcasting:
	
	1. Compare rightmost dimensions: 2 of $(A)$ vs 1 of $(B)$
	    - $1$ can be broadcast to $2$
	2. Next dimension: 3 of $(A)$ vs 3 of $(B)$ - entries match so continue
	3. Next dimension: 4 of $(A)$ vs no dimension of $(B)$
	    - B's shape is expanded to $(1,3,1)$ for broadcasting
	4. Final broadcast shape: $(4,3,2)$
	
	Result: Tensor A remains $(4,3,2)$, while tensor $B$ is broadcast to $(4,3,2)$
	
	**Example 3: Non-broadcastable shapes** A and B with shapes $(3,2)$ and $(2,3)$ respectively.
	
	1. Compare rightmost dimensions: 2 of $(A)$ vs 3 of $(B)$
	    - Neither is 1, and they're not equal
	2. Broadcasting is not possible here.
	Result: The shapes aren't broadcastable


	- Shape broadcasting and matrix multiplication are different ideas in tensor operations.

Matrix multiplication is a strict operation in linear algebra where the number of columns in the first matrix must match the number of rows in the second. For example, to multiply a matrix A with shape (m, n) by a matrix B with shape (n, p), "n" must be the same in both.

In contrast, shape broadcasting is more flexible. It allows a smaller tensor to expand to match the shape of a larger tensor, so they can interact in element-wise operations like addition, subtraction, multiplication, etc. Broadcasting doesn’t require exact matching shapes, only that the dimensions can expand to work together.

So, while matrix multiplication has precise rules, shape broadcasting allows for easier element-wise operations across tensors with compatible shapes.
# References

