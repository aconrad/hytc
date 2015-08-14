from bson import DBRef, ObjectId
from pymongo import MongoClient
from hytc.models import Component, Collector, Dashboard, Widget


def collector_to_doc(collector):
    doc = {
        'buildServers': collector.build_servers,
        'collectorType': collector.type,
        'enabled': collector.enabled,
        'lastExecuted': collector.last_executed,
        'name': collector.name,
        'online': collector.online,
    }

    if collector.id is not None:
        doc['_id'] = collector.id

    return doc


def collector_to_model(doc):
    collector = Collector()
    collector.id = doc['_id']
    collector.name = doc['name']
    collector.type = doc['collectorType']
    collector.enabled = doc['enabled']
    collector.online = doc['online']
    collector.last_executed = doc['lastExecuted']
    collector.build_servers = doc['buildServers']

    return collector


def widget_to_model(doc):
    widget = Widget()
    widget.id = doc['_id']
    widget.name = doc['name']
    widget.options = doc['options']

    component = Component()
    component.id = doc['componentId']
    widget.component = component

    return widget


def widget_to_doc(widget):
    doc = {
        '_id': widget.id,
        'name': widget.name,
        'componentId': widget.component.id,
        'options': widget.options,
    }

    return doc


def dashboard_to_model(doc):
    dashboard = Dashboard()
    dashboard.id = doc['_id']
    dashboard.template = doc['template']
    dashboard.title = doc['title']
    dashboard.owner = doc['owner']

    application = Component()
    application.name = doc['application']['name']
    application.id = doc['application']['components'][0].id

    dashboard.application = application

    for widget_doc in doc['widgets']:
        widget = widget_to_model(widget_doc)
        dashboard.widgets.append(widget)

    return dashboard


def dashboard_to_doc(dashboard):
    application = dashboard.application
    app_doc = {
        'name': application.name,
        'components': [
            DBRef('components', application.id)
        ],
    }

    widget_docs = []
    for widget in dashboard.widgets:
        widget_doc = widget_to_doc(widget)
        widget_docs.append(widget_doc)

    doc = {
        'application': app_doc,
        'owner': dashboard.owner,
        'template': dashboard.template,
        'title': dashboard.title,
        'widgets': widget_docs,
    }

    if dashboard.id is not None:
        doc['_id'] = dashboard.id

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

        if doc is None:
            return

        component = component_to_model(doc)
        return component

    def create_component(self, component):
        doc = component_to_doc(component)
        components = self._db.get_collection('components')
        result = components.insert(doc)
        component.id = result

    def save_dashboard(self, dashboard):
        dashboards = self._db.get_collection('dashboards')
        doc = dashboard_to_doc(dashboard)
        if dashboard.id is None:
            result = dashboards.insert(doc)
            dashboard.id = result
        else:
            result = dashboards.update({'_id': dashboard.id}, doc)

    def get_dashboard_by_title(self, dashboard_title):
        dashboards = self._db.get_collection('dashboards')
        doc = dashboards.find_one({
            'title': dashboard_title
        })

        if doc is None:
            return

        dashboard = dashboard_to_model(doc)
        return dashboard

    def get_build_by_number(self, dashboard):
        pass

    def save_build(self, dashboard, build):
        builds = self._db.get_collection('builds')

    def get_collector_by_name(self, collector_name):
        collectors = self._db.get_collection('collectors')
        doc = collectors.find_one({'name': collector_name})

        if doc is None:
            return

        collector = collector_to_model(doc)
        return collector

    def save_collector(self, collector):
        doc = collector_to_doc(collector)
        collectors = self._db.get_collection('collectors')
        if collector.id is None:
            result = collectors.insert(doc)
            collector.id = result
        else:
            collectors.update({'_id': collector.id}, doc)

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
