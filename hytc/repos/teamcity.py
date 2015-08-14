from pyteamcity import TeamCity
from hytc.models import Build


def build_to_model(build_data):
    build = Build()
#    build.id = build_data['id']
    build.number = build_data['number']
    build.status = build_data['status'].lower()
    build.url = build_data['webUrl']
    build.started_by = build_data['triggered']['user']['name']
    build.start_time = build_data['startDate']
    build.end_time = build_data['finishDate']

    return build


class TeamCityRepo:
    def __init__(self, server, port, account, password):
        self._tc = TeamCity(account, password, server, port)

    def get_projects(self):
        all_projects = self._tc.get_all_projects()
        return all_projects

    def get_builds(self, builds_for):
        builds = self._tc.get_all_builds_by_build_type_id(
            builds_for,
            start=0,
            count=1,
        )
        for build in builds['build']:
            full_build = self._tc.get_build_by_build_id(build['id'])
            build = build_to_model(full_build)
            yield build
