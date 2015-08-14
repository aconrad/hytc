from hytc.models import Dashboard, Component


class Facade:

    def __init__(self, hygieia_repo):
        self.hygieia_repo = hygieia_repo

    @property
    def repo(self):
        return self.hygieia_repo

    def get_dashboard(self, title):
        return self.repo.get_dashboard_by_title(title)

    def create_application(self, app_name):
        component = Component()
        component.name = app_name
        self.repo.create_component(component)
        return component

    def get_application(self, app_name):
        return self.repo.get_component(app_name)

    def get_or_create_application(self, app_name):
        application = self.repo.get_component_by_name(app_name)

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
        self.repo.create_dashboard(dashboard)

        return dashboard

    def get_or_create_dashboard(self, dash_template, dash_title, app_name):
        dashboard = self.get_dashboard(dash_title)
        if dashboard is None:
            dashboard = self.create_dashboard(
                dash_template, dash_title, app_name
            )

        return dashboard
