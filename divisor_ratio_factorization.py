import math

def sieve_interval(x_min, x_max, sieve_limit):
    """
    Returns a list of candidate integers in [x_min, x_max] that are not
    divisible by any prime <= sieve_limit.
    """
    start = max(2, math.ceil(x_min))
    end = math.floor(x_max)
    
    if start > end:
        return []

    size = end - start + 1
    # is_prime_candidate[i] corresponds to integer (start + i)
    is_prime_candidate = [True] * size

    # We need primes up to sieve_limit.
    # Simple sieve to get primes up to sieve_limit
    primes = []
    is_prime = [True] * (sieve_limit + 1)
    for p in range(2, sieve_limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, sieve_limit + 1, p):
                is_prime[i] = False

    # Now sieve the interval [start, end]
    for p in primes:
        # Find the first multiple of p that is >= start
        first_multiple = math.ceil(start / p) * p
        if first_multiple == p:
            # If the first multiple is p itself, don't cross it out (it's prime)
            first_multiple += p
            
        for i in range(first_multiple - start, size, p):
            if i >= 0:
                is_prime_candidate[i] = False

    candidates = [start + i for i in range(size) if is_prime_candidate[i]]
    return candidates

def get_beta(theta_deg):
    """Returns the divisor ratio (>= 1) for a given angle in degrees."""
    theta_rad = math.radians(theta_deg)
    t = math.tan(theta_rad)
    if t > 0:
        return max(t, 1/t)
    return float('inf')

def get_x(N, theta_deg):
    """Returns the x coordinate on the hyperbola xy = N for a given angle."""
    theta_rad = math.radians(theta_deg)
    # y = x * tan(theta) => x^2 * tan(theta) = N => x = sqrt(N / tan(theta))
    t = math.tan(theta_rad)
    if t <= 0:
        return float('inf')
    return math.sqrt(N / t)

def search_angle(theta_start, theta_end, N, max_beta, calculable_range, sieve_limit):
    """
    Recursively searches the angular arc [theta_start, theta_end].
    """
    # Find the minimum beta in this arc.
    # Since beta = max(tan(t), cot(t)), its minimum is at 45 degrees (where beta=1).
    # If 45 is in the interval, min_beta = 1.
    # Otherwise, it's the beta of the endpoint closest to 45.
    if theta_start <= 45 <= theta_end or theta_end <= 45 <= theta_start:
        min_beta = 1.0
    else:
        beta_start = get_beta(theta_start)
        beta_end = get_beta(theta_end)
        min_beta = min(beta_start, beta_end)
        
    # Condition: if min_beta > max_beta, stop searching this branch.
    if min_beta > max_beta:
        return None

    # Determine x range
    x_start = get_x(N, theta_start)
    x_end = get_x(N, theta_end)
    x_min = min(x_start, x_end)
    x_max = max(x_start, x_end)
    
    interval_size = x_max - x_min
    
    if interval_size <= calculable_range:
        # Sieve and check
        candidates = sieve_interval(x_min, x_max, sieve_limit)
        for c in candidates:
            if N % c == 0:
                return (c, N // c)
        return None
        
    # Split the angle in half
    theta_mid = (theta_start + theta_end) / 2.0
    
    # Recursively search the two halves
    res = search_angle(theta_start, theta_mid, N, max_beta, calculable_range, sieve_limit)
    if res:
        return res
        
    res = search_angle(theta_mid, theta_end, N, max_beta, calculable_range, sieve_limit)
    return res

def factorize_by_beta(N, angle_offset_degrees=5.0, calculable_range=1_000_000, sieve_limit=1000):
    theta_min = 45.0 - angle_offset_degrees
    theta_max = 45.0 + angle_offset_degrees
    
    # Assumed max beta is the beta at the edges
    max_beta = max(get_beta(theta_min), get_beta(theta_max))
    
    print(f"Factoring {N}...")
    print(f"Angle range: {theta_min}° to {theta_max}°")
    print(f"Assumed max beta: {max_beta:.4f}")
    print(f"Calculable range: {calculable_range}")
    print(f"Sieve limit: {sieve_limit}")
    
    result = search_angle(theta_min, theta_max, N, max_beta, calculable_range, sieve_limit)
    if result:
        print(f"Found factors: {result[0]} and {result[1]}")
    else:
        print("No factors found in the assumed range.")
    return result

if __name__ == '__main__':
    # Test case: N = 4171 from Example 2 in the paper. 4171 = 43 * 97
    # 97 / 43 = 2.2558...
    # beta = tan(theta) => theta = atan(2.2558) = 66.08 degrees.
    # Offset from 45 is ~21 degrees. 
    # Test with N = 4171, and an angle offset of 25 degrees.
    factorize_by_beta(4171, angle_offset_degrees=25.0, calculable_range=100, sieve_limit=50)

    # Test case 2: User's params (offset=5) for a larger number where beta is very close to 1
    # Let's say p=1013, q=1019, N=1032247
    # beta = 1019/1013 = 1.0059 (very close to 1, offset < 1 degree)
    print("\n--- Testing with user params ---")
    factorize_by_beta(1032247, angle_offset_degrees=5.0, calculable_range=1_000_000, sieve_limit=1000)

    print("\n-----Testing new data-----")
    factorize_by_beta(4385996663, angle_offset_degrees=1.0, calculable_range=1_000_000, sieve_limit=1000)
