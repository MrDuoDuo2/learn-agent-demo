# Day1: 异步调用 LLM

这是一个使用 Poetry 管理的最小 Python 工程，用于学习：

- 使用 `aiohttp` 发起异步 HTTP 请求。
- 使用 `asyncio`/`aiohttp` 超时机制处理请求超时。
- 使用标准库 `logging` 记录请求开始、完成和失败。
- 使用 Pydantic v2 将 LLM 返回的 JSON 校验为 Python 对象。

接口采用 OpenAI-compatible 的 `POST /chat/completions` 格式。

## 目录

```text
day1/
|-- pyproject.toml
|-- poetry.lock
|-- poetry.toml
|-- config.example.json  # 配置模板
|-- config.json          # 本地配置，不提交到 Git
|-- main.py
|-- llm_client.py
|-- models.py
|-- README.md
`-- tests/
    |-- test_llm_client.py
    |-- test_main.py
    `-- test_models.py
```

## 安装

在 `day1` 目录运行：

```powershell
poetry install
```

## 配置

复制 `config.example.json` 为 `config.json`，再填写完整的 chat-completions 地址、API key 和模型名：

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key",
  "model": "gpt-4.1-mini"
}
```

`config.json` 已加入 `.gitignore`，其中的 API key 不会被 Git 跟踪。`api_url` 也可以替换为其他兼容 OpenAI chat-completions 协议的服务地址。

## 运行

```powershell
poetry run python main.py
```

模型必须返回 JSON 文本，例如：

```json
{
  "answer": "Asynchronous programming lets a program wait for I/O without blocking other work.",
  "confidence": 0.95
}
```

程序会使用 `StructuredAnswer.model_validate_json()` 校验该文本：`answer` 必须是非空字符串，`confidence` 可省略，存在时必须在 `0` 到 `1` 之间。

## 测试

测试使用 fake session，不会请求真实 LLM：

```powershell
poetry run python -m unittest discover -s tests -v
```
