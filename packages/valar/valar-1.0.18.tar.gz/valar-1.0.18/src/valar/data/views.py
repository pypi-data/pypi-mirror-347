import json


from .models import MetaField, VModel
from .orm import load_model
from .query import Query
from .. import ValarResponse
from ..channels import ValarSocketSender
from ..channels.utils import execute_channel

from ..data.handlers import save_many_handler
from ..data.utils import get_dao, transform


async def save_many(request,db, entity):
    body = json.loads(request.body)
    data = body.get('data')
    sender = ValarSocketSender(request)
    await execute_channel(save_many_handler, data, sender)
    return ValarResponse(True)

def save_one (request,db, entity):
    item = json.loads(request.body)
    dao = get_dao(db, entity)
    bean = dao.save_one(item)
    return ValarResponse(transform(db,bean))


def update_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body['query'])
    item  = body['item']
    dao = get_dao(db, entity)
    dao.update_many(query, item)
    return ValarResponse(True)

def delete_one(request, db, entity):
    body = json.loads(request.body)
    _id = body['id']
    dao = get_dao(db, entity)
    dao.delete_one(_id)
    return ValarResponse(True)

def delete_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body)
    dao = get_dao(db, entity)
    dao.delete_many(query)
    return ValarResponse(True)

def find_one(request, db, entity):
    body = json.loads(request.body)
    _id = body['id']
    dao = get_dao(db, entity)
    bean = dao.find_one(_id)
    return ValarResponse(transform(db,bean))

def find_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body.get('query'))
    dao = get_dao(db, entity)
    page = body.get('page', 1)
    size = body.get('size', 0)
    code = body.get('code')
    results, total = dao.find_many(query, size, page)
    return ValarResponse({
        'results': transform(db, results, code),
        'total': total
    })


def tree(request, db, entity):
    body = json.loads(request.body)
    code = body.get('code','default')
    root = body.get('root', 0)
    query = Query(body)
    dao = get_dao(db, entity)
    results = [n.json for n in dao.tree(query,root)]
    return ValarResponse(results)


def meta(request):
    body = json.loads(request.body)
    code = body.get('code')
    entity = body.get('entity')
    dao = get_dao('orm', entity)
    view = dao.meta(code)
    return ValarResponse(view)

def fields(request ):
    body = json.loads(request.body)
    entity = body.get('entity')
    dao = get_dao('orm', entity)
    _fields =dao.meta_fields
    return ValarResponse(_fields)



def add_fields(request):
    body = json.loads(request.body)
    entity = body.get('entity')
    view_id = body.get('view_id')
    props = body.get('props')
    dao = get_dao('orm', entity)
    field_dao = get_dao('orm','data.MetaField')
    _fields = dao.meta_fields
    for prop in props:
        field = _fields.get(prop)
        if field:
            field['view_id'] = view_id
            field_dao.save_one(field)
    return ValarResponse(True)

def metas(request):
    mapping = load_model()
    tree = {}
    for entity in mapping:
        _, name = mapping[entity]
        app, model = entity.split('.')
        node = {'label': name, 'value': model}
        root = tree.get(app, {'label': app, 'value': app, 'children': []})
        root['children'].append(node)
        tree[app] = root
    return ValarResponse(list(tree.values()))