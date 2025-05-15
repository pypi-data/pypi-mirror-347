from collections import defaultdict

from agentdojo_core.task_suite.task_suite import TaskSuite

_SUITES: defaultdict[str, dict[str, TaskSuite]] = defaultdict(
    dict,
    {},
)


def register_suite(suite: TaskSuite, version: str) -> None:
    _SUITES[version][suite.name] = suite


def get_suites(benchmark_version: str) -> dict[str, TaskSuite]:
    return _SUITES[benchmark_version]


def get_suite(benchmark_version: str, suite_name: str) -> TaskSuite:
    return _SUITES[benchmark_version][suite_name]
