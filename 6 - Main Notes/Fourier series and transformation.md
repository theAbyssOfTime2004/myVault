2024-11-20 13:44


Tags: [[Mathematics]] , [[DeepLearning]] 

# Fourier series and transform

![[Pasted image 20241130000441.png]]

### Fourier seriers 
- a fourier series is a mathematical representation of a periodic function as a sum of simpler fumctions called harmonics or sine waves.
	- Can be written as:
	-  $$ f(x) = \frac{a_0}{2} + \sum_{n=1}^\infty \left[ a_n \cos\left(\frac{n \pi x}{L}\right) + b_n \sin\left(\frac{n \pi x}{L}\right) \right]. $$
	- ${a_n} = \frac{1}{L} \int_{-L}^L f(x) \cos\left(\frac{n \pi x}{L}\right) dx, \quad$
	- ${b_n} = \frac{1}{L} \int_{-L}^L f(x) \sin\left(\frac{n \pi x}{L}\right) dx.$
	- this can be proven by multiplying both side of the expression by $\cos(\frac{m \pi x}{L})$ for some $m>0$ and integrating one gets:
		$$ \int_{-L}^{L} f(x) \cos \left( \frac{m\pi x}{L} \right) \, dx $$
		$$= \int_{-L}^{L} \frac{a_0}{2} \cos \left( \frac{m\pi x}{L} \right) \, dx + \sum_{n=1}^{\infty} \left[ a_n \int_{-L}^{L} \cos \left( \frac{m\pi x}{L} \right) \cos \left( \frac{n\pi x}{L} \right) \, dx + b_n \int_{-L}^{L} \cos \left( \frac{m\pi x}{L} \right) \sin \left( \frac{n\pi x}{L} \right) \, dx \right] $$
		
		- Analyze each part:
    
    - $$ \int \frac{a_0}{2} \cos \left(\frac{m\pi x}{L}\right) \, dx = 0 $$ since $( m > 0 )$  
			* The function $$ \cos \left( \frac{m \pi x}{L} \right) $$ oscillates with a period of $$ \frac{2L}{m}. $$ When we calculate the integral from $-L  \to  L,$  this function completes a whole number of periods (or at least one full period). For each half-period, from $-L \to  0$ , and from 
			*  $0  \to  L$,  the values of the cosine function in the negative and positive intervals are symmetric: $$\int_{-L}^{0} \cos \left( \frac{m \pi x}{L} \right) dx = - \int_{0}^{L} \cos \left( \frac{m \pi x}{L} \right) dx.$$
			* therefore: $$ \int_{-L}^{L} \cos \left( \frac{m \pi x}{L} \right) dx = 0. $$
    - $$ \int \cos \left(\frac{n\pi x}{L}\right) \cos \left(\frac{m\pi x}{L}\right) \, dx = L $$ when $(n = m)$ and $( = 0 )$ when $( n \neq m )$ 
    - $$ \int \sin \left(\frac{n\pi x}{L}\right) \cos \left(\frac{m\pi x}{L}\right) \, dx = 0 $$
- Therefore:
    
    - The $( {a_0} )$ term gives a result of 0. 
    * In the summation 
    * $\sum$, only the $( n = m )$ component is non-zero and equal to $( L {a_m} )$.  
    * The $( b_n )$ component gives a result of 0.
		$$ = 0 + \sum_{n=1}^{\infty} \left[ a_n L \delta_{m,n} + 0 \right] = L a_m $$

		

### Dirichlet condition
-  The function $f(x)$ satisfies the Dirichlet conditions if: 
	1. $f(x)$ is defined and bounded in the interval $[-L, L]$. 
	2. $f(x)$ has only a **finite number of discontinuities** in $[-L, L]$. 
	3. $f(x)$ has only a **finite number of maxima and minima** (extrema) in $[-L, L]$.
- ### Implications: 
	- At points of **continuity**, the Fourier series accurately reconstructs the value of the function $f(x)$. - 
	- At points of **discontinuity**, the Fourier series does not converge to the exact value of the function but instead converges to the **average of the values on both sides of the discontinuity**.

### Fourier transform 
- Is an mathematical operation that transforms a function in the time domain to its frequenct domain representation.
- This formulation allows the Fourier series to be expressed as a continuous integral, rather than a discrete sum, as the interval $[-L, L]$ becomes unbounded.
- The key steps are:
1. Rewrite the Fourier series using the continuous frequency variable $\Delta ω = nπ/L.$
2. As L approaches infinity, the summation becomes an integral over the continuous frequency domain.
3. The final Fourier series representation is an integral of the continuous Fourier coefficients cω multiplied by the complex exponential term exp(iωx).
- ![[Pasted image 20241128011834.png]] ![[Pasted image 20241128011818.png]]
# References

[But what is a Fourier series? From heat flow to drawing with circles | DE4](https://www.youtube.com/watch?v=r6sGWTCMz2k)

