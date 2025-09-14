import os
import sys
import json
import hashlib
from typing import List, Optional, Tuple, Union, Callable, Any
from mcpuniverse.evaluator.functions import eval_func, FunctionResult
from mcpuniverse.evaluator.functions import compare_func

def is_error(
   text:str
   ):
   # 通过检测是否正常遵循了我们设定的格式来确认有效性
   if not isinstance(text, str) or not text:
      return True
   text_lower = text.lower()
   keywords = [
      "error", "exception", "failed", "invalid", "denied",
      "not found", "cannot", "unable to", "unsupported"
   ]
   if any(keyword in text_lower for keyword in keywords):
      return True
   return False

@compare_func(name="get_content")
async def get_content(
   llm_content: Any, 
   *args, **kwargs
   ):

   data=llm_content.result
   # 如果是空字符串、None就
   if is_error(data):
      return False, "fail to response"
   _, values=args
   
   with open("Data/raw_context.jsonl","a", encoding="utf-8") as file:
      file.write(json.dumps({
      "hash_id": hashlib.sha256(values["question"]),
      "question": values["question"],
      "content": data
      }, ensure_ascii=False)+"\n")
   return  True, "can do"