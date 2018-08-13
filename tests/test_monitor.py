# All tests pass successfully individually but not as a suite
import luigi
from luigi.mock import MockTarget
from luigi_monitor import monitor
import unittest
import os
import mock
import requests
import inspect
from collections import defaultdict


class TestMissingTask(luigi.ExternalTask):

    def output(self):
        return MockTarget('dummy.txt')


class TestSuccessTask(luigi.Task):
    num = luigi.Parameter()

    def output(self):
        return MockTarget('words.txt')

    def run(self):
        # write a dummy list of words to output file
        words = [
            'apple',
            'banana',
            'grapefruit'
        ]

        with self.output().open('w') as f:
            for word in words:
                f.write('{word}\n'.format(word=word))


# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):
    resp = mock.Mock(spec=requests.Response)
    resp.status_code = 200
    return resp


class TestLuigiMonitor(unittest.TestCase):
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_monitor_no_message(self, mock_post):
        with monitor(slack_url='mock://slack', events=['DEPENDENCY_MISSING'], host='testhostname') as m:
            luigi.run(main_task_cls=TestSuccessTask, local_scheduler=True, cmdline_args=['--num', '1'])
            self.assertDictEqual(m.recorded_events, {})
        self.assertEqual(mock_post.call_count, 0, 'Slack webhook called')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_monitor_missing_message(self, mock_post):
        with monitor(slack_url='mock://slack', events=['DEPENDENCY_MISSING'], host='testhostname') as m:
            luigi.run(main_task_cls=TestMissingTask, local_scheduler=True, cmdline_args=[])
            self.assertDictEqual(m.recorded_events, {'DEPENDENCY_MISSING': ['TestMissingTask()']})
        call_data = mock_post.call_args[1]['data']
        call_url = mock_post.call_args[0][0]
        expected = '{"text": ":x: Status report for ' + os.path.basename(
            inspect.stack()[-1][1]) + ' at *testhostname*:\\n' \
                                      'Task could not be completed!' \
                                      '\\n' \
                                      '\\t\\t\\t*Tasks with missing dependencies:*' \
                                      '\\n' \
                                      '\\t\\t\\t\\tTestMissingTask()"}'
        self.assertEqual(call_data, expected)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_monitor_success_message(self, mock_post):
        expected = defaultdict(list)
        expected['SUCCESS'] = ['TestSuccessTask(num=2)']
        expected['FAILURE'] = []
        expected['DEPENDENCY_MISSING'] = []
        with monitor(slack_url='mock://slack', host='testhostname') as m:
            luigi.run(main_task_cls=TestSuccessTask, local_scheduler=True, cmdline_args=['--num', '2'])
            self.assertDictContainsSubset(expected, m.recorded_events)

        call_data = mock_post.call_args[1]['data']
        call_url = mock_post.call_args[0][0]
        expected = '{"text": ":heavy_check_mark: Status report for ' + os.path.basename(
            inspect.stack()[-1][1]) + ' at *testhostname*:\\nTask ran successfully!\\n' \
                                      '\\t\\t\\t*Following 1 tasks succeeded:*' \
                                      '\\n' \
                                      '\\t\\t\\t\\tTestSuccessTask(num=2)"}'
        self.assertEqual(call_data, expected)
