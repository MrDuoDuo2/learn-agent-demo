# Day1 异步 LLM 客户端实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `day1/` 下创建一个最小 Poetry Python 工程，实现异步 LLM 调用、日志、超时/HTTP 错误处理和 Pydantic v2 结构化解析。

**Architecture:** 使用四个职责清晰的文件：`models.py` 定义输出模型，`llm_client.py` 负责 HTTP 调用和异常映射，`main.py` 提供环境变量驱动的示例入口，`tests/` 使用标准库 fake transport 测试行为。客户端允许注入 session 工厂，生产环境使用 `aiohttp.ClientSession`，测试不访问网络。

**Tech Stack:** Python 3.9+、Poetry、aiohttp、Pydantic v2、标准库 `unittest`。

**Spec:** `docs/superpowers/specs/2026-09-08-day1-async-llm-client-design.md`

## Global Constraints

- 运行时依赖仅为 `aiohttp` 和 `pydantic>=2,<3`。
- 对接 OpenAI-compatible `POST /chat/completions`。
- 结构化输出使用 `StructuredAnswer`，通过 `model_validate_json` 校验。
- 超时转换为 `LLMTimeoutError`，网络或 HTTP 错误转换为 `LLMRequestError`。
- 测试使用标准库 `unittest`，不引入 pytest。

---

### Task 1: Poetry 工程和 Pydantic 模型

**Files:**
- Create: `day1/pyproject.toml`
- Create: `day1/models.py`
- Create: `day1/tests/__init__.py`
- Create: `day1/tests/test_models.py`

**Interfaces:**
- Produces `StructuredAnswer(answer: str, confidence: float | None)`。

- [ ] **Step 1: 写失败测试**

```python
from pydantic import ValidationError
from models import StructuredAnswer

def test_parses_valid_json():
    result = StructuredAnswer.model_validate_json('{"answer":"hello","confidence":0.8}')
    assert result.answer == "hello"
    assert result.confidence == 0.8

def test_rejects_confidence_out_of_range():
    try:
        StructuredAnswer.model_validate_json('{"answer":"hello","confidence":1.1}')
    except ValidationError:
        return
    raise AssertionError("expected ValidationError")
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest discover -s day1/tests -v`
Expected: FAIL because `models.py` does not exist.

- [ ] **Step 3: 编写最小实现**

使用 `BaseModel`、`Field(min_length=1, le=1, ge=0)` 定义模型，并在 `pyproject.toml` 声明 Poetry 元数据和两个运行时依赖。

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m unittest discover -s day1/tests -v`
Expected: PASS。

### Task 2: 异步客户端和错误映射

**Files:**
- Create: `day1/llm_client.py`
- Create: `day1/tests/test_llm_client.py`

**Interfaces:**
- `class LLMClient`
- `async request(prompt: str) -> StructuredAnswer`
- `LLMTimeoutError` and `LLMRequestError`

- [ ] **Step 1: 写失败测试**

测试 fake response 返回 `choices[0].message.content`，并分别验证成功解析、Pydantic 失败、超时映射和 HTTP 失败。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest discover -s day1/tests -v`
Expected: FAIL because `llm_client.py` does not exist。

- [ ] **Step 3: 编写最小实现**

创建 `aiohttp.ClientSession`（或使用注入的工厂），设置 `ClientTimeout(total=timeout_seconds)`，发送 JSON 请求；捕获 `asyncio.TimeoutError`、`aiohttp.ClientError`，并检查 `response.status` 后调用 `StructuredAnswer.model_validate_json`。

- [ ] **Step 4: 运行测试确认通过**

Run: `python -m unittest discover -s day1/tests -v`
Expected: PASS。

### Task 3: 示例入口和中文 README

**Files:**
- Create: `day1/main.py`
- Create: `day1/README.md`

**Interfaces:**
- `main.py` 提供可执行的 `asyncio.run(main())` 入口。

- [ ] **Step 1: 编写入口**

读取 `LLM_API_URL`、`LLM_API_KEY`、`LLM_MODEL`，缺失时抛出 `ValueError`；配置日志后调用客户端并打印 `result.model_dump_json()`。

- [ ] **Step 2: 编写 README**

说明目录、`poetry install`、环境变量、`poetry run python main.py` 和标准库测试命令，并给出结构化 JSON 示例。

- [ ] **Step 3: 运行完整验证**

Run: `python -m unittest discover -s day1/tests -v` 和 `python -m compileall day1`。
Expected: 所有测试通过且编译命令退出码为 0。

## Self-review

- spec 中的依赖限制、接口协议、异常类型、结构化解析、日志和测试范围均在上述任务覆盖。
- 计划没有 TODO/TBD 或未定义的接口名称。
- `StructuredAnswer` 和 `LLMClient.request` 的类型在任务之间保持一致。
