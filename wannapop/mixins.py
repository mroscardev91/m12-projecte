from . import db_manager as db

class BaseMixin():
    
    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        return r.save()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def db_query(cls, *args):
        return db.session.query(cls, *args)

    @classmethod
    def db_query_with(cls, join_cls):
        return cls.db_query(join_cls).join(join_cls)

    @classmethod
    def get(cls, id):
        return cls.db_query().get(id)
    
    @classmethod
    def get_all(cls):
        return cls.db_query().all()

    @classmethod
    def get_filtered_by(cls, **kwargs):
        return cls.db_query().filter_by(**kwargs).one_or_none()

    @classmethod
    def get_all_filtered_by(cls, **kwargs):
        return cls.db_query().filter_by(**kwargs).order_by(cls.id.asc()).all()

    @classmethod
    def get_with(cls, id, join_cls):
        return cls.db_query_with(join_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_all_with(cls, join_cls):
        return cls.db_query_with(join_cls).order_by(cls.id.asc()).all()
    
    @staticmethod
    def db_enable_debug():
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from collections import OrderedDict
from sqlalchemy.engine.row import Row

class SerializableMixin():

    exclude_attr = []

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if key not in self.__class__.exclude_attr:
                result[key] = getattr(self, key)
        return result

    @staticmethod
    def to_dict_collection(collection):
        result = []
        for x in collection:  
            if (type(x) is Row):
                obj = {}
                first = True
                for y in x:
                    if first:
                        # model
                        obj = y.to_dict()
                        first = False
                    else:
                        # relationships
                        key = y.__class__.__name__.lower()
                        del obj[key + '_id']
                        obj[key] = y.to_dict()
                result.append(obj)
            else:
                # only model
                result.append(x.to_dict())
        return result