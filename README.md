## Luigi Monitor

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

```python
import luigi
from luigi_monitor import monitor

...

if __name__ == "__main__":
    with monitor(slack_url=<your_slack_url>, max_print=10):
        luigi.run(main_task_cls=MainClass)

```

This is a work in progress. Particularly, note that:

* It only sends notifications for FAILURE and DEPENDENCY_MISSING
events.
* It only sends notifications via Slack
* If you have more than 5 notifications in a category (FAILURE or
DEPENDENCY_MISSING), it will notify you of that rather than posting
a long list of errors.
