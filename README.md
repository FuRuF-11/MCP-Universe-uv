# NoisyIF

现在的Pipline是这样的：用一个ReAct agent调用各类MCP完成一些任务，这些任务产生不同长度的带噪声的long context（8k，12k，20k等等），然后我们以这些context中的信息为基础，构造类似于IFEval的可以解析的指令。然后，（指令+long context）就是我们的benchmark。

---

原MCP-Universe的docker中使用pip和conda管理环境，这里修改为使用uv管理。
使用MCP-Universe作为骨架创建合成数据的pipline

raw_context.jsonl
```json
{
    "hash_id": hash(question,sha256),
    "question": question,
    "content": data
}
```





