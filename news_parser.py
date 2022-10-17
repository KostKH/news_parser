from models import ItemModel, ResourceModel
from parse_handler import ResourceHandler
from dotenv import load_dotenv
import logging
import os
import json
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import insert, select, update
from database import (establish_db_connection, get_parsed_item_added, 
                      get_resource_list, get_resource_added)
import sys

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

def parse_items():
    """action: --parse"""
    engine, resource_table, items_table = establish_db_connection()
    resource_list = get_resource_list(engine, resource_table)
    handler = ResourceHandler()
    all_found_items = []
    for resource in resource_list:
        items_list = handler(resource)
        all_found_items += items_list
    
    for item in all_found_items:
        get_parsed_item_added()
    with open('parse_result.txt', 'w') as result_file:
        for item in all_found_items:
            result_file.write(f'{str(item)}\n')
        result_file.write(f'загружено новостей:\n{len(all_found_items)}')
        result_file.write(f'не удалось загрузить:\n{len(ResourceHandler.not_downloaded)}')
        result_file.write("\n".join(ResourceHandler.not_downloaded))
    pass

def add_resources(data):
    """action: --add-resources-list"""

    if not isinstance(data, list):
        print(
            'Загрузка не удалась. Проверьте, что в параметрах вы передаете '
            'список ресурсов на загрузку в БД, а данные по каждому ресурсу '
            'представлены в виде словаря'
        )
        return

    engine, resource_table, items_table = establish_db_connection()
    results = {
        'updated': [],
        'created': [],
        'failed to create': []
    }
    for resource in data:
        result = get_resource_added(engine, resource_table, resource)
        results[result].append(resource['RESOURCE_NAME'])
    
    print(
        f'Найдено ресурсов во входящих параметрах: {len(data)}\n'
        f'Добавлено новых ресурсов: {len(results["created"])}\n'
        f'Обновлено существовавших ресурсов: {len(results["updated"])}\n'
        f'Не удалась загрузка ресурсов: {len(results["failed to create"])}\n'
        f'список обновленных ресурсов: {results["updated"]}\n\n'
        f'Что не удалось загрузить: {results["failed to create"]}\n'
    )


def delete_resources(data):
    """action: --delete-resources"""
    engine, resource_table, items_table = establish_db_connection()
    pass

def list_resources()
    """action: --list-resources"""
    engine, resource_table, items_table = establish_db_connection()
    resources = get_resource_list(engine, resource_table)
    for resource in resources:
        print(resource, end="\n-----------------------------\n\n")


def main():
    load_dotenv()
    
    logfile = os.getenv('LOGFILE')

    logging.basicConfig(
        level=logging.DEBUG,
        filename=logfile, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    data = load_test_data()

if __name__ == '__main__':
    main()
