import os
import click
from hytc.facades import Facade


hytc = click.Group()


@hytc.command()
@click.argument('app_name')
@click.argument('dashboard')
@click.option('-b', '--builds')
def sync(app_name, dashboard, builds):
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
        'dashboard',
    )

    f = Facade(hygieia_repo)

    dashboard_title = dashboard
    dashboard = f.get_or_create_dashboard(
        'capone',
        dashboard_title,
        app_name,
    )

    for build in tc_repo.get_builds(builds):
        # FIXME: insert build in mongo
        pass
