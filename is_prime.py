import time
import sympy

rsa_100 = 1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139
rsa_100_f1 = 37975227936943673922808872755445627854565536638199
rsa_100_f2 = 40094690950920881030683735292761468389214899724061

def is_prime(n: int) -> bool:
    # sympy uses the Miller-Rabin test for large numbers, which is extremely fast
    return sympy.isprime(n)

print("Starting primality test using sympy...")
start_time = time.time()
result = is_prime(rsa_100_f1)
elapsed = time.time() - start_time

print(f"Is rsa_100_f1 prime? {result}")
print(f"Time taken: {elapsed:.6f} seconds")