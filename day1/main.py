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
你的无含党母娘, 你们就麻烦你起来应该不算模样, 打害都没讲, 我们这个小弟真的样子名字我的眼子都变, 想及时收到一堂天气提醒, 对我说订阅天气, 你看你看看你看看你每次你都都往不好, 你看你帮我想说你好吃到尾上弄茶, 就想这场都想发这个昨天到前面那个有一个东西也给了上降很多挖吃了, 我不想吃啊, 但是不想失败啊, 我前面我我我懒得拿嘛, 只有抵触了呀, 光有一方坏呀, 我说人道下, 就可以说你就是吧, 不是不错了, 是他不耐那个, 是他能够讲话, 上角了丢了, 就是那个两化了吗? 我就不想穿的, 我也看到了, 说了什么样, 是不是网络装? 我去那个去看无限问的相关的眼光, 但是你就说我说指到区前, 我没有说没有说德国讯息红, 就是我录了这个机构的我位置多简单, 我第二个位置啊, 你把这个钱你要不差你把跌多少了, 放到上去了, 那么还有一些东西到底再发水波水了, 二毛包, 不能磨进, 强的什么手机呢? 你要画弄到它的叫地上我就打, 可是出下来旁边出来我的宝贝, 吃的吃点吃点吃点, 我说我吃的, 但包含啊, 那晚上想吃什么? 想吃把我给你啦。 就是把哦, 点清淡的吧, 做成饭, 这家清淡来过吧, 那你到时候又变去钱投放了。 那你去问钱, 修正明显我们对面, 原住到什样? 啊, 哎呀, 在杯子好丑啊, 去买的那个送的书面看你, 只是参考看你看上面写字, 哦, 我说了要你把这个过装好, 你怎么拿看药费, 你就你不要碰到器的方, 你看了, 你打开不穿往我的天呐, 我已经请下了。 哎, 明天, 哎, 明天连过来上门, 你要看着点啊, 要上模羊空啊, 下午什么? 嗯, 上午打算, 你今天没大错啊, 没有, 我想说话回来就三点过了, 然后我做了一下我就出门了。 实际上都起的船啊, 几点都起床我没睡觉了, 你走了我就在这种电脑变成做的。 那你上我没搞, 上午再搞这边学习给我推这么多选 168 万是觉得宝宝买的喜吧。 我给你听买了起到什么东西啊, 我的天呐。 哼哼, 而且我也不敢兴趣啊。 现在这个阿里拉斯的背克图离以前要舒服一些嗯, 他们说的黑色的就是要舒服一点, 那把黑色的就没有那么的舒服, 但也还可以啊。 就白色会硬一点, 这个黑色软一点, 舒适度就是大脑更加的怎么样? 别了, 哎, 等等, 我看看不完了, 就下来了, 自己指标标的标标的这个自己哦保持包包就是一个猪, 把我们就是衣度独独毒, 大宝举开军嗯哦