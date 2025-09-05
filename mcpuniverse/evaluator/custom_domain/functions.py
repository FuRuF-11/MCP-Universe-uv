# 使用proxy的方法进行外部的二次开发

import sys
import os
from typing import List, Optional, Tuple, Union, Any
from mcpuniverse.evaluator.functions import eval_func, FunctionResult
from mcpuniverse.evaluator.functions import compare_func

@eval_func(name="extract_score")
async def extract_score(x: FunctionResult, *args, **kwargs) -> FunctionResult:
    """Extract numerical score from response."""
    if isinstance(x, FunctionResult):
        data = x.result
        if isinstance(data, dict) and 'score' in data:
            return FunctionResult(result=float(data['score']))
        elif isinstance(data, str):
            # Try to extract number from string
            import re
            match = re.search(r'\d+\.?\d*', data)
            if match:
                return FunctionResult(result=float(match.group()))
    raise ValueError("Could not extract score from input")


@compare_func(name="score_threshold")
async def score_threshold(a: Any, b: Any, *args, **kwargs) -> tuple[bool, str]:
    """Check if score meets threshold."""
    if isinstance(a, FunctionResult):
        a = a.result
    if isinstance(b, FunctionResult):
        b = b.result
    
    threshold = float(b)
    score = float(a)
    
    if score >= threshold:
        return True, ""
    return False, f"Score {score} below threshold {threshold}"


try:
    # 1. 计算外部实际模组的绝对路径
    # __file__ 是当前文件 (my_proxy_mod/__init__.py) 的路径
    # 我们需要向上回溯三层目录 (my_proxy_mod -> modules -> MCP-Universe-uv) 到达 NOISYIF 根目录
    # 然后再拼接上 'my_actual_mod'
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 从 /path/to/NOISYIF/MCP-Universe-uv/modules/my_proxy_mod
    # 变成 /path/to/NOISYIF/
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    
    # 构造实际模组的路径
    actual_mod_path = os.path.join(project_root, 'my_actual_mod')

    if project_root not in sys.path:
        # 使用 insert(0, ...) 确保我们的路径优先被搜索，避免潜在的命名冲突
        sys.path.insert(0, project_root)

    from my_actual_mod import *
    
    # (可选) 如果你不想用 *，也可以明确指定要暴露的内容
    # from my_actual_mod import feature_one, utils

    
except ImportError as e:
    raise e