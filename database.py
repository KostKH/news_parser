import os

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        create_engine, delete, insert, select, update)

from models import ResourceModel


def establish_db_connection():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('DB_HOST')
    port = str(os.getenv('DB_PORT'))
    db_name = os.getenv('DB_NAME')

    engine = create_engine(
        f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}',
        echo=True,
        future=True
    )
    metadata_obj = MetaData()
    resource_table = Table(
        'resource',
        metadata_obj,
        Column('RESOURCE_ID', Integer, primary_key=True),
        Column('RESOURCE_NAME', String),
        Column('RESOURCE_URL', String, unique=True),
        Column('top_tag', String),
        Column('bottom_tag', String),
        Column('title_cut', String),
        Column('date_cut', String),
    )
    items_table = Table(
        'items',
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('res_id', ForeignKey('resource.RESOURCE_ID'), nullable=False),
        Column('link', String, unique=True),
        Column('title', String),
        Column('content', String),
        Column('nd_date', String),
        Column('s_date', String),
        Column('not_date', String)
    )
    metadata_obj.create_all(engine)
    return engine, resource_table, items_table


def get_resource_added(engine, resource_table, data):
    with engine.connect() as conn:
        existing_obj = conn.execute(
            select(resource_table.c.RESOURCE_ID)
            .where(resource_table.c.RESOURCE_NAME == data['RESOURCE_NAME']),
        ).first()
        if existing_obj:
            conn.execute(
                update(resource_table)
                .where(resource_table.c.RESOURCE_ID == existing_obj[0])
                .values(data)
            )
            status = 'updated'
        else:
            conn.execute(insert(resource_table), data)
            status = 'created'
        conn.commit()
    return status


def get_resource_list(engine, resource_table):
    with engine.connect() as conn:
        db_rows = conn.execute(
            select(
                resource_table.c.RESOURCE_ID,
                resource_table.c.RESOURCE_NAME,
                resource_table.c.RESOURCE_URL,
                resource_table.c.top_tag,
                resource_table.c.bottom_tag,
                resource_table.c.title_cut,
                resource_table.c.date_cut
            )
        ).all()

    resource_list = []
    for row in db_rows:
        resource = ResourceModel(*row)
        resource_list.append(resource)

    return resource_list


def get_parsed_item_added(engine, items_table, item):
    with engine.connect() as conn:
        existing_obj = conn.execute(
            select(items_table.c.id)
            .where(items_table.c.link == item['link'])
            .where(items_table.c.not_date == item['not_date'])
        ).first()
        if existing_obj:
            conn.execute(
                update(items_table)
                .where(items_table.c.id == existing_obj[0])
                .values(item)
            )
            status = 'updated'
        else:
            conn.execute(insert(items_table), item)
            status = 'created'
        conn.commit()
    return status


def get_resource_deleted(engine, resource_table, resource_id):
    with engine.connect() as conn:
        existing_obj = conn.execute(
            select(resource_table.c.RESOURCE_ID)
            .where(resource_table.c.RESOURCE_ID == resource_id)
        ).first()
        if existing_obj:
            conn.execute(
                delete(resource_table)
                .where(resource_table.c.RESOURCE_ID == existing_obj[0])
            )
            status = 'deleted'
        else:
            status = 'not_found'
        conn.commit()
    return status
