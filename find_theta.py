import math
def estimation(alpha, M, N):
    """
    Estimates parameters based on the provided Maple procedure.
    """
    # k := floor( log2( ln(alpha) / ln( 1 + (sqrt(alpha) / sqrt(1 + alpha^2)) * (M / sqrt(N)) ) ) );
    num = math.log(alpha)
    den = math.log(1 + (math.sqrt(alpha) / math.sqrt(1 + alpha**2)) * (M / math.sqrt(N)))
    k = math.floor(math.log2(num / den))
    
    print(f"k={k}")
    
    powr = 2**k
    upper_bound = int(2**(k - 1))
    
    # for j from 1 to 2^(k-1) do
    for j in range(1, upper_bound + 1):
        # powr-th root of alpha^(j-1) is mathematically equivalent to alpha^((j-1)/powr)
        alpha_term = alpha ** ((j - 1) / powr)
        
        # x := evalf( sqrt(N) / (alpha^((j-1)/powr)) );
        x = math.sqrt(N) / alpha_term
        
        # y := evalf( (alpha^((j-1)/powr)) * sqrt(N) );
        y = alpha_term * math.sqrt(N)
        
        print(f"Q({j})=({x:f} , {y:f} )")
        
    # In Maple, after a 'for' loop finishes, the loop variable retains the value 
    # of the last bound + 1.
    j = upper_bound + 1
    
    # x := evalf( sqrt(N/alpha) ); y := evalf( sqrt(alpha*N) );
    x = math.sqrt(N / alpha)
    y = math.sqrt(alpha * N)
    
    print(f"Q({j})=({x:f} , {y:f} )")
    
    # printf("alpha might be bigger than %f\n", evalf( alpha^((powr-1)/powr) ));
    alpha_bigger_than = alpha ** ((powr - 1) / powr)
    print(f"alpha might be bigger than {alpha_bigger_than:f}")
# Example test call
estimation(1.5, 10, 15)