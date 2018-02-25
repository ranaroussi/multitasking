#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multitasking: Non-blocking Python methods using decorators
# https://github.com/ranaroussi/multitasking
#
# Copyright 2016-2018 Ran Aroussi
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

import time
import random
import signal
import multitasking

# kill all tasks on ctrl-c
signal.signal(signal.SIGINT, multitasking.killall)

# to wait for task to finish, use:
# signal.signal(signal.SIGINT, multitasking.wait_for_tasks)


@multitasking.task
def hello(count):
    sleep = random.randint(1, 10) / 2
    print("Hello %s (sleeping for %ss)" % (count, sleep))
    time.sleep(sleep)
    print("Goodbye %s (after for %ss)" % (count, sleep))


if __name__ == "__main__":
    for i in range(0, 10):
        hello(i + 1)
