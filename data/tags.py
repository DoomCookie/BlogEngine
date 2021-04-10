import datetime
import sqlalchemy

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase



class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    slug = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.datetime.now)


post_to_tag = sqlalchemy.Table(
    'post_to_tag',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('post', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('posts.id')),
    sqlalchemy.Column('tag', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tags.id'))
)
