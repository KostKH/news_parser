from models import ItemModel, ResourceModel
from parse_handler import ResourceHandler
from dotenv import load_dotenv
import logging
import os
from sqlalchemy import create_engine
import database
import json
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import insert, select, update

def load_test_data():
    data = [
        {
            'RESOURCE_NAME': 'nur.kz',
            'RESOURCE_URL': 'https://www.nur.kz',
            'top_tag': json.dumps(['a', {'class': 'post-preview-text js-article-link'}]),
            'bottom_tag': json.dumps(['div', {'class': 'formatted-body io-article-body'}]),
            'title_cut': json.dumps(['h1', {'class': 'main-headline js-main-headline'}]),
            'date_cut': json.dumps(['time', {'class': 'datetime datetime--publication'}]),
        },
        {
            'RESOURCE_NAME': 'scientificrussia.ru/news',
            'RESOURCE_URL': 'https://scientificrussia.ru/news/',
            'top_tag': json.dumps(['a', {'class': 'post-preview-text js-article-link'}]),
            'bottom_tag': json.dumps(['div', {'class': 'formatted-body io-article-body'}]),
            'title_cut': json.dumps(['h1', {'class': 'main-headline js-main-headline'}]),
            'date_cut': json.dumps(['time', {'class': 'datetime datetime--publication'}]),
        },
    ]
    return data

def main():
    load_dotenv()
    
    logfile = os.getenv('LOGFILE')

    logging.basicConfig(
        level=logging.DEBUG,
        filename=logfile, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
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
    data = load_test_data()
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
        else:
            conn.execute(insert(resource_table), data)
        conn.commit()

    
    with engine.connect() as conn:
        existing_objs = conn.execute(
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
    for row in existing_objs:
        resource = ResourceModel(*row)
        resource_list.append(resource)
    
    handler = ResourceHandler()
    all_found_items = []
    for resource in resource_list:
        items_list = handler(resource)
        all_found_items += items_list
    
    for item in all_found_items:
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
            else:
                conn.execute(insert(items_table), item)
            conn.commit()
    with open('parse_result.txt', 'w') as result_file:
        for item in all_found_items:
            result_file.write(f'{str(item)}\n')
        result_file.write(f'загружено новостей:\n{len(all_found_items)}')
        result_file.write(f'не удалось загрузить:\n{len(ResourceHandler.not_downloaded)}')
        result_file.write("\n".join(ResourceHandler.not_downloaded))


if __name__ == '__main__':
    main()
