from bson import DBRef
from pymongo import MongoClient
from hytc.models import Component, Dashboard


def dashboard_to_model(doc):
    dashboard = Dashboard()
    dashboard.template = doc['template']
    dashboard.title = doc['title']
    dashboard.owner = doc['owner']

    application = Component()
    application.name = doc['application']['name']

    dashboard.application = application
    return dashboard


def dashboard_to_doc(dashboard):
    application = dashboard.application
    app_doc = {
        'name': application.name,
        'components': [
            DBRef('components', application.id)
        ],
    }

    widget_doc = []

    doc = {
        'application': app_doc,
        'owner': dashboard.owner,
        'template': dashboard.template,
        'title': dashboard.title,
        'widgets': widget_doc,
    }

    return doc


def component_to_doc(component):
    doc = {
        'name': component.name,
        'collectorItems': {},
    }

    if component.id is not None:
        doc['_id'] = component.id

    return doc


def component_to_model(doc):
    component = Component()
    component.id = doc['_id']
    component.name = doc['name']
    return component


class HygieiaRepo:
    def __init__(self, host, port, db):
        uri = 'mongodb://{host}:{port}'.format(
            host=host,
            port=port,
        )
        self._client = client = MongoClient(uri)
        self._db = client[db]

    def get_component_by_name(self, name):
        components = self._db.get_collection('components')
        doc = components.find_one({'name': name})
        component = component_to_model(doc)
        return component

    def create_component(self, component):
        doc = component_to_doc(component)
        components = self._db.get_collection('components')
        result = components.insert(doc)
        component.id = result

    def create_dashboard(self, dashboard):
        doc = dashboard_to_doc(dashboard)
        dashboards = self._db.get_collection('dashboards')
        doc = dashboard_to_doc(dashboard)
        result = dashboards.insert(doc)
        dashboard.id = result

    def get_dashboard_by_title(self, dashboard_title):
        dashboards = self._db.get_collection('dashboards')
        doc = dashboards.find_one({
            'title': dashboard_title
        })

        if doc is None:
            return

        dashboard = dashboard_to_model(doc)
        return dashboard

    def save_dashboard(self, dashboard):
        doc = dashboard_to_doc(dashboard)
        dashboards = self._db.get_collection('dashboards')
        doc = dashboards.find_one({
            'title': dashboard_title
        })

        if doc is None:
            return

        dashboard = dashboard_to_model(doc)
        return dashboard

    def save_build(self, dashboard, build):
        self._db.dashboards.insert()

{
    "_id": {
        "$oid": "55cd761de4b04bd7da48e732"
    },
    "_class": "com.capitalone.dashboard.model.Dashboard",
    "template": "capone",
    "title": "aconrad",
    "application": {
        "name": "aconrad",
        "components": [
            {
                "$ref": "components",
                "$id": {
                    "$oid": "55cd761de4b04bd7da48e731"
                }
            }
        ]
    },
    "widgets": [
        {
            "_id": {
                "$oid": "55cd7d25e4b04bd7da48e734"
            },
            "name": "repo",
            "componentId": {
                "$oid": "55cd761de4b04bd7da48e731"
            },
            "options": {
                "id": "repo0",
                "scm": {
                    "name": "GitHub",
                    "value": "GitHub"
                },
                "url": "http://code.corp.surveymonkey.com/devmonkeys/anweb",
                "branch": "develop"
            }
        },
        {
            "_id": {
                "$oid": "55cd81aee4b04bd7da48e737"
            },
            "name": "build",
            "componentId": {
                "$oid": "55cd761de4b04bd7da48e731"
            },
            "options": {
                "id": "build0",
                "buildDurationThreshold": 3,
                "consecutiveFailureThreshold": 5
            }
        }
    ],
    "owner": "aconrad"
}
