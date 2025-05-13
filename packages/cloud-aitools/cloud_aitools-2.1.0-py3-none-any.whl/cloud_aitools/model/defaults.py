from concurrent.futures import ProcessPoolExecutor
import os

BUCKET_NUM = 8
BUCKET_PREFIX = "aicompute"
PUBLIC_APPID = "1251001002"
PROC_NUM = max(cpu_num - 1 if (cpu_num := os.cpu_count()) and cpu_num > 1 else 1,  64)
