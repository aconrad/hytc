import time
from bson import ObjectId
from hytc.models import Dashboard, Component, Widget, Collector, CollectorItem


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
        dashboard.owner = 'aconrad'
        self.hygieia_repo.save_dashboard(dashboard)

        return dashboard

    def get_or_create_dashboard(self, dash_template, dash_title, app_name):
        dashboard = self.get_dashboard(dash_title)
        if dashboard is None:
            dashboard = self.create_dashboard(
                dash_template, dash_title, app_name
            )

        return dashboard

    def add_and_save_widget(self, dashboard):
        widget = Widget()
        # Mongo doesn't generate ids for sub-documents
        widget.id = ObjectId()
        widget.name = 'build'
        widget.component = dashboard.application
        widget.options = {
            'buildDurationThreshold': 3,
            'id': 'build0',
            'consecutiveFailureThreshold': 5,
        }
        dashboard.widgets.append(widget)
        self.hygieia_repo.save_dashboard(dashboard)

    def update_builds(self, collector_item, build_type_id):
        builds = list(self.tc_repo.get_builds(build_type_id))

        for build in builds:
            build.collector_item_id = collector_item.id
            self.hygieia_repo.save_build(build)

        return build

    def create_build_from_tc_data(self, collector_item, build_data):
        build = Build()
        build.number = build_data['number']
        build.status = build_data['status']
        build.url = build_data['buildUrl']
        build.collector_item_id = collector_item.id
        return build

    def pluck_new_builds(self, builds):
        for build in builds:
            self.hygieia_repo.get_build_by_number

    def create_collector_item(self, collector, description):
        collector_item = CollectorItem()
        collector_item.collector_id = collector.id
        collector_item.description = description
        collector_item.enabled = True
        collector_item.options = {
            'jobName': description,
            'jobUrl': 'https://tcserver.corp.surveymonkey.com/viewType.html?buildTypeId={}'.format(description),
            'instanceUrl': 'https://tcserver.corp.surveymonkey.com',
        }
        self.hygieia_repo.save_collector_item(collector_item)
        return collector_item

    def get_or_create_teamcity_collector_item(self, collector, build_type_id):
        collector_item = \
            self.hygieia_repo.get_collector_item_by_name(build_type_id)

        if collector_item is None:
            collector_item = self.create_collector_item(
                collector, build_type_id
            )

        return collector_item

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
