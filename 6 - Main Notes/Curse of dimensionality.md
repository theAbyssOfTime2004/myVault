2024-10-25 03:08


Tags: [[Machine Learning]], [[data scientist]], [[supervised learning]]




# Curse of dimensionality

## 1 Concentration of measure
 - As the number of dimensions increase, most of the volume of the high-dimensional shape (such as hypersphere or hypercube) concentrates near its boundary.
 - For example: if you randomly sample points from within a high-dimensional hypersphere, they will almost always be distancing from any reference points (such as center) and tend to be close to the surface. And omst of the points will seem to be at a similar distance from each other, leading to a sense of "sameness" in the data.
 - This is formally described by the fact that for a hypersphere in 𝑑 d-dimensional space, the proportion of the volume close to the surface approaches 1 as 𝑑 d increases.

![[Pasted image 20241026102710.png]]

- In lower dimension (2 or 5) we can see that the distance from center is relatively uniformed, as the dimension get shifting (from 10 to 200) the more left-skewed the plot get
- This phenomenon will cause struggle for:
	- Cluster algorithms 
	- Nearest neighbor search
	- Density estimation
## 2 Distances become similar in higher dimension
- The distances between points tend to become more uniform, which is counterintuitive compared to low-dimensional spaces. In a 2D or 3D space, we expect some points to be close and others to be far away, but in higher dimensions, almost all points are equidistant from each other.
- This is happening because of euclidean distance, $\sqrt{(x_1-y_1)^2+(x_2-y_2)^2 +...+(x_n-y_n)^2}$
, Each (xᵢ-yᵢ)² contributes a small positive value, with many dimensions, the sum of these squared differences tends toward an expected value, therefore the total distance grows.

![[Pasted image 20241026110613.png]]
<sub><sup>simple explanation</sup></sub>

-  In applications like nearest-neighbor search or clustering, this can be problematic. When all points are nearly equidistant, it becomes difficult to distinguish which points are genuinely close to each other and which are far apart.
	![[Pasted image 20241026111516.png]]
	

# References

   