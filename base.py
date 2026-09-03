import time
import sympy as sp

#prime1 = 65839
#prime2 = 66617

prime1 = 9999925913
prime2 = 9987284561

semiprime = prime1 * prime2

start_time = time.time()

sample_range = 1000000
r_value_walk_samples = 5000
r_values = {}
theta_step = ((sp.pi/2)/sample_range).evalf()
theta = 0

for i in range(1, sample_range):
    theta += theta_step 
    r_values[theta] = int(sp.sqrt(2*semiprime/(sp.sin(2*theta))).evalf())

found_factors = None

r_value_index = 1

for theta, r_value in r_values.items():

    print("analyzing index: ", r_value_index, ", theta: ", theta, ", r_value: ", r_value)
    r_value_index += 1

    candidates = []
    
    # Go up r_value_walk_samples steps
    num = int((r_value * sp.cos(theta)).evalf())
    steps = 0
    while steps < r_value_walk_samples:
        if num < 0:
            break
        if num % 2 != 0 and num % 3 != 0:
            candidates.append(num)
            steps += 1
        num += 1
        
    # Go down r_value_walk_samples steps
    num = int((r_value * sp.cos(theta)).evalf())
    steps = 0
    while steps < r_value_walk_samples:
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

print(found_factors)