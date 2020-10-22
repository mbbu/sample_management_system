from api.models.database import BaseModel
from api.search.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    id = None
    query = None
    __tablename__ = None

    @classmethod
    def search(cls, expression, page, per_page):
        """
        The search() class method wraps the query_index() function from the search.py to replace the list of object IDs
        with actual objects. All indexes will be named with the name Flask-SQLAlchemy assigned to the relational table.
        The function returns the list of result IDs, and the total number of results.

        The SQLAlchemy query that retrieves the list of objects by their IDs is based on a CASE statement from the SQL
        language, which needs to be used to ensure that the results from the database come in the same order as the IDs
        are given. This is important because the Elasticsearch query returns results sorted based on relevance.

        The search() function returns the query that replaces the list of IDs, and also passes through the total number
        of search results as a second return value.

        :param expression:
        :param page:
        :param per_page:
        :return:
        """
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """
        The before handler is useful because the session hasn't been committed yet, so we can look at it and figure out
        what objects are going to be added, modified and deleted, available as session.new, session.dirty and
        session.deleted respectively. These objects are not going to be available anymore after the session is committed
        , so they need to be saved before the commit takes place.

        :param session:
        :return:
        """
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    # todo: fix after_commit; Issue is the db has no engine declared at the point the application is starting.
    @classmethod
    def after_commit(cls, session):
        """
        When the after_commit() handler is invoked, the session has been successfully committed, so this is the proper
        time to make changes on the Elasticsearch side. The session object has the _changes variable that were added in
        the before_commit(), so now we can iterate over the added, modified and deleted objects, and make the
        corresponding calls to the indexing functions in the search.py for the objects that have the SearchableMixin
        class.

        :param session:
        :return:
        """
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """
        The reindex() class method is a simple helper method that you can use to refresh an index with all the data from
        the relational side. With this method in place, one can reindex a model to add all the models entries in the
        database to the search index.

        :return:
        """
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db = BaseModel.db
# setup event handlers that will make SQLAlchemy call the before_commit() and after_commit() methods
# before and after each commit respectively.
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
