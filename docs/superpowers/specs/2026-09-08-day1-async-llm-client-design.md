# Day1 异步 LLM 客户端设计

## 目标

在 `day1/` 下创建一个由 Poetry 管理的最小 Python 工程，用于学习如何异步调用 LLM、处理请求失败，以及使用 Pydantic v2 校验结构化输出。

## 范围

- 运行时只使用 `aiohttp` 和 `pydantic>=2,<3`。
- 测试使用 Python 标准库 `unittest`，不额外引入测试依赖。
- 对接 OpenAI-compatible 的 `POST /chat/completions` 接口。
- 一次只处理一个请求；暂不实现重试、流式输出、工具调用和会话存储。

## 工程目录

```text
day1/
|-- pyproject.toml
|-- README.md
|-- main.py
|-- llm_client.py
|-- models.py
`-- tests/
    `-- test_llm_client.py
```

## 组件设计

### `models.py`

定义 Pydantic v2 模型 `StructuredAnswer`：包含必填且非空的 `answer` 字符串，以及取值范围为 `0..1` 的可选 `confidence`。从 assistant 消息中的 JSON 文本调用 `model_validate_json` 构造模型；当输出不是合法 JSON 或不符合模型约束时，抛出 Pydantic 校验异常。

### `llm_client.py`

提供异步 `LLMClient`，配置项包括 API 地址、API key、模型名和超时时间。客户端通过可注入的 `aiohttp` session 工厂发送请求，使测试可以使用 fake session 而不访问真实网络。客户端行为如下：

1. 记录请求开始和完成日志。
2. 将 `asyncio.TimeoutError` 转换为 `LLMTimeoutError`。
3. 将 `aiohttp.ClientError` 转换为 `LLMRequestError`。
4. 将非 2xx 响应转换为包含状态码信息的 `LLMRequestError`。
5. 提取 `choices[0].message.content`，并将其校验为 `StructuredAnswer`。

只有客户端内部创建的 session 由客户端负责关闭；注入的 session 仍由调用方负责。支持 `async with LLMClient(...)`，以便确定性地释放资源。

### `main.py`

从环境变量读取 `LLM_API_URL`、`LLM_API_KEY` 和 `LLM_MODEL`，配置基础日志，发送一次示例 prompt，并打印校验后的 `StructuredAnswer`。缺少必需配置时，给出清晰的错误信息。

## 错误处理

- 配置错误在发起请求前抛出。
- 超时和网络传输错误使用客户端自定义异常表示，并通过异常链保留原始异常。
- HTTP 错误信息包含状态码和长度受限的响应内容片段。
- Pydantic 校验异常直接交给调用方，使学习时能清楚看到 LLM 输出与结构定义的差异。

## 测试策略

使用 `unittest.IsolatedAsyncioTestCase` 和简单的 fake session/response 对象，覆盖以下行为：

- 合法的 assistant JSON 能转换为 `StructuredAnswer`。
- 无效的结构化内容会抛出 Pydantic 校验异常。
- 超时会转换为 `LLMTimeoutError`。
- 非成功 HTTP 响应会转换为 `LLMRequestError`。

测试不访问真实 LLM 服务，除项目运行时依赖外不需要其他依赖。

## 配置与使用方式

`README.md` 说明 `poetry install`、环境变量配置、`poetry run python main.py`，以及 `poetry run python -m unittest discover -s tests -v` 的使用方式。
