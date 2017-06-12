#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multitasking: Non-blocking Python methods using decorators
# https://github.com/ranaroussi/multitasking
#
# Copyright 2016 Ran Aroussi
#
# Licensed under the GNU Lesser General Public License, v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = "0.0.4a"

from sys import exit as sysexit
from os import _exit as osexit

from threading import Thread, Semaphore
from multiprocessing import Process, cpu_count

__CPU_CORES__   = cpu_count()

# processing
__ENGINE__        = "thread"
__MAX_THREADS__   = cpu_count()
__KILL_RECEIVED__ = False
__TASKS__         = []
__POOLS__         = {}
__POOL_NAME__     = "Main"


def set_max_threads(threads=None):
    global __MAX_THREADS__
    if threads is not None:
        __MAX_THREADS__ = threads
    else:
        __MAX_THREADS__ = cpu_count()


def set_engine(kind=""):
    global __ENGINE__
    if "process" in kind.lower():
        __ENGINE__ = "process"
    else:
        __ENGINE__ = "thread"

def getPool(name=None):
    if name is None:
        name = __POOL_NAME__

    return {
        "engine": "thread" if __POOLS__[__POOL_NAME__]["engine"] == Thread else "process",
        "name": name,
        "threads": __POOLS__[__POOL_NAME__]["threads"]
    }

def createPool(name="main", threads=None, engine=None):
    global __MAX_THREADS__, __ENGINE__, __POOLS__, __POOL_NAME__

    __POOL_NAME__ = name

    try: threads = int(threads)
    except: threads = __MAX_THREADS__
    if threads < 2: threads = 0


    engine = engine if engine is not None else "thread"

    __MAX_THREADS__ = threads
    __ENGINE__ = engine

    __POOLS__[__POOL_NAME__] = {
        "pool": Semaphore(threads) if threads > 0 else None,
        "engine": Process if "process" in engine.lower() else Thread,
        "name": name,
        "threads": threads
    }

def task(callee):
    global __KILL_RECEIVED__, __TASKS__, __POOLS__, __POOL_NAME__

    # create default pool if nont exists
    if not __POOLS__:
        createPool()

    def _run_via_pool(*args, **kwargs):
        with __POOLS__[__POOL_NAME__]['pool']:
            return callee(*args, **kwargs)

    def async_method(*args, **kwargs):
        # no threads
        if __POOLS__[__POOL_NAME__]['threads'] == 0:
            return callee(*args, **kwargs)

        # has threads
        if not __KILL_RECEIVED__:
            task = __POOLS__[__POOL_NAME__]['engine'](
                target=_run_via_pool, args=args, kwargs=kwargs, daemon=False)
            __TASKS__.append(task)
            task.start()
            return task

    return async_method

def wait_for_tasks():
    global __KILL_RECEIVED__, __TASKS__, __POOLS__, __POOL_NAME__
    __KILL_RECEIVED__ = True

    if __POOLS__[__POOL_NAME__]['threads'] == 0:
        return True

    try:
        running = len([t.join(1) for t in __TASKS__ if t is not None and t.isAlive()])
        while running > 0:
            running = len([t.join(1) for t in __TASKS__ if t is not None and t.isAlive()])
    except:
        pass
    return True

def killall(cls):
    global __KILL_RECEIVED__
    __KILL_RECEIVED__ = True
    try:
        sysexit(0)
    except SystemExit:
        osexit(0)
