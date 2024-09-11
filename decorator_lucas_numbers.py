import time

def log_time_decorator(func):
    '''
    Decorator function that return the execution time of the decorated function
    '''
    def wrapper(*args, **kwargs):

        begin = time.time()
        
        func_return_val = func(*args, **kwargs)

        end = time.time()
        print("Total time: ", func.__name__, end - begin)

        return func_return_val

    return wrapper

# Lucas number function without memoization
def lucas(n):
    if n <= 0:
        return 2
    elif n == 1:
        return 1
    else:
        return lucas(n - 1) + lucas(n - 2)

# Dictionary that caches the results from the lucas number function
memo_cache = {0: 2, 1: 1}

# Lucas number function with memoization
def lucas_memo(n):
    if n in memo_cache:
        return memo_cache[n]
    else:
        ret_val = lucas_memo(n - 1) + lucas_memo(n - 2)
        memo_cache[n]  = ret_val
        return ret_val

# This function is used as wrapper so that the decorator funciton can log the total time for calculating the lucas number instead of each recursive call
@log_time_decorator   
def lucas_result(n, func):
    return func(n)

def prime_factors(n):
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    for i in range(3, int(n**0.5) + 1, 2):

        while n % i == 0:
            factors.append(i)
            n = n // i

    if n > 2:
        factors.append(n)

    return factors

def main():
    print(f'Lucas number of 35 (no memoization) is: {lucas_result(35, lucas)}')
    print(f'Lucas number of 35 (with memoization) is: {lucas_result(35, lucas_memo)}')
    print(f'Lucas number of 100 (with memoization) is: {lucas_result(100, lucas_memo)}')
    
    l = lucas_memo(60)
    pf = prime_factors(l)

    print(f'Prime factors of L(60): {l} = {'*'.join([str(prime) for prime in pf])}')

    l = lucas_memo(61)
    pf = prime_factors(l)

    print(f'Prime factors of L(61): {l} = {'*'.join([str(prime) for prime in pf])}')

if __name__ == '__main__':
    main()

