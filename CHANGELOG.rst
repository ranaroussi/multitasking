Change Log
===========

0.0.13
-------
- Added ``set_daemon(True|False)`` to opt in to daemon threads/processes for ``@task`` workers (default ``False`` preserves the historical non-daemon contract so existing callers continue to have the interpreter wait for in-flight tasks on exit). Long-lived fire-and-forget workers (schedulers, pollers, infinite cleanup loops) can now call ``multitasking.set_daemon(True)`` once — alongside ``set_engine()`` — to avoid blocking interpreter shutdown.

0.0.12
-------
- Full type hint support across the public API
- Added ``long_description_content_type`` for proper PyPI README rendering
- Declared Python 3.11 / 3.12 / 3.13 support in setup classifiers

0.0.11
-------
- Added ``get_list_of_tasks()``

0.0.10
-------
- Pass optional sleep time to ``wait_for_tasks()`` to prevent cpu burn

0.0.9
-------
- Changed licence to Apache License
- Setting ``config["KILL_RECEIVED"]=False`` after ``wait_for_tasks()`
- Code PEP'ed

0.0.8
-------
- Bugfix

0.0.7
-------
- Bugfix

0.0.6
-------
- Code linting / refactoring

0.0.5
-------
- Fixed ``takes 1 positional argument but 2 were given`` on ``killall()``

0.0.4
-------
- Added Python 3.6 support in pip setup

0.0.3
-------
- Added createPool() and getPool() methods

0.0.2
-------
- Can set max thread # and multi-processing mode

0.0.1
-------
- Initial Release
