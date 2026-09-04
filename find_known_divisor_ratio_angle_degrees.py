import math
import decimal

def find_ideal_angle_offset(p, q):
    # Ensure p <= q
    if p > q:
        p, q = q, p
        
    decimal.getcontext().prec = 200
    p_dec = decimal.Decimal(p)
    q_dec = decimal.Decimal(q)
    
    # Calculate exact beta (divisor ratio)
    beta = q_dec / p_dec
    beta_float = float(beta)
    
    # Calculate angle 
    theta_rad = math.atan(beta_float)
    theta_deg = math.degrees(theta_rad)
    
    # Offset from 45 degrees
    offset = theta_deg - 45.0
    
    print(f"Factor p: {p}")
    print(f"Factor q: {q}")
    print(f"Semiprime N: {p * q}")
    print(f"Exact Divisor Ratio (beta): {beta}")
    print(f"Ideal angle: {theta_deg:.15f} degrees")
    
    # Format offset cleanly
    if offset == 0.0:
        print("Ideal angle_offset_degrees: 0.0 (Factors are identical)")
    else:
        print(f"Ideal angle_offset_degrees: {offset:.15f} degrees")
        
    print("-" * 50)
    print("To guarantee finding these factors in divisor_ratio_factorization.py,")
    print(f"you must set angle_offset_degrees to a value slightly LARGER than {offset:.15f}")
    print("=" * 50 + "\n")
    
    return offset

if __name__ == '__main__':
    # Paper Example 1
    print("--- Example 1 ---")
    find_ideal_angle_offset(31, 43)
    
    # Paper Example 2
    print("--- Example 2 ---")
    find_ideal_angle_offset(43, 97)
    
    # You can add your own test cases here:
    find_ideal_angle_offset(83919638283712617062841452610119459, 97849387404059414449836008001003799)