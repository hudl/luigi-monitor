## Luigi Monitor

[![Pypi Latest Version](https://img.shields.io/pypi/v/luigi-monitor.svg)](https://img.shields.io/pypi/v/luigi-monitor.svg)
[![License](https://img.shields.io/pypi/l/luigi-monitor.svg)](https://img.shields.io/pypi/l/luigi-monitor.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/luigi-monitor.svg)](https://img.shields.io/pypi/pyversions/luigi-monitor.svg)
[![Pypi Format](https://img.shields.io/pypi/format/luigi-monitor.svg)](https://img.shields.io/pypi/format/luigi-monitor.svg)
[![Build Status](https://travis-ci.org/hudl/luigi-monitor.svg?branch=master)](https://travis-ci.org/hudl/luigi-monitor)


![message](https://raw.github.com/hudl/luigi-monitor/master/message.png)

Send summary messages of your Luigi jobs to Slack.

### Overview

[Luigi](https://github.com/spotify/luigi) is a great tool for making
job pipelines, but it's hard to know the status of a run. Luigi has
support for error emails, but this requires configuring your machine
to send email, which is a hassle for short-lived EMR clusters. Further,
it sends an email for every failure, which can quickly swamp your inbox.

By contrast, this tool gathers all your failures and missing dependencies
and sends a summary Slack message when the job is finished.

### Usage

With default app username:
```python
import luigi
from luigi_monitor import monitor

...

if __name__ == "__main__":
    with monitor(slack_url=<your_slack_url>, max_print=10):
        luigi.run(main_task_cls=MainClass)

```

With dynamic app username:
```python
import luigi
from luigi_monitor import monitor

...

if __name__ == "__main__":
    with monitor(slack_url=<your_slack_url>, max_print=10, username="FooBar Monitor"):
        luigi.run(main_task_cls=MainClass)

```

Monitoring and notifying on various events:

Currently supports: `SUCCESS`, `DEPENDENCY_MISSING`, and `FAILURE` 

By default, all three of the above are monitored and notified on. If, `SUCCESS` event is monitored and 
all tasks succeed then the notification text is "Job ran successfully" instead of listing _all_ 
successful tasks. 

```python
import luigi
from luigi_monitor import monitor

...

if __name__ == "__main__":
    with monitor(slack_url=<your_slack_url>, events=['DEPENDENCY_MISSING', 'FAILURE']):
        luigi.run(main_task_cls=MainClass)
```

Alternatively:

`luigi-monitor --module path.to.module TaskName`

NB: if you plan to use luigi-monitor from the command line, set options using `luigi.cfg`:
```
[luigi-monitor]
slack_url=<slack_hook>
max_print=<int>
username=<string>
```


This is a work in progress. Particularly, note that:

* It only sends notifications via Slack
* Untested against Python3
