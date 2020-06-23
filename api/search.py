from flask import current_app

"""
    Data in Elasticsearch is written to indexes. The data is just a JSON object.
"""


def add_to_index(index, model):
    """
    The function uses the __searchable__ class variable in the model to build the doc that is inserted into the index.
    Elasticsearch documents also needed a unique identifier. In this case the unique identifier is the id field of the
    SQLAlchemy model, which is also conveniently unique. This model of using same ID as from the model it allows us to
    link entries in the two databases.

    If you attempt to add an entry with an existing id, then Elasticsearch replaces the old entry with the new one,
    so add_to_index() can be used for new objects as well as for modified ones.

    :param index: Name of the index to add to
    :param model: Model associated with the index
    :return:
    """
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """
    This function deletes the document stored under the given id. Since we used the same ID for indexing as the one from
    the model, this function is then simplified.

    :param index:
    :param model:
    :return:
    """
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """
    The query_index() function takes the index name and a text to search for, along with pagination controls,
    so that search results can be paginated like Flask-SQLAlchemy results are. Instead of using a match query type,
    it has multi_match, which can search across multiple fields. Passing a field name of *, allows Elasticsearch to look
    in all the fields, i.e. searching the entire index.
    This is useful to make this function generic, since different models can have different field names in the index.

    The body argument to es.search() includes pagination arguments in addition to the query itself.
    The from and size arguments control what subset of the entire result set needs to be returned.

    The return statement is somewhat complex. It returns two values: the first is a list of id elements for the search
    results, and the second is the total number of results. Both are obtained from the Python dictionary returned by the
    es.search() function.

    :param index:
    :param query:
    :param page:
    :param per_page:
    :return:
    """
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
