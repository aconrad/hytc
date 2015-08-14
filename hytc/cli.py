import os
import click


hytc = click.Group()


@hytc.command()
@click.argument('project_name')
@click.argument('build_name')
def sync(project_name, build_name):
    from hytc.repos import TeamCityRepo
    from hytc.repos import HygieiaRepo

    tc_repo = TeamCityRepo(
        os.getenv('TEAMCITY_HOST', 'tcserver.corp.surveymonkey.com'),
        os.getenv('TEAMCITY_PORT', 80),
        os.environ['TEAMCITY_USER'],
        os.environ['TEAMCITY_PASSWORD'],
    )

    hygieia_repo = HygieiaRepo(
        'hygieia.corp.surveymonkey.com',
        27017,
        'test',
    )

    tc_repo.get_projects()

    for build in tc_repo.get_builds():
        print(build)
