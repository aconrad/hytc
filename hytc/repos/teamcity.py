from pyteamcity import TeamCity
from hytc.models import Build


def build_to_model(build_data):
    build = Build()
    build.id = build_data['id']
    build.number = build_data['number']
    build.status = build_data['status'].lower()
    build.url = build_data['webUrl']

    return build


class TeamCityRepo:
    def __init__(self, server, port, account, password):
        self._tc = TeamCity(account, password, server, port)

    def get_projects(self):
        import pudb; pudb.set_trace()
        all_projects = self._tc.get_all_projects()
        return all_projects

    def get_builds(self):
        #builds = self._tc.get_all_builds(start=0, count=10)
        anweb = self._tc.get_project_by_project_id('Anweb')
        import pudb; pudb.set_trace()
        for build_data in builds['build']:
            build = build_to_model(build_data)
            import pudb; pudb.set_trace()
            build_by_id = self._tc.get_build_by_build_id(build.id)
            print(build_by_id)
            yield build
