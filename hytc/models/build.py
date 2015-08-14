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
            'id={id}'
            'number={number}, '
            'status={status}'
        ')').format(
            id=self.id,
            number=self.number,
            status=self.status,
        )
