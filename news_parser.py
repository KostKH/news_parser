from models import ResourceModel
from parse_handler import ResourceHandler
from dotenv import load_dotenv
from arg_handler import parse_arguments
import logging
import os
import json
from database import (establish_db_connection, get_parsed_item_added, 
                      get_resource_list, get_resource_added)
import sys


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
        get_parsed_item_added(engine, items_table, item)
    with open('parse_result.txt', 'w') as result_file:
        for item in all_found_items:
            result_file.write(f'{str(item)}\n')
        result_file.write(f'загружено новостей:\n{len(all_found_items)}')
        result_file.write(f'не удалось загрузить:\n{len(ResourceHandler.not_downloaded)}')
        result_file.write("\n".join(ResourceHandler.not_downloaded))
    pass

def add_resources(data):
    """action: --add-resources-list"""

    engine, resource_table, items_table = establish_db_connection()
    results = {
        'updated': [],
        'created': [],
        'failed to create': []
    }
    for resource in data:
        serialized_resource = ResourceModel(**resource).formated_for_db()
        result = get_resource_added(
            engine,
            resource_table,
            serialized_resource
        )
        results[result].append(resource['RESOURCE_NAME'])
    
    print(
        f'Найдено ресурсов во входящих параметрах: {len(data)}\n'
        f'Добавлено новых ресурсов: {len(results["created"])}\n'
        f'Обновлено существовавших ресурсов: {len(results["updated"])}\n'
        f'Не удалась загрузка ресурсов: {len(results["failed to create"])}\n'
        f'\nСписок обновленных ресурсов: {results["updated"]}\n'
        f'\nЧто не удалось загрузить: {results["failed to create"]}\n'
    )


def delete_resources(data):
    """action: --delete-resources"""
    engine, resource_table, items_table = establish_db_connection()
    pass

def list_resources():
    """action: --list-resources"""
    engine, resource_table, items_table = establish_db_connection()
    resources = get_resource_list(engine, resource_table)
    for resource in resources:
        print(resource, end="\n-----------------------------\n\n")


def get_data_from_file(input_file):
    try:
        with open(input_file, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
    except json.decoder.JSONDecodeError as e:
        print(
            "Error: couldn't retrieve list of resources from file. "
            " Please, ensure your file contains data in recommended format"
        )
        sys.exit(1)
    if not isinstance(data, list):
        print(
            "Error: couldn't retrieve list of resources from file. "
            " Please, ensure your file contains data in recommended format"
        )
        sys.exit(1)
    return data

def main():
    load_dotenv()
    
    logfile = os.getenv('LOGFILE')

    logging.basicConfig(
        level=logging.ERROR,
        filename=logfile, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    parser, arguments = parse_arguments()

    if arguments.delete_resources:
        data = get_data_from_file(arguments.delete_resources)
        delete_resources(data)
    elif arguments.add_resources:
        data = get_data_from_file(arguments.add_resources)
        add_resources(data)
    elif arguments.list_resources:
        list_resources()
    elif arguments.parse:
        parse_items()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
