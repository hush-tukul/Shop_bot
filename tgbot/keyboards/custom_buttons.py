from typing import Awaitable, Callable, Dict, List, Optional, Union

from aiogram.types import CallbackQuery, InlineKeyboardButton, WebAppInfo

from aiogram_dialog.api.protocols import DialogManager, DialogProtocol
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.widget_event import (
    ensure_event_processor,
    WidgetEventProcessor,
)


OnClick = Callable[[CallbackQuery, "Button", DialogManager], Awaitable]



class SwitchInlineQuery_2(Keyboard):
    def __init__(
        self,
        text: Text,
        switch_inline_query: Text,
        id: Optional[str] = None,
        when: Union[str, Callable, None] = None,
    ):
        super().__init__(id=id, when=when)
        self.text = text
        self.switch_inline = switch_inline_query

    async def _render_keyboard(
        self,
        data: Dict,
        manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    switch_inline_query_current_chat=await self.switch_inline.render_text(
                        data, manager,
                    ),
                ),
            ],
        ]