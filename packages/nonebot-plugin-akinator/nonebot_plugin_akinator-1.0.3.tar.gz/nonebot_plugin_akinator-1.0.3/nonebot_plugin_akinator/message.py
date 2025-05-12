from typing import TYPE_CHECKING, Optional

from httpx import AsyncClient
from nonebot import logger
from nonebot_plugin_alconna.uniseg import UniMessage

from .config import config
from .const import HTML_RENDER_AVAILABLE

if TYPE_CHECKING:
    from cooaki import BaseAkinator, WinResp


async def get_answer_photo(_: "BaseAkinator", data: "WinResp") -> Optional[bytes]:
    if not data.photo:
        return None
    async with AsyncClient() as cli:
        resp = await cli.get(data.photo)
        resp.raise_for_status()
        return resp.content


async def build_answer_msg(aki: "BaseAkinator", data: "WinResp") -> UniMessage:
    msg = UniMessage()
    msg += f"我猜：\n{data.name_proposition}"
    if data.description_proposition:
        msg += f"\n{data.description_proposition}"

    photo = await get_answer_photo(aki, data)
    if photo:
        msg += "\n"
        msg += UniMessage.image(raw=photo)
        if data.pseudo:
            msg += f"From: {data.pseudo}"

    msg += "\n猜错了？继续游戏 (C)"
    return msg


async def build_question_msg(aki: "BaseAkinator") -> UniMessage:
    state = aki.state
    return UniMessage.text(
        f"问题 {state.step + 1}：\n"
        f"{state.question}\n"
        f"\n"
        f"1. 是 (Y) | 2. 否 (N) | 3. 不知道 (IDK)\n"
        f"4. 或许是 (P) | 5. 或许不是 (PN)\n"
        f"{'' if state.step == 0 else '上一问 (B) | '}退出 (E)",
    )


if not config.akinator_text_mode:
    if not HTML_RENDER_AVAILABLE:
        logger.warning(
            "Required dependencies for rendering images are not installed, "
            "please install them by `pip install nonebot-plugin-akinator[image]`. "
            "Fallback to text mode.",
        )

    else:
        from .render import render_answer_image, render_question_image

        async def build_answer_msg(aki: "BaseAkinator", data: "WinResp") -> UniMessage:
            img = await render_answer_image(
                aki,
                data.name_proposition,
                data.description_proposition,
                await get_answer_photo(aki, data),
                data.pseudo,
            )
            return UniMessage.image(raw=img)

        async def build_question_msg(aki: "BaseAkinator") -> UniMessage:
            state = aki.state
            img = await render_question_image(
                aki,
                state.akitude,
                state.step + 1,
                state.question,
            )
            return UniMessage.image(raw=img)
