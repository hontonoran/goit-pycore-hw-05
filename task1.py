def caching_fibonacci():
    """creates a closure with a cached version of fibonacci func,
    and the inner func uses dict 'cache' to store previously computed numbers"""
    cache = {}
    def inner(n):
        """computes N fibonacci number recursively and caches"""
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:  # if the result is already cached
            return cache[n]
        result = inner(n - 1) + inner(n - 2)
        cache[n] = result  # stores the computed result
        return result
    return inner

#usage example
fib = caching_fibonacci()
res_10 = fib(10)  # computes and caches fib(10)
print("Computing fib(10): {}".format(res_10))
res_15 = fib(15)  # computes and caches fib(15)
print("Computing fib(15): {}".format(res_15))
res_10_cached = fib(10)  # retrieves cached fib(10)
print("Retrieving cached fib(10): {}".format(res_10_cached))
res_15_cached = fib(15)  # retrieves cached fib(15)
print("Retrieving cached fib(15): {}".format(res_15_cached))

