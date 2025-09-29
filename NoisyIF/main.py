import asyncio
from mcpuniverse.tracer.collectors import FileCollector
# from mcpuniverse.tracer.collectors import MemoryCollector  
from mcpuniverse.benchmark.runner import BenchmarkRunner
from mcpuniverse.callbacks.handlers.vprint import get_vprint_callbacks


async def context_sythtic():
    # trace_collector = MemoryCollector()
    trace_collector = FileCollector(log_file="test.log")
    # Choose a benchmark config file under the folder "mcpuniverse/benchmark/configs"
    benchmark = BenchmarkRunner("Configs/data.yaml")
    # Run the specified benchmark
    results = await benchmark.run(
        trace_collector=trace_collector,
        callbacks=get_vprint_callbacks()
    )
    # Get traces
    trace_id = results[0].task_trace_ids["Tasks/test.json"]
    trace_records = trace_collector.get(trace_id)


async def main():
    # 合成context
    context_sythtic()

if __name__ == "__main__":
    asyncio.run(main())
    



# =======================================================
# import unittest
# import pytest
# from mcpuniverse.tracer.collectors import FileCollector
# from mcpuniverse.benchmark.runner import BenchmarkRunner
# from mcpuniverse.benchmark.report import BenchmarkReport
# from mcpuniverse.callbacks.handlers.vprint import get_vprint_callbacks

# class TestBenchmarkRunner(unittest.IsolatedAsyncioTestCase):

#     @pytest.mark.skip
#     async def test(self):
#         trace_collector = FileCollector(log_file="log/3d_design.log")
#         benchmark = BenchmarkRunner("test/3d_design.yaml")

#         benchmark_results = await benchmark.run(trace_collector=trace_collector, callbacks=get_vprint_callbacks())
#         print(benchmark_results)
#         report = BenchmarkReport(benchmark, trace_collector=trace_collector)
#         report.dump()

#         print('=' * 66)
#         print('Evaluation Result')
#         print('-' * 66)
#         for task_name in benchmark_results[0].task_results.keys():
#             print(task_name)
#             print('-' * 66)
#             eval_results = benchmark_results[0].task_results[task_name]['evaluation_results']
#             for eval_result in eval_results:
#                 print("func:", eval_result.config.func)
#                 print("op:", eval_result.config.op)
#                 print("op_args:", eval_result.config.op_args)
#                 print("value:", eval_result.config.value)
#                 print('Passed?:', "\033[32mTrue\033[0m" if eval_result.passed else "\033[31mFalse\033[0m")
#                 print('-' * 66)


# if __name__ == "__main__":
#     unittest.main()