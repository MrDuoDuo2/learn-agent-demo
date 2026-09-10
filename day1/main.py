import asyncio
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from llm_client import LLMClient

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # 切换windows事件循环策略类，解决Event loop is closed报错


@dataclass(frozen=True)
class LLMConfig:
    api_url: str
    api_key: str
    model: str


def load_config(config_path: Path) -> LLMConfig:
    try:
        data: Any = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError("Configuration file not found: {0}".format(config_path)) from error
    except json.JSONDecodeError as error:
        raise ValueError("Configuration file must contain valid JSON") from error

    if not isinstance(data, dict):
        raise ValueError("Configuration file must contain a JSON object")

    required_names = ("api_url", "api_key", "model")
    missing_names = [
        name
        for name in required_names
        if not isinstance(data.get(name), str) or not data[name].strip()
    ]
    if missing_names:
        raise ValueError("Missing required configuration values: {0}".format(", ".join(missing_names)))

    return LLMConfig(
        api_url=data["api_url"],
        api_key=data["api_key"],
        model=data["model"],
    )


# 入口函数
async def main() -> None:
    # 日志系统初始化
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    # 获取配置文件load
    config = load_config(Path(__file__).with_name("config.json"))

    # LLM配置初始化->llm_client.py
    async with LLMClient(
        api_url=config.api_url,
        api_key=config.api_key,
        model=config.model,
    ) as client:
        result = await client.request("用一句话解释异步编程.")

    print(result.model_dump_json())


if __name__ == "__main__":
    asyncio.run(main())
