from bson import DBRef, ObjectId
from pymongo import MongoClient
from hytc.models import Component, Collector, CollectorItem, Dashboard, Widget


def build_to_doc(build):
    doc = {
        'collectorItemId': build.collector_item_id,
        'timestamp': build.timestamp,
        'number': build.number,
        'buildUrl': build.url,
        'startTime': build.start_time,
        'endTime': build.end_time,
        'duration': build.duration,
        'buildStatus': build.status,
        'log': build.log,
        'sourceChangeSet': build.source_changeset,
    }

    if build.id is not None:
        doc['_id'] = build.id

    return doc


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

def collector_item_to_doc(collector_item):
    doc = {
        'description': collector_item.description,
        'enabled': collector_item.enabled,
        'collectorId': collector_item.collector_id,
        'options': collector_item.options,
    }

    if collector_item.id is not None:
        doc['_id'] = collector_item.id

    return doc


def collector_item_to_model(doc):
    collector_item = CollectorItem()
    collector_item.id = doc['_id']
    collector_item.description = doc['description']
    collector_item.enabled = doc['enabled']
    collector_item.collector_id = doc['collectorId']
    collector_item.options = doc['options']
    return collector_item


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
        '_class': "com.capitalone.dashboard.model.Dashboard",
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

    def save_build(self, build):
        doc = build_to_doc(build)
        builds = self._db.get_collection('builds')
        if build.id is None:
            result = builds.insert(doc)
            build.id = result
        else:
            builds.update({'_id': build.id}, doc)

    def get_collector_by_name(self, collector_name):
        collectors = self._db.get_collection('collectors')
        doc = collectors.find_one({'name': collector_name})

        if doc is None:
            return

        collector = collector_to_model(doc)
        return collector

    def get_collector_item_by_name(self, name):
        collector_items = self._db.get_collection('collector_items')
        doc = collector_items.find_one({'description': name})

        if doc is None:
            return

        collector_item = collector_item_to_model(doc)
        return collector_item

    def save_collector_item(self, collector_item):
        doc = collector_item_to_doc(collector_item)
        collector_items = self._db.get_collection('collector_items')
        if collector_item.id is None:
            result = collector_items.insert(doc)
            collector_item.id = result
        else:
            collector_items.update({'_id': collector_item.id}, doc)

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
