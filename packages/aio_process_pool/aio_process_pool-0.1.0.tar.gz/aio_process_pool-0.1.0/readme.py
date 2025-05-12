import asyncio

from aio_process_pool import ProcessPool, Executor

def foo(x=7):
    return x

# sync
executor = Executor()
assert executor.map(foo, [1, 2, 3]) == [1, 2, 3]
executor.shutdown()

# async
async def example():
    pool = ProcessPool()
    executor = Executor()

    # run a function in the pool
    assert await pool.run(foo, 2) == 2
    # map using a process pool
    assert await pool.map(foo, [1, 2, 3]) == [1, 2, 3]

    # use the executor with run_in_executor from asyncio
    loop = asyncio.get_event_loop()
    assert await loop.run_in_executor(executor, foo) == 7

    # use submit
    concurrent_future = executor.submit(foo, 3)
    assert await asyncio.wrap_future(concurrent_future) == 3

    # map again
    assert await executor.map_async(foo, [1, 2, 3]) == [1, 2, 3]

    pool.shutdown()
    await executor.shutdown_async()

asyncio.run(example())
