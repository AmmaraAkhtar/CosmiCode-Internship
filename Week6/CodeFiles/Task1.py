import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  
        result = func(*args, **kwargs)  
        end_time = time.time()     
        print(f"Execution time of {func.__name__}: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(2)  
    print("Slow function completed")


@timing_decorator
def fast_function():
    sum_val = sum(range(1000000))  
    print("Fast function completed")

slow_function()
fast_function()
