import time
import math
import sys
import decimal

class ProgressTracker:
    def __init__(self, total):
        self.total = float(total)
        self.processed = 0.0
        self.last_percent = -1

    def update(self, amount):
        self.processed += float(amount)
        if self.total > 0:
            percent = int((self.processed / self.total) * 100)
        else:
            percent = 100
            
        if percent > self.last_percent:
            # Overwrite the line with the new progress
            sys.stdout.write(f"\rProgress: {percent}% ({int(self.processed)} / {int(self.total)} chunks)")
            sys.stdout.flush()
            self.last_percent = percent

def sieve_interval(x_min, x_max, primes):
    """
    Returns a list of candidate integers in [x_min, x_max] that are not
    divisible by any prime in the primes list.
    """
    start = max(2, int(math.ceil(x_min)))
    end = int(math.floor(x_max))
    
    if start > end:
        return []

    size = end - start + 1
    # is_prime_candidate[i] corresponds to integer (start + i)
    is_prime_candidate = [True] * size

    # Now sieve the interval [start, end]
    for p in primes:
        # Find the first multiple of p that is >= start (using integer division)
        first_multiple = ((start + p - 1) // p) * p
        if first_multiple == p:
            # If the first multiple is p itself, don't cross it out (it's prime)
            first_multiple += p
            
        for i in range(first_multiple - start, size, p):
            if i >= 0:
                is_prime_candidate[i] = False

    candidates = [start + i for i in range(size) if is_prime_candidate[i]]
    return candidates

def factorize_by_beta(N, angle_offset_degrees=5.0, calculable_range=1_000_000, sieve_limit=1000):
    decimal.getcontext().prec = 200
    N_dec = decimal.Decimal(N)
    
    # The paper's algorithm exclusively searches beta >= 1 (i.e. p <= q). 
    # Your bidirectional angle offset mathematically translates to an upper bound for the divisor ratio (alpha).
    alpha = math.tan(math.radians(45.0 + abs(angle_offset_degrees)))
    
    print(f"Factoring {N}...")
    print(f"Assumed max beta (alpha): {alpha:.4f}")
    print(f"Calculable range (M_permissive): {calculable_range}")
    print(f"Sieve limit: {sieve_limit}")
    
    # Step 2: Calculate k (the required geometric splitting depth)
    num = math.log(alpha)
    term = (math.sqrt(alpha) / math.sqrt(1.0 + alpha**2)) * (calculable_range / math.sqrt(float(N)))
    denom = math.log1p(term)
    k = math.floor(math.log2(num / denom))
    k = max(1, k) # Ensure at least 1
    
    print(f"Calculated depth k: {k}")
    
    # Pre-calculate primes for sieving
    primes = []
    is_prime = [True] * (sieve_limit + 1)
    for p in range(2, sieve_limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, sieve_limit + 1, p):
                is_prime[i] = False
                
    total_iterations = 2**(k - 1)
    progress = ProgressTracker(total_iterations)
    
    alpha_dec = decimal.Decimal(str(alpha))
    pow2k = decimal.Decimal(2**k)
    
    # Step 3: Loop j from 1 to 2^(k-1)
    N_int = int(N)
    for j in range(1, total_iterations + 1):
        # Calculate boundaries for chunk j
        pow_prev = decimal.Decimal(j - 1) / pow2k
        pow_curr = decimal.Decimal(j) / pow2k
        
        # x_start is Q_{j-1}.x (which is larger) and x_end is Q_j.x (which is smaller)
        x_max = N_dec.sqrt() / (alpha_dec ** pow_prev)
        x_min = N_dec.sqrt() / (alpha_dec ** pow_curr)
        
        candidates = sieve_interval(x_min, x_max, primes)
        
        for c in candidates:
            if N_int % c == 0:
                print() # Ensure a newline after progress output
                print(f"Found factors: {c} and {N_int // c}")
                return (c, N_int // c)
                
        progress.update(1)
        
    print() # Ensure a newline after progress output
    print("No factors found in the assumed range.")
    return None

if __name__ == '__main__':
    # Test case 1: N = 1333 (Example 1 from paper)
    # alpha = 2 corresponds to offset = atan(2) - 45 = ~18.435 degrees
    # Actually, we can just pass the equivalent offset. Or pass alpha directly.
    # We'll use offset that yields alpha = 2.0. tan(45 + offset) = 2 => offset = atan(2) - 45
    #offset_alpha2 = math.degrees(math.atan(2.0)) - 45.0
    #print("--- Example 1: N=1333, alpha=2.0 ---")
    #factorize_by_beta(1333, angle_offset_degrees=offset_alpha2, calculable_range=10, sieve_limit=10)

    # Test case 2: N = 4171 (Example 2 from paper)
    #print("\n--- Example 2: N=4171, alpha=2.0 ---")
    #factorize_by_beta(4171, angle_offset_degrees=offset_alpha2, calculable_range=10, sieve_limit=10)

    # Test case 3: 60-digit number
    #print("\n--- 60-digit number ---")
    #start_time = time.time()
    #factorize_by_beta(1606938044258990275541962093043441035048642082211966411156409, angle_offset_degrees=1.0, calculable_range=1_000_000, sieve_limit=100000)
    #end_time = time.time()

    print("\n--- 70-digit number ---")
    start_time = time.time()
    factorize_by_beta(8211485197231531569523737489341351104246108693889407026968257302824741, angle_offset_degrees=5.0, calculable_range=1_000_000, sieve_limit=100000)
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.6f} seconds")