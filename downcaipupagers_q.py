# !/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import Queue
import downcaipulists
import time

zx_root_url = "http://www.douguo.com/caipu/zuixin/"


def created_threads(concurrency, jobs, results):
    for i in range(concurrency):
        thread = threading.Thread(target=worker, args=[concurrency, jobs, results])
        thread.daemon = True
        thread.start()


def worker(limit, jobs, results):
    while True:
        try:
            per_page_url = jobs.get()
            downcaipulists.down_per_page(per_page_url)
        finally:
            jobs.task_done()


def add_jobs(count, jobs):
    for i in range(count):
        per_page_url = zx_root_url + str(i * 30)
        jobs.put(per_page_url)


def process(jobs, results, concurrency):
    canceled = False
    try:
        jobs.join()
    except KeyboardInterrupt:
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        pass


def main():
    COUNT = 100
    concurrency = 10
    PAGE_COUNT = 30
    jobs = Queue.Queue()
    results = Queue.Queue()
    created_threads(concurrency, jobs, results)
    add_jobs(PAGE_COUNT, jobs)
    process(jobs, results, concurrency)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print "一共花了 %f 完成下载" % total_time