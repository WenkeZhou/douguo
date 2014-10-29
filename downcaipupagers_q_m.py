# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import multiprocessing
import downcaipulists

zx_root_url = "http://www.douguo.com/caipu/zuixin/"


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


def add_jobs(PAGE_COUNT, jobs):
    for i in range(PAGE_COUNT):
        per_page_url = zx_root_url + str(i * 30)
        jobs.put(per_page_url)


def worker(jobs, results):
    while True:
        try:
            per_page_url = jobs.get()
            downcaipulists.down_per_page(per_page_url)
        finally:
            jobs.task_done()


def create_processes(concurrency, jobs, results):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=[jobs, results])
        process.daemon = True
        process.start()


def main():
    COUNT = 100
    concurrency = 80
    PAGE_COUNT = 300
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_processes(concurrency, jobs, results)
    add_jobs(PAGE_COUNT, jobs)
    process(jobs, results, concurrency)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print "一共花了 %f 完成下载" % total_time