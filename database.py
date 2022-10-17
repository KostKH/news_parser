from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Reflected(DeferredReflection):
    __abstract__ = True


class Resource(Reflected, Base):
    """Класс для обмена данными с таблицей БД resource"""

    __tablename__ = 'resource'
    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String, nullable=False)
    resource_url = Column(String, nullable=False)
    top_tag = Column(String, nullable=False)
    bottom_tag = Column(String, nullable=False)
    title_cut = Column(String, nullable=False)
    date_cut = Column(String, nullable=False)

    def __str__(self):
        return '\n'.join(
            [
                str(Resource.resource_id),
                str(Resource.resource_name),
                str(Resource.resource_url),
                str(Resource.top_tag),
                str(Resource.bottom_tag),
                str(Resource.title_cut),
                str(Resource.date_cut)
            ]
        )



class Item(Reflected, Base):
    """Класс для обмена данными с таблицей БД items"""

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    res_id = relationship(Integer, ForeignKey('resource.resource_id'))
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    nd_date = Column(Integer, nullable=False)
    s_date = Column(Integer, nullable=False)
    not_date = Column(String, nullable=False)

    def __str__(self):
        return '\n'.join(
            [
                str(self.id),
                str(self.res_id),
                str(self.link),
                str(self.title),
                str(self.content),
                str(self.nd_date),
                str(self.s_date),
                str(self.not_date)
            ]
        )
