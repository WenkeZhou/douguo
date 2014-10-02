# !/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import os
import tempfile
import webbrowser


def main():
    limit, concurrency = 10, 20
    # filename = os.path.join(os.path.dirname(__file__), "whatsnew.dat")
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    create_processes(limit, jobs, results, concurrency)
    todo = add_jobs(filename, jobs)
    process(todo, jobs, results, concurrency)


def create_processes(limit, jobs, results, concurrency):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=(limit, jobs,
                results))
        process.daemon = True
        process.start()


def worker(limit, jobs, results):
    while True:
        try:
            feed = jobs.get()
        finally:
            jobs.task_done()


def add_jobs(filename, jobs):
    for todo, feed in enumerate(Feed.iter(filename), start=1):
        jobs.put(feed)
    return todo


def process(todo, jobs, results, concurrency):
    canceled = False
    try:
        jobs.join() # Wait for all the work to be done
    except KeyboardInterrupt: # May not work on Windows
        Qtrac.report("canceling...")
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        done, filename = output(results)
    Qtrac.report("read {}/{} feeds using {} threads{}".format(done, todo,
            concurrency, " [canceled]" if canceled else ""))
    print()
    if not canceled:
        webbrowser.open(filename)

if __name__ == "__main__":
    main()
