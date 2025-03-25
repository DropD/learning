import textual as tx
import textual.app
import textual.containers
import textual.widgets

from . import widgets

__all__ = ["widgets", "AsyncExampleApp", "main"]


class AsyncExampleApp(tx.app.App):
    """A textual app purely to demonstrate async."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "asyncexp.tcss"

    def compose(self) -> tx.app.ComposeResult:
        """This is where the widgets go."""

        yield tx.widgets.Header()
        yield tx.containers.VerticalScroll(
            widgets.RandomCountdown(),
            widgets.RandomCountdown(),
            widgets.RandomCountdown(),
        )
        yield tx.widgets.Footer()

    def action_toggle_dark(self) -> None:
        """Action to toggle dark mode."""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


def main() -> None:
    async_app = AsyncExampleApp()
    async_app.run()
