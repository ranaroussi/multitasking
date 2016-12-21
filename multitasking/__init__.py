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

__version__ = "0.0.1a"

from threading import Thread
from sys import exit as sysexit
from os import _exit as osexit

__KILL_RECEIVED__ = False
__TASKS__ = []

def task(callee):
    global __KILL_RECEIVED__, __TASKS__
    def async_method(*args, **kwargs):
        if not __KILL_RECEIVED__:
            thread = Thread(target=callee, args=args, kwargs=kwargs, daemon=False)
            __TASKS__.append(thread)
            thread.start()
            return thread

    return async_method

def wait_for_tasks(*args, **kwargs):
    global __KILL_RECEIVED__
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
