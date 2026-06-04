import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        duration = time.perf_counter() - start_time
        print(f"函数: {func.__name__} 执行耗时: {duration:.6f} 秒")

        return result

    return wrapper


@timer
def d_test1():
    print(1)


@timer
def d_test2(a):
    print(a)


if __name__ == '__main__':
    d_test1()
    d_test2(22)

