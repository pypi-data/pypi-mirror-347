from rich.text import Text
from rich.table import Table
from readchar import key
from typing import Union, List, Set

from ..base import BasePrompt, Emoji, Choice


class SelectPrompt(BasePrompt):
    def __init__(
        self,
        message: str,
        choices: Union[List[str], List[Choice], List[tuple]],
        **kwargs,
    ):
        self.emoji = Emoji("question_mark")
        super().__init__(message, **kwargs)
        self.choices: List[Choice] = self._normalize_choices(choices)
        self.selected_index = 0

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.expand = True
        table.title_justify = "left"

        table.title = self.message
        table.show_edge = False
        table.pad_edge = False

        for i, choice in enumerate(self.choices):
            prefix = Emoji("arrow_forward") if i == self.selected_index else "  "
            line = Text(f"{prefix} {choice.name}")
            if i == self.selected_index:
                line.stylize("bold green")
            table.add_row(line)

        return table

    def handle_key(self, k: str) -> None:
        if k == key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.choices)
        elif k == key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.choices)
        elif k == key.ENTER:
            self.result = self.choices[self.selected_index].value
            self.done = True
        elif k == key.ESC:
            self.result = None
            self.done = True


class MultiSelectPrompt(BasePrompt):
    def __init__(self, message: str, choices: Union[List[str], List[Choice]], **kwargs):
        super().__init__(message, **kwargs)
        self.choices: List[Choice] = self._normalize_choices(choices)
        self.cursor_index = 0
        self.selected: Set[int] = {i for i, c in enumerate(self.choices) if c.enabled}

    def _normalize_choices(
        self, choices: Union[List[str], List[Choice]]
    ) -> List[Choice]:
        return [c if isinstance(c, Choice) else Choice(c) for c in choices]

    def render(self) -> Table:
        table = Table.grid(padding=(0, 1))
        table.title = self.message

        for i, choice in enumerate(self.choices):
            prefix = Emoji("arrow_forward") if i == self.cursor_index else "  "
            status = Emoji("heavy_check_mark") if i in self.selected else "  "
            line = Text(f"{prefix} {status} {choice.name}")

            if choice.disabled:
                line.stylize("dim")
            elif i == self.cursor_index:
                line.stylize("reverse")

            table.add_row(line)

        return table

    def handle_key(self, k: str) -> None:
        if k == key.UP:
            self._move_cursor(-1)
        elif k == key.DOWN:
            self._move_cursor(1)
        elif k == key.SPACE:
            self._toggle_selection()
        elif k == key.ENTER:
            self.result = [self.choices[i].value for i in sorted(self.selected)]
            self.done = True
        elif k == key.ESC:
            self.result = None
            self.done = True

    def _move_cursor(self, direction: int):
        prev_index = self.cursor_index
        while True:
            self.cursor_index = (self.cursor_index + direction) % len(self.choices)
            if (
                not self.choices[self.cursor_index].disabled
                or self.cursor_index == prev_index
            ):
                break

    def _toggle_selection(self):
        current_choice = self.choices[self.cursor_index]
        if current_choice.disabled:
            return
        if self.cursor_index in self.selected:
            self.selected.remove(self.cursor_index)
        else:
            self.selected.add(self.cursor_index)
