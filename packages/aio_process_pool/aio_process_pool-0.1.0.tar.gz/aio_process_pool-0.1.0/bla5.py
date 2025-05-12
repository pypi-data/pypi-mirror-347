import asyncio
import pytest
from aio_process_pool.worker import Worker
from aio_process_pool import ProcessPool

def foo(x):
    from time import sleep
    sleep(x)
    return x

async def delayed_shutdown(worker, delay):
    await asyncio.sleep(delay)
    worker.shutdown(kill=True)

@pytest.mark.asyncio
async def test_worker_shutdown():
    worker = Worker()
    futures = [worker.run(foo, 1), worker.run(foo, 2), worker.run(foo, 3)]
    loop = asyncio.get_event_loop()
    loop.call_soon(worker.shutdown)
    results = await asyncio.gather(*futures, return_exceptions=True)

    for r in results:
        assert isinstance(r, asyncio.CancelledError)

@pytest.mark.asyncio
async def test_worker_shutdown2():
    worker = Worker()
    futures = [worker.run(foo, 1), worker.run(foo, 2), worker.run(foo, 3)]
    futures += [delayed_shutdown(worker, 0.2)]
    results = await asyncio.gather(*futures, return_exceptions=True)
    for r in results[:-1]:
        assert isinstance(r, asyncio.CancelledError)
    assert results[-1] == None

tpi_pool = ProcessPool()
def blubb(): return True

@pytest.mark.asyncio
async def blub():
    assert await tpi_pool.run(blubb)

# async def blub():
#     await test_worker_shutdown()
#     await test_worker_shutdown2()

asyncio.run(blub())
