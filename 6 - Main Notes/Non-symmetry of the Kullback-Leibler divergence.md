2025-01-11 12:45


Tags: [[statistical]], [[information theory]]

# Non-symmetry of the Kullback-Leibler divergence

**Theorem:** The [Kullback-Leibler divergence](https://statproofbook.github.io/D/kl) is non-symmetric, i.e.

KL[P||Q]≠KL[Q||P](1)(1)KL[P||Q]≠KL[Q||P]

for some [probability distributions](https://statproofbook.github.io/D/dist) PP and QQ.

**Proof:** Let X∈X={0,1,2}X∈X={0,1,2} be a discrete [random variable](https://statproofbook.github.io/D/rvar) and consider the two [probability distributions](https://statproofbook.github.io/D/dist)

$$
\begin{aligned}
P:X∼Bin(2,0.5) \\
\ Q:X∼U(0,2)(2)(2)\quad \tag{2}
\end{aligned}
$$

where Bin(n,p)Bin(n,p) indicates a [binomial distribution](https://statproofbook.github.io/D/bin) and U(a,b)U(a,b) indicates a [discrete uniform distribution](https://statproofbook.github.io/D/duni).

Then, the [probability mass function of the binomial distribution](https://statproofbook.github.io/P/bin-pmf) entails that

$$
p(x) =
\begin{cases} 
\frac{1}{4}, & \text{if } x = 0 \\ 
\frac{1}{2}, & \text{if } x = 1 \\ 
\frac{1}{4}, & \text{if } x = 2 \quad \tag{2}
\end{cases}
$$


and the [probability mass function of the discrete uniform distribution](https://statproofbook.github.io/P/duni-pmf) entails that

q(x)=13,(4)(4)q(x)=13,

such that the [Kullback-Leibler divergence](https://statproofbook.github.io/D/kl) of PP from QQ is

KL[P||Q]=∑x∈Xp(x)⋅logp(x)q(x)=14log34+12log32+14log34=12log34+12log32=12(log34+log32)=12log(34⋅32)=12log98=0.0589(5)(5)KL[P||Q]=∑x∈Xp(x)⋅log⁡p(x)q(x)=14log⁡34+12log⁡32+14log⁡34=12log⁡34+12log⁡32=12(log⁡34+log⁡32)=12log⁡(34⋅32)=12log⁡98=0.0589

and the [Kullback-Leibler divergence](https://statproofbook.github.io/D/kl) of QQ from PP is

$$KL[Q||P]=∑x∈Xq(x)⋅logq(x)p(x)=13log43+13log23+13log43=13(log43+log23+log43)=13log(43⋅23⋅43)=13log3227=0.0566(6)(6)KL[Q||P]=∑x∈Xq(x)⋅log⁡q(x)p(x)=13log⁡43+13log⁡23+13log⁡43=13(log⁡43+log⁡23+log⁡43)=13log⁡(43⋅23⋅43)=13log⁡3227=0.0566$$

which provides an example for

KL[P||Q]≠KL[Q||P](7)(7)KL[P||Q]≠KL[Q||P]

and thus proves the theorem.

# References
