import time
from bson import ObjectId
from hytc.models import Dashboard, Component, Widget, Collector


def epoch_now():
    return int(time.time() * 1000)


class Facade:

    def __init__(self, tc_repo, hygieia_repo):
        self.hygieia_repo = hygieia_repo
        self.tc_repo = tc_repo

    def get_dashboard(self, title):
        return self.hygieia_repo.get_dashboard_by_title(title)

    def create_application(self, app_name):
        component = Component()
        component.name = app_name
        self.hygieia_repo.create_component(component)
        return component

    def get_application(self, app_name):
        return self.hygieia_repo.get_component(app_name)

    def get_or_create_application(self, app_name):
        application = self.hygieia_repo.get_component_by_name(app_name)

        if application is None:
            application = self.create_application(app_name)

        return application

    def create_dashboard(self, dash_template, dash_title, app_name):
        # Create app
        application = self.get_or_create_application(app_name)

        # Create dashboard
        dashboard = Dashboard()
        dashboard.template = dash_template
        dashboard.title = dash_title
        dashboard.application = application
        self.hygieia_repo.save_dashboard(dashboard)

        return dashboard

    def get_or_create_dashboard(self, dash_template, dash_title, app_name):
        dashboard = self.get_dashboard(dash_title)
        if dashboard is None:
            dashboard = self.create_dashboard(
                dash_template, dash_title, app_name
            )

        return dashboard

    def add_and_save_build_widget(self, dashboard):
        widget = Widget()
        # Mongo doesn't generate ids for sub-documents
        widget.id = ObjectId()
        widget.name = 'build'
        widget.component = dashboard.application
        widget.options.append({
            'build_duration_threshold': 3,
            'id': 'build0',
            'consecutive_failure_threshold': 5,
        })
        dashboard.widgets.append(widget)
        self.hygieia_repo.save_dashboard(dashboard)

    def update_builds(self, dashboard, build_type_id):
        builds = list(self.tc_repo.get_builds(build_type_id))
        builds = self.pluck_new_builds(builds)

    def pluck_new_builds(self, builds):
        for build in builds:
            self.hygieia_repo.

    def get_or_create_teamcity_collector_item(self):
        collector_item = self.hygieia_repo.get_collector_by_name()

    def get_or_create_teamcity_collector(self):
        collector_name = 'TeamCity'
        collector_type = 'Build'

        collector = self.hygieia_repo.get_collector_by_name(collector_name)

        if collector is None:
            collector = self.create_collector(
                collector_name,
                collector_type,
                ['http://tcserver.corp.surveymonkey.com/'],
            )

        return collector

    def create_collector(self, name, type, build_servers):
        collector = Collector()
        collector.name = name
        collector.type = type
        collector.enabled = True
        collector.online = True
        collector.last_executed = epoch_now()
        collector.build_servers = build_servers

        self.hygieia_repo.save_collector(collector)

        return collector
