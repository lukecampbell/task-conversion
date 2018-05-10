task-conversion
===============

Converts a CSV of tasks into the taskwarrior JSON format

Copyright 2018 Luke Campbell See LICENSE for details.

Installation
============

```
python setup.py install
```

Usage
=====

```
task-conversion -o tasks.json Tasking.csv
```

From here you can use the Taskwarrior `task` command to import your tasks

```
task import tasks.json
```


