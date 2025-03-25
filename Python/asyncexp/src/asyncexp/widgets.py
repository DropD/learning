import asyncio
import time
import enum
import random

import textual as tx
import textual.widget
import textual.containers


class Status(enum.StrEnum):
    UNINITIALIZED = ""
    LOADING = enum.auto()
    STOPPED = enum.auto()
    FINISHED = enum.auto()


class RandomCountdown(tx.containers.HorizontalGroup):
    """A widget representing the status of an asyncio task."""

    status: Status = tx.reactive.reactive(Status.UNINITIALIZED, repaint=False)

    # swap out the def lines to see responsivity change
    # def on_button_pressed(self, event: tx.widgets.Button.Pressed) -> None:
    async def on_button_pressed(self, event: tx.widgets.Button.Pressed) -> None:
        button_id = event.button.id
        label = self.query_one("#status")
        if button_id == "start":
            self.status = Status.LOADING
            label.loading = True
            self.add_class("running")
            self.run()
        if button_id == "stop":
            self.status = Status.STOPPED
            label.loading = False
            self.remove_class("running")
        label.update(str(self.status))

    @tx.work
    async def run(self) -> None:
        label = self.query_one("#status")
        # swap out the two lines below to see an effect on responsivity
        await asyncio.sleep(random.uniform(1, 5))
        # time.sleep(random.uniform(1, 5))
        label.loading = False
        self.status = Status.FINISHED
        label.update(str(self.status))
        self.remove_class("running")

    def compose(self) -> tx.app.ComposeResult:
        """This is where the child widgets go."""
        yield tx.widgets.Button("start", id="start", variant="success")
        yield tx.widgets.Button("stop", id="stop", variant="error")
        yield tx.widgets.Label(str(self.status), id="status")
