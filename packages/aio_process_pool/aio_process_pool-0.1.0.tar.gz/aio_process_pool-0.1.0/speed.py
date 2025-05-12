from concurrent.futures import ProcessPoolExecutor
from aio_process_pool import Executor

std_exe = ProcessPoolExecutor()
aio_exe = Executor()

