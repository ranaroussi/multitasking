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

__version__ = "0.0.2a"

from sys import exit as sysexit
from os import _exit as osexit

from threading import Thread, Semaphore
from multiprocessing import Process, cpu_count

__KILL_RECEIVED__ = False
__TASKS__ = []

# processing
__ENGINE__      = Thread
__MAX_THREADS__ = cpu_count()
__CPU_CORES__   = cpu_count()
__POOL__        = None

def set_max_threads(threads=None):
    global __MAX_THREADS__
    if threads is not None:
        __MAX_THREADS__ = threads
    else:
        __MAX_THREADS__ = cpu_count()

def set_engine(kind=""):
    global __ENGINE__
    if "process" in kind.lower():
        __ENGINE__ = Process
    else:
        __ENGINE__ = Thread

def _init_pool():
    global __POOL__, __MAX_THREADS__
    if __POOL__ is None:
        __POOL__ = Semaphore(__MAX_THREADS__)

def task(callee):
    global __POOL__, __ENGINE__, __KILL_RECEIVED__, __TASKS__

    _init_pool()

    def _run_via_pool(*args, **kwargs):
        with __POOL__:
            return callee(*args, **kwargs)

    def async_method(*args, **kwargs):
        if not __KILL_RECEIVED__:
            task = __ENGINE__(target=_run_via_pool, args=args, kwargs=kwargs, daemon=False)
            __TASKS__.append(task)
            task.start()
            return task

    return async_method

def wait_for_tasks(*args, **kwargs):
    global __KILL_RECEIVED__, __TASKS__
    __KILL_RECEIVED__ = True

    try:
        running = len([t.join(1) for t in __TASKS__ if t is not None and t.isAlive()])
        while running > 0:
            running = len([t.join(1) for t in __TASKS__ if t is not None and t.isAlive()])
    except:
        pass
    return True

def killall(*args, **kwargs):
    global __KILL_RECEIVED__
    __KILL_RECEIVED__ = True
    try:
        sysexit(0)
    except SystemExit:
        osexit(0)
