import random

import toga
from toga.constants import COLUMN
from toga.style import Pack

from toga_tracked import FileTrackedFactory

tracked_factory = FileTrackedFactory()


class ExampleButtonApp(toga.App):
    def startup(self):
        # Window class
        #   Main window of the application with title and size
        #   Also make the window non-resizable and non-minimizable.
        self.main_window = toga.MainWindow(
            title=self.name, size=(800, 500), resizeable=False, minimizable=False
        )

        self.label = toga.Label("Click the button")
        outer_box = toga.Box(
            children=[
                toga.Button(
                    "Click me!",
                    id="button1",
                    on_press=self.change_label,
                    factory=tracked_factory,
                ),
                toga.Button(
                    "I don't do nothing...", id="button2", factory=tracked_factory
                ),
                self.label,
            ],
            style=Pack(direction=COLUMN, height=10),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

    def change_label(self, widget):
        self.label.text = f"Random number: {random.randint(1, 100)}"


def on_exit(app):
    app.main_window.info_dialog(
        "Before Exit", f'usage report is save in "{tracked_factory.output_path}"'
    )


def main():
    # Application class
    #   App name and namespace
    app = ExampleButtonApp(
        "Button",
        "org.beeware.widgets.buttons",
        factory=tracked_factory,
        on_exit=on_exit,
    )
    return app
