import json
import uuid
from pathlib import Path

from toga.platform import get_platform_factory

from toga_tracked.tracked_widget import TrackedWidget


class TrackedFactory:
    def __init__(self, actual_factory=None, on_save=None):
        self.actual_factory = get_platform_factory(actual_factory)
        self.on_save = on_save
        self.report = {}

    def __getattr__(self, item):
        def widget_builder(*args, **kwargs):
            return TrackedWidget(
                tracked_factory=self, widget_name=item, *args, **kwargs
            )

        return widget_builder

    @property
    def paths(self):
        return self.actual_factory.paths

    @property
    def Icon(self):
        return self.actual_factory.Icon

    @property
    def Font(self):
        return self.actual_factory.Font

    @property
    def on_save(self):
        return self._on_save

    @on_save.setter
    def on_save(self, on_save):
        self._on_save = on_save

    def track_event(self, widget_id, event):
        if widget_id not in self.report:
            self.report[widget_id] = {}
        count = self.report[widget_id].get(event, 0) + 1
        self.report[widget_id][event] = count

    def save(self):
        if self.on_save is not None:
            self.on_save()


class FileTrackedFactory(TrackedFactory):
    def __init__(
        self, actual_factory=None, output_directory=Path.home(), file_name=None
    ):
        super().__init__(actual_factory=actual_factory, on_save=self.on_save)
        if file_name is None:
            file_name = f"{uuid.uuid4()}.json"
        self.output_path = output_directory / file_name

    def on_save(self):
        with open(self.output_path, mode="w") as json_file:
            json.dump(self.report, json_file, indent=2)
