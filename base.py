import time
import sympy as sp

prime1 = 9999925913
prime2 = 9987284561

prime1 = 65839
prime2 = 66617

semiprime = prime1 * prime2
semiprime_root = sp.sqrt(semiprime)

start_time = time.time()

theta_samples = 999
walk_samples = 99
r_values = {}
theta_step = ((sp.pi/2)/theta_samples).evalf()

theta_start = 0.698132 #40 degrees
theta_end = 0.872665 #50 degrees

theta = theta_start

while theta < theta_end:
    theta += theta_step 
    r_values[theta] = int(sp.sqrt(2*semiprime/(sp.sin(2*theta))).evalf())

print("size of dictionary: ", len(r_values))

found_factors = None

index = 1

for theta, r_value in r_values.items():

    print("analyzing index: ", index, ", theta: ", theta, ", r_value: ", r_value)
    index += 1

    candidates = []
    
    # Go up r_value_walk_samples steps
    num = int((r_value * sp.cos(theta)).evalf())
    steps = 0
    while steps < walk_samples:
        if num < 0:
            break
        if num % 2 != 0 and num % 3 != 0:
            candidates.append(num)
            steps += 1
        num += 1
        
    # Go down r_value_walk_samples steps
    num = int((r_value * sp.cos(theta)).evalf())
    steps = 0
    while steps < walk_samples:
        if num < 0:
            break
        if num > 1 and num % 2 != 0 and num % 3 != 0:
            candidates.append(num)
            steps += 1
        num -= 1
        
    for candidate in candidates:
        if sp.isprime(candidate):
            if semiprime % candidate == 0:
                found_factors = (candidate, semiprime // candidate)
                break
                
    if found_factors:
        break

end_time = time.time()

print(found_factors)
print(f"Time taken: {end_time - start_time:.6f} seconds")