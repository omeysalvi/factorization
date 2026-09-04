# Factorization via Rectangular Hyperbola Divisor Ratios

This repository explores a novel integer factorization algorithm inspired by the paper *"New Interesting Property and Application of the Rectangular Hyperbola"* (2022). It maps the integer factorization problem $N = p \times q$ onto a rectangular hyperbola $xy = N$ and searches for factors by bounding and subdividing the "divisor ratio" ($\beta = q/p$).

## Complete Algorithm Breakdown

### Core Concept
Instead of searching linearly for integers $p$ up to $\sqrt{N}$, this algorithm searches the domain of possible **divisor ratios** ($\beta$). 
Because the hyperbola $xy = N$ is symmetric, we can assume without loss of generality that $p \le q$, meaning the divisor ratio $\beta \ge 1$. The center of the hyperbola is at $x = y = \sqrt{N}$, corresponding to $\beta = 1$.

### The Search Process (`divisor_ratio_factorization.py`)
1. **Set Upper Bound ($\alpha$)**: The user provides an `angle_offset_degrees` which determines how far from the 45-degree center to search. This calculates a maximum divisor ratio $\alpha$. The algorithm will only search for factors where $q/p \le \alpha$.
2. **Calculate Depth ($K$)**: It calculates a binary search depth $K$ required to ensure that the physical length of the smallest arcs on the $x$-axis is smaller than a calculable threshold (`M_permissive`).
3. **Binary Search Tree**: Using a Depth-First Search (DFS) stack, the algorithm recursively divides the divisor ratio range $[1, \alpha]$ geometrically in half.
4. **Pruning (Proposition 3)**: At each step, it checks if the current arc's minimum divisor ratio $\beta_{min}$ is strictly greater than a "second value" threshold $V = \alpha^{1 - \frac{1}{2^K}}$. If it is, the arc is discarded under the hypothesis that it cannot contain an odd pair.
5. **Sieving**: Once an arc is subdivided enough that its physical length on the $x$-axis is $\le$ `M_permissive`, a prime sieve is run over that interval to weed out multiples of small primes, and trial division is performed on the remaining candidates.

### Intricacies and Gotchas
* **The "Perfect Square" Illusion**: If you test the algorithm on a perfect square (where $p = q = \sqrt{N}$), the algorithm will find the factor in **0.00 seconds**. This is because the search begins precisely at the center of the hyperbola ($\beta=1$). The algorithm naturally checks values closest to $\sqrt{N}$ first. It gives the illusion of immense speed, but it is just luck of the starting position.
* **The Pruning Fallacy**: The mathematical pruning condition ($V \approx \alpha^{1 - 1/2^K}$) evaluates to a number extremely close to $\alpha$ for large numbers (e.g., for a 70-digit number, $K=94$, meaning $V = \alpha^{1 - 1/2^{94}} \approx \alpha$). Because of this, the pruning condition only shaves a microscopic sliver off the far edge of the search space and does virtually nothing to reduce the bulk of the tree.
* **Over-engineered Trial Division**: By chopping the $x$-axis into blocks of size `M` and sieving them sequentially starting from $\sqrt{N}$ downwards, the algorithm is essentially just a highly sophisticated framework for doing standard trial division.

## Complexity Analysis

The time complexity of this algorithm evaluates to **$\mathcal{O}(\sqrt{N})$** (exponential relative to the number of digits).

* **The Search Space:** The algorithm searches the $x$-axis from $x = \sqrt{N}$ down to $x = \sqrt{N/\alpha}$. The physical distance it has to cover is proportional to $\sqrt{N}$.
* **The Binary Tree:** The recursive binary search breaks this massive distance into smaller chunks of size $M$ (`calculable_range`).
* **Number of Chunks:** The number of chunks (leaf nodes) is roughly $\frac{\sqrt{N}}{M}$.
* **Processing Time:** Running the prime sieve and trial division on a chunk of size $M$ takes $\mathcal{O}(M)$ time.
* **Total Time:** $\left(\frac{\sqrt{N}}{M}\right) \times \mathcal{O}(M) = \mathbf{\mathcal{O}(\sqrt{N})}$. The $M$ mathematically cancels out. 

For a true 70-digit semiprime where the factors are not extremely close to each other, $\sqrt{N}$ is around $10^{35}$. Even processing a billion numbers a second, standard hardware would not finish before the heat death of the universe.

## Repository Files

* **`divisor_ratio_factorization.py`**: The main algorithm implementation using a DFS binary search tree on the rectangular hyperbola with active branch pruning based on Proposition 3.
* **`base.py`**: An alternative, simpler script that attempts to find factors by sampling angles ($\theta$) in polar coordinates and "walking" up and down the integer grid near the hyperbola curve.
* **`benchmark.py`**: A benchmarking script utilizing `sympy.factorint` to establish the baseline factorization time for various test cases (RSA-100, 70-digit, 61-digit).
* **`find_known_divisor_ratio_angle_degrees.py`**: A utility script that takes two known factors $p, q$ and calculates the exact ideal angle offset (and $\alpha$) they represent on the hyperbola. This proves exactly what `angle_offset_degrees` is required in the main script to encapsulate the factors.
* **`find_theta.py`**: A script that translates the original Maple source code from the paper's appendix into Python, calculating the exact boundary points $Q_j$ on the hyperbola for the linear arc search.
* **`is_prime.py`**: A generic mathematical utility script for standard primality testing.
* **`test.py`**: A scratchpad script containing random large-integer arithmetic checks (squaring numbers, subtracting large ints) used during development.
