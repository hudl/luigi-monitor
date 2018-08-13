# Changelog

## v0.1.0
* First version
* Monitors `DEPENDENCY_MISSING` and `FAILURE` events only
* Post to Slack

## v0.2.0
* Package structure updated

## v0.2.1
* Package changes for pypi

## v0.2.3
* Bugfix for monitoring tasks successful for retry of failed event
* Allow control of number of messages to print in notifications using `max_print` 

## v1.0.0
* Allow running from command line
* Don't send notification for recovered issues

## v1.0.1
* Fix bugfix with typo of `Failures` to `Failure`

## v1.0.2
* Add support for posting to slack with custom username using `username` option
* Update pypi long description

## v1.1.0
* Refactor events and notification logic
  * `events` control notification events too allowing exclusion of success notification

## v1.1.1
*  fixed typo for addressing failures in recorded_events dict `Failure` -> `FAILURE`

## v1.1.2
* set notify_events when running luigi-monitor from commandline

## v1.1.3
* enhanced message formatting (incl. emojis for task result states)
