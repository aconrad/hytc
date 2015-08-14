class Dashboard:
    application = None
    id = None
    owner = None
    template = None
    title = None

    def __init__(self):
        self.widgets = []

    def has_build_widget(self):
        for widget in self.widgets:
            if widget.name == 'build':
                return True
        return False


class Component:
    id = None
    name = None
    owner = None

    def __repr__(self):
        return 'Component(name={})'.format(self.name)


class Collector:
    id = None
    name = None
    type = None
    enabled = True
    online = True
    last_executed = None

    def __init__(self):
        self.build_servers = []


class Widget:
    id = None
    name = None
    component = None

    def __init__(self):
        self.options = []

    def __repr__(self):
        return 'Widget(name={})'.format(self.name)


class Build:

    id = None
    artifact_version = None
    duration = None
    end_time = None
    number = None
    start_time = None
    started_by = None
    status = None  # success, failure, unstable, aborted, unknown
    url = None

    def __init__(self):
        self.source_changeset = []

    def __repr__(self):
        return (
            'Build('
            'id={id}, '
            'number={number}, '
            'status={status}'
        ')').format(
            id=self.id,
            number=self.number,
            status=self.status,
        )
