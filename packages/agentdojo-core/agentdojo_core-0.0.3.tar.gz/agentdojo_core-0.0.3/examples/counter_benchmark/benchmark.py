from agentdojo_core.task_suite import register_suite
from counter_benchmark.suites.counter import task_suite

# Name your benchmark to distinguish from our default benchmark.
register_suite(task_suite)
