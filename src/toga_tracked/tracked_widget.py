class TrackedWidget:
    def __init__(self, tracked_factory, widget_name, *args, **kwargs):
        self.__actual_set("tracked_factory", tracked_factory)
        self.__actual_set(
            "actual_widget",
            getattr(tracked_factory.actual_factory, widget_name)(*args, **kwargs),
        )

    def __getattr__(self, item):
        return getattr(self.actual_widget, item)

    def __setattr__(self, key, value):
        setattr(self.actual_widget, key, value)

    def set_on_press(self, handler):
        def new_handler(*args, **kwargs):
            self.tracked_factory.track_event(self.id, "press")
            if handler is not None:
                handler(*args, **kwargs)

        self.interface._on_press = new_handler
        self.actual_widget.set_on_press(new_handler)

    def set_on_exit(self, handler):
        def new_handler(*args, **kwargs):
            self.tracked_factory.save()
            if handler is not None:
                handler(*args, **kwargs)

        self.interface._on_exit = new_handler
        self.actual_widget.set_on_exit(new_handler)

    @property
    def interface(self):
        return self.actual_widget.interface

    @property
    def id(self):
        return self.interface.id

    def __actual_set(self, key, value):
        self.__dict__[key] = value
