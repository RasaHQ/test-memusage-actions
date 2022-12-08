import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Text, List, Tuple, Optional, Union

import memory_profiler
import psutil


PROFILING_INTERVAL = 0.1
max_memory_threshold_mb = 100


def write_results(base_name: Text, results: List[Tuple[float, float]]) -> None:
    mprof_plot = Path(f"{base_name}_plot.txt")
    mprof_results = Path(f"{base_name}_raw.json")

    # plot this via `mprof plot mprof_result.txt`
    with open(mprof_plot, "w") as f:
        for memory, timestamp in results:
            f.write(f"MEM {memory:.6f} {timestamp:.4f}\n")

    # dump result as json to be able analyze them without re-running the test
    with open(mprof_results, "w") as f:
        f.write(json.dumps(results))


def test_for_memory_leak() -> None:
    # Run as separate process to avoid other things affecting the memory usage.
    # Unfortunately `memory-profiler` doesn't work properly with
    # `multiprocessing.Process` as it can't handle the process exit
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            (
                f"from actions import ActionHelloWorld; "
                f"t = ActionHelloWorld();"
                f"t.run_once()"
            ),
        ],
        # Force TensorFlow to use CPU so we can track the memory usage
        env={"CUDA_VISIBLE_DEVICES": "-1"},
    )

    # Wait until process is running to avoid race conditions with the memory
    # profiling
    while not psutil.pid_exists(process.pid):
        time.sleep(0.01)

    results = memory_profiler.memory_usage(
        process,
        interval=PROFILING_INTERVAL,
        include_children=True,
        timestamps=True,
    )

    # `memory-profiler` sometimes adds `None` values at the end which we don't need
    results = [
        memory_timestamp
        for memory_timestamp in results
        if memory_timestamp is not None
    ]

    write_results("memory_usage_custom_action", results)

    max_memory_usage = max(results, key=lambda memory_time: memory_time[0])[0]
    assert max_memory_usage < max_memory_threshold_mb




if __name__ == "__main__":
    test_for_memory_leak()
