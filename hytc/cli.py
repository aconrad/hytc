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

    f = Facade(tc_repo, hygieia_repo)

    dashboard_title = dashboard
    dashboard = f.get_or_create_dashboard(
        'capone',
        dashboard_title,
        app_name,
    )

    build_type_id = builds
    collector = f.get_or_create_teamcity_collector()
    collector_item = f.get_or_create_teamcity_collector_item(
        collector, build_type_id
    )

    if build_type_id is not None:
        if not dashboard.has_build_widget():
            f.add_and_save_build_widget(dashboard)

        f.update_builds(collector_item, build_type_id)
