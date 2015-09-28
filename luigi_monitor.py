import os
import inspect
import json
import luigi
import requests
from contextlib import contextmanager

events = {}

def discovered(task, dependency):
    raise NotImplementedError

def missing(task):
    task = str(task)
    if 'Missing' in events:
        events['Missing'].append(task)
    else:
        events['Missing'] = [task]

def present(task):
    raise NotImplementedError

def broken(task, exception):
    raise NotImplementedError

def start(task):
    raise NotImplementedError

def failure(task, exception):
    task = str(task)
    failure = {'task': task, 'exception': str(exception)}
    if 'Failure' in events:
        events['Failure'].append(failure)
    else:
        events['Failure'] = [failure]

def success(task):
    raise NotImplementedError

def processing_time(task, time):
    raise NotImplementedError

event_map = {
    "DEPENDENCY_DISCOVERED": {"function": discovered, "handler": luigi.Event.DEPENDENCY_DISCOVERED},
    "DEPENDENCY_MISSING": {"function": missing, "handler": luigi.Event.DEPENDENCY_MISSING},
    "DEPENDENCY_PRESENT": {"function": present, "handler": luigi.Event.DEPENDENCY_PRESENT},
    "BROKEN_TASK": {"function": broken, "handler": luigi.Event.BROKEN_TASK},
    "START": {"function": start, "handler": luigi.Event.START},
    "FAILURE": {"function": failure, "handler": luigi.Event.FAILURE},
    "SUCCESS": {"function": success, "handler": luigi.Event.SUCCESS},
    "PROCESSING_TIME": {"function": processing_time, "handler": luigi.Event.PROCESSING_TIME}
}

def set_handlers(events):
    if not isinstance(events, list):
        raise Exception("events must be a list")

    for event in events:
        if not event in event_map:
            raise Exception("{} is not a valid event.".format(event))
        handler = event_map[event]['handler']
        function = event_map[event]['function']
        luigi.Task.event_handler(handler)(function)

def format_message():
    job = os.path.basename(inspect.stack()[-1][1])
    text = ["Status report for {}".format(job)]
    if 'Failure' in events:
        text.append("*Failures:*")
        if len(events['Failure']) > 5:
            text.append("More than 5 failures. Please check logs.")
        else:
            for failure in events['Failure']:
                text.append("Task: {}; Exception: {}".format(failure['task'], failure['exception']))
    if 'Missing' in events:
        text.append("*Tasks with missing dependencies:*")
        if len(events['Missing']) > 5:
            text.append("More than 5 tasks with missing dependencies. Please check logs.")
        else:
            for missing in events['Missing']:
                text.append(missing)
    if len(text) == 1:
        text.append("Job ran successfully!")
    text = "\n".join(text)
    return text

def send_message(slack_url):
    text = format_message()
    if not slack_url:
        print "slack_url not provided. Message will not be sent"
        print text 
        return False
    payload = {"text": text}
    r = requests.post(slack_url, data=json.dumps(payload))
    if not r.status_code == 200:
        raise Exception(r.text)
    return True

@contextmanager
def monitor(events=['FAILURE', 'DEPENDENCY_MISSING'], slack_url=None):
    if events:
        h = set_handlers(events)
    yield
    m = send_message(slack_url)
