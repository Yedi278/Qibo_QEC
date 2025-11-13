import time

def timeit(f):  
    """Measures execution time."""

    def wrap(*args, **kwargs):

        t1 = time.time()  
        
        res = f(*args, **kwargs)  

        print(f"{f.__name__} ran in {time.time() - t1:.6f}s")

        return res
    
    return wrap