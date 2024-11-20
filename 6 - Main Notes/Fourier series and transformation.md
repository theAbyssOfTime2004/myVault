2024-11-20 13:44


Tags:

# Fourier series and transform

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
    
    - $$ \int \frac{a_0}{2} \cos \left(\frac{m\pi x}{L}\right) \, dx = 0 $$ (since \( m > 0 \))  
    - $$ \int \cos \left(\frac{n\pi x}{L}\right) \cos \left(\frac{m\pi x}{L}\right) \, dx = L $$ when $(n = m)$ and $( = 0 )$ when $( n \neq m )$ 
    - $$ \int \sin \left(\frac{n\pi x}{L}\right) \cos \left(\frac{m\pi x}{L}\right) \, dx = 0 $$
- Therefore:
    
    - The $( {a_0} )$ term gives a result of 0. 
    * In the summation 
    * $\sum$, only the $( n = m )$ component is non-zero and equal to $( L {a_m} )$.  
    * The $( b_n )$ component gives a result of 0.
		$$ = 0 + \sum_{n=1}^{\infty} \left[ a_n L \delta_{m,n} + 0 \right] = L a_m $$

		

### Fourier transform 
- Is an mathematical operation that transforms a function in the time domain to its frequenct domain representation.

# References
