from agentdojo_core.task_suite.task_suite import TaskSuite

_SUITES: dict[str, TaskSuite] = {}


def register_suite(suite: TaskSuite) -> None:
    _SUITES[suite.name] = suite


def get_suites() -> dict[str, TaskSuite]:
    return _SUITES


def get_suite(suite_name: str) -> TaskSuite:
    return _SUITES[suite_name]
